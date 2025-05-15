from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, sanitize_inputs
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("activities")
async def delete_activity_from_pipedrive(
    ctx: Context,
    id: str
) -> str:
    """Deletes an activity from Pipedrive CRM.

    This tool marks an activity as deleted in Pipedrive. After deletion, the activity
    will no longer appear in normal API responses, but it remains in the Pipedrive
    database for 30 days before being permanently deleted.

    Format requirements:
    - id: Activity ID as a numeric string (e.g., "123")

    Example:
    ```
    delete_activity_from_pipedrive(
        id="123"
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        id: ID of the activity to delete

    Returns:
        JSON formatted response with the result of the delete operation
    """
    logger.info(f"Tool 'delete_activity_from_pipedrive' ENTERED with raw args: id='{id}'")
    
    # Sanitize inputs
    inputs = {"id": id}
    sanitized = sanitize_inputs(inputs)
    id_str = sanitized["id"]
    
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
    
    try:
        # Call the Pipedrive API to delete the activity
        result = await pd_mcp_ctx.pipedrive_client.activities.delete_activity(
            activity_id=activity_id
        )
        
        # Check if the deletion was successful
        if result.get("id") == activity_id:
            logger.info(f"Successfully deleted activity with ID: {activity_id}")
            return format_tool_response(True, data={"id": activity_id, "success": True})
        else:
            logger.warning(f"Delete activity operation returned unexpected result: {result}")
            return format_tool_response(False, error_message="Delete operation returned unexpected result", data=result)
        
    except PipedriveAPIError as e:
        logger.error(f"Pipedrive API error deleting activity {activity_id}: {str(e)}")
        return format_tool_response(False, error_message=f"Pipedrive API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error deleting activity {activity_id}: {str(e)}")
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")