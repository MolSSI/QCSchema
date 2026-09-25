"""
Contains helper scripts to assist in testing the schema
"""

import glob
import json
import os


def _read_json_file(*filename):
    filename = os.path.join(*filename)
    with open(filename) as infile:
        data = json.load(infile)
    return data


# Find a few required relative paths
_test_path = os.path.dirname(os.path.abspath(__file__))
_base_path = os.path.dirname(_test_path)


def list_tests(folder, ext=".json", matcher=""):
    """
    Lists all tests in a given folder.
    """
    files = glob.glob(os.path.join(_test_path, folder, "*" + matcher + "*" + ext))
    names = [os.path.basename(x).replace(ext, "") for x in files]

    return files, names


def get_test(name):
    return _read_json_file(name)


def filter_versions(versions, exclude_pattern=None):
    """
    Filter versions for testing.

    Args:
        versions: List of version strings to filter
        exclude_pattern: String pattern to exclude (e.g., "qcelemental" to exclude
                        versions starting with that)

    Returns:
        Filtered list of versions
    """
    if exclude_pattern is None:
        return versions

    return [v for v in versions if not v.startswith(exclude_pattern)]
