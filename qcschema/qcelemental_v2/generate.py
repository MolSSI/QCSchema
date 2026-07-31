#!/usr/bin/env python
"""
Generate JSON Schema documents from qcelemental v2 pydantic models.

**Dev-only script** — requires qcelemental package (not a runtime dependency).

This script inspects qcelemental.models (with priority to v2 schemas) and
generates JSON Schema files for each pydantic model using either:
- model_json_schema() if available (pydantic v2)
- .schema() if available (pydantic v1 compatibility mode)

Models with numpy fields may raise errors; these are logged and skipped.

Usage:
    cd qcschema/qcelemental_v2
    python generate.py

Output:
    - schemas/<model_name>.schema (JSON Schema files for each model)

Dependencies:
    - qcelemental (manual install required, not shipped)
"""

import inspect
import json
import sys
from pathlib import Path

import qcelemental.models


def discover_pydantic_models():
    """Discover pydantic models in qcelemental.models, prioritizing v2.

    First tries qcelemental.models.v2 if it exists (future proofing).
    Falls back to qcelemental.models and filters for v2-compatible schemas.
    """
    models = {}

    # Try v2 submodule first (future-proofing for when qcelemental splits versions)
    try:
        import qcelemental.models.v2 as models_v2

        for name in dir(models_v2):
            if name.startswith("_"):
                continue

            obj = getattr(models_v2, name)
            if _is_pydantic_model(obj):
                models[name] = obj

        if models:
            return models
    except (ImportError, AttributeError):
        pass

    # Fall back to qcelemental.models (filtering if needed)
    for name in dir(qcelemental.models):
        if name.startswith("_"):
            continue

        obj = getattr(qcelemental.models, name)
        if _is_pydantic_model(obj):
            models[name] = obj

    return models


def _is_pydantic_model(obj):
    """Check if an object is a pydantic model class."""
    if not inspect.isclass(obj):
        return False

    # Check for pydantic v2 API
    if hasattr(obj, "model_json_schema"):
        return True

    # Check for pydantic v1 API
    if hasattr(obj, "schema"):
        try:
            schema = obj.schema()
            return isinstance(schema, dict) and ("properties" in schema or "title" in schema)
        except Exception:
            return False

    return False


def _get_output_filename(model_name):
    """Map pydantic model names to schema filenames.

    Maps model class names to schema type filenames, using qc_schema_* naming
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
        return f"qc_schema_{schema_type}.schema"

    # Otherwise use the model name as-is
    return f"{model_name}.schema"


def _get_schema(model_class):
    """Get JSON schema from a pydantic model using available API.

    Tries pydantic v2 API first (model_json_schema), then falls back to v1 (schema).
    """
    if hasattr(model_class, "model_json_schema"):
        return model_class.model_json_schema()
    elif hasattr(model_class, "schema"):
        return model_class.schema()
    else:
        raise ValueError(f"{model_class} has no schema generation method")


def generate_schemas(output_dir=None):
    """Generate JSON Schema files for all discovered models."""

    if output_dir is None:
        output_dir = Path(__file__).parent / "schemas"

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    models = discover_pydantic_models()

    if not models:
        print("Warning: No pydantic models found in qcelemental.models")
        return output_dir

    print(f"Found {len(models)} pydantic models")

    successful = []
    skipped = []

    for model_name, model_class in sorted(models.items()):
        try:
            schema = _get_schema(model_class)

            # Write schema to file
            filename = _get_output_filename(model_name)
            output_file = output_dir / filename
            with open(output_file, "w") as f:
                json.dump(schema, f, indent=2)

            successful.append(model_name)
            print(f"✓ {model_name} → {output_file.name}")

        except KeyError as e:
            # Handle numpy dtype errors
            if "dtype" in str(e):
                skipped.append(f"{model_name} (numpy field: {e})")
                print(f"⊘ {model_name} (skipped: numpy field causing {e})")
            else:
                skipped.append(f"{model_name} ({e})")
                print(f"⊘ {model_name} (skipped: {e})")
        except Exception as e:
            skipped.append(f"{model_name} ({type(e).__name__}: {e})")
            print(f"⊘ {model_name} (skipped: {type(e).__name__}: {e})")

    print(f"\n✓ Generated {len(successful)} schemas")
    if skipped:
        print(f"⊘ Skipped {len(skipped)} models:")
        for item in skipped:
            print(f"  - {item}")

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
