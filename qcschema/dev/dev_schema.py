"""
Integrates all components of the QC Schema into a single one.
"""

import copy

from . import molecule
from . import definitions
from . import properties

# The base schema definition
base_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "name": "qc_schema_input",
    "version": "dev",
    "url": "http://schema_host.org/schemas/0/something.schema",
    "description": "The MolSSI Quantum Chemistry Schema",
    "type": "object",
    "properties": {
        "molecule": molecule.molecule,
        "schema_name": {
            "type": "string",
            "pattern": "\W*(qc_schema)\W*"
        },
        "schema_version": {
            "type": "integer"
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
                },
                "basis_spec": {
                    "$ref": "#/definitions/basis_spec"
                }
            },
            "required": [ "method" ],
            "oneOf": [
                {
                    "required": ["basis"]
                },
                {
                    "required": ["basis_spec"]
                }
            ],
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
input_dev_schema["name"] = "qc_schema_input"
input_dev_schema["properties"]["schema_name"]["pattern"] = "\W*(qc_schema_input)\W*"

# Snapshot the input dev schema
output_dev_schema = copy.deepcopy(base_schema)
output_dev_schema["name"] = "qc_schema_output"
output_dev_schema["properties"].update(output_properties)
output_dev_schema["required"].extend(["provenance", "properties", "success", "return_result"])
output_dev_schema["properties"]["schema_name"]["pattern"] = "\W*(qc_schema_output)\W*"

# Build out the molecule schema
molecule_dev_schema = copy.deepcopy(molecule.molecule)

#import json
#print(json.dumps(input_dev_schema, indent=2))
#print(json.dumps(output_dev_schema, indent=2))
