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
            "description": "The version of the program which created this object, blank otherwise. Suggest that versions be interpretable by PEP 440 (https://www.python.org/dev/peps/pep-0440/).",
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

definitions["electron_shell"] = {
    "description": "Information for a single electronic shell",
    "additionalProperties": False,
    "required": [
        "angular_momentum",
        "harmonic_type",
        "exponents",
        "coefficients"
    ],
    "properties": {
        "angular_momentum": {
            "description": "Angular momentum (as an array of integers)",
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "type": "integer",
                "minimum": 0
            }
        },
        "harmonic_type": {
            "description": "Whether this shell is spherical or cartesian",
            "type": "string",
            "enum": ["spherical", "cartesian"]
        },
        "exponents": {
            "description": "Exponents for this contracted shell",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string"
            }
        },
        "coefficients": {
            "description": "General contraction coefficients for this contracted shell",
            "type": "array",
            "minItems": 1,
            "items": {
                "description": "Segmented contraction coefficients",
                "type": "array",
                "minItems": 1,
                "items": {"type": "string"}
            }
        }
    }
}

definitions["ecp_potential"] = {
    "description": "ECP potential",
    "additionalProperties": False,
    "required": [
        "ecp_type",
        "angular_momentum",
        "r_exponents",
        "gaussian_exponents",
        "coefficients"
    ],
    "properties": {
        "ecp_type": {
            "description": "Type of the ECP Potential",
            "type": "string",
            "enum": [ "scalar", "spinorbit" ]
        },
        "angular_momentum": {
            "description": "Angular momentum (as an array of integers)",
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "type": "integer",
                "minimum": 0
            }
        },
        "r_exponents": {
            "description": "Exponents of the r term",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "integer"
            }
        },
        "gaussian_exponents": {
            "description": "Exponents of the gaussian term",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "string"
            }
        },
        "coefficients": {
            "description": "General contraction coefficients for this potential",
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

definitions["center_basis"] = {
    "description": "Data for a single atom/center in the basis set",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "electron_shells": {
            "description": "(Electronic) shells for this element",
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "$ref": "#/definitions/electron_shell"
            }
        },
        "ecp_electrons":
        {
            "description": "Number of electrons replaced by ECP",
            "type": "integer",
            "minimum": 1
        },
        "ecp_potentials": {
            "description": "Effective Core Potential for this element",
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {
                "$ref": "#/definitions/ecp_potential"
            }
        }
    }
}
