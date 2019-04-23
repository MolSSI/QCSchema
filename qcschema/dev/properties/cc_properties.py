"""
The complete list of Coupled-Cluster properties.
"""

cc_properties = {}

cc_properties["ccsd_same_spin_correlation_energy"] = {
    "type":
    "number",
    "description":
    "The portion of CCSD doubles correlation energy from same-spin (i.e. triplet) correlations, without any user scaling."
}

cc_properties["ccsd_opposite_spin_correlation_energy"] = {
    "type":
    "number",
    "description":
    "The portion of CCSD doubles correlation energy from opposite-spin (i.e. singlet) correlations, without any user scaling."
}

cc_properties["ccsd_singles_energy"] = {
    "type": "number",
    "description": "The singles portion of the CCSD correlation energy. Zero except in ROHF."
}

cc_properties["ccsd_doubles_energy"] = {
    "type":
    "number",
    "description":
    "The doubles portion of the CCSD correlation energy including same-spin and opposite-spin correlations."
}

cc_properties['ccsd_correlation_energy'] = {
    "type":
    "number",
    "description":
    "The CCSD correlation energy."
}

cc_properties['ccsd_total_energy'] = {
    "type":
    "number",
    "description":
    "The total CCSD energy (CCSD correlation energy + HF energy)."
}

cc_properties['ccsd_prt_pr_correlation_energy'] = {
    "type":
    "number",
    "description":
    "The CCSD(T) correlation energy."
}

cc_properties['ccsd_prt_pr_total_energy'] = {
    "type":
    "number",
    "description":
    "The total CCSD(T) energy (CCSD(T) correlation energy + HF energy)."
}

cc_properties['ccsdt_correlation_energy'] = {
    "type":
    "number",
    "description":
    "The CCSDT correlation energy."
}

cc_properties['ccsdt_total_energy'] = {
    "type":
    "number",
    "description":
    "The total CCSDT energy (CCSDT correlation energy + HF energy)."
}

cc_properties['ccsdtq_correlation_energy'] = {
    "type":
    "number",
    "description":
    "The CCSDTQ correlation energy."
}

cc_properties['ccsdtq_total_energy'] = {
    "type":
    "number",
    "description":
    "The total CCSDTQ energy (CCSDTQ correlation energy + HF energy)."
}

cc_properties["ccsd_dipole_moment"] = {
    "type": "array",
    "description": "The CCSD X, Y, and Z dipole components.",
    "items": {
        "type": "number"
    }
}

cc_properties["ccsd_prt_pr_dipole_moment"] = {
    "type": "array",
    "description": "The CCSD(T) X, Y, and Z dipole components.",
    "items": {
        "type": "number"
    }
}

cc_properties["ccsdt_dipole_moment"] = {
    "type": "array",
    "description": "The CCSDT X, Y, and Z dipole components.",
    "items": {
        "type": "number"
    }
}

cc_properties["ccsdtq_dipole_moment"] = {
    "type": "array",
    "description": "The CCSDTQ X, Y, and Z dipole components.",
    "items": {
        "type": "number"
    }
}

cc_properties["ccsd_iterations"] = {
    "type": "number",
    "multipleOf": 1.0,
    "description": "The number of CCSD iterations taken before convergence."
}

cc_properties["ccsdt_iterations"] = {
    "type": "number",
    "multipleOf": 1.0,
    "description": "The number of CCSDT iterations taken before convergence."
}

cc_properties["ccsdtq_iterations"] = {
    "type": "number",
    "multipleOf": 1.0,
    "description": "The number of CCSDTQ iterations taken before convergence."
}