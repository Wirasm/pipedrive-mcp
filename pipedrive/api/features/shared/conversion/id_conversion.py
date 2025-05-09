from typing import Optional, Tuple


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