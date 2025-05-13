from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("get_lead_sources_from_pipedrive")
async def get_lead_sources_from_pipedrive(ctx: Context) -> str:
    """
    Get all lead sources from Pipedrive.
    
    Returns:
        JSON response with a list of lead sources.
    """
    logger.info("Getting all lead sources from Pipedrive")
    
    try:
        # Use the Pipedrive client from the context
        pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
        client = pd_mcp_ctx.pipedrive_client
        
        try:
            sources = await client.lead_client.get_lead_sources()
            
            # Format the sources in a standardized way
            sources_data = []
            for source in sources:
                sources_data.append({
                    "name": source.get("name", ""),
                    # Add any other fields that might be present in the response
                })
            
            return format_tool_response(True, data=sources_data)
            
        except PipedriveAPIError as e:
            return format_tool_response(
                False, 
                error_message=f"Pipedrive API error: {str(e)}"
            )
            
    except Exception as e:
        # Handle errors
        logger.error(f"Error getting lead sources: {str(e)}")
        return format_tool_response(False, error_message=f"Failed to get lead sources: {str(e)}")