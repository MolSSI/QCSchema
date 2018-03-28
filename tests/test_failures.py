"""
Tests the JSON schema
"""
import jsonschema
import pytest
import os

import test_helpers
import qc_schema

### Test input validation errors
input_failures = test_helpers.list_tests("input_failures")
input_failure_ids = [x.split("/")[-1].replace(".json", "") for x in input_failures] 

# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", input_failures, ids=input_failure_ids)
@pytest.mark.parametrize("version", qc_schema.list_versions())
def test_input_failures(version, testfile):

    example = test_helpers.get_test(testfile)
    
    with pytest.raises(jsonschema.exceptions.ValidationError):
        qc_schema.validate(example, "input")

### Test output validation errors
output_failures = test_helpers.list_tests("output_failures")
output_failure_ids = [x.split("/")[-1].replace(".json", "") for x in output_failures] 

# Loop over all tests that should pass the tests
@pytest.mark.parametrize("testfile", output_failures, ids=output_failure_ids)
@pytest.mark.parametrize("version", qc_schema.list_versions())
def test_output_failures(version, testfile):

    example = test_helpers.get_test(testfile)
    
    with pytest.raises(jsonschema.exceptions.ValidationError):
        qc_schema.validate(example, "output")

