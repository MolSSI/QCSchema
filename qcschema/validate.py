"""
Schema validation tools
"""

import jsonschema

from . import versions


def validate(data, schema_type, version="dev"):
    """
    Validates a given input for a schema input and output type.
    """
    schema = versions.get_schema(schema_type, version)

    jsonschema.validate(data, schema)
