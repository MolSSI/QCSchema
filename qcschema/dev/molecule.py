"""
The json-schema for the Molecule definition
"""
molecule = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "name": "qc_schema_molecule",
    "version": "dev",
    "url": "http://schema_host.org/schemas/0/something.schema",
    "description": "The MolSSI Quantum Chemistry Molecular Schema",
    "type": "object",
    "properties": {
        "symbols": {
            "description": "(nat, ) atom symbols in title case.",
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "geometry": {
            "description": "(3 * nat, ) vector of XYZ coordinates of the atoms.",
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "masses": {
            "description": "(nat, ) atom masses [u]; canonical weights assumed if not given.",
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "name": {
            "description": "The name of the molecule.",
            "type": "string"
        },
        "comment": {
            "description": "Any additional comment one would attach to the molecule.",
            "type": "string"
        },
        "molecular_charge": {
            "description": "The overall charge of the molecule.",
            "type": "number",
            "default": 0.0
        },
        "molecular_multiplicity": {
            "description": "The overall multiplicity of the molecule.",
            "type": "number",
            "multipleOf": 1.0,
            "default": 1
        },
        "real": {
            "description": "(nat, ) list describing if atoms are real (T) or ghost (F).",
            "type": "array",
            "items": {
                "type": "boolean"
            }
        },
        "connectivity": {
            "description": "(nat, ) list describing bonds within a molecule. Each element is a (atom1, atom2, order) tuple.",
            "type": "array",
            "items": {
                "type": "array",
                "minItems": 3,
                "maxItems": 3,
                "items": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 5,
                }
            }
        },
        "fragments": {
            "description":
            "(nfr, -1) list of indices (0-indexed) grouping atoms into molecular fragments within the topology.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "number",
                    "multipleOf": 1.0
                }
            }
        },
        "fragment_charges": {
            "description": "(nfr, ) list of charges associated with each fragment tuple.",
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "fragment_multiplicities": {
            "description": "(nfr, ) list of multiplicities associated with each fragment tuple.",
            "type": "array",
            "items": {
                "type": "number",
                "multipleOf": 1.0
            }
        },
        "fix_com": {
            "description": "Whether translation of geometry is allowed (fix F) or disallowed (fix T).",
            "type": "boolean",
            "default": False
        },
        "fix_orientation": {
            "description": "Whether rotation of geometry is allowed (fix F) or disallowed (fix T).",
            "type": "boolean",
            "default": False
        },
        "provenance": {
            "type": "object",
            "$ref": "#/definitions/provenance"
        }
    },
    "required": ["symbols", "geometry"],
    "description": "The physical cartesian representation of the molecular system"
}
