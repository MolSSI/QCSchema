"""
Schema validation tools for QCSchema.

Provides validate() function that validates instances against JSON schemas,
selecting the appropriate JSON Schema validator based on version.
"""

import importlib

from . import versions


def validate(data, schema_type, version):
    """
    Validate data against a schema for a given type and version.

    Loads the schema and validator class for the specified version, then
    validates. The validator class (Draft4, Draft202012, etc.) is determined
    by the version's implementation in qcschema/{version}/generate.py.

    Args:
        data: Instance to validate (dict-like)
        schema_type: Schema type (input, output, molecule, basis, properties, provenance)
                     or an alias (AtomicInput, AtomicResult, Molecule, etc.)
        version: Version (int or str, e.g., 1, "1", "1.5"). Required.

    Raises:
        KeyError: If schema_type or version is not found
        FileNotFoundError: If schema file is missing
        jsonschema.ValidationError: If validation fails
        ImportError: If version's utils module cannot be imported
    """
    # Normalize version to string for internal use
    version_str = str(version).replace("_", ".")

    # Load schema from version-specific location
    schema = versions.get_schema(schema_type, version_str)

    # Find the directory name for this version (exact match)
    version_dir_name = None
    for v, d in versions._scan_version_directories():
        if v == version_str:
            version_dir_name = d.name
            break

    if version_dir_name is None:
        raise KeyError(
            f"Cannot find directory for version '{version}'. Available versions: {versions.list_versions(schema_type)}"
        )

    # Import validator class from version-specific generate module
    version_module_name = version_dir_name.replace(".", "_")
    try:
        generate_module = importlib.import_module(f"qcschema.{version_module_name}.generate")
        validator_class = generate_module.get_validator()
    except ImportError as e:
        raise ImportError(
            f"Cannot import validator for version '{version}'. "
            f"qcschema/{version_module_name}/generate.py must define get_validator(). "
            f"Error: {e}"
        ) from e
    except AttributeError as e:
        raise ImportError(
            f"qcschema/{version_module_name}/generate.py must define get_validator() function. " f"Error: {e}"
        ) from e

    # Validate using version-appropriate validator
    validator_class(schema).validate(data)
