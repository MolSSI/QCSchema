"""
A simple program to construct the input and ouput Quantum Chemistry Schema's
from the development branch
"""

from . import dev
from . import data

_schema_input_dict = {}
_schema_output_dict = {}

# Hooks for non-dev versions
# _schema_input_dict.update(data.input_schemas)
# _schema_output_dict.update(data.output_schemas)

# Add in dev schema

_schema_input_dict["dev"] = dev.input_dev_schema
_schema_output_dict["dev"] = dev.output_dev_schema

# Double check all of the keys are correctly entered
assert _schema_input_dict.keys() == _schema_output_dict.keys()

def list_versions():
    """
    Lists all current JSON schema versions.
    """
    return list(_schema_input_dict)

def get_schema(schema_type, version="dev"):
    """
    Returns the requested schema (input or output) for a given version number.
    """

    if version not in _schema_input_dict:
        raise KeyError("Schema version %s not found." % version)

    
    if schema_type.lower() == "input":
        return _schema_input_dict[version] 

    elif schema_type.lower() == "output":
        return _schema_output_dict[version] 
    else:
        raise KeyError("Schema type should either be 'input' or 'output', given: %s." % schema_type)
