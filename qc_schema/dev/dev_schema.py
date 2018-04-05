"""
Integrates all components of the QC Schema into a single one.
"""

import copy

from . import molecule
from . import definitions
from . import properties

# The base schema definition
base_schema = {
    "$schema": "http://json-schema.org/draft-06/schema#",
    "name": "QC_JSON",
    "version": "0.1.dev",
    "url": "http://schema_host.org/schemas/v0.1/something.schema",
    "description": "The MolSSI Quantum Chemistry Schema",
    "type": "object",
    "properties": {
        "molecule": molecule.molecule,
        "schema_name": {
            "type": "string",
            "pattern": "\W*(QC_JSON)\W*"
        },
        "schema_version": {
            "type": "string"
        },
        "driver": {
            "definition": "The type of computation requested",
            "enum": ["energy", "gradient", "hessian"]
        },
        "model": {
            "definition": "The method and basis specification requested",
            "properties": {
                "method": {
                    "type": "string"
                },
                "basis": {
                    "type": "string"
                }
            },
            "required": ["method", "basis"],
            "description": "The quantum chemistry model to be run."
        },
        "keywords": {
            "type": "object",
            "description": "Program specific parameters to be used."
        },
        "provenance": {
            "anyOf": [{
                "type": "object",
                "$ref": "#/definitions/provenance"
            }, {
                "type": "array",
                "items": {
                    "type": "object",
                    "$ref": "#/definitions/provenance"
                }
            }]
        }
    },
    "required": ["schema_name", "schema_version", "molecule", "driver", "keywords", "model"],
    "definitions": definitions.definitions
}

# Additional properties to contain in the output
output_properties = {
    "properties": properties.properties,
    "success": {
        "type": "boolean"
    },
    "error": {
        "definition": "The type and description of error raised.",
        "type": "object",
        "$ref": "#/definitions/error"
    },
    "return_result": {
        "definition": "The primary specified return of the requested computation.",
        "anyOf": [{
            "type": "number"
        }, {
            "type": "array",
            "items": {"type": "number"}
        }]
    }
}

# Snapshot the input dev schema
input_dev_schema = copy.deepcopy(base_schema)

# Add additional output pieces
base_schema["properties"].update(output_properties)
base_schema["required"].extend(["provenance", "properties", "success", "return_result"])

# Snapshot the input dev schema
output_dev_schema = copy.deepcopy(base_schema)

#import json
#print(json.dumps(input_dev_schema, indent=2))
#print(json.dumps(output_dev_schema, indent=2))
