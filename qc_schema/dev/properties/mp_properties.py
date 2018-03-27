"""
The complete list of Moller-Plesset properties.
"""

mp_properties = {}

mp_properties["mp2_same_spin_correlation_energy"] = {
    "type":
    "number",
    "description":
    "The unscaled portion of the MP2 correlation energy from same-spin or triplet doubles correlations."
}

mp_properties["mp2_opposite_spin_correlation_energy"] = {
    "type":
    "number",
    "description":
    "The unscaled portion of the MP2 correlation energy from opposite-spin or singlet doubles correlations."
}

mp_properties["mp2_single_energy"] = {
    "type": "number",
    "description": "The singles portion of the MP2 correlation energy. Zero except in ROHF."
}

mp_properties["mp2_double_energy"] = {
    "type":
    "number",
    "description":
    "The doubles portion of the MP2 correlation energy including same-spin and opposite-spin correlations."
}

mp_properties['mp2_total_correlation_energy'] = {
    "type":
    "number",
    "description":
    "The doubles portion of the MP2 correlation energy including same-spin and opposite-spin correlations."
}
