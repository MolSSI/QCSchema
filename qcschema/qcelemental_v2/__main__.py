"""
Entry point for running the qcelemental v2 schema generator as a module.
Run as: python -m qcschema.qcelemental_v2
"""

import sys

try:
    from .generate import generate_schemas

    schema_dir = generate_schemas()
    print(f"\nSchemas written to: {schema_dir}")
except ImportError as e:
    print(f"Error: qcelemental is not installed or importable: {e}", file=sys.stderr)
    print("Install with: pip install qcelemental", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error during schema generation: {e}", file=sys.stderr)
    import traceback

    traceback.print_exc()
    sys.exit(1)
