import re
from typing import Dict, Optional, List, Any, Union

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.activities.models.activity import Activity
from pipedrive.api.features.shared.conversion.id_conversion import (
    convert_id_string, 
    validate_uuid_string,
    validate_date_string,
    convert_to_api_time_format,
    convert_duration_to_api_format,
    parse_location_data,
    format_participants_data
)
from pipedrive.api.features.shared.utils import (
    format_tool_response,
    format_validation_error,
    sanitize_inputs,
    bool_to_lowercase_str
)
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("activities")
async def create_activity_in_pipedrive(
    ctx: Context,
    subject: str,
    type: str,
    owner_id: Optional[str] = None,
    deal_id: Optional[str] = None,
    lead_id: Optional[str] = None,
    person_id: Optional[str] = None,
    org_id: Optional[str] = None,
    due_date: Optional[str] = None,
    due_time: Optional[str] = None,
    duration: Optional[str] = None,
    busy: Optional[bool] = None,
    done: Optional[bool] = None,
    note: Optional[str] = None,
    location: Optional[Union[str, Dict[str, Any]]] = None,
    public_description: Optional[str] = None,
    priority: Optional[str] = None,
    participants: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Creates a new activity in Pipedrive CRM.

    This tool creates a new activity with the specified attributes. Activities track
    tasks, calls, meetings, and other events in Pipedrive. The subject and type
    fields are required, while all other parameters are optional.

    Format requirements:
    - owner_id, deal_id, org_id: Must be numeric strings (e.g., "123")
    - lead_id: Must be a UUID string (e.g., "123e4567-e89b-12d3-a456-426614174000")
    - due_date: Must be in YYYY-MM-DD format (e.g., "2025-01-15")
    - due_time: Must be in HH:MM format (e.g., "14:30"). Also accepts HH:MM:SS format or
      ISO datetime, which will be converted to HH:MM.
    - duration: Must be in HH:MM format (e.g., "01:30"). Also accepts HH:MM:SS format or
      seconds as a numeric string (e.g., "5400"), which will be converted to HH:MM.
    - location: Can be a string address or a location object (e.g., {"value": "123 Main St"})
    - participants: List of participant objects with person_id for associating persons
      (e.g., [{"person_id": 123, "primary_flag": true}])
    - person_id: NOTE - This is a read-only field. To associate a person, you MUST use
      the participants parameter instead.

    Example:
    ```
    create_activity_in_pipedrive(
        subject="Call with client",
        type="call",
        owner_id="123",
        due_date="2025-01-15",
        due_time="14:30",
        duration="01:30",
        busy=true,
        participants=[{"person_id": "123", "primary_flag": true}],
        location="123 Main St, City"
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        subject: The subject or title of the activity
        type: The type of activity (must match a valid activity type key)
        owner_id: Numeric ID of the user who owns the activity
        deal_id: Numeric ID of the deal linked to the activity
        lead_id: UUID string of the lead linked to the activity
        person_id: Numeric ID of the person linked to the activity (NOTE: read-only field)
        org_id: Numeric ID of the organization linked to the activity
        due_date: Due date in YYYY-MM-DD format
        due_time: Due time in HH:MM format (e.g., "14:30")
        duration: Duration in HH:MM format (e.g., "01:30") or seconds (e.g., "5400")
        busy: Whether the activity marks the assignee as busy (true/false)
        done: Whether the activity is marked as done (true/false)
        note: Additional notes for the activity
        location: Location of the activity as a string or location object
        public_description: Public description of the activity
        priority: Priority of the activity as a numeric string (e.g., "1")
        participants: List of participant objects with person_id for associating persons

    Returns:
        JSON formatted response with the created activity data or error message
    """
    # Log inputs with appropriate redaction of sensitive data
    logger.debug(
        f"Tool 'create_activity_in_pipedrive' ENTERED with raw args: "
        f"subject='{subject}', type='{type}', "
        f"due_date='{due_date}', due_time='{due_time}', duration='{duration}'"
    )

    # Sanitize inputs - convert empty strings to None
    inputs = {
        "subject": subject,
        "type": type,
        "owner_id": owner_id,
        "deal_id": deal_id,
        "lead_id": lead_id,
        "person_id": person_id,
        "org_id": org_id,
        "due_date": due_date,
        "due_time": due_time,
        "duration": duration,
        "note": note,
        "location": location,
        "public_description": public_description,
        "priority": priority
    }
    
    sanitized = sanitize_inputs(inputs)
    subject = sanitized["subject"]
    type = sanitized["type"]
    owner_id = sanitized["owner_id"]
    deal_id = sanitized["deal_id"]
    lead_id = sanitized["lead_id"]
    person_id = sanitized["person_id"]
    org_id = sanitized["org_id"]
    due_date = sanitized["due_date"]
    due_time = sanitized["due_time"]
    duration = sanitized["duration"]
    note = sanitized["note"]
    location_input = sanitized["location"]
    public_description = sanitized["public_description"]
    priority_str = sanitized["priority"]
    
    # Trim strings
    if subject:
        subject = subject.strip()
    if type:
        type = type.strip()
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Validate required fields
    if not subject:
        error_message = "The 'subject' field is required and cannot be empty."
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
        
    if not type:
        error_message = "The 'type' field is required and cannot be empty."
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    # Convert string IDs to integers with proper error handling
    owner_id_int, owner_error = convert_id_string(owner_id, "owner_id", "123")
    if owner_error:
        logger.error(owner_error)
        return format_tool_response(False, error_message=owner_error)
    
    deal_id_int, deal_error = convert_id_string(deal_id, "deal_id", "123")
    if deal_error:
        logger.error(deal_error)
        return format_tool_response(False, error_message=deal_error)
    
    person_id_int, person_error = convert_id_string(person_id, "person_id", "123")
    if person_error:
        logger.error(person_error)
        return format_tool_response(False, error_message=person_error)
    
    # Add warning about person_id being read-only
    if person_id and not participants:
        warning_message = "NOTE: 'person_id' is a read-only field in the Pipedrive API. " \
                         "To associate a person with an activity, you MUST use the 'participants' parameter. " \
                         "Your provided person_id will be ignored by the API."
        logger.warning(warning_message)
        # We'll still include it in the payload, but warn the user it won't work
    
    org_id_int, org_error = convert_id_string(org_id, "org_id", "123")
    if org_error:
        logger.error(org_error)
        return format_tool_response(False, error_message=org_error)
    
    # Validate lead_id as UUID
    lead_id_uuid, lead_error = validate_uuid_string(
        lead_id, 
        "lead_id", 
        "123e4567-e89b-12d3-a456-426614174000"
    )
    if lead_error:
        logger.error(lead_error)
        return format_tool_response(False, error_message=lead_error)
    
    # Validate date format
    validated_due_date, date_error = validate_date_string(
        due_date, 
        "due_date", 
        "YYYY-MM-DD",
        "2025-01-15"
    )
    if date_error:
        logger.error(date_error)
        return format_tool_response(False, error_message=date_error)
    
    # Convert due_time to API format (HH:MM)
    validated_due_time, time_error = convert_to_api_time_format(due_time, "due_time")
    if time_error:
        logger.error(time_error)
        return format_tool_response(False, error_message=time_error)
    
    # Convert duration to API format (HH:MM)
    validated_duration, duration_error = convert_duration_to_api_format(duration, "duration")
    if duration_error:
        logger.error(duration_error)
        return format_tool_response(False, error_message=duration_error)
    
    # Process location data
    location_obj, location_error = parse_location_data(location_input)
    if location_error:
        logger.error(location_error)
        return format_tool_response(False, error_message=location_error)
    
    # Format participants data if provided
    formatted_participants, participants_error = format_participants_data(participants)
    if participants_error:
        logger.error(participants_error)
        return format_tool_response(False, error_message=participants_error)
    
    # Convert priority string to integer
    priority_int = None
    if priority_str:
        try:
            priority_int = int(priority_str)
            if priority_int < 0:
                error_message = f"Priority must be a positive integer. Example: '1'"
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
        except ValueError:
            error_message = f"Priority must be a numeric string. Example: '1'"
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
    
    try:
        # Validate inputs with Pydantic model
        activity = Activity(
            subject=subject,
            type=type,
            owner_id=owner_id_int,
            deal_id=deal_id_int,
            lead_id=lead_id_uuid,
            person_id=person_id_int,
            org_id=org_id_int,
            due_date=validated_due_date,
            due_time=validated_due_time,
            duration=validated_duration,
            busy=busy,
            done=done,
            note=note,
            location=location_obj,
            public_description=public_description,
            priority=priority_int,
            participants=formatted_participants
        )
        
        # Convert model to API-compatible dict
        payload = activity.to_api_dict()
        
        logger.debug(f"Prepared payload for activity creation: {payload}")
        
        # Call the Pipedrive API using the activities client
        created_activity = await pd_mcp_ctx.pipedrive_client.activities.create_activity(**payload)
        
        logger.info(
            f"Successfully created activity '{subject}' with ID: {created_activity.get('id')}"
        )
        
        # Return the API response
        return format_tool_response(True, data=created_activity)
        
    except ValidationError as e:
        logger.error(f"Validation error creating activity '{subject}': {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(f"Pipedrive API error creating activity '{subject}': {str(e)}")
        return format_tool_response(
            False, error_message=f"Pipedrive API error: {str(e)}"
        )
    except Exception as e:
        logger.error(
            f"Unexpected error creating activity '{subject}': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )