"""
The primary specified return  wavefunction quantities.
"""

result_wavefunction = {}

# Orbitals
result_wavefunction["orbitals_a"] = {
    "type": "string",
    "description": "Alpha-spin orbitals in the AO basis of the primary return. "
}


result_wavefunction["orbitals_b"] = {
    "type": "string",
    "description": "Beta-spin orbitals in the AO basis of the primary return."
}

# Density
result_wavefunction["density_a"] = {
    "type": "string",
    "description": "Alpha-spin density in the AO basis of the primary return."
}


result_wavefunction["density_b"] = {
    "type": "string",
    "description": "Beta-spin density in the AO basis of the primary return."
}


# Fock matrix
result_wavefunction["fock_a"] = {
    "type": "string",
    "description": "Alpha-spin Fock matrix in the AO basis of the primary return."
}


result_wavefunction["fock_b"] = {
    "type": "string",
    "description": "Beta-spin Fock matrix in the AO basis of the primary return."
}


# Eigenvalues
result_wavefunction["eigenvalues_a"] = {
    "type": "string",
    "description": "Alpha-spin orbital eigenvalues of the primary return."
}


result_wavefunction["eigenvalues_b"] = {
    "type": "string",
    "description": "Beta-spin orbital eigenvalues of the primary return."
}


# Occupations
result_wavefunction["occupations_a"] = {
    "type": "string",
    "description": "Alpha-spin orbital occupations of the primary return."
}


result_wavefunction["occupations_b"] = {
    "type": "string",
    "description": "Beta-spin orbital occupations of the primary return."
}
