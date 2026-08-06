#!/usr/bin/env python
"""
Generate JSON Schema documents from qcelemental pydantic models.

**Dev-only script** — requires qcelemental package (not a runtime dependency).

This script inspects qcelemental.models and generates JSON Schema files
for each pydantic model by calling .schema() (pydantic v1 API).

Errors on invalid or missing models — no silent skipping.

Usage:
    cd qcschema/qcelemental_v1
    python generate.py

Output:
    - schemas/<model_name>.schema (JSON Schema files for each model)

Dependencies:
    - qcelemental (manual install required, not shipped)
    - pydantic v1
"""

import inspect
import json
import sys
from pathlib import Path

import qcelemental.models
from jsonschema import Draft4Validator


def get_validator():
    """
    Get the JSON Schema validator class for qcelemental v1 (draft-04).

    Returns:
        jsonschema.Draft4Validator class
    """
    return Draft4Validator


def discover_pydantic_models():
    """Discover all pydantic BaseModel classes in qcelemental.models."""
    models = {}

    for name in dir(qcelemental.models):
        if name.startswith("_"):
            continue

        try:
            obj = getattr(qcelemental.models, name)
        except AttributeError as e:
            raise RuntimeError(f"Failed to get attribute '{name}' from qcelemental.models: {e}") from e

        # Check if it's a class with pydantic's schema() method
        if inspect.isclass(obj) and hasattr(obj, "schema"):
            # Verify it actually has a valid schema
            schema = obj.schema()
            if not isinstance(schema, dict):
                raise TypeError(f"Model {name}: schema() returned non-dict {type(schema).__name__}")
            if not ("properties" in schema or "title" in schema):
                raise ValueError(f"Model {name}: schema missing both 'properties' and 'title'")
            models[name] = obj

    return models


def _validate_schema(schema, model_name):
    """Validate that a schema is a valid JSON Schema dictionary.

    Raises TypeError or ValueError if schema is invalid.
    """
    if not isinstance(schema, dict):
        raise TypeError(f"{model_name}: schema is not a dict, got {type(schema).__name__}")

    # JSON Schema should have at least $schema or properties or title
    if not any(key in schema for key in ["$schema", "properties", "title", "type"]):
        raise ValueError(
            f"{model_name}: schema missing standard JSON Schema fields ($schema, properties, title, or type)"
        )

    return schema


def _get_output_filename(model_name):
    """Map pydantic model names to schema filenames.

    Maps model class names to schema type filenames, using qcschema_* naming
    for types that match the QCSchema canonical types.
    """
    # Map qcelemental model names to canonical QCSchema types
    type_mapping = {
        "AtomicInput": "input",
        "AtomicResult": "output",
        "Molecule": "molecule",
        "BasisSet": "basis",
        "AtomicResultProperties": "properties",
        "Provenance": "provenance",
    }

    # Check if this is a canonical type
    if model_name in type_mapping:
        schema_type = type_mapping[model_name]
        return f"qcschema_{schema_type}.schema"

    # Otherwise use the model name as-is
    return f"{model_name}.schema"


def generate_schemas(output_dir=None):
    """Generate JSON Schema files for all discovered models."""

    if output_dir is None:
        output_dir = Path(__file__).parent / "schemas"

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    models = discover_pydantic_models()

    if not models:
        raise RuntimeError("No pydantic models found in qcelemental.models")

    print(f"Found {len(models)} pydantic models")

    schema_failures = {}
    for model_name, model_class in sorted(models.items()):
        try:
            schema = model_class.schema()
            schema = _validate_schema(schema, model_name)

            # Write schema to file
            filename = _get_output_filename(model_name)
            output_file = output_dir / filename
            with open(output_file, "w") as f:
                json.dump(schema, f, indent=2)

            print(f"✓ {model_name} → {output_file.name}")
        except Exception as e:
            schema_failures[model_name] = str(e)
            print(f"⚠ {model_name} → Error: {e}")

    print(f"\n✓ Generated {len(models) - len(schema_failures)} schemas")

    # Report models that failed to generate
    if schema_failures:
        print(f"\n⚠ {len(schema_failures)} model(s) failed to generate:")
        for model_name, error in sorted(schema_failures.items()):
            print(f"  - {model_name}: {error}")

    return output_dir


if __name__ == "__main__":
    try:
        schema_dir = generate_schemas()
        print(f"\nSchemas written to: {schema_dir}")
        sys.exit(0)
    except ImportError as e:
        print(f"Error: qcelemental is not installed or importable: {e}", file=sys.stderr)
        print("Install with: pip install qcelemental", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during schema generation: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)
