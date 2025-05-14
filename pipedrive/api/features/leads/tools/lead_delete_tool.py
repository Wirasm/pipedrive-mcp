from typing import Any, Dict, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import validate_uuid_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("leads")
async def delete_lead_from_pipedrive(
    ctx: Context,
    lead_id: str,
) -> str:
    """Permanently deletes a lead from Pipedrive.
    
    This tool removes a lead completely from your Pipedrive account. This action cannot be
    undone, so use with caution. The lead will be permanently removed along with all its
    associated data.
    
    Format requirements:
        - lead_id: Required UUID of the lead to delete, in standard UUID format
          (example: "adf21080-0e10-11eb-879b-05d71fb426ec")
    
    Example:
        delete_lead_from_pipedrive(
            lead_id="adf21080-0e10-11eb-879b-05d71fb426ec"
        )
    
    Args:
        ctx: Context object containing the Pipedrive client
        lead_id: The UUID of the lead to delete
    
    Returns:
        JSON string containing success status and deletion confirmation or error message.
    """
    logger.debug(f"Tool 'delete_lead_from_pipedrive' ENTERED with lead_id: '{lead_id}'")
    
    # Validate required field
    if not lead_id or not lead_id.strip():
        error_msg = "Lead ID is required and cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    # Validate UUID format
    validated_uuid, error = validate_uuid_string(lead_id, "lead_id")
    if error:
        logger.error(f"Invalid lead_id format: {error}")
        return format_tool_response(
            False, 
            error_message=f"Invalid lead_id format: {error}. Lead ID must be a valid UUID."
        )
    
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
        logger.error(f"Validation error deleting lead with ID '{lead_id}': {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'delete_lead_from_pipedrive' for ID '{lead_id}': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        # Handle other errors
        logger.exception(
            f"Unexpected error in tool 'delete_lead_from_pipedrive' for ID '{lead_id}': {str(e)}"
        )
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")