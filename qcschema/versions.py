"""
A simple program to construct the input and ouput Quantum Chemistry Schema's
from the development branch
"""

import json

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from . import dev

_data_path = Path(__file__).parent.resolve() / "data"

_aliases = {
    "input": ["input", "AtomicInput"],
    "output": ["output", "AtomicResult"],
    "molecule": ["molecule", "topology", "Molecule"],
    "basis": ["basis", "BasisSet"],
    "properties": ["properties", "AtomicResultProperties"],
    "provenance": ["provenance", "Provenance"],
}
_laliases = {k: [v2.lower() for v2 in v] for k, v in _aliases.items()}

_versions_list = {
    "input": [1, 2, "dev"],
    "output": [1, 2, "dev"],
    "molecule": [1, 2, "dev"],
    "basis": ["dev"],
    "properties": ["dev"],
    "provenance": ["dev"],
}
_sversions_list = {k: [str(v2) for v2 in v] for k, v in _versions_list.items()}


def list_versions(schema_type):
    """
    Lists all current JSON schema versions.
    """
    for sk, aliases in _laliases.items():
        if schema_type.lower() in aliases:
            return _versions_list[sk]

    raise KeyError("Schema type should be among {} (+aliases), not '{}'.".format(list(_aliases.keys()), schema_type))


def get_schema(schema_type, version="dev"):
    """
    Returns the requested schema (input or output) for a given version number.
    """

    for sk, aliases in _laliases.items():
        if schema_type.lower() in aliases:
            if str(version) in _sversions_list[sk]:
                if version == "dev" or int(version) > 2:
                    fname = _aliases[sk][-1]
                else:  # v1, v2
                    fname = "qc_schema_" + sk
                break
            else:
                raise KeyError("Schema version should be among {}, not '{}'.".format(_versions_list[sk], version))
    else:
        raise KeyError(
            "Schema type should be among {} (+aliases), not '{}'.".format(list(_aliases.keys()), schema_type)
        )

    fpath = _data_path / ("v" + str(version)) / (fname + ".schema")
    ret = json.loads(fpath.read_text())

    return ret
