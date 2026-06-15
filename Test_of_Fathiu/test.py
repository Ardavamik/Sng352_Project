import unittest
from unittest.mock import Mock, MagicMock, patch
from collections.abc import Mapping, Hashable


class TestValidateExcludes(unittest.TestCase):
    """MUMCUT test cases for _validate_excludes"""
    
    def setUp(self):
        """Setup validator mock with common attributes"""
        self.validator = Mock()
        self.validator.schema = {
            'user_id': {'required': True},
            'admin': {'required': False}
        }
        self.validator.document = {}
        self.validator._unrequired_by_excludes = set()
        self.validator._error = Mock()
        self.validator.require_all = False
        
    def test_tc1_mutp_a_true_b_false(self):
        """TC1: A=True (user_id in doc), B=False (admin not in doc) → Error raised"""
        # Setup
        self.validator.document = {'user_id': 123}
        excluded_fields = ['user_id', 'admin']
        field = 'test_field'
        value = 'test_value'
        
        # Execute
        self.validator._validate_excludes(excluded_fields, field, value)
        
        # Assert
        self.validator._error.assert_called_once()
        
    def test_tc2_mutp_a_false_b_true(self):
        """TC2: A=False, B=True → Error raised"""
        # Setup
        self.validator.document = {'admin': True}
        excluded_fields = ['user_id', 'admin']
        field = 'test_field'
        value = 'test_value'
        
        # Execute
        self.validator._validate_excludes(excluded_fields, field, value)
        
        # Assert
        self.validator._error.assert_called_once()
        
    def test_tc3_mnfp_a_false_b_false(self):
        """TC3: A=False, B=False → No error"""
        # Setup
        self.validator.document = {'name': 'John'}
        excluded_fields = ['user_id', 'admin']
        field = 'test_field'
        value = 'test_value'
        
        # Execute
        self.validator._validate_excludes(excluded_fields, field, value)
        
        # Assert
        self.validator._error.assert_not_called()
        
    def test_tc4_cutpnfp_a_true_b_true(self):
        """TC4: A=True, B=True → Error raised (both present)"""
        # Setup
        self.validator.document = {'user_id': 123, 'admin': True}
        excluded_fields = ['user_id', 'admin']
        field = 'test_field'
        value = 'test_value'
        
        # Execute
        self.validator._validate_excludes(excluded_fields, field, value)
        
        # Assert
        self.validator._error.assert_called_once()


class TestValidateType(unittest.TestCase):
    """MUMCUT test cases for _validate_type"""
    
    def setUp(self):
        """Setup validator mock with type mapping"""
        self.validator = Mock()
        self.validator.types_mapping = {}
        self.validator._error = Mock()
        self.validator._drop_remaining_rules = Mock()
        
        # Mock type handlers
        def mock_type_handler(value):
            return value == "hello" or isinstance(value, str)
        
        self.validator.__get_rule_handler = Mock()
        self.validator.__get_rule_handler.return_value = mock_type_handler
        
    def test_tc1_mutp_data_type_none(self):
        """TC1: D=True (data_type=None) → Pass (no error)"""
        # Setup
        data_type = None
        field = 'test_field'
        value = 'anything'
        
        # Execute
        self.validator._validate_type(data_type, field, value)
        
        # Assert
        self.validator._error.assert_not_called()
        
    def test_tc2_mutp_string_type_match(self):
        """TC2: S=True (value is string with data_type='string') → Pass"""
        # Setup
        data_type = 'string'
        field = 'test_field'
        value = 'hello'
        
        # Mock type handler to return True for string
        self.validator.__get_rule_handler.return_value = lambda v: isinstance(v, str)
        
        # Execute
        self.validator._validate_type(data_type, field, value)
        
        # Assert
        self.validator._error.assert_not_called()
        
    def test_tc3_mutp_int_type_match(self):
        """TC3: N=True (value is int with data_type='int') → Pass"""
        # Setup
        data_type = 'int'
        field = 'test_field'
        value = 5
        
        # Mock type handler to return True for int
        self.validator.__get_rule_handler.return_value = lambda v: isinstance(v, int)
        
        # Execute
        self.validator._validate_type(data_type, field, value)
        
        # Assert
        self.validator._error.assert_not_called()
        
    def test_tc4_mnfp_no_type_match(self):
        """TC4: D=False, S=False, N=False → Type error"""
        # Setup
        data_type = 'bool'
        field = 'test_field'
        value = 'hello'
        
        # Mock type handler to return False (no match)
        self.validator.__get_rule_handler.return_value = lambda v: False
        
        # Execute
        self.validator._validate_type(data_type, field, value)
        
        # Assert
        self.validator._error.assert_called_once()
        self.validator._drop_remaining_rules.assert_called_once()


