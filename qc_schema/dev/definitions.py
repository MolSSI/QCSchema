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
    "required": ["creator"],
    "description": "A short provenance of the object.",
    "additionalProperties": True
}
