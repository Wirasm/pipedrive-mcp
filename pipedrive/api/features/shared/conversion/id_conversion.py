import re
import uuid
from typing import Optional, Tuple, Union


def convert_id_string(id_str: Optional[str], field_name: str, 
                     example: str = "123") -> Tuple[Optional[int], Optional[str]]:
    """
    Convert a string ID to an integer, with improved error handling.
    
    Args:
        id_str: String ID to convert
        field_name: Name of the field for error messages
        example: Example of valid format for error message
        
    Returns:
        Tuple of (converted_id, error_message)
        If conversion succeeds, error_message is None
        If conversion fails, converted_id is None and error_message contains the error
    """
    if id_str is None or not id_str.strip():
        return None, None
        
    try:
        value = int(id_str)
        if value <= 0:
            return None, f"{field_name} must be a positive integer. Example: '{example}'"
        return value, None
    except ValueError:
        return None, f"{field_name} must be a numeric string. Example: '{example}'"


def validate_uuid_string(uuid_str: Optional[str], field_name: str, 
                        example: str = "123e4567-e89b-12d3-a456-426614174000") -> Tuple[Optional[str], Optional[str]]:
    """
    Validate a string as a valid UUID, with improved error handling.
    
    Args:
        uuid_str: String UUID to validate
        field_name: Name of the field for error messages
        example: Example of valid format for error message
        
    Returns:
        Tuple of (validated_uuid, error_message)
        If validation succeeds, error_message is None
        If validation fails, validated_uuid is None and error_message contains the error
    """
    if uuid_str is None or not uuid_str.strip():
        return None, None
    
    # UUID pattern (RFC 4122)
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    
    try:
        # First check with regex for performance
        if not re.match(uuid_pattern, uuid_str.lower()):
            return None, f"{field_name} must be a valid UUID string. Example: '{example}'"
        
        # Then validate with the uuid module for completeness
        uuid_obj = uuid.UUID(uuid_str)
        return str(uuid_obj), None
    except ValueError:
        return None, f"{field_name} must be a valid UUID string. Example: '{example}'"


def validate_date_string(date_str: Optional[str], field_name: str, 
                        expected_format: str = "YYYY-MM-DD",
                        example: str = "2025-01-15") -> Tuple[Optional[str], Optional[str]]:
    """
    Validate a string as a valid date, with improved error handling.
    
    Args:
        date_str: String date to validate
        field_name: Name of the field for error messages
        expected_format: Description of the expected format
        example: Example of valid format for error message
        
    Returns:
        Tuple of (validated_date, error_message)
        If validation succeeds, error_message is None
        If validation fails, validated_date is None and error_message contains the error
    """
    if date_str is None or not date_str.strip():
        return None, None
    
    # ISO date pattern YYYY-MM-DD
    date_pattern = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
    
    if not re.match(date_pattern, date_str):
        return None, f"{field_name} must be in {expected_format} format. Example: '{example}'"
    
    # We don't need more validation - Pydantic models will validate the date further if needed
    return date_str, None


def validate_time_string(time_str: Optional[str], field_name: str,
                        expected_format: str = "HH:MM:SS",
                        example: str = "14:30:00") -> Tuple[Optional[str], Optional[str]]:
    """
    Validate a string as a valid time, with improved error handling.
    
    Args:
        time_str: String time to validate
        field_name: Name of the field for error messages
        expected_format: Description of the expected format
        example: Example of valid format for error message
        
    Returns:
        Tuple of (validated_time, error_message)
        If validation succeeds, error_message is None
        If validation fails, validated_time is None and error_message contains the error
    """
    if time_str is None or not time_str.strip():
        return None, None
    
    # HH:MM:SS pattern
    time_pattern = r'^[0-9]{2}:[0-9]{2}:[0-9]{2}$'
    
    if not re.match(time_pattern, time_str):
        return None, f"{field_name} must be in {expected_format} format. Example: '{example}'"
    
    # Split by : to validate hour, minute, second ranges
    try:
        hours, minutes, seconds = map(int, time_str.split(':'))
        if not (0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
            return None, f"{field_name} contains invalid values. Hours (0-23), minutes (0-59), seconds (0-59). Example: '{example}'"
    except ValueError:
        return None, f"{field_name} must be in {expected_format} format. Example: '{example}'"
    
    return time_str, None