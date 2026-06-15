import unittest
from cerberus import Validator

class TestForbiddenMUMCUT(unittest.TestCase):
    
    def setUp(self):
        self.v = Validator()

    ## Test case for forbidden with a string field

    ## Test case for Sequence branch with no forbidden values.
    ## A = True, B = False
    ## Expected to pass as the forbidden value is not present in the sequence.
    def test_forbidden_sequence_valid(self):
        schema = {'colors': {'forbidden': ['red']}}
        doc = {'colors': ['blue', 'green']}
        self.assertTrue(self.v.validate(doc, schema))

    ## Test case for Sequence branch with forbidden value present.
    ## A = True, B = False
    ## Expected to fail as the forbidden value 'red' is present in the sequence.
    def test_forbidden_sequence_invalid(self):
        schema = {'colors': {'forbidden': ['red']}}
        doc = {'colors': ['blue', 'red']}
        self.assertFalse(self.v.validate(doc, schema))

    ## Test case for String value
    ## A = True, B = True
    ## Expected to fail as the forbidden value 'red' is present in the string field.    
    def test_forbidden_string_invalid(self):
        schema = {'colors': {'forbidden': ['red']}}
        doc = {'colors': ['blue', 'red']}
        self.assertFalse(self.v.validate(doc, schema))

    ## Test case for String value
    ## A = True, B = True
    ## Expected to pass as the forbidden value 'red' is not present in the string field.
    def test_forbidden_string_valid(self):
        schema = {'colors': {'forbidden': ['red']}}
        doc = {'colors': ['blue']}
        self.assertTrue(self.v.validate(doc, schema))

    ## Test case for integer value
    ## A = False, B = False
    ## Expected to fail as the forbidden value 5 is present in the integer field.
    def test_forbidden_integer_valid(self):
        schema = {'number': {'forbidden': [5]}}
        doc = {'number': 3}
        self.assertTrue(self.v.validate(doc, schema))

