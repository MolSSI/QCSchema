"""
Integrates all components of the QC Schema into a single one.
"""

import copy

from . import molecule
from . import definitions
from . import properties
from . import basis

# The base schema definition
base_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "name": "qcschema_input",
    "version": "1.dev",
    "description": "The MolSSI Quantum Chemistry Schema",
    "type": "object",
    "properties": {
        "molecule": molecule.molecule,
        "schema_name": {
            "type": "string",
            "pattern": "^(qc_?schema)$"
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
                  "anyOf": [
                    basis.basis,
                    {
                        "description": "Name of the basis set to apply to the whole molecule",
                        "type": "string"
                    },
                  ]
                }
            },
            "required": [ "method", "basis" ],
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
input_dev_schema["name"] = "qcschema_input"
input_dev_schema["properties"]["schema_name"]["pattern"] = "^(qc_?schema_input)$"

# Snapshot the input dev schema
output_dev_schema = copy.deepcopy(base_schema)
output_dev_schema["name"] = "qcschema_output"
output_dev_schema["properties"].update(output_properties)
output_dev_schema["required"].extend(["provenance", "properties", "success", "return_result"])
output_dev_schema["properties"]["schema_name"]["pattern"] = "^(qc_?schema_output)$"

# Build out the molecule schema
molecule_dev_schema = copy.deepcopy(molecule.molecule)

# Build out the basis schema
basis_dev_schema = copy.deepcopy(basis.basis)

#import json
#print(json.dumps(input_dev_schema, indent=2))
#print(json.dumps(output_dev_schema, indent=2))
