"""
A simple program to construct the input and ouput Quantum Chemistry Schema's
from the development branch
"""
import json

with open("dev/base.json") as infile:
    schema = json.load(infile)

for part in ["molecule"]:
    with open("dev/" + part + ".json") as infile:
        schema["definitions"][part] = json.load(infile)

with open("qc_schema.schema", "w") as outfile:
    json.dump(schema, outfile)

print(json.dumps(schema, indent=2))
