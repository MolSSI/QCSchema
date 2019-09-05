"""
The complete list of localized-orbital SCF wavefunction quantities.
"""

localized_wavefunction = {}

# Orbitals
localized_wavefunction["localized_orbitals_a"] = {
    "type": "array",
    "description": "Localized alpha-spin orbitals in the AO basis. "
                   "All N_AO orbitals are included, even only a subset were localized.",
    "items": {"type": "number"}
}


localized_wavefunction["localized_orbitals_b"] = {
    "type": "array",
    "description": "Localized beta-spin orbitals in the AO basis."
                   "All N_AO orbitals are included, even only a subset were localized.",
    "items": {"type": "number"}
}


# Fock matrix
localized_wavefunction["localized_fock_a"] = {
    "type": "array",
    "description": "Alpha-spin Fock matrix in the localized molecular orbital basis."
                   "All N_AO orbitals are included, even only a subset were localized.",
    "items": {"type": "number"}
}


localized_wavefunction["localized_fock_b"] = {
    "type": "array",
    "description": "Beta-spin Fock matrix in the localized molecular orbital basis."
                   "All N_AO orbitals are included, even only a subset were localized.",
    "items": {"type": "number"}
}

# Note that localized density, eigenvalues, and occupations are not included since they are the same as the SCF density
