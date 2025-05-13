from typing import Any, Dict, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import validate_uuid_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("delete_lead_from_pipedrive")
async def delete_lead_from_pipedrive(
    ctx: Context,
    lead_id: str,
) -> str:
    """
    Delete a lead from Pipedrive.
    
    Args:
        lead_id: 
            The UUID of the lead to delete.
    
    Returns:
        JSON response confirming deletion or error information.
    """
    logger.info(f"Deleting lead with ID: {lead_id}")
    
    # Validate UUID format
    validated_uuid, error = validate_uuid_string(lead_id, "lead_id")
    if error:
        return format_tool_response(False, error_message=error)
    
    try:
        # Use the Pipedrive client from the context
        pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
        client = pd_mcp_ctx.pipedrive_client
        
        try:
            result = await client.lead_client.delete_lead(lead_id=validated_uuid)
            
            # Check if deletion was successful
            if result and not result.get("error_details"):
                return format_tool_response(
                    True, 
                    data={"id": lead_id, "message": "Lead successfully deleted"}
                )
            else:
                return format_tool_response(
                    False,
                    error_message=f"Failed to delete lead with ID {lead_id}",
                    data=result.get("error_details")
                )
        
        except PipedriveAPIError as e:
            return format_tool_response(
                False, 
                error_message=f"Pipedrive API error: {str(e)}"
            )
            
    except ValueError as e:
        # Handle validation errors
        return format_tool_response(False, error_message=str(e))
    except Exception as e:
        # Handle other errors
        logger.error(f"Error deleting lead: {str(e)}")
        return format_tool_response(False, error_message=f"Failed to delete lead: {str(e)}")