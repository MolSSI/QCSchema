import textwrap

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

def write_key_table(top_file, properties, keys=None):
    table_widths = [45, 120, 27]
    fmt_string = '   | {:%s} | {:%s} | {:%s} |' % tuple(table_widths)
    dash_inds = tuple("-" * w for w in table_widths)
    equals_inds = tuple("=" * w for w in table_widths)
   
    top_file.append("   +-{}-+-{}-+-{}-+".format(*dash_inds))
    top_file.append(fmt_string.format("Key Name", "Description", "Field Type"))
    top_file.append("   +={}=+={}=+={}=+".format(*equals_inds))
  
    if keys is None:
        keys = properties.keys() 

    for key in keys:
        value = properties[key]
   
        dtype = value["type"]
   
        if value["type"] == "object":
            description = value["$ref"]
        else:
            description = value["description"]
   
        if value["type"] == "array":
            dtype = "array[" + value["items"]["type"] + "]"
   
        # Figure out the needed slices
   
        desc_parts = textwrap.wrap(description, width=table_widths[1])
        top_file.append(fmt_string.format(key, desc_parts[0], dtype))
   
        for dp in desc_parts[1:]:
            top_file.append(fmt_string.format("", dp, ""))
   
        top_file.append("   +-{}-+-{}-+-{}-+".format(*dash_inds))
