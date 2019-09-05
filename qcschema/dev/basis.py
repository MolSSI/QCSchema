"""
The json-schema for the Basis Set definition
"""

basis = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "name": "qcschema_basis",
    "version": "1.dev",
    "description": "The MolSSI Quantum Chemistry Basis Set Schema",
    "type": "object",
    "required": [
        "basis_data",
        "basis_atom_map",
        "name"
    ],
    "additionalProperties": False,
    "properties": {
        "schema_name": {
            "type": "string",
            "pattern": "^(qcschema_basis)$"
        },
        "schema_version": {
            "type": "integer"
        },
        "name": {
            "description": "Name of the basis set",
            "type": "string"
        },
        "description": {
            "description": "Brief description of the basis set",
            "type": "string"
        },
        "basis_data": {
            "description": "Shared basis data for all atoms/centers in the molecule",
            "type": "object",
            "additionalProperties": {
                "$ref": "#/definitions/center_basis"
            }
        },
        "basis_atom_map": {
            "description": "Mapping of all atoms/centers in the molecule to data in basis_data",
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    }
}
