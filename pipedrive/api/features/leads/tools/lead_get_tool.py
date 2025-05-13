from typing import Any, Dict, Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.leads.models.lead import Lead
from pipedrive.api.features.shared.conversion.id_conversion import validate_uuid_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("get_lead_from_pipedrive")
async def get_lead_from_pipedrive(
    ctx: Context,
    lead_id: str,
) -> str:
    """
    Get a lead by ID from Pipedrive.
    
    Args:
        lead_id: 
            The UUID of the lead to retrieve.
    
    Returns:
        JSON response with lead details or error information.
    """
    logger.info(f"Getting lead with ID: {lead_id}")
    
    # Validate UUID format
    validated_uuid, error = validate_uuid_string(lead_id, "lead_id")
    if error:
        return format_tool_response(False, error_message=error)
    
    try:
        # Use the Pipedrive client from the context
        pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
        client = pd_mcp_ctx.pipedrive_client
        
        try:
            lead_data = await client.lead_client.get_lead(lead_id=validated_uuid)
            
            if not lead_data:
                return format_tool_response(
                    False,
                    error_message=f"Lead with ID {lead_id} not found"
                )
            
            # Create a Lead model from the response for consistent formatting
            lead_model = Lead.from_api_dict(lead_data)
            
            return format_tool_response(True, data=lead_model.model_dump())
            
        except PipedriveAPIError as e:
            return format_tool_response(
                False, 
                error_message=f"Pipedrive API error: {str(e)}"
            )
            
    except ValidationError as e:
        # Handle validation errors
        return format_tool_response(False, error_message=str(e))
    except Exception as e:
        # Handle other errors
        logger.error(f"Error getting lead: {str(e)}")
        return format_tool_response(False, error_message=f"Failed to get lead: {str(e)}")