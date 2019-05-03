"""
The json-schema for the Basis Set definition
"""

basis = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "name": "qcschema_basis",
    "version": "1.dev",
    "description": "The MolSSI Quantum Chemistry Basis Set Schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "schema_name": {
            "type": "string",
            "pattern": "^(qcschema_basis)$"
        },
        "schema_version": {
            "type": "integer"
        },
        "description": {
            "description": "Brief description of the basis set",
            "type": "string"
        },
        "element_basis": {
            "description": "Per-element basis data",
            "type": "object",
            "additionalProperties": False,
            "patternProperties": {
                "^\\d+$": {
                    "$ref": "#/definitions/center_basis"
                }
            }
        },
        "atom_basis": {
            "description":
            "Basis set overrides for particular atoms or centers",
            "type": "object",
            "additionalProperties": False,
            "patternProperties": {
                "^\\d+$": {
                    "$ref": "#/definitions/center_basis"
                }
            }
        }
    }
}
