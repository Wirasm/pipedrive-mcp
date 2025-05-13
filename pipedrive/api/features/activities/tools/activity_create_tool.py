from typing import Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.activities.models.activity import Activity
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string, validate_uuid_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("activities")
async def create_activity_in_pipedrive(
    ctx: Context,
    subject: str,
    type: str,
    owner_id_str: Optional[str] = None,
    deal_id_str: Optional[str] = None,
    lead_id_str: Optional[str] = None,
    person_id_str: Optional[str] = None,
    org_id_str: Optional[str] = None,
    due_date: Optional[str] = None,
    due_time: Optional[str] = None,
    duration: Optional[str] = None,
    busy: Optional[bool] = None,
    done: Optional[bool] = None,
    note: Optional[str] = None,
    location: Optional[str] = None,
    public_description: Optional[str] = None,
    priority_str: Optional[str] = None,
):
    """Creates a new activity in Pipedrive CRM.

    This tool creates a new activity with the specified attributes.

    args:
    ctx: Context
    subject: str - The subject of the activity
    type: str - The type of the activity (must match a valid activity type key_string)
    owner_id_str: Optional[str] = None - The ID of the user who owns the activity
    deal_id_str: Optional[str] = None - The ID of the deal linked to the activity
    lead_id_str: Optional[str] = None - The ID of the lead linked to the activity
    person_id_str: Optional[str] = None - The ID of the person linked to the activity
    org_id_str: Optional[str] = None - The ID of the organization linked to the activity
    due_date: Optional[str] = None - The due date in YYYY-MM-DD format
    due_time: Optional[str] = None - The due time in HH:MM:SS format
    duration: Optional[str] = None - The duration in HH:MM:SS format
    busy: Optional[bool] = None - Whether the activity marks the assignee as busy
    done: Optional[bool] = None - Whether the activity is marked as done
    note: Optional[str] = None - Note for the activity
    location: Optional[str] = None - Location of the activity
    public_description: Optional[str] = None - Public description of the activity
    priority_str: Optional[str] = None - Priority of the activity (numeric)
    """
    # Log inputs with appropriate redaction of sensitive data
    logger.debug(
        f"Tool 'create_activity_in_pipedrive' ENTERED with raw args: "
        f"subject='{subject}', type='{type}', "
        f"due_date='{due_date}', due_time='{due_time}', duration='{duration}'"
    )

    # Sanitize empty strings to None
    subject = subject.strip() if subject else subject
    type = type.strip() if type else type
    owner_id_str = None if owner_id_str == "" else owner_id_str
    deal_id_str = None if deal_id_str == "" else deal_id_str
    lead_id_str = None if lead_id_str == "" else lead_id_str
    person_id_str = None if person_id_str == "" else person_id_str
    org_id_str = None if org_id_str == "" else org_id_str
    due_date = None if due_date == "" else due_date
    due_time = None if due_time == "" else due_time
    duration = None if duration == "" else duration
    note = None if note == "" else note
    location = None if location == "" else location
    public_description = None if public_description == "" else public_description
    priority_str = None if priority_str == "" else priority_str
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Convert string IDs to integers with proper error handling
    owner_id, owner_error = convert_id_string(owner_id_str, "owner_id")
    if owner_error:
        logger.error(owner_error)
        return format_tool_response(False, error_message=owner_error)
    
    deal_id, deal_error = convert_id_string(deal_id_str, "deal_id")
    if deal_error:
        logger.error(deal_error)
        return format_tool_response(False, error_message=deal_error)
    
    person_id, person_error = convert_id_string(person_id_str, "person_id")
    if person_error:
        logger.error(person_error)
        return format_tool_response(False, error_message=person_error)
    
    org_id, org_error = convert_id_string(org_id_str, "org_id")
    if org_error:
        logger.error(org_error)
        return format_tool_response(False, error_message=org_error)
    
    # Validate lead_id as UUID
    lead_id, lead_error = validate_uuid_string(lead_id_str, "lead_id")
    if lead_error:
        logger.error(lead_error)
        return format_tool_response(False, error_message=lead_error)
    
    # Convert priority string to integer
    priority = None
    if priority_str:
        try:
            priority = int(priority_str)
        except ValueError:
            error_message = f"Invalid priority format: '{priority_str}'. Must be a valid number."
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
    
    try:
        # Validate inputs with Pydantic model
        activity = Activity(
            subject=subject,
            type=type,
            owner_id=owner_id,
            deal_id=deal_id,
            lead_id=lead_id,
            person_id=person_id,
            org_id=org_id,
            due_date=due_date,
            due_time=due_time,
            duration=duration,
            busy=busy,
            done=done,
            note=note,
            location=location,
            public_description=public_description,
            priority=priority
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