"""
Tests the JSON schema
"""

import pytest
import test_helpers

import qcschema

### Test input validation errors
simple_input = test_helpers.list_tests("simple", matcher="input")

# Filter out qcelemental versions (they have incompatible schema_name conventions)
# qcelemental-specific tests are in test_qcelemental_schemas.py
input_versions = test_helpers.filter_versions(qcschema.list_versions("input"), exclude_pattern="qcelemental")


# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", simple_input[0], ids=simple_input[1])
@pytest.mark.parametrize("version", input_versions)
def test_simple_input(version, testfile, request):
    example = test_helpers.get_test(testfile)
    qcschema.validate(example, "input", version=version)


### Test output validation
simple_output = test_helpers.list_tests("simple", matcher="output")

output_versions = test_helpers.filter_versions(qcschema.list_versions("output"), exclude_pattern="qcelemental")


# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", simple_output[0], ids=simple_output[1])
@pytest.mark.parametrize("version", output_versions)
def test_simple_output(version, testfile, request):
    example = test_helpers.get_test(testfile)
    qcschema.validate(example, "output", version=version)


### Test basis inputs
basis_input = test_helpers.list_tests("basis", matcher="input")

basis_input_versions = test_helpers.filter_versions(qcschema.list_versions("input"), exclude_pattern="qcelemental")


# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", basis_input[0], ids=basis_input[1])
@pytest.mark.parametrize("version", basis_input_versions)
def test_simple_basis_input(version, testfile, request):
    example = test_helpers.get_test(testfile)
    qcschema.validate(example, "input", version=version)


### Test wavefunction outputs
wavefunction_output = test_helpers.list_tests("wavefunction", matcher="output")

wavefunction_output_versions = test_helpers.filter_versions(
    qcschema.list_versions("output"), exclude_pattern="qcelemental"
)


# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", wavefunction_output[0], ids=wavefunction_output[1])
@pytest.mark.parametrize("version", wavefunction_output_versions)
def test_wavefunction_output(version, testfile, request):
    example = test_helpers.get_test(testfile)
    qcschema.validate(example, "output", version=version)
