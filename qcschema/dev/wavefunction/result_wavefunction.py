"""
The primary specified return  wavefunction quantities.
"""

result_wavefunction = {}

# Orbitals
result_wavefunction["return_result_orbitals_a"] = {
    "type": "array",
    "description": "The primary specified return alpha-spin orbitals in the AO basis",
    "items": {"type": "number"},
    "shape": {"nao", "nmo"}
}


result_wavefunction["return_result_orbitals_b"] = {
    "type": "array",
    "description": "The primary specified return beta-spin orbitals in the AO basis",
    "items": {"type": "number"},
    "shape": {"nao", "nmo"}
}

# Density
result_wavefunction["return_result_density_a"] = {
    "type": "array",
    "description": "The primary specified return alpha-spin density in the AO basis",
    "items": {"type": "number"},
    "shape": {"nao", "nao"}
}


result_wavefunction["return_result_density_b"] = {
    "type": "array",
    "description": "The primary specified return beta-spin density in the AO basis",
    "items": {"type": "number"},
    "shape": {"nao", "nao"}
}


# Fock matrix
result_wavefunction["return_result_fock_a"] = {
    "type": "array",
    "description": "The primary specified return alpha-spin Fock matrix in the AO basis",
    "items": {"type": "number"},
    "shape": {"nao", "nao"}
}


result_wavefunction["return_result_fock_b"] = {
    "type": "array",
    "description": "The primary specified return beta-spin Fock matrix in the AO basis",
    "items": {"type": "number"},
    "shape": {"nao", "nao"}
}


# Eigenvalues
result_wavefunction["return_result_eigenvalues_a"] = {
    "type": "array",
    "description": "The primary specified return alpha-spin orbital eigenvalues",
    "items": {"type": "number"},
    "shape": {"nmo"}
}


result_wavefunction["return_result_eigenvalues_b"] = {
    "type": "array",
    "description": "SCF beta-spin orbital eigenvalues",
    "items": {"type": "number"},
    "shape": {"nmo"}
}


# Occupations
result_wavefunction["return_result_occupations_a"] = {
    "type": "array",
    "description": "SCF alpha-spin orbital occupations",
    "items": {"type": "number"},
    "shape": {"nmo"}
}


result_wavefunction["return_result_occupations_b"] = {
    "type": "array",
    "description": "SCF beta-spin orbital occupations",
    "items": {"type": "number"},
    "shape": {"nmo"}
}
