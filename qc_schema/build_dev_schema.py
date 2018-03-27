"""
A simple program to construct the input and ouput Quantum Chemistry Schema's
from the development branch
"""
import os
import json
import glob

def read_json(filename):
    with open(filename, "r") as infile:
        data = json.load(infile)
    return data

# Load in the base JSON
with open("dev/base.json") as infile:
    schema = json.load(infile)

# Add the definitions together
for def_file in glob.glob("dev/definitions/*"):
    def_json = read_json(def_file)
    name = os.path.basename(def_file).replace(".json", "")

    schema["definitions"][name] = def_json
    
# Load in larger pieces like molecule and variables spec
for base_spec in ["molecule"]:
    def_json = read_json("dev/" + base_spec + ".json")
    schema["properties"][base_spec] = def_json

# Write out the input and output specs
input_required = ["molecule", "driver", "keywords"]
output_required = input_required + ["provenance", "properties", "error", "success", "raw_output"]

for prefix, required in zip(["input", "output"], [input_required, output_required]):
    schema["required"] = required
    with open(prefix + "_qc_schema.schema", "w") as outfile:
        json.dump(schema, outfile)

# Print the output spec for prosperity
# print(json.dumps(schema, indent=2))
