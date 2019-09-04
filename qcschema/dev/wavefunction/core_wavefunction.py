"""
(Effective) core (aka one-electron) Hamiltonian
"""

core_wavefunction = {}

# core hamiltonian
core_wavefunction["h_core_a"] = {
    "type": "array",
    "description": "Alpha-spin core (one-electron) Hamiltonian in the AO basis",
    "items": {"type": "number"}
}


core_wavefunction["h_core_b"] = {
    "type": "array",
    "description": "Beta-spin core (one-electron) Hamiltonian in the AO basis",
    "items": {"type": "number"}
}


# effective core hamiltonian
core_wavefunction["h_eff_a"] = {
    "type": "array",
    "description": "Alpha-spin effective core (one-electron) Hamiltonian in the AO basis",
    "items": {"type": "number"}
}


core_wavefunction["h_eff_b"] = {
    "type": "array",
    "description": "Beta-spin effective core (one-electron) Hamiltonian in the AO basis",
    "items": {"type": "number"}
}
