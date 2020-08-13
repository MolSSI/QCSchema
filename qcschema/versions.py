"""
A simple program to construct the input and ouput Quantum Chemistry Schema's
from the development branch
"""

import json
import os
from pathlib import Path

from . import dev

_data_path = Path(__file__).resolve().parent / "data"

_input_version_list = ["dev", 1, 2]
_output_version_list = ["dev", 1, 2]
_molecule_version_list = ["dev", 1, 2]

_schema_input_dict = {"dev": dev.input_dev_schema}
_schema_output_dict = {"dev": dev.output_dev_schema}
_schema_molecule_dict = {"dev": dev.molecule_dev_schema}


def _load_schema(schema_type, version):
    if schema_type == "input":
        fname = "qc_schema_input.schema"
    elif schema_type == "output":
        fname = "qc_schema_output.schema"
    elif schema_type == "molecule":
        fname = "qc_schema_molecule.schema"
    else:
        raise KeyError("Schema type %s not understood." % schema_type)

    fpath = _data_path / ("v" + str(version)) / fname
    ret = json.loads(fpath.read_text())

    return ret


def list_versions(schema_type):
    """
    Lists all current JSON schema versions.
    """
    if schema_type == "input":
        return list(_input_version_list)
    elif schema_type == "output":
        return list(_output_version_list)
    elif schema_type == "molecule":
        return list(_molecule_version_list)
    else:
        raise KeyError("Schema type %s not understood." % schema_type)


def get_schema(schema_type, version="dev"):
    """
    Returns the requested schema (input or output) for a given version number.
    """

    schema_type = schema_type.lower()

    # Correctly type the results
    if schema_type == "input":
        versions = _input_version_list
        data = _schema_input_dict
    elif schema_type == "output":
        versions = _output_version_list
        data = _schema_output_dict
    elif schema_type == "molecule":
        versions = _molecule_version_list
        data = _schema_molecule_dict
    else:
        raise KeyError("Schema type should either be 'input', 'output', or 'molecule' given: %s." %
                       schema_type)

    if version not in versions:
        raise KeyError("Schema version %s not found." % version)

    # Lazy load data
    if version not in data:
        data[version] = _load_schema(schema_type, version)

    return data[version]
