from typing import Dict, Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.activities.models.activity import Activity
from pipedrive.api.features.shared.conversion.id_conversion import (
    convert_id_string, 
    validate_uuid_string,
    validate_date_string,
    validate_time_string
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
    location: Optional[str] = None,
    public_description: Optional[str] = None,
    priority: Optional[str] = None,
) -> str:
    """Creates a new activity in Pipedrive CRM.

    This tool creates a new activity with the specified attributes. Activities track
    tasks, calls, meetings, and other events in Pipedrive. The subject and type
    fields are required, while all other parameters are optional.

    Format requirements:
    - owner_id, deal_id, org_id: Must be numeric strings (e.g., "123")
    - lead_id: Must be a UUID string (e.g., "123e4567-e89b-12d3-a456-426614174000")
    - due_date: Must be in YYYY-MM-DD format (e.g., "2025-01-15")
    - due_time: IMPORTANT - The API expects ISO datetime format with timezone (e.g., "2025-01-15T14:30:00Z")
    - duration: IMPORTANT - The API expects duration in seconds as an integer string (e.g., "3600" for 1 hour)
    - busy, done: Boolean values as lowercase true or false
    - priority: Must be a numeric string (e.g., "1")
    - person_id: NOTE - This is a read-only field. To associate a person, you must use the participants parameter.

    Example:
    ```
    create_activity_in_pipedrive(
        subject="Call with client",
        type="call",
        owner_id="123",
        due_date="2025-01-15",
        due_time="2025-01-15T14:30:00Z",
        duration="3600",
        busy=true
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
        due_time: Due time in ISO datetime format with timezone (e.g., "2025-01-15T14:30:00Z")
        duration: Duration in seconds as a numeric string (e.g., "3600" for 1 hour)
        busy: Whether the activity marks the assignee as busy (true/false)
        done: Whether the activity is marked as done (true/false)
        note: Additional notes for the activity
        location: Location of the activity as a string
        public_description: Public description of the activity
        priority: Priority of the activity as a numeric string (e.g., "1")

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
    location = sanitized["location"]
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
    if person_id:
        logger.warning("Note: 'person_id' is a read-only field in the Pipedrive API. "
                    "To associate a person with an activity, you should use participants instead. "
                    "The person_id might not be set as expected.")
    
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
    
    # Validate due_time format (ISO datetime)
    if due_time:
        # Simple ISO datetime validation (full validation would be more complex)
        iso_pattern = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$'
        if not re.match(iso_pattern, due_time):
            error_message = f"due_time must be in ISO datetime format with timezone. Example: '2025-01-15T14:30:00Z'"
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
        validated_due_time = due_time
    else:
        validated_due_time = None
    
    # Validate duration (seconds as a string)
    if duration:
        try:
            duration_int = int(duration)
            if duration_int < 0:
                error_message = f"duration must be a positive integer representing seconds. Example: '3600' for 1 hour"
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
            validated_duration = duration
        except ValueError:
            error_message = f"duration must be a numeric string representing seconds. Example: '3600' for 1 hour"
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
    else:
        validated_duration = None
    
    # Convert priority string to integer
    priority_int = None
    if priority:
        try:
            priority_int = int(priority)
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
            location=location,
            public_description=public_description,
            priority=priority_int
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