"""
The complete list of localized-orbital SCF wavefunction quantities.
"""

localized_wavefunction = {}

# Orbitals
localized_wavefunction["localized_orbitals_a"] = {
    "type": "array",
    "description": "Localized alpha-spin orbitals in the AO basis. "
                   "All nmo orbitals are included, even if only a subset were localized.",
    "items": {"type": "number"},
    "shape": {"nao", "nmo"}
}


localized_wavefunction["localized_orbitals_b"] = {
    "type": "array",
    "description": "Localized beta-spin orbitals in the AO basis. "
                   "All nmo orbitals are included, even if only a subset were localized.",
    "items": {"type": "number"},
    "shape": {"nao", "nmo"}
}


# Fock matrix
localized_wavefunction["localized_fock_a"] = {
    "type": "array",
    "description": "Alpha-spin Fock matrix in the localized molecular orbital basis. "
                   "All nmo orbitals are included, even if only a subset were localized.",
    "items": {"type": "number"},
    "shape": {"nmo", "nmo"}
}


localized_wavefunction["localized_fock_b"] = {
    "type": "array",
    "description": "Beta-spin Fock matrix in the localized molecular orbital basis. "
                   "All nmo orbitals are included, even if only a subset were localized.",
    "items": {"type": "number"},
    "shape": {"nmo", "nmo"}
}

# Note that localized density, eigenvalues, and occupations are not included since they are the same as the SCF density