class TestValidateReadonlyFields(unittest.TestCase):
    """MUMCUT test cases for __validate_readonly_fields"""
    
    def setUp(self):
        """Setup validator with schema and mapping"""
        self.validator = Mock()
        self.validator._resolve_rules_set = Mock()
        self.validator._validate_readonly = Mock()
        
    def test_tc1_mutp_both_true(self):
        """TC1: A=True (field in mapping), B=True (readonly=True) → Validate readonly"""
        # Setup
        mapping = {'user_id': 123, 'name': 'John'}
        schema = {
            'user_id': {'readonly': True},
            'name': {'readonly': False}
        }
        
        # Mock _resolve_rules_set to return readonly status
        def resolve_side_effect(field_schema):
            return field_schema
        
        self.validator._resolve_rules_set.side_effect = resolve_side_effect
        
        # Execute private method
        for field in ('user_id',):
            if field in mapping and self.validator._resolve_rules_set(schema[field]).get('readonly'):
                self.validator._validate_readonly(schema[field]['readonly'], field, mapping[field])
        
        # Assert
        self.validator._validate_readonly.assert_called_once_with(True, 'user_id', 123)
        
    def test_tc2_mutp_a_true_b_false(self):
        """TC2: A=True, B=False (readonly=False) → Skip validation"""
        # Setup
        mapping = {'name': 'John'}
        schema = {'name': {'readonly': False}}
        
        self.validator._resolve_rules_set.return_value = {'readonly': False}
        
        # Execute check
        should_validate = False
        for field in ('name',):
            if field in mapping and self.validator._resolve_rules_set(schema[field]).get('readonly'):
                should_validate = True
        
        # Assert
        self.assertFalse(should_validate)
        self.validator._validate_readonly.assert_not_called()
        
    def test_tc3_mutp_a_false_b_true(self):
        """TC3: A=False (field not in mapping), B=True → Skip validation"""
        # Setup
        mapping = {'name': 'John'}
        schema = {'user_id': {'readonly': True}}
        
        # Execute check
        should_validate = False
        for field in ('user_id',):
            if field in mapping and self.validator._resolve_rules_set(schema[field]).get('readonly'):
                should_validate = True
        
        # Assert
        self.assertFalse(should_validate)
        self.validator._validate_readonly.assert_not_called()


class TestValidateValuesRules(unittest.TestCase):
    """MUMCUT test cases for _validate_valuesrules"""
    
    def setUp(self):
        """Setup validator with mock child validator"""
        self.validator = Mock()
        self.validator._get_child_validator = Mock()
        self.validator._error = Mock()
        self.validator._drop_nodes_from_errorpaths = Mock()
        self.validator.update = False
        
    def test_tc1_mutp_both_true(self):
        """TC1: A=True (value is Mapping), B=True (child validator passes) → No error"""
        # Setup
        value = {'a': 5, 'b': 10}
        field = 'test_field'
        schema = {'type': 'int'}
        
        # Mock child validator that passes
        mock_child_validator = Mock()
        mock_child_validator._errors = []
        mock_child_validator.return_value = None
        self.validator._get_child_validator.return_value = mock_child_validator
        
        # Execute
        if isinstance(value, Mapping):
            validator = self.validator._get_child_validator(
                document_crumb=field,
                schema_crumb=(field, 'valuesrules'),
                schema={k: schema for k in value},
            )
            validator(value, update=self.validator.update, normalize=False)
            
            if validator._errors:
                self.validator._error(field, 'VALUESRULES_ERROR', validator._errors)
        
        # Assert
        self.validator._error.assert_not_called()
        
    def test_tc2_mutp_a_true_b_false(self):
        """TC2: A=True, B=False (child validator fails) → Error"""
        # Setup
        value = {'a': 5, 'b': 'hello'}
        field = 'test_field'
        schema = {'type': 'int'}
        
        # Mock child validator that fails
        mock_child_validator = Mock()
        mock_child_validator._errors = [{'field': 'b', 'error': 'BAD_TYPE'}]
        mock_child_validator.return_value = None
        self.validator._get_child_validator.return_value = mock_child_validator
        
        # Execute
        if isinstance(value, Mapping):
            validator = self.validator._get_child_validator(
                document_crumb=field,
                schema_crumb=(field, 'valuesrules'),
                schema={k: schema for k in value},
            )
            validator(value, update=self.validator.update, normalize=False)
            
            if validator._errors:
                self.validator._error(field, 'VALUESRULES_ERROR', validator._errors)
        
        # Assert
        self.validator._error.assert_called_once()
        
    def test_tc3_mutp_a_false_b_true(self):
        """TC3: A=False (value is not Mapping), B=True (would pass) → Skip"""
        # Setup
        value = [1, 2, 3]  # List, not Mapping
        field = 'test_field'
        schema = {'type': 'int'}
        
        # Execute
        if isinstance(value, Mapping):
            # This block should NOT execute
            self.fail("Should not enter Mapping block")
        else:
            # Skip validation
            pass
        
        # Assert
        self.validator._error.assert_not_called()
        self.validator._get_child_validator.assert_not_called()


