# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for checking and updating environment's state/status file(s).

"""

import json
import logging
import os
import sys
from typing import Dict, Optional, Union

import tornado
from notebook.base.handlers import APIHandler

from .qbraid_core import env_path, sys_qbraid_envs_path

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def install_status_codes(slug: str) -> Dict[str, Union[int, str]]:
    """Return environment's install status codes."""

    def read_from_json(file_path: str) -> Dict[str, Union[int, str]]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                return json_data.get("install", {})
        except (IOError, json.JSONDecodeError) as err:
            logging.error("Error reading state.json: %s", err)
            return {}

    def read_from_txt(file_path: str) -> Dict[str, Union[int, str]]:
        data = {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.split(":", 1)
                    if key in ["complete", "success"]:
                        data[key] = int(value.strip())
                    elif key == "message":
                        data[key] = value.strip()
        except IOError as err:
            logging.error("Error reading install_status.txt: %s", err)
        return data

    slug_path = env_path(slug)
    status_path = os.path.join(slug_path, "state.json")
    status_path_deprec = os.path.join(slug_path, "install_status.txt")

    data = {"complete": 1, "success": 1, "message": ""}

    if os.path.exists(os.path.join(sys_qbraid_envs_path, slug)):
        return data
    if os.path.isfile(status_path):
        data.update(read_from_json(status_path))
    elif os.path.isfile(status_path_deprec):
        data.update(read_from_txt(status_path_deprec))

    return data


def update_install_status(
    slug_path: str, complete: int, success: int, message: Optional[str] = None
) -> None:
    """Update environment's install status values in a JSON file.
    Truth table values: 0 = False, 1 = True, -1 = Unknown
    """
    message = message.replace("\n", " ") if message else ""

    state_json_path = os.path.join(slug_path, "state.json")

    data = {"install": {}}

    # Read existing data if file exists
    if os.path.exists(state_json_path):
        with open(state_json_path, "r+", encoding="utf-8") as f:  # r+ mode for reading and writing
            try:
                data = json.load(f)
                f.seek(0)  # Reset file position to the beginning
            except json.JSONDecodeError as err:
                # Keep default data if JSON is invalid
                logging.error("Error opening state.json: %s", err)

            # Update the data
            data["install"]["complete"] = complete
            data["install"]["success"] = success
            data["install"]["message"] = message

            # Write updated data back to state.json
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.truncate()  # Remove leftover data
    else:
        # File doesn't exist, just create a new one with the data
        data["install"] = {
            "complete": complete,
            "success": success,
            "message": message,
        }
        with open(state_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


class InstallStatusHandler(APIHandler):
    """Handler for checking environment's install status."""

    @tornado.web.authenticated
    def get(self):
        """Return codes describing environment's install status."""
        slug = self.get_query_argument("slug")
        data = install_status_codes(slug)
        if data["complete"] == 1 and data["success"] == 1:
            self.handle_successful_install(slug)
        self.finish(json.dumps(data))

    def handle_successful_install(self, slug: str) -> None:
        """Commands to execute after successfully installing environment."""
        slug_path = env_path(slug)

        try:
            # Create symlink from lib64 to lib
            self.create_lib64_symlink(slug_path)
        except Exception as err:  # pylint: disable=broad-exception-caught
            logging.error("Error creating symlink for environment: %s", err)

    @staticmethod
    def create_lib64_symlink(slug_path: str) -> None:
        """Create symlink from lib64 to lib in virtual environment."""
        pyenv_lib = os.path.join(slug_path, "pyenv", "lib")
        pyenv_lib64 = os.path.join(slug_path, "pyenv", "lib64")

        def supports_symlink() -> bool:
            """Check if the current OS supports symlinks."""
            # POSIX compliant systems (Unix-like systems) support symlinks
            # Windows supports symlinks from Vista onwards, but creating them might require
            # administrator privileges unless Developer Mode is enabled on Windows 10 and later
            return os.name == "posix" or (sys.version_info >= (3, 2) and os.name == "nt")

        if os.path.exists(pyenv_lib) and not os.path.exists(pyenv_lib64) and supports_symlink():
            try:
                os.symlink(pyenv_lib, pyenv_lib64)
            except OSError as err:
                logging.error("Error creating symlink for environment: %s", err)
