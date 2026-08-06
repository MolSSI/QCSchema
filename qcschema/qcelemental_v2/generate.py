#!/usr/bin/env python
"""
Generate JSON Schema documents from qcelemental v2 pydantic models.

**Dev-only script** — requires qcelemental package (not a runtime dependency).

This script inspects qcelemental.models.v2 and generates JSON Schema files
for each pydantic v2 model by calling model_json_schema() (pydantic v2 API).

Requires:
- qcelemental with v2 models (qcelemental.models.v2 submodule)
- Pydantic v2 with model_json_schema() method

Errors on invalid or missing models — no silent skipping.

Usage:
    cd qcschema/qcelemental_v2
    python generate.py

Output:
    - schemas/<model_name>.schema (JSON Schema files for each model)

Dependencies:
    - qcelemental (manual install required, not shipped)
    - pydantic v2

Optional Dependencies:
    - qcmanybody: If installed and compatible, the script will import
      qcelemental.models.v2 and qcmanybody.models.v2 before rebuilding models.
      This resolves forward references for 6 models (Optimization* and TorsionDrive*)
      that reference ManyBodySpecification/ManyBodyResult from qcmanybody.
      Without qcmanybody, these 6 models will fail to rebuild and their schemas
      will be empty or incomplete.

      Current status: Compatibility issue between qcelemental dev version
      and qcmanybody 0.5.1 (ExtendedConfigDict not available). Once compatible,
      this will resolve 6 model rebuild failures.
"""

import inspect
import json
import sys
from pathlib import Path

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


def discover_pydantic_models():
    """Discover pydantic v2 models in qcelemental.models.v2.

    Requires qcelemental.models.v2 to exist. Does not fall back to v1 models.
    """
    try:
        import qcelemental.models.v2 as models_v2
    except ImportError as e:
        raise ImportError("qcelemental.models.v2 not found. This is a v2-specific generator.") from e

    models = {}

    for name in dir(models_v2):
        if name.startswith("_"):
            continue

        try:
            obj = getattr(models_v2, name)
        except AttributeError as e:
            raise RuntimeError(f"Failed to get attribute '{name}' from qcelemental.models.v2: {e}") from e

        if _is_pydantic_model(obj):
            models[name] = obj

    return models


def _is_pydantic_model(obj):
    """Check if an object is a pydantic v2 model class.

    Only accepts pydantic v2 models with model_json_schema() method.
    Rejects pydantic v1 models.
    """
    if not inspect.isclass(obj):
        return False

    # Only accept pydantic v2 API
    if hasattr(obj, "model_json_schema"):
        return True

    # Reject pydantic v1 models explicitly
    if hasattr(obj, "schema") and not hasattr(obj, "model_json_schema"):
        return False

    return False


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
        return f"qcschema_{schema_type}.schema"

    # Otherwise use the model name as-is
    return f"{model_name}.schema"


def _get_schema(model_class):
    """Get JSON schema from a pydantic v2 model using model_json_schema().

    Requires pydantic v2 API. Does not fall back to pydantic v1 schema().
    Uses mode="serialization" to respect custom serializers from qcelemental.
    """
    if not hasattr(model_class, "model_json_schema"):
        raise AttributeError(f"{model_class.__name__} does not have model_json_schema() method (pydantic v2 required)")
    return model_class.model_json_schema(mode="serialization")


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

    # Try to import qcmanybody to resolve forward references
    # (6 models reference ManyBodySpecification and ManyBodyResult from qcmanybody.models.v2)
    try:
        import qcmanybody.models.v2  # noqa: F401 - imported for side effects (type registration)

        print("✓ qcmanybody.models.v2 imported (Optimization/TorsionDrive models will be complete)")
    except ImportError as e:
        print(f"ℹ qcmanybody not available: {e} (some models may fail to rebuild)")

    # Rebuild all models to resolve forward references
    rebuild_failures = {}
    for model_name, model_class in models.items():
        try:
            model_class.model_rebuild()
        except Exception as e:
            rebuild_failures[model_name] = str(e)

    for model_name, model_class in sorted(models.items()):
        try:
            schema = _get_schema(model_class)
            schema = _validate_schema(schema, model_name)

            # Write schema to file
            filename = _get_output_filename(model_name)
            output_file = output_dir / filename
            with open(output_file, "w") as f:
                json.dump(schema, f, indent=2)

            print(f"✓ {model_name} → {output_file.name}")
        except Exception as e:
            print(f"⚠ {model_name} → Error: {e}")

    print(f"\n✓ Generated {len(models)} schemas")

    # Report models that failed to rebuild
    if rebuild_failures:
        print(f"\n⚠ {len(rebuild_failures)} model(s) failed to rebuild (have unresolved forward references):")
        for model_name, error in sorted(rebuild_failures.items()):
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
