# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for aggregating environment and package list data.

"""

import configparser
import json
import logging
import os
import re
import subprocess
import sys
from typing import List, Optional

import tornado
from notebook.base.handlers import APIHandler

from .envs_state import install_status_codes
from .jobs import quantum_jobs_enabled, quantum_jobs_supported
from .kernels import get_kernels
from .qbraid_core import (
    env_path,
    is_valid_python,
    local_qbraid_envs_path,
    replace_str,
    sys_qbraid_envs_path,
    which_python,
)

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def _uri_to_filepath(uri: str) -> str:
    """Convert a file URI to a local file path."""
    if uri.startswith("file://"):
        return uri[len("file://") :]
    raise ValueError(f"Invalid URI: {uri}")


def _extract_package_version(pip_freeze_string: str) -> Optional[str]:
    """Extract the version of a package from a pip freeze string.
    Return None if the version cannot be extracted."""

    # semantic versioning pattern
    semver_pattern = r"(\d+\.\d+\.\d+)"
    match = re.search(semver_pattern, pip_freeze_string)
    if match:
        return match.group(1)

    # git repo editable mode install version pattern
    git_editable_pattern = (
        r"^-e\s+"
        r"git\+https:\/\/github\.com\/"
        r"[a-zA-Z0-9._-]+\/[a-zA-Z0-9._-]+\.git@"
        r"[a-fA-F0-9]{40}#"
        r"egg=[a-zA-Z0-9._-]+$"
    )
    if re.match(git_editable_pattern, pip_freeze_string):
        parts = pip_freeze_string.split("#egg=")
        return parts[0].split(" ", 1)[-1]

    try:
        # extract version from locally installed package setup file path
        maybe_uri = pip_freeze_string.split(" @ ")[1]
        filepath = _uri_to_filepath(maybe_uri).strip("\n")
        setup_cfg_path = os.path.join(filepath, "setup.cfg")
        config = configparser.ConfigParser()
        config.read(setup_cfg_path)
        return config.get("metadata", "version")
    except Exception as err:  # pylint: disable=broad-exception-caught
        logging.error("Error extracting package version: %s", err)
    return None


def _rewrite_requirements_file(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as file:
        requirements = file.readlines()

    updated_requirements = []

    for requirement in requirements:
        if requirement.strip() == "":
            continue

        if len(requirement.split(" ")) == 3 and "@" in requirement:
            package = requirement.split(" @ ")[0]
            if package is None or package.strip() == "":
                continue

            version = _extract_package_version(requirement)
            if version is None:
                version = requirement.split(" ")[-1].strip("\n")

            requirement = f"{package}=={version}\n"

        elif requirement.startswith("-e"):
            package = requirement.split("egg=")[-1].strip("\n")
            if package is None or package.strip() == "":
                continue

            version = _extract_package_version(requirement)
            if version is None:
                continue

            requirement = f"{package}=={version}\n"

        if "==" not in requirement:
            continue

        updated_requirements.append(requirement)

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(updated_requirements)


def get_pip_list(slug: str) -> List[str]:
    """Return packages in requirements.txt in list form.
    If file not found, return empty list."""
    slug_path = env_path(slug)
    reqs_txt = os.path.join(slug_path, "requirements.txt")

    pip_list = []

    if os.path.isfile(reqs_txt):
        with open(f"{reqs_txt}", "r", encoding="utf-8") as f:
            pip_lines = f.readlines()
        for line in pip_lines:
            pkg = line.strip("\n")
            pip_list.append(pkg)

    return pip_list


def put_pip_list(slug: str, system_site_packages: Optional[bool] = True) -> List[str]:
    """Update/insert requirements.txt and return pip list."""
    python = which_python(slug)
    if is_valid_python(python) and python != sys.executable:
        slug_path = env_path(slug)
        cfg = os.path.join(slug_path, "pyenv", "pyvenv.cfg")
        reqs_txt = os.path.join(slug_path, "requirements.txt")
        replace_str("true", "false", cfg)
        with open(reqs_txt, "w", encoding="utf-8") as file:
            subprocess.run(
                [python, "-m", "pip", "freeze"],
                stdout=file,
                text=True,
                check=True,
            )
        _rewrite_requirements_file(reqs_txt)
        if system_site_packages:
            replace_str("false", "true", cfg)

    return get_pip_list(slug)


class PipListEnvironmentHandler(APIHandler):
    """Handler for managing environment package list data."""

    @tornado.web.authenticated
    def post(self):
        """Get pip list of environment."""
        input_data = self.get_json_body()
        slug = input_data.get("slug")
        system_site_packages = input_data.pop("systemSitePackages", None)
        system_site_packages_bool = (
            True if system_site_packages is None else bool(system_site_packages)
        )
        package_lst = put_pip_list(slug, system_site_packages=system_site_packages_bool)

        data = {}
        data["packages"] = package_lst

        self.finish(json.dumps(data))


class ListInstalledEnvironmentsHandler(APIHandler):
    """Handler for managing installed environment list data."""

    @tornado.web.authenticated
    def get(self):
        """Gets data surrounding installed environments including any installing
        environment, installed environments, active environments, and pip lists
        of all installed environments."""
        _, kernels_list = get_kernels()  # list of names of installed kernels

        # list of directories where environments can be installed
        env_dir_lst = [sys_qbraid_envs_path, local_qbraid_envs_path]

        installing = None  # name of currently installing, if any
        installed = []  # list of installed environments
        active = []  # list of active environments
        qjobs_supported = []  # list of environments with quantum jobs functionality
        qjobs_enabled = []  # list of environments with quantum jobs enabled
        sys_python = []  # environments for which $(which python) = sys.executable

        for env_dir_path in env_dir_lst:
            if not os.path.isdir(env_dir_path):
                continue  # Skip if the path is not a directory

            for slug in os.listdir(env_dir_path):
                slug_path = os.path.join(env_dir_path, slug)

                # Skip if the path is not a directory or if it's not a valid slug directory
                if not os.path.isdir(slug_path) or not self.is_slug_dir(slug):
                    continue

                # Add to installed environments list
                installed.append(slug)

                if which_python(slug) == sys.executable:
                    sys_python.append(slug)

                # Check if the environment is active
                if self.is_active(slug_path, kernels_list):
                    active.append(slug)

                # Initialize 'installing' status if it's None
                if installing is None:
                    installing = self.check_install_status(slug)

                # Check if quantum jobs are supported and/or enabled
                try:
                    if quantum_jobs_supported(slug_path):
                        qjobs_supported.append(slug)
                        if quantum_jobs_enabled(slug_path):
                            qjobs_enabled.append(slug)
                except Exception as err:  # pylint: disable=broad-exception-caught
                    logging.error("Error determining quantum jobs state: %s", err)

        installing = "" if installing is None else installing

        data = {
            "installed": installed,
            "active": active,
            "installing": installing,
            "quantumJobs": qjobs_supported,
            "quantumJobsEnabled": qjobs_enabled,
            "sysPython": sys_python,
        }

        self.finish(json.dumps(data))

    def is_slug_dir(self, slug: str) -> bool:
        """Return True if slug is a valid slug directory, False otherwise.

        TODO: Replace with qbraid.api.system.is_valid_slug
        """
        try:
            base_name = os.path.splitext(slug)[0]
            return len(base_name) > 7 and base_name[-7] == "_"
        except Exception as err:  # pylint: disable=broad-exception-caught
            logging.error("Error processing candidate slug directory name: %s", err)
            return False

    def check_install_status(self, slug: str) -> Optional[str]:
        """Return slug if environment is installing, None otherwise."""
        try:
            install_data = install_status_codes(slug)
            if install_data["complete"] == 0:
                return slug
            return None
        except Exception as err:  # pylint: disable=broad-exception-caught
            logging.error("Error checking install status: %s", err)
            return None

    def is_active(self, slug_path: str, kernels_list: List[str]) -> bool:
        """Return True if env kernel is in kernel list, False otherwise"""
        try:
            env_kernels_dir = os.path.join(slug_path, "kernels")
            if not os.path.isdir(env_kernels_dir):
                return False
            env_kernels = os.listdir(env_kernels_dir)
            if len(env_kernels) == 0:
                return False
            # Some envs have more than one kernel
            for f in env_kernels:
                if f not in kernels_list:
                    return False
            return True
        except Exception as err:  # pylint: disable=broad-exception-caught
            logging.error("Error checking if environment kernel is active: %s", err)
            return False
