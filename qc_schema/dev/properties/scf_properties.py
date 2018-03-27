"""
The complete list of SCF level properties.
"""

scf_properties = {}

scf_properties["scf_one_electron_energy"] = {
    "description": "The one-electron energy contribution [H] to the total SCF energy.",
    "type": "number"
}

scf_properties["scf_two_electron_energy"] = {
    "type": "number",
    "description": "The two-electron energy contribution [H] to the total SCF energy."
}

scf_properties["nuclear_repulsion_energy"] = {
    "type":
    "number",
    "description":
    """
The nuclear repulsion energy contribution [H] to the total SCF energy.
.. math:: E_{NN} = \sum_{i, j<i}^{N_{atom}}\frac{Z_i Z_j}{|\mathbf{R}_i - \mathbf{R}_j|}
"""
}

scf_properties["scf_vv10_energy"] = {
    "type": "number",
    "description": "The VV10 functional energy contribution to the total SCF energy."
}

scf_properties["scf_xc_energy"] = {
    "type": "number",
    "description": "The functional energy contribution [H] to the total SCF energy."
}

scf_properties["scf_dispersion_correction_energy"] = {
    "type":
    "number",
    "description":
    """
The dispersion correction appended to an underlying functional
when a DFT-D method is requested.`
"""
}

scf_properties["scf_dipole"] = {
    "type": "array",
    "description": "The X, Y, and Z dipole components.",
    "type": "array",
    "items": {
        "type": "number"
    }
}

scf_properties["scf_total_energy"] = {
    "type":
    "number",
    "description":
    """
The total electronic energy of the SCF stage of the calculation.
This is represented as the sum of the ... quantities.
"""
}

scf_properties["scf_iterations"] = {
    "type": "number",
    "multipleOf": 1.0,
    "description": "The number of SCF iterations taken before convergence."
}
