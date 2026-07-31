"""
Utilities for v1.5 schema generation and validation.
"""

import json
from pathlib import Path

from jsonschema import Draft4Validator


def write_schema(schema, filepath):
    """
    Write a v1.5 schema to a JSON file (minified, single line, with spacing).
    v1.5 schemas have a trailing newline.

    Args:
        schema: Schema dictionary
        filepath: Path to write to
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(schema, f, separators=(", ", ": "))
        f.write("\n")


def get_validator():
    """
    Get the JSON Schema validator class for v1.5 (draft-04).

    Returns:
        jsonschema.Draft4Validator class
    """
    return Draft4Validator
