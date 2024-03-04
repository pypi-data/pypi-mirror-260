from __future__ import annotations

import errno
import json
import logging
import os
from datetime import timedelta, datetime, timezone
from enum import Enum, auto
from itertools import chain
from pathlib import Path
from typing import Optional, Generator, Union, Tuple
from urllib.parse import urlencode

from urllib3 import PoolManager, BaseHTTPResponse

from .configurations_metadata import DeviceGroupMetadata, load_metadata_file, save_metadata_file, ConfigurationMetadata
from .file import file_md5, remove_subdirs_if_empty

log = logging.getLogger(__name__)


class State(Enum):
    Outdated = auto()
    MetadataDownloaded = auto()
    Valid = auto()

    Invalid_FailedToLoadMetadata = auto()
    Invalid_FailedToDownload = auto()


class ClientState(str, Enum):
    Configurations_Applied = "configurations_applied"
    Upvote = "upvote"
    Downvote = "downvote"


class _IdentityManager:
    def __init__(self):
        self._id: Optional[str] = None

    def set_id(self, id: str):
        self._id = id

    def get_id(self) -> str:
        if self._id is None:
            raise ValueError("Client must be identified first. Please call Client.identify first")
        else:
            return self._id


class Client:
    BASE_URL = "https://api.configgery.com/device/"

    def __init__(self, sdk_key: str, configurations_directory: Union[str, Path, None] = None):
        """
        :param sdk_key: API key for the organization
        :param configurations_directory: Directory to store configuration files. If None, use '.configgery' within the
        user's home directory.
        """
        self._state: State = State.Outdated
        self._pool = PoolManager(headers={"X-API-KEY": sdk_key})
        self._client_id_manager = _IdentityManager()
        self._device_group_metadata: Optional[DeviceGroupMetadata] = None

        if configurations_directory is None:
            root_directory = Path.home() / ".configgery"
        elif isinstance(configurations_directory, str):
            root_directory = Path(configurations_directory)
        else:
            root_directory = configurations_directory

        self._configurations_directory = root_directory.joinpath("configurations")
        self._configurations_directory.mkdir(parents=True, exist_ok=True)
        self._configurations_metadata_file = root_directory.joinpath("configurations.json")

        if self._configurations_metadata_file.exists():
            log.info("Loading cached configuration data")
            self._device_group_metadata = load_metadata_file(self._configurations_metadata_file)
        else:
            log.info("No cached configuration data found")

    def _remove_old_configurations(self):
        log.info("Removing old configurations")
        if self._device_group_metadata is None:
            log.error("Unable to remove old configurations without device group metadata")
            return

        valid_paths = {config.path for config in self._device_group_metadata.configurations_metadata}
        if self._device_group_metadata is not None:
            for file in chain(self._configurations_directory.glob("**/*"), self._configurations_directory.glob("*")):
                try:
                    rel_path = file.relative_to(self._configurations_directory)
                    if file.is_file() and str(rel_path) not in valid_paths:
                        try:
                            log.debug(f'Deleting file "{file}"')
                            file.unlink()
                        except FileNotFoundError:
                            log.warning(f'Could not delete file "{file}"')
                            # Do nothing
                            pass
                except ValueError:
                    log.error(f'Could not understand path for file "{file}"')

            remove_subdirs_if_empty(self._configurations_directory)

    def outdated_configurations(self) -> Generator[ConfigurationMetadata, None, None]:
        """
        List all configurations that are out-of-date.
        If any configurations are out-of-date, a call to `download_configurations` should be made.
        :return: A generator yielding configurations that need to be downloaded or replaced with more recent versions
        """
        for config in sorted(self._device_group_metadata.configurations_metadata, key=lambda x: x.path):
            if config.md5 != file_md5(self._configurations_directory.joinpath(config.path)):
                yield config

    def is_download_needed(self) -> bool:
        """
        Check to see if the currently cached configuration data requires a download of configuration files.
        If required, a call to `download_configurations` should be made.
        :return: True if a download is required
        """
        for _ in self.outdated_configurations():
            return True
        return False

    def identify(self, client_name: str):
        """
        Identify client to the server with the specified `client_name`. This is a value of your choosing, and should be
        chosen to help you identify which client is making the request(s).

        For example, for an IoT device you may wish to use the device's serial number as the `client_name`.
        :param client_name: A name for the current client
        :return: None
        :raises ValueError:
        """
        log.info(f"Identifying as {client_name}")
        r: BaseHTTPResponse = self._pool.request(
            "POST", Client.BASE_URL + "v1/identify", json={"client_name": client_name}
        )
        if r.status == 200:
            data = json.loads(r.data.decode("utf-8"))
            self._client_id_manager.set_id(data["id"])
        else:
            raise ValueError(f"Could not identify client as {client_name}")

    def check_latest(self) -> bool:
        """
        Check to see if the current configuration data matches that on the server.
        :return: True if it was possible to retrieve configuration data from the server
        :raises urllib3.exceptions.HTTPError:
        """
        log.info("Checking for latest configuration data")
        r: BaseHTTPResponse = self._pool.request(
            "GET",
            Client.BASE_URL + "v1/current_configurations",
            fields=dict(client_id=self._client_id_manager.get_id()),
        )
        if r.status == 200:
            data = json.loads(r.data.decode("utf-8"))
            self._device_group_metadata = DeviceGroupMetadata.from_server(data)
            save_metadata_file(self._device_group_metadata, self._configurations_metadata_file)
            self._state = State.MetadataDownloaded
            return True
        else:
            log.error(f'Failed to fetch latest configuration data: {r.status}: "{r.data.decode("utf-8")}"')
            self._state = State.Invalid_FailedToLoadMetadata
            self._device_group_metadata = None
            return False

    def time_since_last_checked(self) -> timedelta:
        """
        Time since checking for the latest configuration data from the server
        :return: `timedelta` object
        """
        now = datetime.now(tz=timezone.utc)
        if self._device_group_metadata is None:
            return now - datetime.fromtimestamp(0, tz=timezone.utc)
        else:
            return now - self._device_group_metadata.last_checked

    def download_configurations(self) -> bool:
        """
        Download the latest configurations and save them to disk.
        This will also check for the latest configurations if not already done so,
        and remove old configurations if they are no longer relevant.
        :return: True if no download was needed, or the downloads were successful
        :raises urllib3.exceptions.HTTPError:
        """
        if self._device_group_metadata is None and not self.check_latest():
            return False

        self._remove_old_configurations()

        all_ok = True
        for config in self.outdated_configurations():
            path = self._configurations_directory.joinpath(config.path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wb") as fp:
                r = self._pool.request(
                    "GET",
                    Client.BASE_URL + "v1/configuration",
                    fields=dict(
                        configuration_id=config.configuration_id,
                        version=config.version,
                        client_id=self._client_id_manager.get_id(),
                    ),
                )
                if r.status == 200:
                    fp.write(r.data)
                else:
                    log.error(
                        (
                            f'Failed to get configuration "{config.configuration_id}" version {config.version}. '
                            f'Received response {r.status}: "{r.data.decode("utf-8")}"'
                        )
                    )
                    self._state = State.Invalid_FailedToDownload
                    all_ok = False
                    break

        if hasattr(os, "sync"):
            os.sync()

        if all_ok:
            log.info("Configurations downloaded")
            self._state = State.Valid
            return True
        else:
            return False

    def update_state(self, device_state: ClientState) -> bool:
        """
        Communicate to the server with the current device state
        :param device_state: An enum value indicating the new state
        :return: True if the server call was successful
        :raises urllib3.exceptions.HTTPError:
        """
        if self._device_group_metadata is None:
            log.error(f'Cannot update state with "{device_state.value}" without first getting configuration data')
            return False

        log.info(f'Updating device state with "{device_state.value}"')
        r = self._pool.request(
            "POST",
            Client.BASE_URL + "v1/update_state?" + urlencode(dict(client_id=self._client_id_manager.get_id())),
            body=json.dumps(
                {
                    "device_group_id": str(self._device_group_metadata.device_group_id),
                    "device_group_version": self._device_group_metadata.device_group_version,
                    "action": device_state.value,
                }
            ).encode("utf-8"),
        )
        if r.status in [200, 204]:
            return True
        else:
            log.error(
                f'Failed to update state with "{device_state.value}". '
                f'Received response {r.status}: "{r.data.decode("utf-8")}"'
            )
            return False

    def get_configuration(self, path: str) -> Tuple[bool, bytes]:
        """
        Retrieve a configuration that has been downloaded onto the device
        :param path: Path of configuration. If not path with this value exists,
        match with any configuration with that alias.
        :return: A tuple of two values.
        The first value indicates whether the configuration was successfully retrieved.
        The second value is the file contents
        :raises FileNotFoundError:
        :raises OSError: File is inaccessible (e.g. permission error)
        """
        if self._device_group_metadata is None:
            log.error(f'Cannot get configuration "{path}" without first getting configuration data')
            return False, b""

        if self.is_download_needed():
            log.error(f'Cannot get configuration "{path}" with outdated configurations')
            return False, b""

        for config in self._device_group_metadata.configurations_metadata:
            if config.path == path:
                return True, self._configurations_directory.joinpath(config.path).read_bytes()

        for config in self._device_group_metadata.configurations_metadata:
            if config.alias == path:
                return True, self._configurations_directory.joinpath(config.alias).read_bytes()

        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
