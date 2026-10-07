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


result_wavefunction["density_mo_a"] = {
    "type": "string",
    "description": "Alpha-spin density in the MO basis of the primary return."
}


result_wavefunction["density_mo_b"] = {
    "type": "string",
    "description": "Beta-spin density in the MO basis of the primary return."
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


result_wavefunction["fock_mo_a"] = {
    "type": "string",
    "description": "Alpha-spin Fock matrix in the MO basis of the primary return."
}


result_wavefunction["fock_mo_b"] = {
    "type": "string",
    "description": "Beta-spin Fock matrix in the MO basis of the primary return."
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


# Electron-Repulsion Integrals
result_wavefunction["eri"] = {
    "type": "string",
    "description": "Electron-repulsion integrals in the AO basis of the primary return."
}


result_wavefunction["eri_mo_aa"] = {
    "type": "string",
    "description": "Alpha-alpha-spin electron-repulsion integrals in the MO basis of the primary return."
}


result_wavefunction["eri_mo_ab"] = {
    "type": "string",
    "description": "Alpha-beta-spin electron-repulsion integrals in the MO basis of the primary return."
}


result_wavefunction["eri_mo_ba"] = {
    "type": "string",
    "description": "Beta-alpha-spin electron-repulsion integrals in the MO basis of the primary return."
}


result_wavefunction["eri_mo_bb"] = {
    "type": "string",
    "description": "Beta-beta-spin electron-repulsion integrals in the MO basis of the primary return."
}
