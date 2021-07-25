"""
Contains helper scripts to assist in testing the schema
"""

import glob
import json
import os


def _read_json_file(*filename):
    filename = os.path.join(*filename)
    with open(filename, "r") as infile:
        data = json.load(infile)
    return data

# Find a few required relative paths
_test_path = os.path.dirname(os.path.abspath(__file__))


def list_tests(folder, ext=".json", matcher=""):
    """
    Lists all tests in a given folder.

    Since this function operates under the assumption that tests were expected
    in the given folder, raise a RuntimeError if none were found.  This is a
    workaround for tests being skipped when their parametrizations receive no
    values.
    """
    files = glob.glob(os.path.join(_test_path, folder, "*" + matcher + "*" + ext))
    names = [os.path.basename(x).replace(ext, "") for x in files]

    if not files:
        raise RuntimeError(
            "No files were found in the folder "
            "{} with the extension '{}' and matcher '{}'".format(
                os.path.abspath(folder), ext, matcher
            )
        )

    return files, names

def get_test(name):
    return _read_json_file(name)
    
