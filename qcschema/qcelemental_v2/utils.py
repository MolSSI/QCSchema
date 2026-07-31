"""
Utilities for qcelemental v2 schema validation.
"""

from jsonschema import Draft4Validator


def get_validator():
    """
    Get the JSON Schema validator class for qcelemental v2.

    Returns Draft4Validator for current qcelemental (which generates draft-04).
    Will be updated to Draft202012Validator when qcelemental v2 moves to 2020-12.

    Returns:
        jsonschema.Draft4Validator class
    """
    return Draft4Validator
