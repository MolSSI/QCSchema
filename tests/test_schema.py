"""
Tests the JSON schema
"""
import jsonschema
import pytest
import os

import test_helpers

# Loop over all tests that should pass the tests
@pytest.mark.parametrize("version", test_helpers.list_versions())
@pytest.mark.parametrize("testfile", test_helpers.list_tests("simple"))
def test_schema_validation(version, testfile):

    schema = test_helpers.find_schema(version, "output")
    example = test_helpers.get_test(testfile)
    jsonschema.validate(example, schema)




