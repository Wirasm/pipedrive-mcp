import json
from typing import Any, List, Optional
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
