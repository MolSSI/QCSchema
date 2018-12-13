"""
The json-schema for the Molecule definition
"""
molecule = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "name": "qc_schema_molecule",
    "version": "dev",
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
            "description": "(3 * nat, ) vector of XYZ coordinates [a0] of the atoms.",
            "guidance": "Atom ordering is fixed; that is, a consumer who shuffles atoms must not reattach the input (pre-shuffling) molecule schema instance to any output (post-shuffling) per-atom results (e.g., gradient).",
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
        "atomic_numbers": {
            "description": "(nat, ) atomic numbers, nuclear charge for atoms. Ghostedness should be indicated through 'real' field, not zeros here.",
            "type": "array",
            "items": {
                "type": "number",
                "multipleOf": 1.0
            }
        },
        "mass_numbers": {
            "description": "(nat, ) mass numbers for atoms, if known isotope, else -1.",
            "type": "array",
            "items": {
                "type": "number",
                "multipleOf": 1.0
            }
        },
        "atom_labels": {
            "description": "(nat, ) atom labels with any user tagging information.",
            "type": "array",
            "items": {
                "type": "string"
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
            "description": "A list describing bonds within a molecule. Each element is a (atom1, atom2, order) tuple.",
            "guidance": "Bonds may be freely reordered and inverted.",
            "type": "array",
            "items": {
                "type": "array",
                "minItems": 3,
                "maxItems": 3,
                "items": [
                    {
                        "description": "Atom number (0-indexed) at one end of bond.",
                        "type": "number",
                        "multipleOf": 1.0
                    },
                    {
                        "description": "Atom number (0-indexed) at other end of bond.",
                        "type": "number",
                        "multipleOf": 1.0
                    },
                    {
                        "description": "Bond order.",
                        "type": "number",
                        "minimum": 0,
                        "maximum": 5,
                    }
                ]
            }
        },
        "fragments": {
            "description":
            "(nfr, <varies>) list of indices (0-indexed) grouping atoms into molecular fragments within the topology.",
            "guidance": "Fragment ordering is fixed; that is, a consumer who shuffles fragments must not reattach the input (pre-shuffling) molecule schema instance to any output (post-shuffling) per-fragment results (e.g., n-body energy arrays).",
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
            "guidance": "A consumer who translates the geometry must not reattach the input (pre-translation) molecule schema instance to any output (post-translation) origin-sensitive results (e.g., an ordinary energy when EFP present).",
            "type": "boolean",
            "default": False
        },
        "fix_orientation": {
            "description": "Whether rotation of geometry is allowed (fix F) or disallowed (fix T).",
            "guidance": "A consumer who rotates the geometry must not reattach the input (pre-rotation) molecule schema instance to any output (post-rotation) frame-sensitive results (e.g., molecular vibrations).",
            "type": "boolean",
            "default": False
        },
        "fix_symmetry":{
            "description": "Maximal point group symmetry at which `geometry` should be treated. Lowercase.",
            "type": "string"
        },
        "provenance": {
            "type": "object",
            "$ref": "#/definitions/provenance"
        }
    },
    "required": ["symbols", "geometry"],
    "description": "The physical cartesian representation of the molecular system"
}
