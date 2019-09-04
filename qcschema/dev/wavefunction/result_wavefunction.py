"""
The primary specified return  wavefunction quantities.
"""

result_wavefunction = {}

# Orbitals
result_wavefunction["return_result_orbitals_a"] = {
    "type": "array",
    "description": "The primary specified return alpha-spin orbitals",
    "items": {"type": "number"}
}


result_wavefunction["return_result_orbitals_b"] = {
    "type": "array",
    "description": "The primary specified return beta-spin orbitals",
    "items": {"type": "number"}
}

# Density
result_wavefunction["return_result_density_a"] = {
    "type": "array",
    "description": "The primary specified return alpha-spin density",
    "items": {"type": "number"}
}


result_wavefunction["return_result_density_b"] = {
    "type": "array",
    "description": "The primary specified return beta-spin density",
    "items": {"type": "number"}
}


# Fock matrix
result_wavefunction["return_result_fock_a"] = {
    "type": "array",
    "description": "The primary specified return alpha-spin Fock matrix",
    "items": {"type": "number"}
}


result_wavefunction["return_result_fock_b"] = {
    "type": "array",
    "description": "The primary specified return beta-spin Fock matrix",
    "items": {"type": "number"}
}


# Eigenvalues
result_wavefunction["return_result_eigenvalues_a"] = {
    "type": "array",
    "description": "The primary specified return alpha-spin orbital eigenvalues",
    "items": {"type": "number"}
}


result_wavefunction["return_result_eigenvalues_b"] = {
    "type": "array",
    "description": "SCF beta-spin orbital eigenvalues",
    "items": {"type": "number"}
}


# Occupations
result_wavefunction["return_result_occupations_a"] = {
    "type": "array",
    "description": "SCF alpha-spin orbital occupations",
    "items": {"type": "number"}
}


result_wavefunction["return_result_occupations_b"] = {
    "type": "array",
    "description": "SCF beta-spin orbital occupations",
    "items": {"type": "number"}
}
