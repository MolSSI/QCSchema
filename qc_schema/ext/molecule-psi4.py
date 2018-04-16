"""
The json-schema extension defining Psi4 Molecules

"""
molecule = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "properties": {
        "psi4:elez": {
            "description": "(nat, ) atomic numbers, nuclear charge for atoms.",
            "type": "array",
            "items": {
                "type": "number",
                "multipleOf": 1.0
            }
        },
        "psi4:elea": {
            "description": "(nat, ) mass numbers for atoms, if known isotope, else -1.",
            "type": "array",
            "items": {
                "type": "number",
                "multipleOf": 1.0
            }
        },
        "psi4:elbl": {
            "description": "(nat, ) atom labels with any tagging information from element spec.",
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "psi4:units": {
            "description": "Units for `geometry`.",
            "type": "string",
            "enum": ["Angstrom", "Bohr"]
        },
        "psi4:input_units_to_au": {
            "description": "If `units='Angstrom'`, overrides consumer's value for [A]-->[a0] conversion.",
            "type": "number"
        },
        "psi4:fragment_files": {
            "description": "(nfr, ) lowercased names of efp fragment files (no path info).",
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "psi4:hint_types": {
            "description": "(nfr, ) type of fragment orientation hint.",
            "type": "string",
            "enum": ["xyzabc", "points"]
        },
        "psi4:geom_hints": {
            "description": "(nfr, ) inner lists have length 6 (xyzabc; to orient the center) or
                            9 (points; to orient the first three atoms) of the EFP fragment.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            }
        },
        "psi4:geom_unsettled": {
            "description": "(nat, )  all-string Cartesian and/or zmat anchor and value contents.",
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "psi4:variables": {
            "description": "(nvar, 2) pairs of variables (str) and values (float). May be incomplete.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "string",
                }
            }
        }
    },
    "required": ["symbols", "geometry"],
    "description": "The physical cartesian representation of the molecular system"
}
