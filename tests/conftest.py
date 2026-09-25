"""
Pytest configuration for QCSchema test suite.

Provides:
- Auto-skip logic for tests that don't apply to certain versions
- Graceful handling for optional qcelemental dependency
- Management of external pytest plugins
- Test environment setup

Note: If you see "ModuleNotFoundError: No module named 'qcelemental.models._v1v2'"
from a pytest plugin, it means an external package (e.g., qcarchivetesting from
a local QCFractal checkout) has a pytest11 entry point that fails on import.
"""

import pytest

# Version support matrix: which test data applies to which versions
_UNSUPPORTED_TESTS = {
    "v1": {
        "CCSD": "CCSD properties not supported in v1 schema",
        "MP2_output": "MP2 output properties not supported in v1 schema",
        "631G": "Basis set objects not supported in v1 schema (string names only)",
        "STO3G_DEF2": "Basis set objects not supported in v1 schema (string names only)",
        "wavefunction": "Wavefunction feature not supported in v1",
    },
    "v1.5": {},
}


def pytest_runtest_setup(item):
    """
    Auto-skip tests that don't apply to the version being tested.

    This hook runs before each test. If the test has 'version' and 'testfile'
    parameters, we check if the test should be skipped for that combination.
    """
    # Only process parametrized tests with version/testfile
    if not hasattr(item, "callspec"):
        return

    if "version" not in item.callspec.params or "testfile" not in item.callspec.params:
        return

    version = item.callspec.params["version"]
    testfile = item.callspec.params["testfile"]
    filename = testfile.split("/")[-1]

    # Check unsupported tests for this version
    if version in _UNSUPPORTED_TESTS:
        for key, reason in _UNSUPPORTED_TESTS[version].items():
            if key in filename:
                pytest.skip(reason)
                return

    # Skip schema v3 data for all versions (not supported anywhere)
    if "water_output_v3" in filename:
        pytest.skip(f"{version} schema does not support schema_version 3 data")


def pytest_configure(config):
    """
    Configure pytest at session start.

    Registers custom markers for optional dependencies and sets up
    the test environment. Runs after plugins are loaded.
    """
    config.addinivalue_line(
        "markers", "requires_qcelemental: mark test as requiring qcelemental (skipped if unavailable)"
    )


def pytest_sessionstart(session):
    """
    Initialize session and check optional dependency availability.

    Runs after plugin loading. If qcelemental import failed during plugin
    loading, the test process will have already errored with ModuleNotFoundError
    from an external pytest plugin. See _handle_qcelemental_import_error below.
    """
    _check_qcelemental_availability()


def _check_qcelemental_availability():
    """Check if qcelemental is available in the current environment."""
    try:
        import qcelemental  # noqa: F401

        return True
    except ImportError:
        return False


@pytest.fixture
def requires_qcelemental():
    """
    Fixture that skips the test if qcelemental is not available.

    Use this in tests that import or depend on qcelemental:
        def test_something(requires_qcelemental):
            # qcelemental is available or test is skipped
            ...

    If qcelemental is missing, the test is skipped with a clear message.
    """
    if not _check_qcelemental_availability():
        pytest.skip("qcelemental not available")
    import qcelemental

    return qcelemental


@pytest.fixture
def qcelemental_or_skip():
    """
    Fixture that returns qcelemental or skips the test if unavailable.

    Simpler alternative to requires_qcelemental for inline use:
        def test_foo(qcelemental_or_skip):
            qcelemental_or_skip.something()
    """
    if not _check_qcelemental_availability():
        pytest.skip("qcelemental not available")
    import qcelemental

    return qcelemental
