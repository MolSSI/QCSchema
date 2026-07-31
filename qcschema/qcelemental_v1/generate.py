#!/usr/bin/env python
"""
Generate JSON Schema documents from qcelemental pydantic models.

**Dev-only script** — requires qcelemental package (not a runtime dependency).

This script inspects qcelemental.models and generates JSON Schema files
for each pydantic model by calling .schema() (pydantic v1 API).

Models with numpy fields may raise errors; these are logged and skipped.

Usage:
    cd qcschema/qcelemental_v1
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
    """Discover all pydantic BaseModel classes in qcelemental.models."""
    models = {}

    for name in dir(qcelemental.models):
        if name.startswith("_"):
            continue

        obj = getattr(qcelemental.models, name)

        # Check if it's a class with pydantic's schema() method
        if inspect.isclass(obj) and hasattr(obj, "schema"):
            try:
                # Verify it actually has a valid schema
                schema = obj.schema()
                if isinstance(schema, dict) and ("properties" in schema or "title" in schema):
                    models[name] = obj
            except Exception:
                # Skip if schema() fails
                pass

    return models


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
            schema = model_class.schema()

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
