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
    sanitize_inputs
)
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("activities")
async def update_activity_in_pipedrive(
    ctx: Context,
    id: str,
    subject: Optional[str] = None,
    type: Optional[str] = None,
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
    participants: Optional[List[Dict[str, Any]]] = None
) -> str:
    """Updates an existing activity in Pipedrive CRM.

    This tool updates an activity with the specified attributes. Activities track
    tasks, calls, meetings, and other events in Pipedrive. You must provide the activity ID
    and at least one field to update.

    Format requirements:
    - id: Activity ID as a numeric string (e.g., "123")
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
    update_activity_in_pipedrive(
        id="123",
        subject="Updated call with client",
        due_date="2025-01-16",
        due_time="15:30",
        participants=[{"person_id": "123", "primary_flag": true}]
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        id: ID of the activity to update
        subject: Updated subject of the activity
        type: Updated type of the activity
        owner_id: Updated ID of the user who owns the activity
        deal_id: Updated ID of the deal linked to the activity
        lead_id: Updated UUID of the lead linked to the activity
        person_id: Updated ID of the person linked to the activity (NOTE: read-only field)
        org_id: Updated ID of the organization linked to the activity
        due_date: Updated due date in YYYY-MM-DD format
        due_time: Updated due time in HH:MM format (e.g., "14:30")
        duration: Updated duration in HH:MM format (e.g., "01:30") or seconds (e.g., "5400")
        busy: Updated busy flag (true/false)
        done: Updated done flag (true/false)
        note: Updated note for the activity
        location: Updated location as a string address or location object
        public_description: Updated public description of the activity
        priority: Updated priority as a numeric string (e.g., "1")
        participants: Updated list of participant objects with person_id

    Returns:
        JSON formatted response with the updated activity data or error message
    """
    # Log inputs
    logger.debug(
        f"Tool 'update_activity_in_pipedrive' ENTERED with raw args: "
        f"id='{id}', subject='{subject}', type='{type}'"
    )
    
    # Sanitize inputs - convert empty strings to None
    inputs = {
        "id": id,
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
    id_str = sanitized["id"]
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
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Convert activity ID string to integer
    activity_id, id_error = convert_id_string(id_str, "activity_id", "123")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)
    
    if activity_id is None:
        error_message = "Activity ID is required"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    # Process fields to update, converting values as needed
    update_fields = {}
    
    # Convert string IDs to integers
    owner_id_int, owner_error = convert_id_string(owner_id, "owner_id", "123")
    if owner_error:
        logger.error(owner_error)
        return format_tool_response(False, error_message=owner_error)
    if owner_id_int is not None:
        update_fields["owner_id"] = owner_id_int
    
    deal_id_int, deal_error = convert_id_string(deal_id, "deal_id", "123")
    if deal_error:
        logger.error(deal_error)
        return format_tool_response(False, error_message=deal_error)
    if deal_id_int is not None:
        update_fields["deal_id"] = deal_id_int
    
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
    
    if person_id_int is not None:
        update_fields["person_id"] = person_id_int
    
    org_id_int, org_error = convert_id_string(org_id, "org_id", "123")
    if org_error:
        logger.error(org_error)
        return format_tool_response(False, error_message=org_error)
    if org_id_int is not None:
        update_fields["org_id"] = org_id_int
    
    # Validate lead_id as UUID
    lead_id_uuid, lead_error = validate_uuid_string(
        lead_id, 
        "lead_id", 
        "123e4567-e89b-12d3-a456-426614174000"
    )
    if lead_error:
        logger.error(lead_error)
        return format_tool_response(False, error_message=lead_error)
    if lead_id_uuid is not None:
        update_fields["lead_id"] = lead_id_uuid
    
    # Validate date format
    if due_date is not None:
        validated_due_date, date_error = validate_date_string(
            due_date, 
            "due_date", 
            "YYYY-MM-DD",
            "2025-01-15"
        )
        if date_error:
            logger.error(date_error)
            return format_tool_response(False, error_message=date_error)
        update_fields["due_date"] = validated_due_date
    
    # Convert due_time to API format (HH:MM)
    if due_time is not None:
        validated_due_time, time_error = convert_to_api_time_format(due_time, "due_time")
        if time_error:
            logger.error(time_error)
            return format_tool_response(False, error_message=time_error)
        update_fields["due_time"] = validated_due_time
    
    # Convert duration to API format (HH:MM)
    if duration is not None:
        validated_duration, duration_error = convert_duration_to_api_format(duration, "duration")
        if duration_error:
            logger.error(duration_error)
            return format_tool_response(False, error_message=duration_error)
        update_fields["duration"] = validated_duration
    
    # Process location data
    if location_input is not None:
        location_obj, location_error = parse_location_data(location_input)
        if location_error:
            logger.error(location_error)
            return format_tool_response(False, error_message=location_error)
        update_fields["location"] = location_obj
    
    # Format participants data if provided
    if participants is not None:
        formatted_participants, participants_error = format_participants_data(participants)
        if participants_error:
            logger.error(participants_error)
            return format_tool_response(False, error_message=participants_error)
        update_fields["participants"] = formatted_participants
    
    # Convert priority string to integer
    if priority_str is not None:
        try:
            priority_int = int(priority_str)
            if priority_int < 0:
                error_message = f"Priority must be a positive integer. Example: '1'"
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
            update_fields["priority"] = priority_int
        except ValueError:
            error_message = f"Priority must be a numeric string. Example: '1'"
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
    
    # Add string fields if provided
    if subject is not None:
        update_fields["subject"] = subject
    if type is not None:
        update_fields["type"] = type
    if note is not None:
        update_fields["note"] = note
    if public_description is not None:
        update_fields["public_description"] = public_description
    
    # Add boolean fields if provided
    if busy is not None:
        update_fields["busy"] = busy
    if done is not None:
        update_fields["done"] = done
    
    # Ensure there's at least one field to update
    if not update_fields:
        error_message = "At least one field must be provided for updating an activity"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    try:
        # Validate updated fields with Pydantic model
        activity = Activity(id=activity_id, **update_fields)
        
        # Call the Pipedrive API to update the activity
        updated_activity = await pd_mcp_ctx.pipedrive_client.activities.update_activity(
            activity_id=activity_id,
            **update_fields
        )
        
        logger.info(f"Successfully updated activity with ID: {activity_id}")
        return format_tool_response(True, data=updated_activity)
        
    except ValidationError as e:
        logger.error(f"Validation error updating activity {activity_id}: {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(f"Pipedrive API error updating activity {activity_id}: {str(e)}")
        return format_tool_response(False, error_message=f"Pipedrive API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error updating activity {activity_id}: {str(e)}")
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")