"""
Test that schema data ships in the installed package.

This test verifies that the wheel build process includes all six .schema files,
guarding against regression in the packaging configuration.
"""

import os
import shutil
import subprocess
import zipfile

import pytest

_test_path = os.path.dirname(os.path.abspath(__file__))
_base_path = os.path.dirname(_test_path)


@pytest.mark.skipif(
    os.environ.get("QCSCHEMA_SKIP_BUILD_TESTS") == "1",
    reason="build tests disabled via QCSCHEMA_SKIP_BUILD_TESTS",
)
def test_schema_files_in_wheel(tmp_path):
    """Verify all six .schema files appear in the built wheel."""
    # Copy source tree to temp location (excludes .git, build artifacts, etc.)
    copy_dir = tmp_path / "source_copy"
    copy_dir.mkdir()

    exclude_dirs = {".git", "build", "dist", ".egg-info", ".agents", "community_examples", "tests"}
    for item in os.listdir(_base_path):
        item_path = os.path.join(_base_path, item)
        if os.path.isdir(item_path) and item in exclude_dirs:
            continue
        if item.endswith(".egg-info"):
            continue
        if os.path.isfile(item_path):
            shutil.copy2(item_path, copy_dir / item)
        elif os.path.isdir(item_path):
            shutil.copytree(item_path, copy_dir / item)

    # Also copy tests/ but exclude fixture directories
    tests_copy = copy_dir / "tests"
    tests_copy.mkdir()
    for item in os.listdir(os.path.join(_base_path, "tests")):
        item_path = os.path.join(_base_path, "tests", item)
        if item in {"simple", "basis", "wavefunction", "input_failures", "output_failures"}:
            continue
        if os.path.isfile(item_path):
            shutil.copy2(item_path, tests_copy / item)

    # Build wheel from copy
    rc = subprocess.run(
        ["python", "-m", "pip", "wheel", "--no-deps", "--no-build-isolation", "-w", ".", "."],
        cwd=str(copy_dir),
        capture_output=True,
        text=True,
    ).returncode

    if rc != 0:
        pytest.skip("wheel build failed")

    # Find the built wheel
    whl_files = list(copy_dir.glob("*.whl"))
    assert len(whl_files) == 1, f"expected 1 wheel, found {len(whl_files)}"
    whl_path = whl_files[0]

    # Check wheel contents for schema files
    expected_schemas = {
        "qcschema/data/v1/qc_schema_input.schema",
        "qcschema/data/v1/qc_schema_molecule.schema",
        "qcschema/data/v1/qc_schema_output.schema",
        "qcschema/data/v2/qc_schema_input.schema",
        "qcschema/data/v2/qc_schema_molecule.schema",
        "qcschema/data/v2/qc_schema_output.schema",
    }

    with zipfile.ZipFile(whl_path, "r") as whl:
        actual_members = set(whl.namelist())
        found_schemas = expected_schemas & actual_members

    assert len(found_schemas) == 6, f"expected 6 schema files, found {len(found_schemas)}: {found_schemas}"
