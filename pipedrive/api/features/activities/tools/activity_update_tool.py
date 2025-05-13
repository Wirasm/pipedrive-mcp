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
async def update_activity_in_pipedrive(
    ctx: Context,
    id_str: str,
    subject: Optional[str] = None,
    type: Optional[str] = None,
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
    priority_str: Optional[str] = None
):
    """Updates an existing activity in Pipedrive CRM.

    This tool updates an activity with the specified attributes.

    args:
    ctx: Context
    id_str: str - The ID of the activity to update
    subject: Optional[str] = None - The subject of the activity
    type: Optional[str] = None - The type of the activity
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
    # Log inputs
    logger.debug(
        f"Tool 'update_activity_in_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', subject='{subject}', type='{type}'"
    )
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Convert activity ID string to integer
    activity_id, id_error = convert_id_string(id_str, "activity_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)
    
    if activity_id is None:
        error_message = "Activity ID is required"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    # Process fields to update, converting IDs where needed
    update_fields = {}
    
    # Convert string IDs to integers
    owner_id, owner_error = convert_id_string(owner_id_str, "owner_id")
    if owner_error:
        logger.error(owner_error)
        return format_tool_response(False, error_message=owner_error)
    if owner_id is not None:
        update_fields["owner_id"] = owner_id
    
    deal_id, deal_error = convert_id_string(deal_id_str, "deal_id")
    if deal_error:
        logger.error(deal_error)
        return format_tool_response(False, error_message=deal_error)
    if deal_id is not None:
        update_fields["deal_id"] = deal_id
    
    person_id, person_error = convert_id_string(person_id_str, "person_id")
    if person_error:
        logger.error(person_error)
        return format_tool_response(False, error_message=person_error)
    if person_id is not None:
        update_fields["person_id"] = person_id
    
    org_id, org_error = convert_id_string(org_id_str, "org_id")
    if org_error:
        logger.error(org_error)
        return format_tool_response(False, error_message=org_error)
    if org_id is not None:
        update_fields["org_id"] = org_id
    
    # Validate lead_id as UUID
    lead_id, lead_error = validate_uuid_string(lead_id_str, "lead_id")
    if lead_error:
        logger.error(lead_error)
        return format_tool_response(False, error_message=lead_error)
    if lead_id is not None:
        update_fields["lead_id"] = lead_id
    
    # Convert priority string to integer
    priority = None
    if priority_str:
        try:
            priority = int(priority_str)
            update_fields["priority"] = priority
        except ValueError:
            error_message = f"Invalid priority format: '{priority_str}'. Must be a valid number."
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
    
    # Add string fields if provided
    if subject is not None:
        update_fields["subject"] = subject
    if type is not None:
        update_fields["type"] = type
    if due_date is not None:
        update_fields["due_date"] = due_date
    if due_time is not None:
        update_fields["due_time"] = due_time
    if duration is not None:
        update_fields["duration"] = duration
    if note is not None:
        update_fields["note"] = note
    if location is not None:
        update_fields["location"] = location
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