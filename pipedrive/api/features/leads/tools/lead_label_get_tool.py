from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.leads.models.lead_label import LeadLabel
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("leads")
async def get_lead_labels_from_pipedrive(ctx: Context) -> str:
    """Retrieves all available lead labels from Pipedrive.
    
    This tool fetches the complete list of lead labels configured in your Pipedrive account.
    Lead labels are used to categorize and visually distinguish leads in Pipedrive. The labels
    include information about their name, color, and ID, which can be used when creating
    or updating leads.
    
    Common lead labels include "Hot", "Cold", and "Warm", but your account may have custom
    labels as well. The IDs of these labels can be used with the label_ids parameter in
    lead create and update operations.
    
    Example:
        get_lead_labels_from_pipedrive()
    
    Args:
        ctx: Context object containing the Pipedrive client
    
    Returns:
        JSON string containing success status with a list of lead labels, or error message.
        Each label contains id, name, color, and timestamp information.
    """
    logger.debug("Tool 'get_lead_labels_from_pipedrive' ENTERED")
    
    try:
        # Use the Pipedrive client from the context
        pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
        client = pd_mcp_ctx.pipedrive_client
        
        try:
            labels = await client.lead_client.get_lead_labels()
            
            # Convert each label to a LeadLabel model for consistent formatting
            labels_data = []
            for label_data in labels:
                try:
                    label_model = LeadLabel.from_api_dict(label_data)
                    labels_data.append(label_model.model_dump())
                except Exception as e:
                    logger.warning(f"Error processing lead label data: {str(e)}")
                    # Include the raw data if we can't parse it
                    labels_data.append(label_data)
            
            return format_tool_response(True, data=labels_data)
            
        except PipedriveAPIError as e:
            return format_tool_response(
                False, 
                error_message=f"Pipedrive API error: {str(e)}"
            )
            
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'get_lead_labels_from_pipedrive': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        # Handle errors
        logger.exception(
            f"Unexpected error in tool 'get_lead_labels_from_pipedrive': {str(e)}"
        )
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")