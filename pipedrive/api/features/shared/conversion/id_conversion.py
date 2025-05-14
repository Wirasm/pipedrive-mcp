import re
import uuid
from typing import Optional, Tuple, Union
from datetime import datetime, timedelta


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


def convert_to_api_time_format(time_str: Optional[str], field_name: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Convert various time formats to the API-expected format (HH:MM format).
    
    Handles conversions from:
    - HH:MM:SS -> HH:MM
    - HH:MM -> HH:MM (no change needed)
    - ISO datetime -> HH:MM
    
    Args:
        time_str: Time string to convert
        field_name: Name of the field for error messages
        
    Returns:
        Tuple of (converted_time, error_message)
        If conversion succeeds, error_message is None
        If conversion fails, converted_time is None and error_message contains the error
    """
    if time_str is None or not time_str.strip():
        return None, None
    
    time_str = time_str.strip()
    
    # Regular expression patterns for different formats
    time_pattern_hhmmss = r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$'  # HH:MM:SS
    time_pattern_hhmm = r'^([01]\d|2[0-3]):([0-5]\d)$'  # HH:MM
    iso_datetime_pattern = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:Z|[+-][0-9]{2}:[0-9]{2})?$'
    
    # Check if it's already in HH:MM format
    if re.match(time_pattern_hhmm, time_str):
        return time_str, None
    
    # Check if it's in HH:MM:SS format and convert to HH:MM
    if re.match(time_pattern_hhmmss, time_str):
        return time_str[:5], None
    
    # Check if it's in ISO datetime format and extract HH:MM
    if re.match(iso_datetime_pattern, time_str):
        try:
            # Extract time part (HH:MM) from ISO format
            if 'T' in time_str:
                time_part = time_str.split('T')[1]
                if ':' in time_part:
                    return time_part[:5], None
        except Exception:
            pass
    
    # If we get here, format is not recognized
    return None, f"Invalid {field_name} format. Expected format: HH:MM, HH:MM:SS, or ISO datetime. Examples: '14:30', '14:30:00', '2025-01-15T14:30:00Z'"


def convert_duration_to_api_format(duration_str: Optional[str], field_name: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Convert various duration formats to the API-expected format (HH:MM).
    
    Handles conversions from:
    - HH:MM:SS -> HH:MM
    - HH:MM -> HH:MM (no change needed)
    - Seconds as integer or string -> HH:MM
    
    Args:
        duration_str: Duration string to convert
        field_name: Name of the field for error messages
        
    Returns:
        Tuple of (converted_duration, error_message)
        If conversion succeeds, error_message is None
        If conversion fails, converted_duration is None and error_message contains the error
    """
    if duration_str is None or not duration_str.strip():
        return None, None
    
    duration_str = duration_str.strip()
    
    # Regular expression patterns
    time_pattern_hhmmss = r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$'  # HH:MM:SS
    time_pattern_hhmm = r'^([01]\d|2[0-3]):([0-5]\d)$'  # HH:MM
    seconds_pattern = r'^\d+$'  # Integer seconds
    
    # Check if it's already in HH:MM format
    if re.match(time_pattern_hhmm, duration_str):
        return duration_str, None
    
    # Check if it's in HH:MM:SS format
    if re.match(time_pattern_hhmmss, duration_str):
        return duration_str[:5], None
    
    # Check if it's seconds as an integer
    if re.match(seconds_pattern, duration_str):
        try:
            # Convert seconds to HH:MM format
            seconds = int(duration_str)
            hours, remainder = divmod(seconds, 3600)
            minutes = remainder // 60
            
            # Format as HH:MM
            return f"{hours:02d}:{minutes:02d}", None
        except ValueError:
            pass
    
    # If we get here, format is not recognized
    return None, f"Invalid {field_name} format. Expected formats: HH:MM, HH:MM:SS, or seconds as integer. Examples: '01:30', '01:30:00', '5400'"


def parse_location_data(location: Optional[Union[str, dict]], field_name: str = "location") -> Tuple[Optional[dict], Optional[str]]:
    """
    Process location data into the format expected by the Pipedrive API.
    
    The Pipedrive API expects location as an object, but users might provide:
    - A string (address)
    - A dictionary with properly formatted location data
    
    Args:
        location: Location data as string or dict
        field_name: Name of the field for error messages
        
    Returns:
        Tuple of (location_dict, error_message)
        If processing succeeds, error_message is None
        If processing fails, location_dict is None and error_message contains the error
    """
    if location is None:
        return None, None
    
    # If it's already a dictionary, validate it has required keys
    if isinstance(location, dict):
        # Minimal validation - could be expanded based on API requirements
        return location, None
    
    # If it's a string, convert to the expected format
    if isinstance(location, str) and location.strip():
        # For string addresses, convert to the format expected by Pipedrive
        # Simple implementation - just put the string in a value field
        return {"value": location.strip()}, None
    
    # Empty string or invalid type
    return None, f"Invalid {field_name} format. Expected formats: string address or location object. Example: '123 Main St, City' or {{ 'value': '123 Main St, City' }}"


def format_participants_data(participants_data: Optional[list], field_name: str = "participants") -> Tuple[Optional[list], Optional[str]]:
    """
    Format participants data into the structure expected by the Pipedrive API.
    
    Args:
        participants_data: List of participant data
        field_name: Name of the field for error messages
        
    Returns:
        Tuple of (formatted_participants, error_message)
        If formatting succeeds, error_message is None
        If formatting fails, formatted_participants is None and error_message contains the error
    """
    if participants_data is None:
        return None, None
    
    if not isinstance(participants_data, list):
        return None, f"{field_name} must be a list of participant objects with person_id. Example: [{{ 'person_id': 123, 'primary_flag': true }}]"
    
    formatted_participants = []
    
    for i, participant in enumerate(participants_data):
        if not isinstance(participant, dict):
            return None, f"Each participant must be an object. Invalid participant at position {i}"
        
        # Check for required person_id
        if 'person_id' not in participant:
            return None, f"Each participant must have a 'person_id' field. Missing in participant at position {i}"
        
        # Convert person_id to integer if it's a string
        if isinstance(participant['person_id'], str):
            try:
                person_id = int(participant['person_id'])
                if person_id <= 0:
                    return None, f"person_id must be a positive integer in participant at position {i}"
                
                # Create a new dict with the integer person_id
                formatted_participant = dict(participant)
                formatted_participant['person_id'] = person_id
                formatted_participants.append(formatted_participant)
            except ValueError:
                return None, f"person_id must be a numeric value in participant at position {i}"
        else:
            # If it's already an integer, just validate it's positive
            if not isinstance(participant['person_id'], int) or participant['person_id'] <= 0:
                return None, f"person_id must be a positive integer in participant at position {i}"
            
            formatted_participants.append(participant)
    
    return formatted_participants, None