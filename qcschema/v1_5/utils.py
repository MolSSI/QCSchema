"""
Utilities for v1.5 schema generation.
"""

import json
from pathlib import Path


def write_schema(schema, filepath):
    """
    Write a v1.5 schema to a JSON file (minified, single line, with spacing).
    v1.5 schemas (v2 format) have a trailing newline.

    Args:
        schema: Schema dictionary
        filepath: Path to write to
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(schema, f, separators=(", ", ": "))
        f.write("\n")
