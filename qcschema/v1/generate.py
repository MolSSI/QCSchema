#!/usr/bin/env python
"""
Generate v1 JSON Schema documents in frozen v1 format.

The v1 format is the original QCSchema with classic basis definitions.
Generates schemas to qcschema/v1/schemas/ directory.

Run as: python -m qcschema.v1.generate
"""

import copy
import json
import sys
from pathlib import Path

from jsonschema import Draft4Validator

# Add generator/properties to Python path
sys.path.insert(0, str(Path(__file__).parent / "generator" / "properties"))
from .generator.properties.calcinfo_properties import calcinfo_properties
from .generator.properties.mp_properties import mp_properties
from .generator.properties.scf_properties import scf_properties


def write_schema(schema, filepath):
    """
    Write a v1 schema to a JSON file (minified, single line, with spacing).
    v1 schemas have no trailing newline.

    Args:
        schema: Schema dictionary
        filepath: Path to write to
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(schema, f, separators=(", ", ": "))


def get_validator():
    """
    Get the JSON Schema validator class for v1 (draft-04).

    Returns:
        jsonschema.Draft4Validator class
    """
    return Draft4Validator


def _validate_property_imports():
    """Validate that property imports are valid dictionaries.

    Raises TypeError if any property module is not a dict.
    """
    if not isinstance(scf_properties, dict):
        raise TypeError(f"scf_properties is not a dict, got {type(scf_properties).__name__}")
    if not isinstance(mp_properties, dict):
        raise TypeError(f"mp_properties is not a dict, got {type(mp_properties).__name__}")
    if not isinstance(calcinfo_properties, dict):
        raise TypeError(f"calcinfo_properties is not a dict, got {type(calcinfo_properties).__name__}")


def _validate_schema_return(schema, schema_name):
    """Validate that a schema return value is a valid dictionary.

    Raises TypeError or ValueError if schema is invalid.
    """
    if not isinstance(schema, dict):
        raise TypeError(f"{schema_name}: returned value is not a dict, got {type(schema).__name__}")

    # JSON Schema should have at least $schema or properties or title
    if not any(key in schema for key in ["$schema", "properties", "title", "type"]):
        raise ValueError(f"{schema_name}: schema missing standard JSON Schema fields")

    return schema


def _validate_definitions(definitions, def_name):
    """Validate that a definitions object is a valid dictionary of schema fragments.

    Raises TypeError or ValueError if definitions is invalid.
    """
    if not isinstance(definitions, dict):
        raise TypeError(f"{def_name}: not a dict, got {type(definitions).__name__}")

    if not definitions:
        raise ValueError(f"{def_name}: definitions dict is empty")

    # Validate each component is a dict with schema-like structure
    for component_name, component in definitions.items():
        if not isinstance(component, dict):
            raise TypeError(f"{def_name}['{component_name}']: not a dict, got {type(component).__name__}")

        # Each definition should have at least some schema keywords
        if not any(key in component for key in ["type", "properties", "enum", "description", "$ref"]):
            raise ValueError(
                f"{def_name}['{component_name}']: missing schema keywords (type, properties, enum, description, or $ref)"
            )

    return definitions


def _build_v1_molecule():
    """Build the frozen v1 molecule schema (original format without schema_name/version)."""
    return {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "name": "qcschema_molecule",
        "version": 1,
        "description": "The physical cartesian representation of the molecular system",
        "type": "object",
        "properties": {
            "symbols": {
                "description": "(nat, ) atom symbols in title case.",
                "type": "array",
                "items": {"type": "string"},
            },
            "geometry": {
                "description": "(3 * nat, ) vector of XYZ coordinates of the atoms.",
                "type": "array",
                "items": {"type": "number"},
            },
            "masses": {
                "description": "(nat, ) atom masses [u]; canonical weights assumed if not given.",
                "type": "array",
                "items": {"type": "number"},
            },
            "name": {"description": "The name of the molecule.", "type": "string"},
            "comment": {"description": "Any additional comment one would attach to the molecule.", "type": "string"},
            "molecular_charge": {
                "description": "The overall charge of the molecule.",
                "type": "number",
                "default": 0.0,
            },
            "molecular_multiplicity": {
                "description": "The overall multiplicity of the molecule.",
                "type": "number",
                "multipleOf": 1.0,
                "default": 1,
            },
            "real": {
                "description": "(nat, ) list describing if atoms are real (T) or ghost (F).",
                "type": "array",
                "items": {"type": "boolean"},
            },
            "connectivity": {
                "description": "(nat, ) list describing bonds within a molecule. Each element is a (atom1, atom2, order) tuple.",
                "type": "array",
                "items": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 3,
                    "items": {"type": "number", "minimum": 0, "maximum": 5},
                },
            },
            "fragments": {
                "description": "(nfr, -1) list of indices (0-indexed) grouping atoms into molecular fragments within the topology.",
                "type": "array",
                "items": {"type": "array", "items": {"type": "number", "multipleOf": 1.0}},
            },
            "fragment_charges": {
                "description": "(nfr, ) list of charges associated with each fragment tuple.",
                "type": "array",
                "items": {"type": "number"},
            },
            "fragment_multiplicities": {
                "description": "(nfr, ) list of multiplicities associated with each fragment tuple.",
                "type": "array",
                "items": {"type": "number", "multipleOf": 1.0},
            },
            "fix_com": {
                "description": "Whether translation of geometry is allowed (fix F) or disallowed (fix T).",
                "type": "boolean",
                "default": False,
            },
            "fix_orientation": {
                "description": "Whether rotation of geometry is allowed (fix F) or disallowed (fix T).",
                "type": "boolean",
                "default": False,
            },
            "provenance": {"type": "object", "$ref": "#/definitions/provenance"},
        },
        "required": ["symbols", "geometry"],
    }


def _build_v1_properties():
    """Build v1-specific properties in exact order to match frozen reference."""
    v1_props = {}

    # Order must match data/v1 exactly:
    # 1. scf_*
    # 2. mp2_same_spin_correlation_energy
    # 3. mp2_opposite_spin_correlation_energy
    # 4. mp2_singles_energy
    # 5. mp2_doubles_energy
    # 6. mp2_total_correlation_energy (inserted here, before mp2_total_energy)
    # 7. mp2_total_energy
    # 8. calcinfo_*
    # 9. return_energy

    # Add scf properties
    v1_props.update(scf_properties)

    # Add selected mp properties in order, excluding correlation_energy and dipole_moment
    mp_order = [
        "mp2_same_spin_correlation_energy",
        "mp2_opposite_spin_correlation_energy",
        "mp2_singles_energy",
        "mp2_doubles_energy",
        "mp2_total_energy",
    ]
    for key in mp_order:
        if key not in mp_properties:
            raise KeyError(f"Required MP2 property '{key}' not found in mp_properties")
        v1_props[key] = mp_properties[key]

    # Fix mp2 property descriptions to match reference exactly
    v1_props["mp2_opposite_spin_correlation_energy"]["description"] = (
        "The unscaled portion of the MP2 correlation energy from opposite-spin or singlet doubles correlations."
    )
    v1_props["mp2_same_spin_correlation_energy"]["description"] = (
        "The unscaled portion of the MP2 correlation energy from same-spin or triplet doubles correlations."
    )
    v1_props["mp2_total_energy"]["description"] = "The total MP2 energy (MP2 correlatin energy + HF energy)."

    # Add mp2_total_correlation_energy before mp2_total_energy in the dict
    # Since we added mp2_total_energy above, we need to remove it, add mp2_total_correlation_energy, then re-add it
    mp2_total_energy_def = v1_props.pop("mp2_total_energy")
    v1_props["mp2_total_correlation_energy"] = {
        "type": "number",
        "description": "The doubles portion of the MP2 correlation energy including same-spin and opposite-spin correlations.",
    }
    v1_props["mp2_total_energy"] = mp2_total_energy_def

    # Include calcinfo properties
    v1_props.update(calcinfo_properties)

    return {
        "type": "object",
        "properties": v1_props,
        "description": "The resulting properties of a computation",
        "additionalProperties": False,
    }


def _build_v1_definitions():
    """Build the frozen v1 definitions with basis_* naming."""
    return {
        "error": {
            "properties": {
                "error_type": {
                    "description": "The type of error raised.",
                    "enum": ["convergence_error", "file_error", "memory_error"],
                },
                "error_message": {"description": "A description of the raised error.", "type": "string"},
            },
            "required": ["error_type", "error_message"],
            "description": "The type of error message raised.",
            "additionalProperties": False,
        },
        "provenance": {
            "properties": {
                "creator": {
                    "description": "The name of the person or program who created this object.",
                    "type": "string",
                },
                "version": {
                    "description": "The version of the program which created this object, blank otherwise.",
                    "type": "string",
                },
                "routine": {
                    "description": "The routine of the program which created this object, blank otherwise.",
                    "type": "string",
                },
            },
            "required": ["creator"],
            "description": "A short provenance of the object.",
            "additionalProperties": True,
        },
        "basis_electron_shell": {
            "description": "Information for a single electronic shell",
            "additionalProperties": False,
            "required": ["shell_angular_momentum", "shell_exponents", "shell_coefficients"],
            "properties": {
                "shell_region": {
                    "description": "The region this shell describes",
                    "type": "string",
                    "enum": ["valence", "polarization", "core", "tight", "diffuse"],
                },
                "shell_angular_momentum": {
                    "description": "Angular momentum (as an array of integers)",
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"type": "integer", "minimum": 0},
                },
                "shell_exponents": {
                    "description": "Exponents for this contracted shell",
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string"},
                },
                "shell_coefficients": {
                    "description": "General contraction coefficients for this contracted shell",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "description": "Segmented contraction coefficients",
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "string"},
                    },
                },
            },
        },
        "basis_ecp_potential": {
            "description": "ECP potential",
            "additionalProperties": False,
            "required": [
                "potential_ecp_type",
                "potential_angular_momentum",
                "potential_r_exponents",
                "potential_gaussian_exponents",
                "potential_coefficients",
            ],
            "properties": {
                "potential_ecp_type": {
                    "description": "Type of the ECP Potential",
                    "type": "string",
                    "enum": ["scalar", "spinorbit"],
                },
                "potential_angular_momentum": {
                    "description": "Angular momentum (as an array of integers)",
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"type": "integer", "minimum": 0},
                },
                "potential_r_exponents": {
                    "description": "Exponents of the r term",
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "integer"},
                },
                "potential_gaussian_exponents": {
                    "description": "Exponents of the gaussian term",
                    "type": "array",
                    "minItems": 1,
                    "items": {"type": "string"},
                },
                "potential_coefficients": {
                    "description": "General contraction coefficients for this contracted shell",
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "description": "Segmented contraction coefficients",
                        "type": "array",
                        "minItems": 1,
                        "items": {"type": "string"},
                    },
                },
            },
        },
        "basis_single_data": {
            "description": "Data for a single atom/center in the basis set",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "element_electron_shells": {
                    "description": "(Electronic) shells for this element",
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"$ref": "#/definitions/basis_electron_shell"},
                },
                "element_ecp_electrons": {
                    "description": "Number of electrons replaced by ECP",
                    "type": "integer",
                    "minimum": 1,
                },
                "element_ecp": {
                    "description": "Effective Core Potential for this element",
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"$ref": "#/definitions/basis_ecp_potential"},
                },
            },
        },
        "basis_spec": {
            "description": "Specification for a basis applied to a molecule",
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "basis_set_description": {"description": "Brief description of the basis set", "type": "string"},
                "basis_function_type": {
                    "description": "Type of function for this basis",
                    "type": "string",
                    "enum": ["gto", "sto"],
                },
                "basis_harmonic_type": {
                    "description": "Harmonic type (spherical, cartesian)",
                    "type": "string",
                    "enum": ["spherical", "cartesian"],
                },
                "basis_set_elements": {
                    "description": "Per-element basis data",
                    "type": "object",
                    "additionalProperties": False,
                    "patternProperties": {"^\\d+$": {"$ref": "#/definitions/basis_single_data"}},
                },
                "basis_set_atoms": {
                    "description": "Basis set overrides for particular atoms or centers",
                    "type": "object",
                    "additionalProperties": False,
                    "patternProperties": {"^\\d+$": {"$ref": "#/definitions/basis_single_data"}},
                },
            },
        },
    }


def build_v1_schemas():
    """Build and return v1 schemas (input, output, molecule) in frozen v1 format.

    Validates all property imports and schema return values.
    """
    # Validate property imports first
    _validate_property_imports()

    # Build schemas with validation
    molecule_schema = _validate_schema_return(_build_v1_molecule(), "v1 molecule schema")
    definitions = _validate_definitions(_build_v1_definitions(), "v1 definitions")

    base_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "name": "qcschema_input",
        "version": 1,
        "description": "The MolSSI Quantum Chemistry Schema",
        "type": "object",
        "properties": {
            "molecule": molecule_schema,
            "schema_name": {"type": "string", "pattern": "\\W*(qcschema)\\W*"},
            "schema_version": {"type": "integer"},
            "driver": {"definition": "The type of computation requested", "enum": ["energy", "gradient", "hessian"]},
            "model": {
                "definition": "The method and basis specification requested",
                "properties": {
                    "method": {"type": "string"},
                    "basis": {"type": "string"},
                    "basis_spec": {"$ref": "#/definitions/basis_spec"},
                },
                "required": ["method"],
                "oneOf": [{"required": ["basis"]}, {"required": ["basis_spec"]}],
                "description": "The quantum chemistry model to be run.",
            },
            "keywords": {"type": "object", "description": "Program specific parameters to be used."},
            "provenance": {
                "anyOf": [
                    {"type": "object", "$ref": "#/definitions/provenance"},
                    {"type": "array", "items": {"type": "object", "$ref": "#/definitions/provenance"}},
                ]
            },
        },
        "required": ["schema_name", "schema_version", "molecule", "driver", "keywords", "model"],
        "definitions": definitions,
    }

    input_schema = copy.deepcopy(base_schema)
    input_schema["name"] = "qcschema_input"
    input_schema["properties"]["schema_name"]["pattern"] = "\\W*(qcschema_input)\\W*"

    output_schema = copy.deepcopy(base_schema)
    output_schema["name"] = "qcschema_output"
    output_schema["properties"]["schema_name"]["pattern"] = "\\W*(qcschema_output)\\W*"
    output_schema["required"].extend(["provenance", "properties", "success", "return_result"])
    v1_properties = _validate_schema_return(_build_v1_properties(), "v1 properties schema")
    output_schema["properties"].update(
        {
            "properties": v1_properties,
            "success": {"type": "boolean"},
            "error": {
                "definition": "The type and description of error raised.",
                "type": "object",
                "$ref": "#/definitions/error",
            },
            "return_result": {
                "definition": "The primary specified return of the requested computation.",
                "anyOf": [{"type": "number"}, {"type": "array", "items": {"type": "number"}}],
            },
        }
    )

    # Validate all schemas before returning
    schemas = {
        "input": input_schema,
        "output": output_schema,
        "molecule": molecule_schema,
    }

    for schema_name, schema in schemas.items():
        _validate_schema_return(schema, f"v1 {schema_name} schema")

    return schemas


def write_schemas(schemas, schema_dir=None):
    """Write schemas to disk.

    Validates schemas exist and writes them to disk.
    Raises KeyError if required schema keys missing.
    Raises RuntimeError if write operations fail.
    """
    if schema_dir is None:
        schema_dir = Path(__file__).parent / "schemas"

    schema_dir = Path(schema_dir)
    schema_dir.mkdir(parents=True, exist_ok=True)

    # Validate that all required schema keys exist
    required_keys = {"input", "output", "molecule"}
    missing_keys = required_keys - set(schemas.keys())
    if missing_keys:
        raise KeyError(f"Schemas missing required keys: {missing_keys}")

    # Write each schema with error handling
    try:
        write_schema(schemas["input"], schema_dir / "qcschema_input.schema")
    except Exception as e:
        raise RuntimeError(f"Failed to write input schema: {e}") from e

    try:
        write_schema(schemas["output"], schema_dir / "qcschema_output.schema")
    except Exception as e:
        raise RuntimeError(f"Failed to write output schema: {e}") from e

    try:
        write_schema(schemas["molecule"], schema_dir / "qcschema_molecule.schema")
    except Exception as e:
        raise RuntimeError(f"Failed to write molecule schema: {e}") from e

    return schema_dir


if __name__ == "__main__":
    schemas = build_v1_schemas()
    schema_dir = write_schemas(schemas)
    print(f"✓ v1 schemas generated in {schema_dir}/")
