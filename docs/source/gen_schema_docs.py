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

### Schema Properties

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


### Schema Topology

top_file = ["Schema Topology"]
top_file.append("=" * len(top_file[-1]))

top_file.extend("""
A full description of the overall molecule its geometry, fragments, and charges.
""".splitlines())

topo_props = qc_schema.dev.molecule.molecule["properties"]
topo_req = qc_schema.dev.molecule.molecule["required"]

table_widths = [27, 80, 20]
fmt_string = '   | {:%s} | {:%s} | {:%s} |' % tuple(table_widths)
dash_inds = tuple("-" * w for w in table_widths)
equals_inds = tuple("=" * w for w in table_widths)

write_header(top_file, "Required Keys")

top_file.extend("""
The following properties are required for a topology.

""".splitlines())

top_file.append("   +-{}-+-{}-+-{}-+".format(*dash_inds))
top_file.append(fmt_string.format("Key Name", "Description", "Field Type"))
top_file.append("   +={}=+={}=+={}=+".format(*equals_inds))

for key in topo_req:
    value = topo_props[key]

    dtype = value["type"]

    if value["type"] == "object":
        description = value["$ref"]
    else:
        description = value["description"]

    if value["type"] == "array":
        dtype = "array of " + value["items"]["type"] + "s"

    if len(description) >= table_widths[1]:    
        while len(description) > 0:
            top_file.append(fmt_string.format(key, description, dtype))
            top_file.append("   +-{}-+-{}-+-{}-+".format(*dash_inds))
    else:
        top_file.append(fmt_string.format(key, description, dtype))
    top_file.append("   +-{}-+-{}-+-{}-+".format(*dash_inds))

# Optional properties
write_header(top_file, "Optional Keys")

top_file.extend("""
The following keys are optional for the topology specification.

""".splitlines())

top_file.append("   +-{}-+-{}-+-{}-+".format(*dash_inds))
top_file.append(fmt_string.format("Key Name", "Description", "Field Type"))
top_file.append("   +={}=+={}=+={}=+".format(*equals_inds))

for key, value in topo_props.items():
    if key in topo_req:
        continue

    dtype = value["type"]

    if value["type"] == "object":
        description = value["$ref"]
    else:
        description = value["description"]

    if value["type"] == "array":
        dtype = "array of " + value["items"]["type"] + "s"
    
    top_file.append(fmt_string.format(key, description, dtype))
    top_file.append("   +-{}-+-{}-+-{}-+".format(*dash_inds))

# Write out the file
with open("auto_topology.rst", "w") as outfile:
    outfile.write("\n".join(top_file))
