"""
Tests the JSON schema
"""
import jsonschema
import pytest
import os

import test_helpers
import qcschema

### Test input validation errors
input_failures = test_helpers.list_tests("input_failures")

# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", input_failures[0], ids=input_failures[1])
@pytest.mark.parametrize("version", qcschema.list_versions())
def test_input_failures(version, testfile):

    example = test_helpers.get_test(testfile)
    
    with pytest.raises(jsonschema.exceptions.ValidationError):
        qcschema.validate(example, "input")

### Test output validation errors
output_failures = test_helpers.list_tests("output_failures")

# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", output_failures[0], ids=output_failures[1])
@pytest.mark.parametrize("version", qcschema.list_versions())
def test_output_failures(version, testfile):

    example = test_helpers.get_test(testfile)
    
    with pytest.raises(jsonschema.exceptions.ValidationError):
        qcschema.validate(example, "output")

