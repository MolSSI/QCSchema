"""
The complete list of Coupled-Cluster properties.
"""

cc_properties = {}

cc_properties["ccsd_same_spin_correlation_energy"] = {
    "type":
    "number",
    "description":
    "The unscaled portion of the CCSD correlation energy from same-spin or triplet doubles correlations."
}

cc_properties["ccsd_opposite_spin_correlation_energy"] = {
    "type":
    "number",
    "description":
    "The unscaled portion of the CCSD correlation energy from opposite-spin or singlet doubles correlations."
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

cc_properties['ccsd_total_correlation_energy'] = {
    "type":
    "number",
    "description":
    "The total CCSD correlation energy. "
}

cc_properties['ccsd_total_energy'] = {
    "type":
    "number",
    "description":
    "The total CCSD energy (CCSD correlation energy + HF energy)."
}