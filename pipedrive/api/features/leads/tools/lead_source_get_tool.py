from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("leads")
async def get_lead_sources_from_pipedrive(ctx: Context) -> str:
    """Retrieves all available lead source types from Pipedrive.
    
    This tool fetches the complete list of lead source categories configured in your Pipedrive
    account. Lead sources indicate where a lead originated from, such as "API", "Web forms", 
    "Import", etc. These are pre-defined values in Pipedrive and cannot be customized.
    
    Lead source information is useful for tracking and analyzing the effectiveness of
    different lead generation channels. All leads created through the Pipedrive API will
    automatically have the source "API" assigned to them.
    
    Example:
        get_lead_sources_from_pipedrive()
    
    Args:
        ctx: Context object containing the Pipedrive client
    
    Returns:
        JSON string containing success status with a list of lead sources, or error message.
        Each source contains a name property indicating the source type.
    """
    logger.debug("Tool 'get_lead_sources_from_pipedrive' ENTERED")
    
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
            
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'get_lead_sources_from_pipedrive': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        # Handle errors
        logger.exception(
            f"Unexpected error in tool 'get_lead_sources_from_pipedrive': {str(e)}"
        )
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")