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
calcinfo_props = qcschema.dev.properties.calcinfo_properties.calcinfo_properties

### Schema Properties

prop_file = ["Schema Properties"]
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
    ("Moller-Plesset", """
A list of fields added at the Moller-Plesset (MP) level.
""", mp_props),
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

top_file = ["Schema Topology"]
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
