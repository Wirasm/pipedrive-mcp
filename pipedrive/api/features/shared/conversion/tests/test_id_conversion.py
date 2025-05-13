import pytest

from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string, validate_uuid_string


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


class TestUuidValidation:
    """Tests for UUID validation utility"""
    
    def test_validate_uuid_string_with_valid_uuid(self):
        """Test validating a valid UUID string"""
        valid_uuid = "adf21080-0e10-11eb-879b-05d71fb426ec"
        result, error = validate_uuid_string(valid_uuid, "lead_id")
        
        assert result == valid_uuid
        assert error is None
    
    def test_validate_uuid_string_with_uppercase_uuid(self):
        """Test validating a valid UUID with uppercase characters"""
        uppercase_uuid = "ADF21080-0E10-11EB-879B-05D71FB426EC"
        result, error = validate_uuid_string(uppercase_uuid, "lead_id")
        
        assert result == uppercase_uuid.lower()  # Returns normalized lowercase
        assert error is None
    
    def test_validate_uuid_string_with_invalid_format(self):
        """Test validating an invalid UUID format"""
        invalid_uuid = "not-a-valid-uuid"
        result, error = validate_uuid_string(invalid_uuid, "lead_id")
        
        assert result is None
        assert "Invalid lead_id format" in error
        assert "Must be a valid UUID string" in error
    
    def test_validate_uuid_string_with_wrong_length(self):
        """Test validating a UUID with incorrect length"""
        wrong_length = "adf21080-0e10-11eb-879b-05d71fb426e"  # Missing last character
        result, error = validate_uuid_string(wrong_length, "lead_id")
        
        assert result is None
        assert "Invalid lead_id format" in error
    
    def test_validate_uuid_string_with_invalid_chars(self):
        """Test validating a UUID with invalid characters"""
        invalid_chars = "adf21080-0e10-11eb-879b-05d71fb426ez"  # 'z' at the end
        result, error = validate_uuid_string(invalid_chars, "lead_id")
        
        assert result is None
        assert "Invalid lead_id format" in error
    
    def test_validate_uuid_string_with_empty_string(self):
        """Test validating an empty string"""
        result, error = validate_uuid_string("", "lead_id")
        
        assert result is None
        assert error is None
    
    def test_validate_uuid_string_with_whitespace(self):
        """Test validating a string with only whitespace"""
        result, error = validate_uuid_string("   ", "lead_id")
        
        assert result is None
        assert error is None
    
    def test_validate_uuid_string_with_none(self):
        """Test validating None"""
        result, error = validate_uuid_string(None, "lead_id")
        
        assert result is None
        assert error is None