"""
The primary specified return  wavefunction quantities.
"""

result_wavefunction = {}

# Orbitals
result_wavefunction["orbitals_a"] = {
    "type": "array",
    "description": "Alpha-spin orbitals in the AO basis of the primary return.",
    "items": {"type": "number"},
    "shape": {"nao", "nmo"}
}


result_wavefunction["orbitals_b"] = {
    "type": "array",
    "description": "Beta-spin orbitals in the AO basis of the primary return.",
    "items": {"type": "number"},
    "shape": {"nao", "nmo"}
}

# Density
result_wavefunction["density_a"] = {
    "type": "array",
    "description": "Alpha-spin density in the AO basis of the primary return.",
    "items": {"type": "number"},
    "shape": {"nao", "nao"}
}


result_wavefunction["density_b"] = {
    "type": "array",
    "description": "Beta-spin density in the AO basis of the primary return.",
    "items": {"type": "number"},
    "shape": {"nao", "nao"}
}


# Fock matrix
result_wavefunction["fock_a"] = {
    "type": "array",
    "description": "Alpha-spin Fock matrix in the AO basis of the primary return.",
    "items": {"type": "number"},
    "shape": {"nao", "nao"}
}


result_wavefunction["fock_b"] = {
    "type": "array",
    "description": "Beta-spin Fock matrix in the AO basis of the primary return.",
    "items": {"type": "number"},
    "shape": {"nao", "nao"}
}


# Eigenvalues
result_wavefunction["eigenvalues_a"] = {
    "type": "array",
    "description": "Alpha-spin orbital eigenvalues of the primary return.",
    "items": {"type": "number"},
    "shape": {"nmo"}
}


result_wavefunction["eigenvalues_b"] = {
    "type": "array",
    "description": "Beta-spin orbital eigenvalues of the primary return.",
    "items": {"type": "number"},
    "shape": {"nmo"}
}


# Occupations
result_wavefunction["occupations_a"] = {
    "type": "array",
    "description": "Alpha-spin orbital occupations of the primary return.",
    "items": {"type": "number"},
    "shape": {"nmo"}
}


result_wavefunction["occupations_b"] = {
    "type": "array",
    "description": "Beta-spin orbital occupations of the primary return.",
    "items": {"type": "number"},
    "shape": {"nmo"}
}
