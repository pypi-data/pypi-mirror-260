# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for uninstalling/removing environments.

"""

import json
import logging
import os
import re
import shutil
import threading
import time
from typing import Optional

import tornado
from notebook.base.handlers import APIHandler

from .kernels import get_kernels
from .qbraid_core import local_qbraid_envs_path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class UninstallThreader:
    """Class for performing recursive removal of files and directories using multi-threading."""

    def __init__(self):
        self._counter = 0

    def counter(self) -> int:
        """Return the number of threads invoked."""
        return self._counter

    def remove(self, path: str) -> None:
        """Remove a file."""
        try:
            self._counter += 1
            os.remove(path)
        except Exception:  # pylint: disable=broad-exception-caught
            pass

    def unlink(self, path: str) -> None:
        """Remove a symbolic link."""
        try:
            self._counter += 1
            os.unlink(path)
        except Exception:  # pylint: disable=broad-exception-caught
            pass

    def rmtree(self, path: str) -> None:
        """Remove a directory and its contents."""
        try:
            self._counter += 1
            shutil.rmtree(path, ignore_errors=True)
        except Exception:  # pylint: disable=broad-exception-caught
            pass

    def threaded_remove(self, src_path: str) -> None:
        """Remove files and directories using multi-threading."""
        for filename in os.listdir(src_path):
            file_path = os.path.join(src_path, filename)
            if os.path.isfile(file_path):
                thread = threading.Thread(target=self.remove, args=(file_path,))
                thread.daemon = True
                thread.start()
            elif os.path.islink(file_path):
                thread = threading.Thread(target=self.unlink, args=(file_path,))
                thread.daemon = True
                thread.start()
            elif os.path.isdir(file_path):
                for nested_filename in os.listdir(file_path):
                    nested_filepath = os.path.join(file_path, nested_filename)
                    if os.path.isfile(nested_filepath):
                        thread = threading.Thread(target=self.remove, args=(nested_filepath,))
                        thread.daemon = True
                        thread.start()
                    elif os.path.islink(nested_filepath):
                        thread = threading.Thread(target=self.unlink, args=(nested_filepath,))
                        thread.daemon = True
                        thread.start()
                    elif os.path.isdir(nested_filepath):
                        thread = threading.Thread(target=self.rmtree, args=(nested_filepath,))
                        thread.daemon = True
                        thread.start()
                    else:
                        pass
            else:
                pass
        thread = threading.Thread(target=self.remove, args=(src_path,))
        thread.daemon = True
        thread.start()

    def join_threads(self) -> None:
        """Wait for all threads to complete."""
        main_thread = threading.current_thread()
        for thread in threading.enumerate():
            if thread is main_thread:
                continue
            thread.join()

    def reset_counter(self) -> None:
        """Reset the counter to 0."""
        self._counter = 0


class UninstallEnvironmentHandler(APIHandler):
    """Handler for uninstalling environments."""

    @tornado.web.authenticated
    def post(self):
        """Remove environment's kernels and change slug directory
        to tmp so it can be deleted in the background."""
        input_data = self.get_json_body()
        slug = input_data.get("slug")

        env_path = os.path.join(local_qbraid_envs_path, slug)
        env_kernels = os.path.join(local_qbraid_envs_path, slug, "kernels")

        if os.path.isdir(env_kernels):
            kernel_spec_manager, kernels_list = get_kernels()
            for f in os.listdir(env_kernels):
                if f in kernels_list:
                    kernel_spec_manager.remove_kernel_spec(f)

        if os.path.isdir(env_path):
            tmp_dirs = sorted(
                (d for d in os.listdir(local_qbraid_envs_path) if re.match(r"tmp\d+$", d)),
                key=lambda x: int(x[3:]),
            )
            tmpn = f"tmp{int(tmp_dirs[-1][3:]) + 1}" if tmp_dirs else "tmp0"

            rm_dir = os.path.join(local_qbraid_envs_path, tmpn)
            os.makedirs(rm_dir, exist_ok=True)

            shutil.move(env_path, rm_dir)
            os.chmod(rm_dir, 0o777)

            thread = threading.Thread(target=self.remove_tmps, args=(local_qbraid_envs_path,))
            thread.start()

        data = {
            "status": 202,
            "message": f"Uninstalling environment {slug}.",
        }
        self.finish(json.dumps(data))

    def _remove_tmp_dirs(self, envs_path: str, threader: Optional[UninstallThreader] = None) -> int:
        pattern = re.compile(r"^tmp\d{1,2}$")  # Regex for tmp directories

        tmp_dirs = [os.path.join(envs_path, d) for d in os.listdir(envs_path) if pattern.match(d)]
        num_removed = 0

        for tmpdir in tmp_dirs:
            try:
                if threader:
                    threader.threaded_remove(tmpdir)
                else:
                    shutil.rmtree(tmpdir)
                num_removed += 1
            except Exception as err:  # pylint: disable=broad-exception-caught
                logging.error("Error removing directory %s: %s", tmpdir, err)
        return num_removed

    def remove_tmps(self, envs_path: str) -> None:
        """Remove tmp directories in the background."""
        start = time.time()
        threader = UninstallThreader()

        # Initial attempt to remove tmp directories using threaded removal
        num_envs = self._remove_tmp_dirs(envs_path, threader)

        # Wait for all threads to complete before proceeding
        time.sleep(5)  # TODO: Consider implementing a more dynamic wait based on thread completion

        # Re-check and remove any remaining tmp directories without threading
        num_rechecked = self._remove_tmp_dirs(envs_path)

        stop = time.time()
        delta = stop - start
        num_threads = threader.counter()  # Ensure this correctly returns the number of threads used
        threader.join_threads()
        threader.reset_counter()

        logging.info(
            "Successfully uninstalled %d env(s) in %.2fs using %d threads. "
            "Rechecked and found %d additional env(s).",
            num_envs,
            delta,
            num_threads,
            num_rechecked,
        )
