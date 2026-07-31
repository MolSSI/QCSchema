"""
Schema loading and version management for QCSchema.

Dynamically discovers schema versions by scanning qcschema/*/ directories
for a schemas/ subdirectory. Each version can be used with validate() by
passing version as a parameter.
"""

import json
from pathlib import Path


def _normalize_version_name(dir_name):
    """
    Normalize version name from directory name.

    Any directory name is a valid version. Optionally normalize underscores
    to dots for clarity when the name looks numeric (e.g., v1_5 -> v1.5, 1_5 -> 1.5).

    Args:
        dir_name: Directory name to parse

    Returns:
        Normalized version string
    """

    # dots as underscores
    return dir_name.replace("_", ".")


def _scan_version_directories():
    """
    Scan qcschema/ directory for version directories with schemas/ subdirectory.

    Returns:
        List of (version_string, version_dir_path) tuples, sorted by version
    """
    base_path = Path(__file__).parent
    versions = []

    for dir_entry in sorted(base_path.iterdir()):
        if not dir_entry.is_dir():
            continue

        schemas_dir = dir_entry / "schemas"
        if not schemas_dir.exists():
            continue

        version = _normalize_version_name(dir_entry.name)
        versions.append((version, dir_entry))

    return versions


def list_versions(schema_type):
    """
    List all available versions for a given schema type.

    Scans qcschema/*/ directories for available schemas matching the type.
    Supports aliases: input/AtomicInput, output/AtomicResult, molecule/Molecule, etc.

    Args:
        schema_type: Schema type (input, output, molecule, basis, properties, provenance)
                     or an alias (AtomicInput, AtomicResult, Molecule, etc.)

    Returns:
        List of available versions (e.g., [1, '1.5'])

    Raises:
        KeyError: If schema_type is not found or no versions support it
    """
    aliases = {
        "input": ["input", "AtomicInput"],
        "output": ["output", "AtomicResult"],
        "molecule": ["molecule", "Molecule", "topology"],
        "basis": ["basis", "BasisSet"],
        "properties": ["properties", "AtomicResultProperties"],
        "provenance": ["provenance", "Provenance"],
    }

    laliases = {k: [v2.lower() for v2 in v] for k, v in aliases.items()}

    # Find which schema type we're looking for
    schema_key = None
    for key, aliases_list in laliases.items():
        if schema_type.lower() in aliases_list:
            schema_key = key
            break

    if schema_key is None:
        raise KeyError(f"Schema type should be among {list(aliases.keys())} (+aliases), not '{schema_type}'.")

    # Scan for available versions
    versions = []
    for version, version_dir in _scan_version_directories():
        schemas_dir = version_dir / "schemas"

        # Check if this version has schemas for our type
        for schema_file in schemas_dir.glob("*.schema"):
            schema_data = json.loads(schema_file.read_text())
            # Match by internal schema name or filename patterns
            schema_name = schema_data.get("name", "").lower()
            filename = schema_file.stem.lower()

            if schema_key in schema_name or schema_key in filename or filename.endswith(schema_key):
                if version not in versions:
                    versions.append(version)

    if not versions:
        raise KeyError(
            f"No versions found for schema type '{schema_type}'. Available directories: "
            + ", ".join(v for v, _ in _scan_version_directories())
        )

    return versions


def get_schema(schema_type, version="1.5"):
    """
    Load a schema for a given type and version.

    Loads from qcschema/{version}/schemas/ directory. Supports aliases for
    schema types.

    Args:
        schema_type: Schema type (input, output, molecule, basis, properties, provenance)
                     or an alias
        version: Version (int or str, e.g., 1, "1", "1.5"). Defaults to "1.5".

    Returns:
        Schema dictionary (parsed from JSON)

    Raises:
        KeyError: If schema_type or version is not found
        FileNotFoundError: If schema file is missing
    """
    aliases = {
        "input": ["input", "AtomicInput"],
        "output": ["output", "AtomicResult"],
        "molecule": ["molecule", "Molecule", "topology"],
        "basis": ["basis", "BasisSet"],
        "properties": ["properties", "AtomicResultProperties"],
        "provenance": ["provenance", "Provenance"],
    }

    laliases = {k: [v2.lower() for v2 in v] for k, v in aliases.items()}

    # Find schema key
    schema_key = None
    for key, aliases_list in laliases.items():
        if schema_type.lower() in aliases_list:
            schema_key = key
            break

    if schema_key is None:
        raise KeyError(f"Schema type should be among {list(aliases.keys())} (+aliases), not '{schema_type}'.")

    # Normalize version string (underscores to dots)
    version_str = str(version).replace("_", ".")

    # Find the version directory (exact match only)
    version_dir = None
    for v, d in _scan_version_directories():
        if v == version_str:
            version_dir = d
            break

    if version_dir is None:
        raise KeyError(
            f"Schema version '{version}' not found. Available versions: " + ", ".join(list_versions(schema_type))
        )

    schemas_dir = version_dir / "schemas"

    # Find the schema file for this type
    # Filenames are qc_schema_*
    schema_file = schemas_dir / f"qc_schema_{schema_key}.schema"

    if not schema_file.exists():
        raise FileNotFoundError(
            f"Schema file not found: {schema_file}. "
            f"Available schemas in {schemas_dir}: {list(schemas_dir.glob('*.schema'))}"
        )

    return json.loads(schema_file.read_text())
