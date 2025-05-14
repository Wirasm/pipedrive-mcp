from typing import Optional, List

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list, sanitize_inputs
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("activities")
async def get_activity_from_pipedrive(
    ctx: Context,
    id: str,
    include_fields: Optional[str] = None
) -> str:
    """Gets activity details from Pipedrive CRM.

    This tool retrieves the detailed information of a specific activity from Pipedrive.
    It returns all fields of the activity record, including the current status, related
    entities, and scheduling information.

    Format requirements:
    - id: Activity ID as a numeric string (e.g., "123")
    - include_fields: Optional comma-separated list of additional fields to include
      (e.g., "attendees")

    Example:
    ```
    get_activity_from_pipedrive(
        id="123",
        include_fields="attendees"
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        id: ID of the activity to retrieve
        include_fields: Optional comma-separated list of additional fields to include

    Returns:
        JSON formatted response with the activity data or error message
    """
    logger.info(f"Tool 'get_activity_from_pipedrive' ENTERED with raw args: id='{id}'")
    
    # Sanitize inputs
    inputs = {"id": id, "include_fields": include_fields}
    sanitized = sanitize_inputs(inputs)
    id_str = sanitized["id"]
    include_fields_str = sanitized["include_fields"]
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Convert activity ID string to integer with proper error handling
    activity_id, id_error = convert_id_string(id_str, "activity_id", "123")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)
    
    if activity_id is None:
        error_message = "Activity ID is required"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    # Parse include_fields_str to list if provided
    include_fields_list = safe_split_to_list(include_fields_str)
    
    try:
        # Call the Pipedrive API to get the activity
        activity_data = await pd_mcp_ctx.pipedrive_client.activities.get_activity(
            activity_id=activity_id,
            include_fields=include_fields_list
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