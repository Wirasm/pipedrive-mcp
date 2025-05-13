from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("activities")
async def get_activity_types_from_pipedrive(
    ctx: Context,
):
    """Gets all activity types from Pipedrive CRM.

    This tool retrieves all available activity types that can be used when creating activities.

    args:
    ctx: Context
    """
    logger.info("Tool 'get_activity_types_from_pipedrive' ENTERED")
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    try:
        # Call the Pipedrive API to get activity types
        activity_types = await pd_mcp_ctx.pipedrive_client.activities.get_activity_types()
        
        if not activity_types:
            logger.warning("No activity types found")
            
        logger.info(f"Successfully retrieved {len(activity_types)} activity types")
        return format_tool_response(True, data=activity_types)
        
    except PipedriveAPIError as e:
        logger.error(f"Pipedrive API error getting activity types: {str(e)}")
        return format_tool_response(False, error_message=f"Pipedrive API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error getting activity types: {str(e)}")
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")