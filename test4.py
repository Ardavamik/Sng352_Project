import unittest
from cerberus import Validator

class TestItemsMUMCUT(unittest.TestCase):
    
    def setUp(self):
        self.v = Validator()

    ## Test case for items with a list field
    
    ## Test case for valid items match with correct types
    ## A = True
    ## Expected to pass as the list items match the specified types in the schema.
    def test_items_valid(self):
        schema = {
            'person': {
                'items': [
                    {'type': 'string'},
                    {'type': 'integer'}
                ]
            }
        }
        doc = {'person': ['John', 25]}
        self.assertTrue(self.v.validate(doc, schema))


    ## Test case for too few items in the list
    ## A = False
    ## Expected to fail as the list does not contain enough items to satisfy the schema requirements.
    def test_items_too_few(self):
        schema = {
            'person': {
                'items': [
                    {'type': 'string'},
                    {'type': 'integer'}
                ]
            }
        }
        doc = {'person': ['John']}
        self.assertFalse(self.v.validate(doc, schema))


    ## Test case for invalid type in the first item of the list
    ## B = True
    ## Expected to fail as the first item does not match the specified type in the schema.
    def test_items_first_invalid(self):
        schema = {
            'person': {
                'items': [
                    {'type': 'string'},
                    {'type': 'integer'}
                ]
            }
        }
        doc = {'person': [123, 25]}
        self.assertFalse(self.v.validate(doc, schema))

    ## Test case for invalid type in the second item of the list
    ## B = False
    ## Expected to fail as the second item does not match the specified type in the schema.
    def test_items_second_invalid(self):
        schema = {
            'person': {
                'items': [
                    {'type': 'string'},
                    {'type': 'integer'}
                ]
            }
        }
        doc = {'person': ['John', 'twenty-five']}
        self.assertFalse(self.v.validate(doc, schema))




    