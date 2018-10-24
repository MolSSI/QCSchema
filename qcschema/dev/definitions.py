"""
A list of definitions involved in the JSON schema.
"""

definitions = {}

definitions["error"] = {
    "properties": {
        "error_type": {
            "description": "The type of error raised.",
            "enum": ["convergence_error", "file_error", "memory_error"]
        },
        "error_message": {
            "description": "A description of the raised error.",
            "type": "string"
        }
    },
    "required": ["error_type", "error_message"],
    "description": "The type of error message raised.",
    "additionalProperties": False
}

definitions["provenance"] = {
    "properties": {
        "creator": {
            "description": "The name of the person or program who created this object.",
            "type": "string"
        },
        "version": {
            "description": "The version of the program which created this object, blank otherwise.",
            "type": "string"
        },
        "routine": {
            "description": "The routine of the program which created this object, blank otherwise.",
            "type": "string"
        }
    },
    "required": ["creator", "version", "routine"],
    "description": "A short provenance of the object.",
    "additionalProperties": True
}

definitions["basis_electron_shell"] = {
    "description": "Information for a single electronic shell",
    "additionalProperties": False,
    "required": [
        "shell_angular_momentum",
        "shell_exponents",
        "shell_coefficients"
    ],
    "properties": {
        "shell_region": {
            "description": "The region this shell describes",
            "type": "string",
            "enum": [ "valence", "polarization", "core", "tight", "diffuse" ]
        },
        "shell_angular_momentum": {
            "description": "Angular momentum (as an array of integers)",
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "type": "integer",
                "minimum": 0
            }
        },
        "shell_exponents": {
            "description": "Exponents for this contracted shell",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string"
            }
        },
        "shell_coefficients": {
            "description": "General contraction coefficients for this contracted shell",
            "type": "array",
            "minItems": 1,
            "items": {
                "description": "Segmented contraction coefficients",
                "type": "array",
                "minItems": 1,
                "items": { "type": "string" }
            }
        }
    }
}

definitions["basis_ecp_potential"] = {
    "description": "ECP potential",
    "additionalProperties": False,
    "required": [
        "potential_ecp_type",
        "potential_angular_momentum",
        "potential_r_exponents",
        "potential_gaussian_exponents",
        "potential_coefficients"
    ],
    "properties": {
        "potential_ecp_type": {
            "description": "Type of the ECP Potential",
            "type": "string",
            "enum": [ "scalar", "spinorbit" ]
        },
        "potential_angular_momentum": {
            "description": "Angular momentum (as an array of integers)",
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "type": "integer",
                "minimum": 0
            }
        },
        "potential_r_exponents": {
            "description": "Exponents of the r term",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "integer"
            }
        },
        "potential_gaussian_exponents": {
            "description": "Exponents of the gaussian term",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string"
            }
        },
        "potential_coefficients": {
            "description": "General contraction coefficients for this contracted shell",
            "type": "array",
            "minItems": 1,
            "items": {
                "description": "Segmented contraction coefficients",
                "type": "array",
                "minItems": 1,
                "items": { "type": "string" }
            }
        }
    }
}

definitions["basis_single_data"] = {
    "description": "Data for a single atom/center in the basis set",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "element_electron_shells": {
            "description": "(Electronic) shells for this element",
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "$ref": "#/definitions/basis_electron_shell"
            }
        },
        "element_ecp_electrons":
        {
            "description": "Number of electrons replaced by ECP",
            "type": "integer",
            "minimum": 1
        },
        "element_ecp": {
            "description": "Effective Core Potential for this element",
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "$ref": "#/definitions/basis_ecp_potential"
            }
        }
    }
}

definitions["basis_spec"] = {
    "description": "Specification for a basis applied to a molecule",
    "type": "object",
    "additionalProperties": False,
    "properties":
    {
        "basis_set_description": {
            "description": "Brief description of the basis set",
            "type": "string"
        },  
        "basis_function_type": {
            "description": "Type of function for this basis",
            "type": "string",
            "enum": [ "gto", "sto" ]
        },
        "basis_harmonic_type": {
            "description": "Harmonic type (spherical, cartesian)",
            "type": "string",
            "enum": [ "spherical", "cartesian" ]
        },
        "basis_set_elements": {
            "description": "Per-element basis data",
            "type": "object",
            "additionalProperties": False,
            "patternProperties":   {   
                "^\\d+$" : { 
                    "$ref" : "#/definitions/basis_single_data"
                }   
            }   
        },  
        "basis_set_atoms": {
            "description": "Basis set overrides for particular atoms or centers",
            "type": "object",
            "additionalProperties": False,
            "patternProperties":   {   
                "^\\d+$" : { 
                    "$ref" : "#/definitions/basis_single_data"
                }   
            }   
        }   
    }
}
