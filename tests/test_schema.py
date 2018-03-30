"""
Tests the JSON schema
"""
import jsonschema
import pytest
import os

import test_helpers
import qc_schema

# Loop over all tests that should pass the tests
@pytest.mark.parametrize("version", qc_schema.list_versions())
@pytest.mark.parametrize("testfile", test_helpers.list_tests("simple"))
def test_schema_validation(version, testfile):

    example = test_helpers.get_test(testfile)
    qc_schema.validate(example, "output")




