"""
Very hacky way to write out the schema (for demo purposes only)
"""
import qc_schema

scf_props = qc_schema.dev.properties.scf_properties.scf_properties
mp_props = qc_schema.dev.properties.mp_properties.mp_properties

def write_header(data, header):
    data.append("")
    data.append(header)
    data.append("-" * len(header))
    data.append("")

def write_line_items(data, key, item):
    data.append("")
    data.append(key)
    data.append("~" * len(key))
    data.append("")
    if "description" in item:
        data.append(item["description"])
    else:
        data.append("No description available")
    data.append("")


prop_file = ["Schema Properties"]
prop_file.append("=" * len(prop_file[-1]))

intro = """
A list of valid quantum chemistry properties tracked by the schema.
"""

prop_file.extend(intro.split())

# Write out SCF properties
write_header(prop_file, "SCF Properties")

for key, value in scf_props.items():
    write_line_items(prop_file, key, value)

# Write out MP properties
write_header(prop_file, "Moller-Plesset Properties")

for key, value in mp_props.items():
    write_line_items(prop_file, key, value)

# Write out the file
with open("auto_props.rst", "w") as outfile:
    outfile.write("\n".join(prop_file))


### Write out Topology

top_file = ["Schema Topology"]
top_file.append("=" * len(top_file[-1]))

intro = """
A list of valid quantum chemistry properties tracked by the schema.
"""

top_file.extend(intro.split())

topo_props = qc_schema.dev.molecule.molecule["properties"]

for key, value in topo_props.items():
    write_line_items(top_file, key, value)

# Write out the file
with open("auto_topology.rst", "w") as outfile:
    outfile.write("\n".join(top_file))
