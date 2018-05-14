"""
Very hacky way to write out the schema (for demo purposes only)
"""
import qc_schema
import textwrap

# Import headers from this
import sys
import os

sys.path.insert(1, os.path.dirname(__file__))
import schema_doc_helpers as sh

scf_props = qc_schema.dev.properties.scf_properties.scf_properties
mp_props = qc_schema.dev.properties.mp_properties.mp_properties

### Schema Properties

prop_file = ["Schema Properties"]
prop_file.append("=" * len(prop_file[-1]))

intro = """
A list of valid quantum chemistry properties tracked by the schema.
"""

prop_file.extend(intro.split())

# Write out SCF properties
sh.write_header(prop_file, "SCF Properties")

sh.write_key_table(prop_file, scf_props) 

# Write out MP properties
sh.write_header(prop_file, "Moller-Plesset Properties")

sh.write_key_table(prop_file, mp_props) 

# Write out the file
with open("auto_props.rst", "w") as outfile:
    outfile.write("\n".join(prop_file))


### Schema Topology

top_file = ["Schema Topology"]
top_file.append("=" * len(top_file[-1]))

top_file.extend("""
A full description of the overall molecule its geometry, fragments, and charges.
""".splitlines())

topo_props = qc_schema.dev.molecule.molecule["properties"]
topo_req = qc_schema.dev.molecule.molecule["required"]

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
