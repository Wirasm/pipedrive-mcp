import pytest

from pipedrive.api.features.shared.conversion.id_conversion import (
    convert_id_string,
    validate_date_string,
    validate_time_string,
    validate_uuid_string,
)


class TestConvertIdString:
    def test_valid_id_conversion(self):
        """Test valid ID string conversion."""
        result, error = convert_id_string("123", "test_field")
        assert result == 123
        assert error is None

    def test_empty_id_conversion(self):
        """Test empty ID string conversion."""
        result, error = convert_id_string("", "test_field")
        assert result is None
        assert error is None

        result, error = convert_id_string(None, "test_field")
        assert result is None
        assert error is None

    def test_whitespace_id_conversion(self):
        """Test whitespace ID string conversion."""
        result, error = convert_id_string("  ", "test_field")
        assert result is None
        assert error is None

    def test_non_numeric_id_conversion(self):
        """Test non-numeric ID string conversion."""
        result, error = convert_id_string("abc", "test_field")
        assert result is None
        assert error is not None
        assert "numeric string" in error
        assert "Example: '123'" in error

    def test_negative_id_conversion(self):
        """Test negative ID string conversion."""
        result, error = convert_id_string("-5", "test_field")
        assert result is None
        assert error is not None
        assert "positive integer" in error
        assert "Example: '123'" in error

    def test_zero_id_conversion(self):
        """Test zero ID string conversion."""
        result, error = convert_id_string("0", "test_field")
        assert result is None
        assert error is not None
        assert "positive integer" in error

    def test_custom_example_id_conversion(self):
        """Test custom example in error message."""
        result, error = convert_id_string("abc", "test_field", "456")
        assert "Example: '456'" in error


class TestValidateUuidString:
    def test_valid_uuid_validation(self):
        """Test valid UUID string validation."""
        test_uuid = "123e4567-e89b-12d3-a456-426614174000"
        result, error = validate_uuid_string(test_uuid, "test_field")
        assert result == test_uuid
        assert error is None

    def test_empty_uuid_validation(self):
        """Test empty UUID string validation."""
        result, error = validate_uuid_string("", "test_field")
        assert result is None
        assert error is None

        result, error = validate_uuid_string(None, "test_field")
        assert result is None
        assert error is None

    def test_whitespace_uuid_validation(self):
        """Test whitespace UUID string validation."""
        result, error = validate_uuid_string("  ", "test_field")
        assert result is None
        assert error is None

    def test_invalid_uuid_format_validation(self):
        """Test invalid UUID format validation."""
        # Wrong format
        result, error = validate_uuid_string("123-456-789", "test_field")
        assert result is None
        assert error is not None
        assert "valid UUID string" in error
        assert "Example:" in error

        # Too short
        result, error = validate_uuid_string("123e4567-e89b-12d3-a456", "test_field")
        assert result is None
        assert error is not None

        # Too long
        result, error = validate_uuid_string(
            "123e4567-e89b-12d3-a456-4266141740001", "test_field"
        )
        assert result is None
        assert error is not None

    def test_custom_example_uuid_validation(self):
        """Test custom example in error message."""
        custom_example = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
        result, error = validate_uuid_string("invalid", "test_field", custom_example)
        assert f"Example: '{custom_example}'" in error


class TestValidateDateString:
    def test_valid_date_validation(self):
        """Test valid date string validation."""
        result, error = validate_date_string("2025-01-15", "test_field")
        assert result == "2025-01-15"
        assert error is None

    def test_empty_date_validation(self):
        """Test empty date string validation."""
        result, error = validate_date_string("", "test_field")
        assert result is None
        assert error is None

        result, error = validate_date_string(None, "test_field")
        assert result is None
        assert error is None

    def test_whitespace_date_validation(self):
        """Test whitespace date string validation."""
        result, error = validate_date_string("  ", "test_field")
        assert result is None
        assert error is None

    def test_invalid_date_format_validation(self):
        """Test invalid date format validation."""
        # Wrong separator
        result, error = validate_date_string("2025/01/15", "test_field")
        assert result is None
        assert error is not None
        assert "YYYY-MM-DD format" in error

        # Wrong order
        result, error = validate_date_string("15-01-2025", "test_field")
        assert result is None
        assert error is not None

        # Missing parts
        result, error = validate_date_string("2025-01", "test_field")
        assert result is None
        assert error is not None

    def test_custom_format_and_example_date_validation(self):
        """Test custom format and example in error message."""
        custom_format = "ISO date format"
        custom_example = "2030-12-31"
        result, error = validate_date_string(
            "invalid", "test_field", custom_format, custom_example
        )
        assert custom_format in error
        assert f"Example: '{custom_example}'" in error


class TestValidateTimeString:
    def test_valid_time_validation(self):
        """Test valid time string validation."""
        result, error = validate_time_string("14:30:00", "test_field")
        assert result == "14:30:00"
        assert error is None

    def test_empty_time_validation(self):
        """Test empty time string validation."""
        result, error = validate_time_string("", "test_field")
        assert result is None
        assert error is None

        result, error = validate_time_string(None, "test_field")
        assert result is None
        assert error is None

    def test_whitespace_time_validation(self):
        """Test whitespace time string validation."""
        result, error = validate_time_string("  ", "test_field")
        assert result is None
        assert error is None

    def test_invalid_time_format_validation(self):
        """Test invalid time format validation."""
        # Wrong separator
        result, error = validate_time_string("14.30.00", "test_field")
        assert result is None
        assert error is not None
        assert "HH:MM:SS format" in error

        # Missing seconds
        result, error = validate_time_string("14:30", "test_field")
        assert result is None
        assert error is not None

        # Invalid values
        result, error = validate_time_string("24:30:00", "test_field")  # Hours > 23
        assert result is None
        assert error is not None
        assert "invalid values" in error

        result, error = validate_time_string("14:60:00", "test_field")  # Minutes > 59
        assert result is None
        assert error is not None
        assert "invalid values" in error

        result, error = validate_time_string("14:30:60", "test_field")  # Seconds > 59
        assert result is None
        assert error is not None
        assert "invalid values" in error

    def test_custom_format_and_example_time_validation(self):
        """Test custom format and example in error message."""
        custom_format = "24-hour clock format"
        custom_example = "23:59:59"
        result, error = validate_time_string(
            "invalid", "test_field", custom_format, custom_example
        )
        assert custom_format in error
        assert f"Example: '{custom_example}'" in error
