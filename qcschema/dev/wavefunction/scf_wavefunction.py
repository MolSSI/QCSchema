"""
The complete list of SCF level wavefunction quantities.
"""

scf_wavefunction = {}

# Orbitals
scf_wavefunction["scf_orbitals_a"] = {
    "type": "array",
    "description": "SCF alpha-spin orbitals in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nmo"]
}


scf_wavefunction["scf_orbitals_b"] = {
    "type": "array",
    "description": "SCF beta-spin orbitals in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nmo"]
}

# Density
scf_wavefunction["scf_density_a"] = {
    "type": "array",
    "description": "SCF alpha-spin density in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao"]
}


scf_wavefunction["scf_density_b"] = {
    "type": "array",
    "description": "SCF beta-spin density in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao"]
}


# Fock matrix
scf_wavefunction["scf_fock_a"] = {
    "type": "array",
    "description": "SCF alpha-spin Fock matrix in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao"]
}


scf_wavefunction["scf_fock_b"] = {
    "type": "array",
    "description": "SCF beta-spin Fock matrix in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao"]
}


scf_wavefunction["scf_coulomb_a"] = {
    "type": "array",
    "description": "SCF alpha-spin Coulomb matrix in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao"]
}


scf_wavefunction["scf_coulomb_b"] = {
    "type": "array",
    "description": "SCF beta-spin Coulomb matrix in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao"]
}


scf_wavefunction["scf_exchange_a"] = {
    "type": "array",
    "description": "SCF alpha-spin exchange matrix in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao"]
}


scf_wavefunction["scf_exchange_b"] = {
    "type": "array",
    "description": "SCF beta-spin exchange matrix in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao"]
}


# Eigenvalues
scf_wavefunction["scf_eigenvalues_a"] = {
    "type": "array",
    "description": "SCF alpha-spin orbital eigenvalues.",
    "items": {"type": "number"},
    "shape": ["nmo"]
}


scf_wavefunction["scf_eigenvalues_b"] = {
    "type": "array",
    "description": "SCF beta-spin orbital eigenvalues.",
    "items": {"type": "number"},
    "shape": ["nmo"]
}


# Occupations
scf_wavefunction["scf_occupations_a"] = {
    "type": "array",
    "description": "SCF alpha-spin orbital occupations.",
    "items": {"type": "number"},
    "shape": ["nmo"]
}


scf_wavefunction["scf_occupations_b"] = {
    "type": "array",
    "description": "SCF beta-spin orbital occupations.",
    "items": {"type": "number"},
    "shape": ["nmo"]
}


# Electron-Repulsion Integrals
scf_wavefunction["scf_eri_aa"] = {
    "type": "array",
    "description": "SCF alpha-alpha-spin electron-repulsion integrals in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao", "nao", "nao"],
}


scf_wavefunction["scf_eri_ab"] = {
    "type": "array",
    "description": "SCF alpha-beta-spin electron-repulsion integrals in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao", "nao", "nao"],
}


scf_wavefunction["scf_eri_ba"] = {
    "type": "array",
    "description": "SCF beta-alpha-spin electron-repulsion integrals in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao", "nao", "nao"],
}


scf_wavefunction["scf_eri_bb"] = {
    "type": "array",
    "description": "SCF beta-beta-spin electron-repulsion integrals in the AO basis.",
    "items": {"type": "number"},
    "shape": ["nao", "nao", "nao", "nao"],
}
