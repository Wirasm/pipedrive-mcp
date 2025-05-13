from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.leads.models.lead_label import LeadLabel
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("get_lead_labels_from_pipedrive")
async def get_lead_labels_from_pipedrive(ctx: Context) -> str:
    """
    Get all lead labels from Pipedrive.
    
    Returns:
        JSON response with a list of lead labels.
    """
    logger.info("Getting all lead labels from Pipedrive")
    
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
            
    except Exception as e:
        # Handle errors
        logger.error(f"Error getting lead labels: {str(e)}")
        return format_tool_response(False, error_message=f"Failed to get lead labels: {str(e)}")