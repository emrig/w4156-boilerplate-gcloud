# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helpers for reading the Google Cloud SDK's configuration."""

import json
import os
import subprocess

from google.auth import environment_vars
import google.oauth2.credentials


# The ~/.config subdirectory containing gcloud credentials.
_CONFIG_DIRECTORY = 'gcloud'
# Windows systems store config at %APPDATA%\gcloud
_WINDOWS_CONFIG_ROOT_ENV_VAR = 'APPDATA'
# The name of the file in the Cloud SDK config that contains default
# credentials.
_CREDENTIALS_FILENAME = 'application_default_credentials.json'
# The name of the Cloud SDK shell script
_CLOUD_SDK_POSIX_COMMAND = 'gcloud'
_CLOUD_SDK_WINDOWS_COMMAND = 'gcloud.cmd'
# The command to get the Cloud SDK configuration
_CLOUD_SDK_CONFIG_COMMAND = ('config', 'config-helper', '--format', 'json')


def get_config_path():
    """Returns the absolute path the the Cloud SDK's configuration directory.

    Returns:
        str: The Cloud SDK config path.
    """
    # If the path is explicitly set, return that.
    try:
        return os.environ[environment_vars.CLOUD_SDK_CONFIG_DIR]
    except KeyError:
        pass

    # Non-windows systems store this at ~/.config/gcloud
    if os.name != 'nt':
        return os.path.join(
            os.path.expanduser('~'), '.config', _CONFIG_DIRECTORY)
    # Windows systems store config at %APPDATA%\gcloud
    else:
        try:
            return os.path.join(
                os.environ[_WINDOWS_CONFIG_ROOT_ENV_VAR],
                _CONFIG_DIRECTORY)
        except KeyError:
            # This should never happen unless someone is really
            # messing with things, but we'll cover the case anyway.
            drive = os.environ.get('SystemDrive', 'C:')
            return os.path.join(
                drive, '\\', _CONFIG_DIRECTORY)


def get_application_default_credentials_path():
    """Gets the path to the application default credentials file.

    The path may or may not exist.

    Returns:
        str: The full path to application default credentials.
    """
    config_path = get_config_path()
    return os.path.join(config_path, _CREDENTIALS_FILENAME)


def load_authorized_user_credentials(info):
    """Loads an authorized user credential.

    Args:
        info (Mapping[str, str]): The loaded file's data.

    Returns:
        google.oauth2.credentials.Credentials: The constructed credentials.

    Raises:
        ValueError: if the info is in the wrong format or missing data.
    """
    return google.oauth2.credentials.Credentials.from_authorized_user_info(
        info)


def get_project_id():
    """Gets the project ID from the Cloud SDK.

    Returns:
        Optional[str]: The project ID.
    """
    if os.name == 'nt':
        command = _CLOUD_SDK_WINDOWS_COMMAND
    else:
        command = _CLOUD_SDK_POSIX_COMMAND

    try:
        output = subprocess.check_output(
            (command,) + _CLOUD_SDK_CONFIG_COMMAND,
            stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, OSError, IOError):
        return None

    try:
        configuration = json.loads(output.decode('utf-8'))
    except ValueError:
        return None

    try:
        return configuration['configuration']['properties']['core']['project']
    except KeyError:
        return None
