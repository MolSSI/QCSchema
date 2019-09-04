"""
The complete list of SCF level wavefunction quantities.
"""

scf_wavefunction = {}

# Orbitals
scf_wavefunction["scf_orbitals_a"] = {
    "type": "array",
    "description": "SCF alpha-spin orbitals",
    "items": {"type": "number"}
}


scf_wavefunction["scf_orbitals_b"] = {
    "type": "array",
    "description": "SCF beta-spin orbitals",
    "items": {"type": "number"}
}

# Density
scf_wavefunction["scf_density_a"] = {
    "type": "array",
    "description": "SCF alpha-spin density",
    "items": {"type": "number"}
}


scf_wavefunction["scf_density_b"] = {
    "type": "array",
    "description": "SCF beta-spin density",
    "items": {"type": "number"}
}


# Fock matrix
scf_wavefunction["scf_fock_a"] = {
    "type": "array",
    "description": "SCF alpha-spin Fock matrix",
    "items": {"type": "number"}
}


scf_wavefunction["scf_fock_b"] = {
    "type": "array",
    "description": "SCF beta-spin Fock matrix",
    "items": {"type": "number"}
}


# Eigenvalues
scf_wavefunction["scf_eigenvalues_a"] = {
    "type": "array",
    "description": "SCF alpha-spin orbital eigenvalues",
    "items": {"type": "number"}
}


scf_wavefunction["scf_eigenvalues_b"] = {
    "type": "array",
    "description": "SCF beta-spin orbital eigenvalues",
    "items": {"type": "number"}
}


# Occupations
scf_wavefunction["scf_occupations_a"] = {
    "type": "array",
    "description": "SCF alpha-spin orbital occupations",
    "items": {"type": "number"}
}


scf_wavefunction["scf_occupations_b"] = {
    "type": "array",
    "description": "SCF beta-spin orbital occupations",
    "items": {"type": "number"}
}
