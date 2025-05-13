import re
import uuid
from typing import Optional, Tuple, Union


def convert_id_string(id_str: Optional[str], field_name: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Convert a string ID to an integer, with error handling.
    
    Args:
        id_str: String ID to convert
        field_name: Name of the field for error messages
        
    Returns:
        Tuple of (converted_id, error_message)
        If conversion succeeds, error_message is None
        If conversion fails, converted_id is None and error_message contains the error
    """
    if id_str is None or not id_str.strip():
        return None, None
        
    try:
        return int(id_str), None
    except ValueError:
        return None, f"Invalid {field_name} format: '{id_str}'. Must be an integer string."


def validate_uuid_string(uuid_str: Optional[str], field_name: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Validate a string as a valid UUID, with error handling.
    
    Args:
        uuid_str: String UUID to validate
        field_name: Name of the field for error messages
        
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
            return None, f"Invalid {field_name} format: '{uuid_str}'. Must be a valid UUID string."
        
        # Then validate with the uuid module for completeness
        uuid_obj = uuid.UUID(uuid_str)
        return str(uuid_obj), None
    except ValueError:
        return None, f"Invalid {field_name} format: '{uuid_str}'. Must be a valid UUID string."