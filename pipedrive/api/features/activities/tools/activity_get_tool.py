from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("activities")
async def get_activity_from_pipedrive(
    ctx: Context,
    id_str: str,
    include_fields_str: Optional[str] = None
):
    """Gets activity details from Pipedrive CRM.

    This tool retrieves the details of a specific activity.

    args:
    ctx: Context
    id_str: str - The ID of the activity to retrieve
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include (e.g., "attendees")
    """
    logger.info(f"Tool 'get_activity_from_pipedrive' ENTERED with raw args: id_str='{id_str}'")
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Convert activity ID string to integer with proper error handling
    activity_id, id_error = convert_id_string(id_str, "activity_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)
    
    if activity_id is None:
        error_message = "Activity ID is required"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    # Parse include_fields_str to list if provided
    include_fields = safe_split_to_list(include_fields_str)
    
    try:
        # Call the Pipedrive API to get the activity
        activity_data = await pd_mcp_ctx.pipedrive_client.activities.get_activity(
            activity_id=activity_id,
            include_fields=include_fields
        )
        
        if not activity_data:
            error_message = f"Activity with ID {activity_id} not found"
            logger.warning(error_message)
            return format_tool_response(False, error_message=error_message)
        
        logger.info(f"Successfully retrieved activity with ID: {activity_id}")
        return format_tool_response(True, data=activity_data)
        
    except PipedriveAPIError as e:
        logger.error(f"Pipedrive API error getting activity {activity_id}: {str(e)}")
        return format_tool_response(False, error_message=f"Pipedrive API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error getting activity {activity_id}: {str(e)}")
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")