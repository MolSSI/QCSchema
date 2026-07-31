"""
Shared utilities for QCSchema generation and management.
"""

import copy
import json
from pathlib import Path


def assemble_schema(base, properties_dict, definitions_dict):
    """
    Assemble a complete schema from base, properties, and definitions.

    Args:
        base: Base schema dictionary
        properties_dict: Additional properties to add
        definitions_dict: Definitions block

    Returns:
        Complete schema dictionary
    """
    schema = copy.deepcopy(base)
    if properties_dict:
        schema["properties"].update(properties_dict)
    if definitions_dict:
        schema["definitions"] = definitions_dict
    return schema


def write_schema(schema, filepath):
    """
    Write a schema to a JSON file (minified, single line, with spacing).

    Args:
        schema: Schema dictionary
        filepath: Path to write to
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(schema, f, separators=(", ", ": "))


def read_schema(filepath):
    """
    Read a schema from a JSON file.

    Args:
        filepath: Path to read from

    Returns:
        Schema dictionary
    """
    with open(filepath) as f:
        return json.load(f)


def get_schema_dir(version):
    """
    Get the directory path for a given schema version.

    Args:
        version: Version string (e.g., '1', '1.5', 'qcelemental_v1')

    Returns:
        Path to schemas directory
    """
    return Path(__file__).parent / f"{version}" / "schemas"
