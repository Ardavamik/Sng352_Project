import unittest
from cerberus import Validator

class TestRegexMUMCUT(unittest.TestCase):
    
    def setUp(self):
        self.v = Validator()

    ## Test case for regex with a string field

    ## Test case for valid regex match
    ## A = True
    ## C = True
    ## Expected to pass as the value matches the regex pattern.
    def test_regex_valid_match(self):
        schema = {'code': {'regex': '[A-Z]{3}'}}
        doc = {'code': 'ABC'}
        self.assertTrue(self.v.validate(doc, schema))

    ## Test case for invalid regex match
    ## A = True
    ## C = False
    ## Expected to fail as the value does not match the regex pattern.
    def test_regex_lowercase_fail(self):
        schema = {'code': {'regex': '[A-Z]{3}'}}
        doc = {'code': 'abc'}
        self.assertFalse(self.v.validate(doc, schema))

    ## Test case for regex with incorrect length
    ## C = False
    ## Expected to fail as the value does not match the regex pattern due to length.
    def test_regex_length_fail(self):
        schema = {'code': {'regex': '[A-Z]{3}'}}
        doc = {'code': 'ABCD'}
        self.assertFalse(self.v.validate(doc, schema))

    ## Test case for regex with boundary values
    ## C = True
    ## Expected to pass as the value matches the regex pattern at the boundary.
    def test_regex_boundary_valid(self):
        schema = {'code': {'regex': '[A-Z]{3}'}}
        doc = {'code': 'XYZ'}
        self.assertTrue(self.v.validate(doc, schema))