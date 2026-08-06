"""
Entry point for running the v1 schema generator as a module.
Run as: python -m qcschema.v1
"""

from .generate import build_v1_schemas, write_schemas

schemas = build_v1_schemas()
schema_dir = write_schemas(schemas)
print(f"✓ v1 schemas generated in {schema_dir}/")
