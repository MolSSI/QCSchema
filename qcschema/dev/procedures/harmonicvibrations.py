"""
The json-schema for the harmonic vibrational analysis definition
"""
harmvib = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "name": "qc_schema_harmvib",
    "version": "dev",
    "description": "The MolSSI Quantum Chemistry Harmonic Vibrational Analysis Schema",
    "type": "object",
    "properties": {
        "omega": {
            "description": "(nvib, ) for each vibration, frequency of vibration [cm^-1]; +/- for real/imaginary modes.",
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "q": {
            "description":
            "(nvib, 3 * nat) for each vibration, vector of XYZ displacements [a0 u^1/2] for normal mode, normalized mass-weighted.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "number",
                }
            }
        },
        "w": {
            "description":
            "(nvib, 3 * nat) for each vibration, vector of XYZ displacements [a0] for normal mode, un-mass-weighted.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "number",
                }
            }
        },
        "x": {
            "description":
            "(nvib, 3 * nat) for each vibration, vector of XYZ displacements [a0] for normal mode, normalized un-mass-weighted.",
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "number",
                }
            }
        },
        "degeneracy": {
            "description": "(nvib, ) for each vibration, degree of degeneracy.",
            "type": "array",
            "items": {
                "type": "number"
                "multipleOf": 1.0,
            }
        },
        "TRV": {
            "description": "(nvib, ) for each vibration, translation/rotation/vibration classification: 'TR' or 'V' or '-' for partial.",
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "gamma": {
            "description": "(nvib, ) for each vibration, irreducible representation or None if unclassifiable.",
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "mu": {
            "description": "(nvib, ) for each vibration, reduced mass [u]; +/+ for real/imaginary modes.",
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "k": {
            "description": "(nvib, ) for each vibration, force constant [mDyne/A]; +/- for real/imaginary modes.",
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "DQ0": {
            "description": "(nvib, ) for each vibration, RMS deviation v=0 [a0 u^1/2]; +/0 for real/imaginary modes.",
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "Qtp0": {
            "description": "(nvib, ) for each vibration, turning point v=0 [a0 u^1/2]; +/0 for real/imaginary modes.",
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "Xtp0": {
            "description": "(nvib, ) for each vibration, turnin point v=0 [a0]; +/0 for real/imaginary modes.",
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "theta_vib": {
            "description": "(nvib, ) for each vibration, characteristic temperature [K]; +/0 for real/imaginary modes.",
            "type": "array",
            "items": {
                "type": "number"
                "multipleOf": 1.0,
            }
        },
        "provenance": {
            "type": "object",
            "$ref": "#/definitions/provenance"
        }
    },
    "required": ["omega", "q"],
    "description": "The solved results of a Hessian calculation"
}
