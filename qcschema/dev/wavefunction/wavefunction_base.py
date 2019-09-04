"""
The base file for QC Schema properties.
"""

from .result_wavefunction import result_wavefunction
from .scf_wavefunction import scf_wavefunction
from .localized_wavefunction import localized_wavefunction
from ..basis import basis

output_wavefunction = {
    "type": "object",
    "properties": {
        "basis": basis
    },
    "description": "Wavefunction properties resulting from a computation",
    "additionalProperties": False,
    "required": ["basis"]
}

# Update new keys
output_wavefunction["properties"].update(result_wavefunction)
output_wavefunction["properties"].update(scf_wavefunction)
output_wavefunction["properties"].update(localized_wavefunction)


