"""
Tests for qcelemental schema generation and validation.

Tests that qcelemental-specific schemas can be loaded and used for validation.
Note: qcelemental uses different schema_name conventions than the original
qcschema (e.g., "qcschema_output" vs "qcschema_output"), so this test file
uses qcelemental-appropriate data rather than the qcschema test fixtures.
"""

import pytest
from jsonschema import Draft4Validator

import qcschema


@pytest.mark.parametrize("version", ["qcelemental.v1", "qcelemental.v2"])
class TestQCElementalSchemas:
    """Test qcelemental schema versions."""

    def test_schema_discovery(self, version):
        """Verify qcelemental versions are discoverable."""
        # These are the canonical types that should be available
        required_types = ["molecule", "input", "output", "basis", "properties", "provenance"]
        missing_types = []

        for schema_type in required_types:
            try:
                schema = qcschema.get_schema(schema_type, version)
                assert isinstance(schema, dict), f"{schema_type}: schema is not dict"
                assert (
                    "$schema" in schema or "properties" in schema or "title" in schema
                ), f"{schema_type}: schema missing required fields ($schema, properties, or title)"
            except KeyError as e:
                missing_types.append((schema_type, str(e)))

        # Report any missing types explicitly (no silent skipping)
        if missing_types:
            missing_str = ", ".join([f"{t} ({e})" for t, e in missing_types])
            raise AssertionError(f"{version} missing schema types: {missing_str}")

    def test_molecule_schema_loading(self, version):
        """Test that Molecule schema can be loaded."""
        schema = qcschema.get_schema("molecule", version)
        assert schema.get("title") == "Molecule"
        assert "properties" in schema
        # qcelemental Molecule has specific properties
        assert "symbols" in schema["properties"]

    def test_atomic_input_schema_loading(self, version):
        """Test that AtomicInput (input) schema can be loaded."""
        schema = qcschema.get_schema("input", version)
        assert "properties" in schema
        # qcelemental models expect specific field names
        assert "molecule" in schema["properties"]

    def test_atomic_result_schema_loading(self, version):
        """Test that AtomicResult (output) schema can be loaded."""
        schema = qcschema.get_schema("output", version)
        assert "properties" in schema
        # qcelemental output has specific fields
        assert "return_result" in schema["properties"]

    def test_basis_schema_loading(self, version):
        """Test that BasisSet (basis) schema can be loaded."""
        schema = qcschema.get_schema("basis", version)
        assert "properties" in schema

    def test_properties_schema_loading(self, version):
        """Test that AtomicResultProperties (properties) schema can be loaded."""
        schema = qcschema.get_schema("properties", version)
        assert "properties" in schema

    def test_provenance_schema_loading(self, version):
        """Test that Provenance schema can be loaded."""
        schema = qcschema.get_schema("provenance", version)
        assert "properties" in schema

    def test_minimal_molecule_validation(self, version):
        """Test validation of a minimal molecule using qcelemental schema."""
        schema = qcschema.get_schema("molecule", version)

        # Minimal valid molecule for qcelemental
        molecule = {
            "schema_name": "qcschema_molecule",
            "schema_version": 2,
            "symbols": ["H", "H"],
            "geometry": [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        }

        # This should validate without error
        validator = Draft4Validator(schema)
        validator.validate(molecule)

    def test_minimal_atomic_input_validation(self, version):
        """Test validation of minimal AtomicInput using qcelemental schema.

        Uses simple, non-manybody test data appropriate for each version.
        """
        schema = qcschema.get_schema("input", version)

        molecule = {
            "schema_name": "qcschema_molecule",
            "schema_version": 2,
            "symbols": ["H", "H"],
            "geometry": [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        }

        if version == "qcelemental.v1":
            # v1 format: driver/model/keywords at top level
            atomic_input = {
                "schema_name": "qcschema_input",
                "schema_version": 1,
                "molecule": molecule,
                "driver": "energy",
                "model": {"method": "HF", "basis": "sto-3g"},
                "keywords": {},
            }
        else:
            # v2 format: driver/model inside specification
            atomic_input = {
                "schema_name": "qcschema_input",
                "schema_version": 2,
                "molecule": molecule,
                "specification": {
                    "schema_name": "qcschema_atomic_specification",
                    "driver": "energy",
                    "model": {"method": "HF", "basis": "sto-3g"},
                },
            }

        validator = Draft4Validator(schema)
        validator.validate(atomic_input)

    def test_schema_list_versions(self, version):
        """Test that version appears in list_versions for supported types."""
        # All qcelemental versions should support molecule
        versions = qcschema.list_versions("molecule")
        assert version in versions


class TestQCElementalVersSupport:
    """Test that qcelemental versions are properly integrated."""

    def test_both_versions_discoverable(self):
        """Test that both qcelemental.v1 and qcelemental.v2 are discoverable."""
        versions = qcschema.list_versions("molecule")
        assert "qcelemental.v1" in versions
        assert "qcelemental.v2" in versions

    def test_all_canonical_types_available(self):
        """Test that all canonical schema types are available in qcelemental versions."""
        for schema_type in ["molecule", "input", "output", "basis", "properties", "provenance"]:
            versions = qcschema.list_versions(schema_type)
            assert any(v.startswith("qcelemental") for v in versions), f"No qcelemental version found for {schema_type}"

    def test_schema_validator_available(self):
        """Test that validators can be obtained for qcelemental versions."""
        from qcschema.qcelemental_v1 import generate as v1_generate
        from qcschema.qcelemental_v2 import generate as v2_generate

        v1_validator = v1_generate.get_validator()
        v2_validator = v2_generate.get_validator()

        # Both should return Draft4Validator (for now)
        assert v1_validator is Draft4Validator
        assert v2_validator is Draft4Validator

    def test_no_runtime_imports(self):
        """Test that importing qcschema doesn't import qcelemental.

        Note: This test verifies that qcschema doesn't pull in qcelemental
        as a runtime dependency. The test runs in subprocess to avoid
        noise from pytest's own imports (which may include numpy via IPython).
        """
        import subprocess
        import sys

        # Run in subprocess to get clean environment
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys; import qcschema; "
                "assert 'qcelemental' not in sys.modules, 'qcelemental should not be imported'; "
                "print('OK')",
            ],
            env={"PYTHONPATH": "."},
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Failed: {result.stderr}"
        assert "OK" in result.stdout
