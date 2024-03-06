"""
Script for updating the pre-release version in package.json.

"""

import json
import os

import requests
from packaging.version import Version, parse

PACKAGE_NAME = "jupyter_environment_manager"


def get_current_local_version() -> str:
    """Get the version from the package.json file."""
    try:
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "package.json",
        )

        with open(file_path, "r", encoding="utf-8") as file:
            package_json = json.load(file)
            version = package_json["version"]
            return version

    except (FileNotFoundError, KeyError, IOError) as err:
        raise Exception("Unable to find or read package.json") from err


def get_latest_pypi_version(package_name: str) -> str:
    """
    Fetch the latest release and pre-release versions of a package from PyPI.

    :param package_name: Name of the package on PyPI.
    :return: Dictionary with 'latest_release' and 'pre_releases' versions.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    data = response.json()

    try:
        all_versions = list(data["releases"].keys())
    except KeyError as err:
        raise Exception("Failed to fetch versions from PyPI") from err

    if len(all_versions) == 0:
        raise Exception(f"No versions found for {package_name}")

    latest_version = all_versions[-1]
    return latest_version


def get_bumped_version(latest: str, local: str) -> str:
    """Compare latest and local versions and return the bumped version."""
    latest_version = parse(latest)
    local_version = parse(local)

    def bump_prerelease(version: Version) -> str:
        if version.pre:
            pre_type, pre_num = version.pre[0], version.pre[1]
            return f"{version.base_version}-{pre_type}.{pre_num + 1}"
        return f"{version.base_version}-a.0"

    if local_version.base_version > latest_version.base_version:
        return f"{local_version.base_version}-a.0"
    if local_version.base_version == latest_version.base_version:
        if latest_version.is_prerelease:
            if local_version.is_prerelease:
                if local_version.pre[0] == latest_version.pre[0]:
                    if local_version.pre[1] > latest_version.pre[1]:
                        raise ValueError("Local version prerelease is newer than latest version.")
                    return bump_prerelease(latest_version)
                if local_version.pre[0] < latest_version.pre[0]:
                    return bump_prerelease(latest_version)
                return f"{local_version.base_version}-{local_version.pre[0]}.0"
            raise ValueError("Latest version is prerelease but local version is not.")
        if local_version.is_prerelease:
            return f"{local_version.base_version}-{local_version.pre[0]}.0"
        if local_version == latest_version:
            return f"{local_version.base_version}-a.0"
        raise ValueError("Local version base is equal to latest, but no clear upgrade path found.")
    raise ValueError("Latest version base is greater than local, cannot bump.")


def update_version(new_version: str) -> None:
    """Update the version in the package.json file."""
    try:
        # Define the path to the package.json file
        file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "package.json",
        )

        # Read the current contents of the package.json file
        with open(file_path, "r", encoding="utf-8") as file:
            package_json = json.load(file)

        # Update the version key with the new version
        package_json["version"] = new_version

        # Write the updated dictionary back to the package.json file
        with open(file_path, "w") as file:
            json.dump(package_json, file, indent=4)  # Use indent for pretty-printing

    except (FileNotFoundError, KeyError, IOError) as err:
        raise Exception("Unable to find or update package.json") from err


if __name__ == "__main__":

    local_version = get_current_local_version()
    latest_version = get_latest_pypi_version(PACKAGE_NAME)
    prerelease_version = get_bumped_version(latest_version, local_version)
    update_version(prerelease_version)
