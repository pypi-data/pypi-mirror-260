# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module containing core functionality shared across environment manager handlers.

"""

import json
import logging
import os
import shutil
import stat
import subprocess
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# TODO: change to one qBraid envs path env variable $QBRAID_ENVS_PATH
# pylint: disable-next=unnecessary-lambda-assignment
default_path = lambda prefix: os.path.join(prefix, ".qbraid", "environments")
local_qbraid_envs_path = os.getenv("QBRAID_USR_ENVS", default_path(os.path.expanduser("~")))
sys_qbraid_envs_path = os.getenv("QBRAID_SYS_ENVS", default_path("/opt"))

TEST = False


def echo_log(message: str) -> None:
    """Write message to log file."""
    home_dir = Path.home()
    log_file_path = home_dir / ".qbraid" / "log.txt"
    log_file_path.parent.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")


def env_path(slug: str) -> str:
    """Return path to qbraid environment."""
    sys_slug_path = os.path.join(sys_qbraid_envs_path, slug)
    if os.path.exists(sys_slug_path):
        return sys_slug_path
    return os.path.join(local_qbraid_envs_path, slug)


def is_exe(fpath: str) -> bool:
    """Return true if fpath is a file we have access to that is executable."""
    accessmode = os.F_OK | os.X_OK
    if os.path.exists(fpath) and os.access(fpath, accessmode) and not os.path.isdir(fpath):
        filemode = os.stat(fpath).st_mode
        return bool(filemode & stat.S_IXUSR or filemode & stat.S_IXGRP or filemode & stat.S_IXOTH)
    return False


def is_valid_python(python_path: str) -> bool:
    """Return true if python_path is a valid Python executable."""
    if shutil.which(python_path) is None:
        return False

    if sys.platform != "win32" and not is_exe(python_path):
        return False

    try:
        output = subprocess.check_output([python_path, "--version"], stderr=subprocess.STDOUT)
        return "Python" in output.decode()
    except subprocess.CalledProcessError:
        return False


def which_python(slug: str) -> str:
    """Return environment's python path"""
    try:
        slug_path = env_path(slug)
        kernels_dir = os.path.join(slug_path, "kernels")
        for resource_dir in os.listdir(kernels_dir):
            if "python" in resource_dir:
                kernel_json = os.path.join(kernels_dir, resource_dir, "kernel.json")
                with open(kernel_json, encoding="utf-8") as f:
                    data = json.load(f)
                    if data["language"] == "python":
                        python_path = data["argv"][0]
                        if is_valid_python(python_path):
                            return python_path

        # fallback: check pyenv bin for python executable
        if sys.platform == "win32":
            python_path = os.path.join(slug_path, "pyenv", "Scripts", "python.exe")
        else:
            python_path = os.path.join(slug_path, "pyenv", "bin", "python")
        if is_valid_python(python_path):
            return python_path
    except Exception as err:  # pylint: disable=broad-exception-caught
        logging.error("Error determining Python path: %s", err)

    return sys.executable


def replace_str(target: str, replacement: str, file_path: str) -> None:
    """Replace all instances of string in file"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    content = content.replace(target, replacement)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
