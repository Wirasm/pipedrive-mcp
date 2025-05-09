import pytest

from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string


class TestIdConversion:
    def test_valid_id_conversion(self):
        """Test conversion of valid ID string"""
        id_value, error = convert_id_string("123", "test_id")
        
        assert id_value == 123
        assert error is None
    
    def test_empty_id_conversion(self):
        """Test conversion of empty ID string"""
        id_value, error = convert_id_string("", "test_id")
        
        assert id_value is None
        assert error is None
    
    def test_whitespace_id_conversion(self):
        """Test conversion of whitespace ID string"""
        id_value, error = convert_id_string("  ", "test_id")
        
        assert id_value is None
        assert error is None
    
    def test_none_id_conversion(self):
        """Test conversion of None ID"""
        id_value, error = convert_id_string(None, "test_id")
        
        assert id_value is None
        assert error is None
    
    def test_invalid_id_conversion(self):
        """Test conversion of invalid ID string"""
        id_value, error = convert_id_string("abc", "test_id")
        
        assert id_value is None
        assert error == "Invalid test_id format: 'abc'. Must be an integer string."
    
    def test_float_id_conversion(self):
        """Test conversion of float string"""
        id_value, error = convert_id_string("123.45", "test_id")
        
        assert id_value is None
        assert "Invalid test_id format" in error