import unittest
from cerberus import Validator

class TestAnyOfMUMCUT(unittest.TestCase):
    
    def setUp(self):
        self.v = Validator()


    ## Test case for anyof with a string field
    
    ## Test case for valid anyof match with a string value
    ## A = True
    ## Expected to pass as the value matches one of the anyof conditions.
    def test_anyof_string_valid(self):
        schema = {
            'value': {
                'anyof': [
                    {'type': 'string'},
                    {'type': 'integer'}
                ]
            }
        }

        doc = {'value': 'hello'}

        self.assertTrue(self.v.validate(doc, schema))


    ## Test case for valid anyof match with an integer value
    ## A = True
    ## Expected to pass as the value matches another anyof condition.
    def test_anyof_integer_valid(self):
        schema = {
            'value': {
                'anyof': [
                    {'type': 'string'},
                    {'type': 'integer'}
                ]
            }
        }

        doc = {'value': 42}

        self.assertTrue(self.v.validate(doc, schema))


    ## Test case for no match in anyof
    ## A = False
    ## Expected to fail as the value does not match any of the anyof conditions.
    def test_anyof_no_match(self):
        schema = {
            'value': {
                'anyof': [
                    {'type': 'string'},
                    {'type': 'integer'}
                ]
            }
        }

        doc = {'value': 3.14}

        self.assertFalse(self.v.validate(doc, schema))


    ## Test case for anyof with multiple matches
    ## A = True
    ## Expected to pass as the value matches multiple anyof conditions.
    def test_anyof_multiple_matches(self):
        schema = {
            'value': {
                'anyof': [
                    {'min': 0},
                    {'max': 100}
                ]
            }
        }

        doc = {'value': 50}

        self.assertTrue(self.v.validate(doc, schema))