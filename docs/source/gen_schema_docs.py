"""
Very hacky way to write out the schema (for demo purposes only)
"""
import qcschema
import textwrap

# Import headers from this
import sys
import os

sys.path.insert(1, os.path.dirname(__file__))
import schema_doc_helpers as sh

scf_props = qcschema.dev.properties.scf_properties.scf_properties
mp_props = qcschema.dev.properties.mp_properties.mp_properties
cc_props = qcschema.dev.properties.cc_properties.cc_properties
calcinfo_props = qcschema.dev.properties.calcinfo_properties.calcinfo_properties

### Schema Properties

prop_file = ["Properties Schema"]
prop_file.append("=" * len(prop_file[-1]))

prop_file.extend("""
A list of valid quantum chemistry properties tracked by the schema.
""".splitlines())

prop_categories = [
    ("Calculation Information", """
A list of fields that involve basic information of the requested computation.
""", calcinfo_props),
    ("Self-Consistent Field", """
A list of fields added at the self-consistent field (SCF) level. This includes
both Hartree--Fock and Density Functional Theory.
""", scf_props),
    ("Møller-Plesset", """
A list of fields added at the Møller--Plesset (MP) level.
""", mp_props),
    ("Coupled Cluster", """
A list of fields added at the Coupled Cluster (CC) level.
""", cc_props),
]

for cat in prop_categories:
    sh.write_header(prop_file, cat[0])

    prop_file.extend(cat[1].splitlines())
    prop_file.append("")

    sh.write_key_table(prop_file, cat[2])

# Write out the file
with open("auto_props.rst", "w") as outfile:
    outfile.write("\n".join(prop_file))

### Schema Topology

top_file = ["Topology Schema"]
top_file.append("=" * len(top_file[-1]))

top_file.extend("""
A full description of the overall molecule its geometry, fragments, and charges.
""".splitlines())

topo_props = qcschema.dev.molecule.molecule["properties"]
topo_req = qcschema.dev.molecule.molecule["required"]

sh.write_header(top_file, "Required Keys")

top_file.extend("""
The following properties are required for a topology.

""".splitlines())

sh.write_key_table(top_file, topo_props, topo_req)

### Optional properties
sh.write_header(top_file, "Optional Keys")

top_file.extend("""
The following keys are optional for the topology specification.

""".splitlines())

sh.write_key_table(top_file, topo_props, set(topo_props.keys()) - set(topo_req))

# Write out the file
with open("auto_topology.rst", "w") as outfile:
    outfile.write("\n".join(top_file))


### Wavefunction Properties

result_wf = qcschema.dev.wavefunction.result_wavefunction.result_wavefunction
scf_wf = qcschema.dev.wavefunction.scf_wavefunction.scf_wavefunction
localized_wf = qcschema.dev.wavefunction.localized_wavefunction.localized_wavefunction
core_wf = qcschema.dev.wavefunction.core_wavefunction.core_wavefunction

wf_file = ["Wavefunction Schema"]
wf_file.append("=" * len(wf_file[-1]))

wf_file.extend("""
A list of valid quantum chemistry wavefunction properties tracked by the schema.
Matrices are in column-major order.
AO basis functions are ordered according to the CCA standard. [TODO]
""".splitlines())

sh.write_header(wf_file, "Basis Set")
wf_file.extend("""
One-electron AO basis set. See :doc:`auto_basis`.
""".splitlines())

wf_categories = [
    ("Result", """
A list of fields comprising the primary result information. 
e.g. SCF quantities for a DFT calculation and MP2 quantities for an MP2 calculation.  
""", result_wf),
    ("Self-Consistent Field", """
A list of fields added at the self-consistent field (SCF) level. This includes
both Hartree--Fock and Density Functional Theory.
""", scf_wf),
    ("Localized Orbitals", """
A list of fields added at by orbital localization. 
Full MO matrices are stored even if only a subset of MOs are localized.
""", localized_wf),
    ("Core Hamiltonian", """
A list of fields associated with (effective) one-electron (AKA) core Hamiltonians. 
""", core_wf)
]

for cat in wf_categories:
    sh.write_header(wf_file, cat[0])

    wf_file.extend(cat[1].splitlines())
    wf_file.append("")

    sh.write_key_table(wf_file, cat[2])

# Write out the file
with open("auto_wf.rst", "w") as outfile:
    outfile.write("\n".join(wf_file))


### Schema Basis

basis_file = ["Basis Set Schema"]
basis_file.append("=" * len(basis_file[-1]))

basis_file.extend("""
A full description of the basis set. 
""".splitlines())

basis_props = qcschema.dev.basis.basis["properties"]
basis_req = qcschema.dev.basis.basis["required"]

sh.write_header(basis_file, "Required Keys")

basis_file.extend("""
The following properties are required for a basis set.

""".splitlines())

sh.write_key_table(basis_file, basis_props, basis_req)

### Optional properties
sh.write_header(basis_file, "Optional Keys")

basis_file.extend("""
The following keys are optional for the basis set specification.

""".splitlines())

sh.write_key_table(basis_file, basis_props, set(basis_props.keys()) - set(basis_req))

# Write out the file
with open("auto_basis.rst", "w") as outfile:
    outfile.write("\n".join(basis_file))

