"""
Utilities for qcelemental v1 schema validation.
"""

from jsonschema import Draft4Validator


def get_validator():
    """
    Get the JSON Schema validator class for qcelemental v1 (draft-04).

    Returns:
        jsonschema.Draft4Validator class
    """
    return Draft4Validator
