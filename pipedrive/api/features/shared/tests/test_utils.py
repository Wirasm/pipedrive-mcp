import json
from datetime import date, datetime

import pytest

from pipedrive.api.features.shared.utils import (
    DateTimeEncoder,
    bool_to_lowercase_str,
    format_tool_response,
    format_validation_error,
    safe_split_to_list,
    sanitize_inputs,
)


class TestDateTimeEncoder:
    def test_datetime_encoding(self):
        """Test date and datetime encoding."""
        test_date = date(2025, 1, 15)
        test_datetime = datetime(2025, 1, 15, 14, 30, 0)

        data = {"date": test_date, "datetime": test_datetime, "other": "string_value"}

        json_str = json.dumps(data, cls=DateTimeEncoder)

        # Parse it back to check the values
        parsed = json.loads(json_str)

        assert parsed["date"] == "2025-01-15"
        assert parsed["datetime"] == "2025-01-15T14:30:00"
        assert parsed["other"] == "string_value"


class TestFormatToolResponse:
    def test_success_response_with_data(self):
        """Test formatting success response with data."""
        data = {"id": 123, "name": "Test"}
        response = format_tool_response(True, data=data)

        # Parse the JSON response
        parsed = json.loads(response)

        assert parsed["success"] is True
        assert parsed["data"] == data
        assert parsed["error"] is None

    def test_error_response(self):
        """Test formatting error response."""
        error_message = "An error occurred"
        response = format_tool_response(False, error_message=error_message)

        # Parse the JSON response
        parsed = json.loads(response)

        assert parsed["success"] is False
        assert parsed["data"] is None
        assert parsed["error"] == error_message

    def test_response_with_date_objects(self):
        """Test formatting response with date objects."""
        data = {"date": date(2025, 1, 15)}
        response = format_tool_response(True, data=data)

        # Parse the JSON response
        parsed = json.loads(response)

        assert parsed["success"] is True
        assert parsed["data"]["date"] == "2025-01-15"


class TestFormatValidationError:
    def test_format_validation_error(self):
        """Test validation error formatting."""
        field_name = "id"
        value = "abc"
        expected_format = "Must be a numeric string"
        example = "123"

        error = format_validation_error(field_name, value, expected_format, example)

        assert f"Invalid {field_name} format: '{value}'" in error
        assert expected_format in error
        assert f"Example: '{example}'" in error


class TestSanitizeInputs:
    def test_sanitize_empty_strings(self):
        """Test sanitizing empty strings to None."""
        inputs = {
            "empty": "",
            "whitespace": "   ",
            "normal": "value",
            "number": 123,
            "boolean": True,
            "none": None,
        }

        sanitized = sanitize_inputs(inputs)

        assert sanitized["empty"] is None
        assert sanitized["whitespace"] is None
        assert sanitized["normal"] == "value"
        assert sanitized["number"] == 123
        assert sanitized["boolean"] is True
        assert sanitized["none"] is None


class TestBoolToLowercaseStr:
    def test_true_conversion(self):
        """Test True to lowercase string conversion."""
        result = bool_to_lowercase_str(True)
        assert result == "true"

    def test_false_conversion(self):
        """Test False to lowercase string conversion."""
        result = bool_to_lowercase_str(False)
        assert result == "false"

    def test_none_conversion(self):
        """Test None conversion."""
        result = bool_to_lowercase_str(None)
        assert result is None


class TestSafeSplitToList:
    def test_valid_comma_separated_string(self):
        """Test splitting valid comma-separated string."""
        result = safe_split_to_list("one,two,three")
        assert result == ["one", "two", "three"]

    def test_trim_whitespace(self):
        """Test trimming whitespace from items."""
        result = safe_split_to_list(" one , two , three ")
        assert result == ["one", "two", "three"]

    def test_empty_string(self):
        """Test empty string returns None."""
        result = safe_split_to_list("")
        assert result is None

    def test_none_input(self):
        """Test None input returns None."""
        result = safe_split_to_list(None)
        assert result is None

    def test_string_with_empty_items(self):
        """Test string with empty items filters them out."""
        result = safe_split_to_list("one,,three")
        assert result == ["one", "three"]

    def test_all_empty_items(self):
        """Test string with all empty items returns None."""
        result = safe_split_to_list(",,,")
        assert result is None
