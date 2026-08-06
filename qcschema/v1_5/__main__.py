"""
Entry point for running the v1.5 schema generator as a module.
Run as: python -m qcschema.v1_5
"""

from .generate import build_v1p5_schemas, write_schemas

schemas = build_v1p5_schemas()
schema_dir = write_schemas(schemas)
print(f"✓ v1.5 schemas generated in {schema_dir}/")
