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
    "description": "The MolSSI Quantum Chemistry Schema",
    "type": "object",
    "version": "0.1.dev",
    "properties": {
        "molecule": molecule.molecule,
        "driver": {
            "definition": "The type of computation requested",
            "enum": ["energy", "gradient", "hessian", "property"]
        },
        "keywords": {
            "type": "object"
        },
        "provenance": {
            "type": "object",
            "$ref": "#/definitions/provenance"
        }
    },
    "required": ["molecule", "driver", "keywords"],
    "definitions": definitions.definitions
}

# Additional properties to contain in the output
output_properties = {
    "properties": properties.properties,
    "success": {
        "type": "boolean"
    },
    "error": {
        "type": "object",
        "$ref": "#/definitions/error"
    },
}

# Snapshot the input dev schema
input_dev_schema = copy.deepcopy(base_schema)

# Add additional output pieces
base_schema["properties"].update(output_properties)
base_schema["required"].extend(["provenance", "properties", "success"])

# Snapshot the input dev schema
output_dev_schema = copy.deepcopy(base_schema)

#import json
#print(json.dumps(input_dev_schema, indent=2))
#print(json.dumps(output_dev_schema, indent=2))
