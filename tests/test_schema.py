"""
Tests the JSON schema
"""
import jsonschema
import pytest
import os

import test_helpers
import qcschema


### Test input validation errors
simple_input = test_helpers.list_tests("simple", matcher="input")

# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", simple_input[0], ids=simple_input[1])
@pytest.mark.parametrize("version", qcschema.list_versions("input"))
def test_simple_input(version, testfile):

    example = test_helpers.get_test(testfile)
    if isinstance(version, int) and version < example["schema_version"]:
        with pytest.raises(jsonschema.exceptions.ValidationError):
            qcschema.validate(example, "input", version=version)
    else:
        qcschema.validate(example, "input", version=version)


### Test input validation errors
simple_output = test_helpers.list_tests("simple", matcher="output")

# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", simple_output[0], ids=simple_output[1])
@pytest.mark.parametrize("version", qcschema.list_versions("output"))
def test_simple_output(version, testfile):

    example = test_helpers.get_test(testfile)
    if isinstance(version, int) and version < example["schema_version"]:
        with pytest.raises(jsonschema.exceptions.ValidationError):
            qcschema.validate(example, "output", version=version)
    else:
        qcschema.validate(example, "output", version=version)


### Test basis inputs
basis_input = test_helpers.list_tests("basis", matcher="input")

# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", basis_input[0], ids=basis_input[1])
@pytest.mark.parametrize("version", qcschema.list_versions("input"))
def test_simple_basis_input(version, testfile):

    example = test_helpers.get_test(testfile)
    if isinstance(version, int) and version < example["schema_version"]:
        with pytest.raises(jsonschema.exceptions.ValidationError):
            qcschema.validate(example, "input", version=version)
    else:
        qcschema.validate(example, "input", version=version)


### Test wavefunction outputs
wavefunction_output = test_helpers.list_tests("wavefunction", matcher="output")

# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", wavefunction_output[0], ids=wavefunction_output[1])
@pytest.mark.parametrize("version", qcschema.list_versions("output"))
def test_wavefunction_output(version, testfile, request):

    example = test_helpers.get_test(testfile)

    # by chance, this validates with v1 instead of triggering pytest.raises below, so skip
    if version == 1 and ("water_output_v3" in request.node.name):
        pytest.skip()

    # a proper failure, where schema is not back-compatible, so xfail
    if version == "dev" and ("water_output]" in request.node.name):
        with pytest.raises(jsonschema.exceptions.ValidationError) as e:
            qcschema.validate(example, "output", version=version)

        assert "'restricted' is a required property" in str(e.value)
        pytest.xfail()

    # ordinary operation
    if isinstance(version, int) and version < example["schema_version"]:
        with pytest.raises(jsonschema.exceptions.ValidationError):
            qcschema.validate(example, "output", version=version)
    else:
        qcschema.validate(example, "output", version=version)
