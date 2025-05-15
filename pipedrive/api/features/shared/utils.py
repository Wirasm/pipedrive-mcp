import json
from typing import Any, Dict, List, Optional
from datetime import date, datetime


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that can handle dates and datetimes."""
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


def format_tool_response(
    success: bool, data: Optional[Any] = None, error_message: Optional[str] = None
) -> str:
    """
    Format a consistent JSON response for tool results.
    
    Args:
        success: Whether the operation was successful
        data: The data to return on success
        error_message: The error message to return on failure
        
    Returns:
        JSON formatted string with success status and data or error
    """
    return json.dumps(
        {"success": success, "data": data, "error": error_message}, 
        indent=2,
        cls=DateTimeEncoder
    )


def safe_split_to_list(comma_separated_string: Optional[str]) -> Optional[List[str]]:
    """
    Safely convert a comma-separated string to a list of strings.
    
    Args:
        comma_separated_string: A comma-separated string, or None
        
    Returns:
        A list of strings, or None if the input is None or empty
    """
    if not comma_separated_string:
        return None
        
    # Split by comma and strip whitespace
    result = [item.strip() for item in comma_separated_string.split(",") if item.strip()]
    
    # Return None if the result is an empty list
    return result if result else None


def format_validation_error(
    field_name: str, value: str, expected_format: str, example: str
) -> str:
    """
    Create a consistent validation error message with example.
    
    Args:
        field_name: Name of the field that failed validation
        value: The invalid value provided
        expected_format: Description of the expected format
        example: Example of valid value
        
    Returns:
        Formatted error message
    """
    return f"Invalid {field_name} format: '{value}'. {expected_format} Example: '{example}'"


def sanitize_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize input strings by converting empty strings to None.
    
    Args:
        inputs: Dictionary of input parameters
        
    Returns:
        Dictionary with sanitized inputs
    """
    sanitized = {}
    for key, value in inputs.items():
        if isinstance(value, str) and value.strip() == "":
            sanitized[key] = None
        else:
            sanitized[key] = value
    return sanitized


def bool_to_lowercase_str(value: Optional[bool]) -> Optional[str]:
    """
    Convert a boolean value to a lowercase string 'true' or 'false'.
    
    Args:
        value: Boolean value to convert
        
    Returns:
        String 'true' or 'false', or None if input is None
    """
    if value is None:
        return None
    return str(value).lower()
