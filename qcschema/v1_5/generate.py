#!/usr/bin/env python
"""
Generate v1.5 JSON Schema documents from schema component definitions.

v1.5 includes v1 base schemas plus wavefunction support.

Can be run as: python -m qcschema.v1_5.generate
Or imported to build schemas programmatically.

Usage:
    python -m qcschema.v1_5.generate

Output:
    - qcschema/v1_5/schemas/qc_schema_input.schema
    - qcschema/v1_5/schemas/qc_schema_molecule.schema
    - qcschema/v1_5/schemas/qc_schema_output.schema
"""

import copy
from pathlib import Path

from . import utils
from .generator import basis, definitions, molecule, properties, wavefunction


def build_v1p5_schemas():
    """Build v1.5 schemas (v1 base + wavefunction support)."""

    base_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "name": "qcschema_input",
        "version": "1.dev",
        "description": "The MolSSI Quantum Chemistry Schema",
        "type": "object",
        "properties": {
            "molecule": molecule.molecule,
            "schema_name": {"type": "string", "pattern": "^(qc_?schema)$"},
            "schema_version": {"type": "integer"},
            "driver": {"definition": "The type of computation requested", "enum": ["energy", "gradient", "hessian"]},
            "model": {
                "definition": "The method and basis specification requested",
                "properties": {
                    "method": {"type": "string"},
                    "basis": {
                        "anyOf": [
                            basis.basis,
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
        "definitions": definitions.definitions,
    }

    output_properties = {
        "properties": properties.properties,
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
    output_schema["properties"]["wavefunction"] = wavefunction.output_wavefunction
    output_schema["required"].extend(["provenance", "properties", "success", "return_result"])
    output_schema["properties"]["schema_name"]["pattern"] = "^(qc_?schema_output)$"

    molecule_schema = copy.deepcopy(molecule.molecule)

    return {
        "input": input_schema,
        "output": output_schema,
        "molecule": molecule_schema,
    }


def write_schemas(schemas, schema_dir=None):
    """Write schemas to disk."""
    if schema_dir is None:
        schema_dir = Path(__file__).parent / "schemas"

    schema_dir = Path(schema_dir)
    schema_dir.mkdir(parents=True, exist_ok=True)

    utils.write_schema(schemas["input"], schema_dir / "qc_schema_input.schema")
    utils.write_schema(schemas["output"], schema_dir / "qc_schema_output.schema")
    utils.write_schema(schemas["molecule"], schema_dir / "qc_schema_molecule.schema")

    return schema_dir


if __name__ == "__main__":
    schemas = build_v1p5_schemas()
    schema_dir = write_schemas(schemas)
    print(f"✓ v1.5 schemas generated in {schema_dir}/")
