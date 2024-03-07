# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for carrying out quantum jobs actions (enable, disable, etc.)

"""

import json
import logging
import os
import re
import shutil
import subprocess
from typing import Dict, Union

import tornado
from notebook.base.handlers import APIHandler

from .qbraid_core import TEST, env_path

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def quantum_jobs_enabled(slug_path: str) -> bool:
    """Checks if quantum jobs are enabled in environment"""
    proxy_file = os.path.join(slug_path, "qbraid", "proxy")
    try:
        with open(proxy_file, "r", encoding="utf-8") as file:
            for line in file:
                if line.lower().strip().startswith("active"):
                    split_line = line.replace("\n", "").split("=")
                    if len(split_line) == 2:
                        key, value = [
                            item.strip().lower() for item in split_line
                        ]  # strip spaces from both key and value, convert to lowercase
                        if key == "active" and value == "true":
                            return True
    except (FileNotFoundError, IOError) as err:
        logging.error("Error opening or reading file: %s", err)
        return False
    return False


def quantum_jobs_supported(slug_path: str) -> bool:
    """Checks if quantum jobs are supported in environment

    TODO: Replace with qbraid.api.system.qbraid_jobs_state()
    """
    proxy_dir = os.path.join(slug_path, "qbraid")
    proxy_file = os.path.join(proxy_dir, "proxy")

    # Check if directory exists
    if not os.path.isdir(proxy_dir):
        return False

    # Check if 'proxy' file exists in the directory
    if not os.path.isfile(proxy_file):
        return False

    # Check the first line of the 'proxy' file
    with open(proxy_file, "r", encoding="utf-8") as file:
        first_line = file.readline().strip()
        if not re.match(r"^active = (true|false)$", first_line):
            return False

    # Check if there's at least one more directory inside
    if not any(
        os.path.isdir(os.path.join(proxy_dir, subdir_name)) for subdir_name in os.listdir(proxy_dir)
    ):
        return False

    return True


class QuantumJobsHandler(APIHandler):
    """Handler for quantum jobs actions."""

    @tornado.web.authenticated
    def get(self):
        """Gets quantum jobs status of environment."""
        slug = self.get_query_argument("slug")
        supported = quantum_jobs_supported(env_path(slug))
        enabled = False if not supported else quantum_jobs_enabled(env_path(slug))
        status = {"supported": int(supported), "enabled": int(enabled)}
        self.finish(json.dumps(status))

    @tornado.web.authenticated
    def put(self):
        """Enable/disable quantum jobs in environment."""
        input_data = self.get_json_body()
        slug = input_data.get("slug")
        action = input_data.get("action")  # enable or disable

        if TEST:
            try:
                data = self.toggle_quantum_jobs_mock(action, slug)
            except Exception as err:  # pylint: disable=broad-exception-caught
                logging.error("Error toggling quantum jobs: %s", err)
                data = {
                    "success": 0,
                    "stdout": "",
                    "stderr": f"Error {action[:-1]}ing quantum jobs",
                }
        elif shutil.which("qbraid") is None:
            data = {
                "success": 0,
                "stdout": "",
                "stderr": f"Error {action[:-1]}ing quantum jobs: qbraid-cli is not installed.",
            }
        else:
            data = self.toggle_quantum_jobs(action, slug)

        self.finish(json.dumps(data))

    def toggle_quantum_jobs(self, action: str, slug: str) -> Dict[str, Union[int, str]]:
        """Toggles quantum jobs functionality using subprocess."""
        result = subprocess.run(["qbraid", "jobs", action, slug], capture_output=True, check=False)

        return {
            # exit code 0 --> 1 == true for javascript
            "success": 1 if result.returncode == 0 else 0,
            "stdout": result.stdout.decode("utf-8"),
            "stderr": result.stderr.decode("utf-8"),
        }

    def toggle_quantum_jobs_mock(self, action: str, slug: str) -> Dict[str, Union[int, str]]:
        """Mimics toggle quantum jobs functionality for testing."""
        slug_path = env_path(slug)
        proxy_file = os.path.join(slug_path, "qbraid", "proxy")
        expr = "true" if action == "enable" else "false"

        with open(proxy_file, "w", encoding="utf-8") as file:
            file.write(f"active = {expr}\n")

        return {
            "success": 1,
            "stdout": f"Successfully {action}d quantum jobs",
            "stderr": "",
        }

    @tornado.web.authenticated
    def post(self):
        """Adds quantum jobs functionality to environment."""
        input_data = self.get_json_body()
        slug = input_data.get("slug")

        if TEST:
            try:
                data = self.add_quantum_jobs_mock(slug)
            except Exception as err:  # pylint: disable=broad-exception-caught
                logging.error("Error adding quantum jobs: %s", err)
                data = {
                    "success": 0,
                    "stdout": "",
                    "stderr": "Error adding quantum jobs functionality",
                }
        else:
            data = self.add_quantum_jobs(slug)

        self.finish(json.dumps(data))

    def add_quantum_jobs(self, slug: str) -> Dict[str, Union[int, str]]:
        """Adds quantum jobs functionality using subprocess."""
        result = subprocess.run(["qbraid", "jobs", "add", slug], capture_output=True, check=False)

        return {
            # exit code 0 --> 1 == true for javascript
            "success": 1 if result.returncode == 0 else 0,
            "stdout": result.stdout.decode("utf-8"),
            "stderr": result.stderr.decode("utf-8"),
        }

    def add_quantum_jobs_mock(self, slug: str) -> Dict[str, Union[int, str]]:
        """Mimics add quantum jobs functionality for testing."""
        slug_path = env_path(slug)
        proxy_dir = os.path.join(slug_path, "qbraid")
        proxy_file = os.path.join(proxy_dir, "proxy")

        os.makedirs(proxy_dir, exist_ok=True)
        os.makedirs(os.path.join(proxy_dir, "amazon-braket-sdk"), exist_ok=True)
        os.makedirs(os.path.join(proxy_dir, "botocore"), exist_ok=True)

        with open(proxy_file, "w", encoding="utf-8") as file:
            file.write("active = true\n")

        return {
            "success": 1,
            "stdout": "Successfully added quantum jobs functionality",
            "stderr": "",
        }

    @tornado.web.authenticated
    def delete(self):
        """Removes quantum jobs functionality from environment."""
        input_data = self.get_json_body()
        slug = input_data.get("slug")

        try:
            slug_path = env_path(slug)
            if quantum_jobs_supported(slug_path):
                self.toggle_quantum_jobs("disable", slug)
                jobs_dir = os.path.join(slug_path, "qbraid")
                if os.path.exists(jobs_dir):
                    shutil.rmtree(jobs_dir)
                status = 200
            else:
                status = 304
        except Exception as err:  # pylint: disable=broad-exception-caught
            logging.error("Error removing quantum jobs functionality: %s", err)
            status = 500

        self.finish(json.dumps({status: status}))
