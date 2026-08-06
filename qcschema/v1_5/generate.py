#!/usr/bin/env python
"""
Generate v1.5 JSON Schema documents from schema component definitions.

v1.5 includes v1 base schemas plus wavefunction support.

Can be run as: python -m qcschema.v1_5.generate
Or imported to build schemas programmatically.

Usage:
    python -m qcschema.v1_5.generate

Output:
    - qcschema/v1_5/schemas/qcschema_input.schema
    - qcschema/v1_5/schemas/qcschema_molecule.schema
    - qcschema/v1_5/schemas/qcschema_output.schema
"""

import copy
import json
import sys
from pathlib import Path

from jsonschema import Draft4Validator

sys.path.insert(0, str(Path(__file__).parent / "generator" / "properties"))
from .generator import basis, definitions, molecule, properties, wavefunction


def write_schema(schema, filepath):
    """
    Write a v1.5 schema to a JSON file (minified, single line, with spacing).
    v1.5 schemas have a trailing newline.

    Args:
        schema: Schema dictionary
        filepath: Path to write to
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(schema, f, separators=(", ", ": "))
        f.write("\n")


def get_validator():
    """
    Get the JSON Schema validator class for v1.5 (draft-04).

    Returns:
        jsonschema.Draft4Validator class
    """
    return Draft4Validator


def _validate_schema_component(component, name):
    """Validate that a schema component is a valid dictionary with schema structure.

    For definition components, validates that each sub-component has schema keywords.
    Raises TypeError or ValueError if component is invalid.
    """
    if not isinstance(component, dict):
        raise TypeError(f"Schema component '{name}' is not a dict, got {type(component).__name__}")

    if not component:
        raise ValueError(f"Schema component '{name}' is empty")

    # If this looks like a definitions object (contains multiple schema fragments),
    # validate that each fragment has schema keywords
    if "definitions" in name or name.endswith("definitions"):
        for component_name, fragment in component.items():
            if not isinstance(fragment, dict):
                raise TypeError(f"Component '{name}[{component_name}]' is not a dict, got {type(fragment).__name__}")

            if not any(key in fragment for key in ["type", "properties", "enum", "description", "$ref"]):
                raise ValueError(f"Component '{name}[{component_name}]' missing schema keywords")

    return component


def _validate_full_schema(schema, schema_name):
    """Validate that a schema is a valid JSON Schema dictionary.

    Raises TypeError or ValueError if schema is invalid.
    """
    if not isinstance(schema, dict):
        raise TypeError(f"{schema_name}: schema is not a dict, got {type(schema).__name__}")

    # JSON Schema should have at least $schema or properties or title
    if not any(key in schema for key in ["$schema", "properties", "title", "type"]):
        raise ValueError(
            f"{schema_name}: schema missing standard JSON Schema fields ($schema, properties, title, or type)"
        )

    return schema


def build_v1p5_schemas():
    """Build v1.5 schemas (v1 base + wavefunction support).

    Validates all imported schema components and returned schemas.
    """
    # Validate imported components
    molecule_component = _validate_schema_component(molecule.molecule, "molecule.molecule")
    basis_component = _validate_schema_component(basis.basis, "basis.basis")
    definitions_component = _validate_schema_component(definitions.definitions, "definitions.definitions")
    properties_component = _validate_schema_component(properties.properties, "properties.properties")
    wavefunction_component = _validate_schema_component(
        wavefunction.output_wavefunction, "wavefunction.output_wavefunction"
    )

    base_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "name": "qcschema_input",
        "version": "1.dev",
        "description": "The MolSSI Quantum Chemistry Schema",
        "type": "object",
        "properties": {
            "molecule": molecule_component,
            "schema_name": {"type": "string", "pattern": "^(qc_?schema)$"},
            "schema_version": {"type": "integer"},
            "driver": {"definition": "The type of computation requested", "enum": ["energy", "gradient", "hessian"]},
            "model": {
                "definition": "The method and basis specification requested",
                "properties": {
                    "method": {"type": "string"},
                    "basis": {
                        "anyOf": [
                            basis_component,
                            {"description": "Name of the basis set to apply to the whole molecule", "type": "string"},
                        ]
                    },
                },
                "required": ["method", "basis"],
                "description": "The quantum chemistry model to be run.",
            },
            "keywords": {"type": "object", "description": "Program specific parameters to be used."},
            "provenance": {
                "anyOf": [
                    {"type": "object", "$ref": "#/definitions/provenance"},
                    {"type": "array", "items": {"type": "object", "$ref": "#/definitions/provenance"}},
                ]
            },
        },
        "required": ["schema_name", "schema_version", "molecule", "driver", "keywords", "model"],
        "definitions": definitions_component,
    }

    output_properties = {
        "properties": properties_component,
        "success": {"type": "boolean"},
        "error": {
            "definition": "The type and description of error raised.",
            "type": "object",
            "$ref": "#/definitions/error",
        },
        "return_result": {
            "definition": "The primary specified return of the requested computation.",
            "anyOf": [{"type": "number"}, {"type": "array", "items": {"type": "number"}}],
        },
    }

    input_schema = copy.deepcopy(base_schema)
    input_schema["name"] = "qcschema_input"
    input_schema["properties"]["schema_name"]["pattern"] = "^(qc_?schema_input)$"

    output_schema = copy.deepcopy(base_schema)
    output_schema["name"] = "qcschema_output"
    output_schema["version"] = "1.dev"
    output_schema["properties"].update(output_properties)
    output_schema["properties"]["wavefunction"] = wavefunction_component
    output_schema["required"].extend(["provenance", "properties", "success", "return_result"])
    output_schema["properties"]["schema_name"]["pattern"] = "^(qc_?schema_output)$"

    molecule_schema = copy.deepcopy(molecule_component)

    # Validate all schemas before returning
    schemas = {
        "input": input_schema,
        "output": output_schema,
        "molecule": molecule_schema,
    }

    for schema_name, schema in schemas.items():
        _validate_full_schema(schema, f"v1.5 {schema_name} schema")

    return schemas


def write_schemas(schemas, schema_dir=None):
    """Write schemas to disk.

    Validates schemas exist and writes them to disk.
    Raises KeyError if required schema keys missing.
    """
    if schema_dir is None:
        schema_dir = Path(__file__).parent / "schemas"

    schema_dir = Path(schema_dir)
    schema_dir.mkdir(parents=True, exist_ok=True)

    # Validate that all required schema keys exist
    required_keys = {"input", "output", "molecule"}
    missing_keys = required_keys - set(schemas.keys())
    if missing_keys:
        raise KeyError(f"Schemas missing required keys: {missing_keys}")

    # Write each schema
    try:
        write_schema(schemas["input"], schema_dir / "qcschema_input.schema")
    except Exception as e:
        raise RuntimeError(f"Failed to write input schema: {e}") from e

    try:
        write_schema(schemas["output"], schema_dir / "qcschema_output.schema")
    except Exception as e:
        raise RuntimeError(f"Failed to write output schema: {e}") from e

    try:
        write_schema(schemas["molecule"], schema_dir / "qcschema_molecule.schema")
    except Exception as e:
        raise RuntimeError(f"Failed to write molecule schema: {e}") from e

    return schema_dir


if __name__ == "__main__":
    schemas = build_v1p5_schemas()
    schema_dir = write_schemas(schemas)
    print(f"✓ v1.5 schemas generated in {schema_dir}/")
