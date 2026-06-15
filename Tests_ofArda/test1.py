import unittest
from cerberus import Validator

class TestDependenciesMUMCUT(unittest.TestCase):
    
    def setUp(self):
        self.v = Validator()

    ## Test case for dependencies with a list of fields

    ## Test case for dependencies with a string field
    ## A = True, B = True
    ## Expected to pass as the required dependency field is present in the document.
    def test_d1_string_dependency(self):
        schema = {
            'user_type': {
                'type': 'string'
            },
            'age': {
                'type': 'integer',
                'dependencies': 'user_type'
            }
        }

        doc = {
            'user_type': 'adult',
            'age': 25
        }

        self.assertTrue(self.v.validate(doc, schema))

    ## Test case for missing string dependency field
    ## A = True, B = True
    ## Expected to fail as the required dependency field is missing from the document.
    def test_d1_string_dependency_missing(self):
        schema = {
            'user_type': {
                'type': 'string'
            },
            'age': {
                'type': 'integer',
                'dependencies': 'user_type'
            }
        }

        doc = {
            'age': 25
        }

        self.assertFalse(self.v.validate(doc, schema))


    ## Test case for list dependency
    ## A = False, B = True
    ## Expected to pass as the required dependency field is present in the document.
    def test_d1_list_dependency(self):
        schema = {
            'user_type': {
                'type': 'string'
            },
            'age': {
                'type': 'integer',
                'dependencies': ['user_type']
            }
        }

        doc = {
            'user_type': 'adult',
            'age': 25
        }

        self.assertTrue(self.v.validate(doc, schema))


    ## Test case for mapping dependency
    ## A = False, B = True
    ## Expected to pass as the required dependency field is present in the document.
    def test_d1_mapping_dependency(self):
        schema = {
            'user_type': {
                'type': 'string'
            },
            'age': {
                'type': 'integer',
                'dependencies': {
                    'user_type': 'adult'
                }
            }
        }

        doc = {
            'user_type': 'adult',
            'age': 25
        }

        self.assertTrue(self.v.validate(doc, schema))

    
    ## Test case for sequence dependencies with a string field
    ## C = True, D = True
    ## Expected to pass as the required dependency field is present in the document.
    def test_d2_sequence_string(self):
        schema = {
            'user_type': {
                'type': 'string'
            },
            'age': {
                'type': 'integer',
                'dependencies': {
                    'user_type': 'adult'
                }
            }
        }

        doc = {
            'user_type': 'adult',
            'age': 25
        }

        self.assertTrue(self.v.validate(doc, schema))

    
    ## Test case for sequence dependencies with a list of fields
    ## C = True, D = True
    ## Expected to pass as the required dependency field is present in the document.
    def test_d2_sequence_list(self):
        schema = {
            'user_type': {
                'type': 'string'
            },
            'age': {
                'type': 'integer',
                'dependencies': ['user_type']
            }
        }

        doc = {
            'user_type': 'adult',
            'age': 25
        }

        self.assertTrue(self.v.validate(doc, schema))

    
    ## Test case for sequence dependencies with a mapping
    ## C = True, D = True
    ## Expected to pass as the required dependency field is present in the document.
    def test_d2_mapping_valid(self):
        schema = {
            'user_type': {
                'type': 'string'
            },
            'age': {
                'type': 'integer',
                'dependencies': {
                    'user_type': 'adult'
                }
            }
        }

        doc = {
            'user_type': 'adult',
            'age': 25
        }

        self.assertTrue(self.v.validate(doc, schema))

    ## Test case for sequence dependencies with a mapping (invalid)
    ## C = True, D = False
    ## Expected to fail as the required dependency field does not match the specified value in the schema.
    def test_d2_mapping_invalid(self):
        schema = {
            'user_type': {
                'type': 'string'
            },
            'age': {
                'type': 'integer',
                'dependencies': {
                    'user_type': 'adult'
                }
            }
        }

        doc = {
            'user_type': 'child',
            'age': 25
        }

        self.assertFalse(self.v.validate(doc, schema))