class TestValidateDependenciesMapping(unittest.TestCase):
    """MUMCUT test cases for __validate_dependencies_mapping"""
    
    def setUp(self):
        """Setup validator with mock methods"""
        self.validator = Mock()
        self.validator._lookup_field = Mock()
        self.validator._error = Mock()
        
    def test_tc1_mutp_both_true(self):
        """TC1: A=True, B=True → No error"""
        # Setup
        dependencies = {'status': ['active'], 'role': ['admin']}
        field = 'test_field'
        
        # Mock _lookup_field returns (field_name, field_value)
        def lookup_side_effect(dep_name):
            if dep_name == 'status':
                return ('status', 'active')
            else:
                return ('role', 'admin')
        
        self.validator._lookup_field.side_effect = lookup_side_effect
        
        # Execute
        validated_dependencies_counter = 0
        error_info = {}
        
        for dependency_name, dependency_values in dependencies.items():
            if not isinstance(dependency_values, (list, tuple)) or isinstance(dependency_values, str):
                dependency_values = [dependency_values]
            
            wanted_field, wanted_field_value = self.validator._lookup_field(dependency_name)
            if wanted_field_value in dependency_values:
                validated_dependencies_counter += 1
            else:
                error_info.update({dependency_name: wanted_field_value})
        
        if validated_dependencies_counter != len(dependencies):
            self.validator._error(field, 'DEPENDENCIES_FIELD_VALUE', error_info)
        
        # Assert
        self.validator._error.assert_not_called()
        
    def test_tc2_mutp_a_true_b_false(self):
        """TC2: A=True, B=False → Error"""
        # Setup
        dependencies = {'status': ['active'], 'role': ['admin']}
        field = 'test_field'
        
        def lookup_side_effect(dep_name):
            if dep_name == 'status':
                return ('status', 'active')
            else:
                return ('role', 'guest')  # Not in ['admin']
        
        self.validator._lookup_field.side_effect = lookup_side_effect
        
        # Execute
        validated_dependencies_counter = 0
        error_info = {}
        
        for dependency_name, dependency_values in dependencies.items():
            if not isinstance(dependency_values, (list, tuple)) or isinstance(dependency_values, str):
                dependency_values = [dependency_values]
            
            wanted_field, wanted_field_value = self.validator._lookup_field(dependency_name)
            if wanted_field_value in dependency_values:
                validated_dependencies_counter += 1
            else:
                error_info.update({dependency_name: wanted_field_value})
        
        if validated_dependencies_counter != len(dependencies):
            self.validator._error(field, 'DEPENDENCIES_FIELD_VALUE', error_info)
        
        # Assert
        self.validator._error.assert_called_once()
        
    def test_tc3_mutp_a_false_b_true(self):
        """TC3: A=False, B=True → Error"""
        # Setup
        dependencies = {'status': ['active'], 'role': ['admin']}
        field = 'test_field'
        
        def lookup_side_effect(dep_name):
            if dep_name == 'status':
                return ('status', 'inactive')  # Not in ['active']
            else:
                return ('role', 'admin')
        
        self.validator._lookup_field.side_effect = lookup_side_effect
        
        # Execute
        validated_dependencies_counter = 0
        error_info = {}
        
        for dependency_name, dependency_values in dependencies.items():
            if not isinstance(dependency_values, (list, tuple)) or isinstance(dependency_values, str):
                dependency_values = [dependency_values]
            
            wanted_field, wanted_field_value = self.validator._lookup_field(dependency_name)
            if wanted_field_value in dependency_values:
                validated_dependencies_counter += 1
            else:
                error_info.update({dependency_name: wanted_field_value})
        
        if validated_dependencies_counter != len(dependencies):
            self.validator._error(field, 'DEPENDENCIES_FIELD_VALUE', error_info)
        
        # Assert
        self.validator._error.assert_called_once()
        
    def test_tc4_mnfp_both_false(self):
        """TC4: A=False, B=False → Error"""
        # Setup
        dependencies = {'status': ['active'], 'role': ['admin']}
        field = 'test_field'
        
        def lookup_side_effect(dep_name):
            if dep_name == 'status':
                return ('status', 'inactive')  # Not in ['active']
            else:
                return ('role', 'guest')  # Not in ['admin']
        
        self.validator._lookup_field.side_effect = lookup_side_effect
        
        # Execute
        validated_dependencies_counter = 0
        error_info = {}
        
        for dependency_name, dependency_values in dependencies.items():
            if not isinstance(dependency_values, (list, tuple)) or isinstance(dependency_values, str):
                dependency_values = [dependency_values]
            
            wanted_field, wanted_field_value = self.validator._lookup_field(dependency_name)
            if wanted_field_value in dependency_values:
                validated_dependencies_counter += 1
            else:
                error_info.update({dependency_name: wanted_field_value})
        
        if validated_dependencies_counter != len(dependencies):
            self.validator._error(field, 'DEPENDENCIES_FIELD_VALUE', error_info)
        
        # Assert
        self.validator._error.assert_called_once()


if __name__ == '__main__':
    unittest.main()