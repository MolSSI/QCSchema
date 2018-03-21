"""
Contains helper scripts to assist in testing the schema
"""

import pytest
import os
import glob
import copy
import json
import subprocess


def _read_json_file(*filename):
    filename = os.path.join(*filename)
    with open(filename, "r") as infile:
        data = json.load(infile)
    return data

# Find a few required relative paths
_test_path = os.path.dirname(os.path.abspath(__file__))
_base_path = os.path.dirname(_test_path)
_schema_path = os.path.join(_base_path, "schema")

# Generate the schema quickly (super hacky change later)
os.chdir(_schema_path)
subprocess.call(["python", "build_dev_schema.py"])
os.chdir(_test_path)

# Dictionary of known schema versions
_input_schemas = {}
_output_schemas = {}
_schema_versions = ["dev"]

# Pull in dev schema
_input_schemas["dev"] = _read_json_file(_schema_path, "input_qc_schema.schema")
_output_schemas["dev"] = _read_json_file(_schema_path, "output_qc_schema.schema")

# Pull in previous versions
for version_path in glob.glob(os.path.join(_schema_path, "v*")):
    version = os.path.basename(version_path)

    _input_schemas[version] = _read_json_file(version_path, "input_qc_schema.schema")
    _output_schemas[version] = _read_json_file(version_path, "output_qc_schema.schema")
    _schema_versions.append(version)

def list_versions():
    """
    Lists all schema versions detected by the tests.
    """
    return copy.deepcopy(_schema_versions)

def test_folder():
    """
    Returns the testing folder.
    """
    return _test_path

def list_tests(folder):
    """
    Lists all tests in a given folder.
    """
    files = glob.glob(os.path.join(_test_path, folder, "*"))
    files = [x.replace(_test_path, "") for x in files]

    return files

def get_test(name):
    return _read_json_file(_test_path + name)
    

def find_schema(version, schema_type):
    """
    Returns the appropriate schema version.
    """

    if schema_type == "input":
        return _input_schemas[version]
    elif schema_type == "output":
        return _output_schemas[version]
    else:
        raise KeyError("schema_type can only be either 'input' or 'output', found %s" % schema_type)


