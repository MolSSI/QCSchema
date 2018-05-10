"""
The complete list of the general computation properties.
"""

calcinfo_properties = {}

calcinfo_properties["calcinfo_nbasis"] = {
    "type": "number",
    "multipleOf": 1.0,
    "description": "The number of basis functions for the computation."
}

calcinfo_properties["calcinfo_nmo"] = {
    "type": "number",
    "multipleOf": 1.0,
    "description": "The number of molecular orbitals for the computation."
}

calcinfo_properties["calcinfo_nalpha"] = {
    "type": "number",
    "multipleOf": 1.0,
    "description": "The number of alpha electrons in the computation."
}

calcinfo_properties["calcinfo_nbeta"] = {
    "type": "number",
    "multipleOf": 1.0,
    "description": "The number of beta electrons in the computation."
}

calcinfo_properties["calcinfo_natom"] = {
    "type": "number",
    "multipleOf": 1.0,
    "description": "The number of atoms in the computation."
}

calcinfo_properties["return_energy"] = {
    "type": "number",
    "description": "The energy of the requested method, idential to `return_value` for energy computations."
}
