"""
The base file for QC Schema properties.
"""

from .scf_properties import scf_properties
from .mp_properties import mp_properties
from .cc_properties import cc_properties
from .calcinfo_properties import calcinfo_properties

properties = {
    "type": "object",
    "properties": {},
    "description": "The resulting properties of a computation",
    "additionalProperties": False
}

# Update new keys
properties["properties"].update(scf_properties)
properties["properties"].update(mp_properties)
properties["properties"].update(cc_properties)
properties["properties"].update(calcinfo_properties)
