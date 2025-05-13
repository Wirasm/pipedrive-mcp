from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.leads.models.lead import Lead
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string, validate_uuid_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("update_lead_in_pipedrive")
async def update_lead_in_pipedrive(
    ctx: Context,
    lead_id: str,
    title: Optional[str] = None,
    value: Optional[str] = None,
    currency: Optional[str] = None,
    person_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    owner_id: Optional[str] = None,
    label_ids: Optional[str] = None,
    expected_close_date: Optional[str] = None,
    visible_to: Optional[str] = None,
    is_archived: Optional[str] = None,
    was_seen: Optional[str] = None,
) -> str:
    """
    Update an existing lead in Pipedrive.
    
    Args:
        lead_id: 
            The UUID of the lead to update.
            
        title: 
            The updated title of the lead.
            
        value: 
            The updated monetary value of the lead.
            
        currency: 
            Updated currency for the lead value.
            
        person_id: 
            Updated ID of the person to associate with this lead.
            
        organization_id: 
            Updated ID of the organization to associate with this lead.
            
        owner_id: 
            Updated ID of the user who will be the owner of the lead.
            
        label_ids: 
            Updated comma-separated list of lead label IDs to apply.
            
        expected_close_date: 
            Updated expected close date in ISO format (YYYY-MM-DD).
            
        visible_to: 
            Updated visibility setting (1, 3, 5, or 7).
            
        is_archived: 
            Whether the lead is archived ("true" or "false").
            
        was_seen: 
            Whether the lead was seen ("true" or "false").
    
    Returns:
        JSON response with updated lead details or error information.
    """
    logger.info(f"Updating lead with ID: {lead_id}")
    
    # Validate UUID format
    validated_uuid, error = validate_uuid_string(lead_id, "lead_id")
    if error:
        return format_tool_response(False, error_message=error)
    
    # Convert string parameters to appropriate types
    person_id_int = None
    if person_id is not None:
        person_id_int, error = convert_id_string(person_id, "person_id")
        if error:
            return format_tool_response(False, error_message=error)
    
    organization_id_int = None
    if organization_id is not None:
        organization_id_int, error = convert_id_string(organization_id, "organization_id")
        if error:
            return format_tool_response(False, error_message=error)
    
    owner_id_int = None
    if owner_id is not None:
        owner_id_int, error = convert_id_string(owner_id, "owner_id")
        if error:
            return format_tool_response(False, error_message=error)
    
    visible_to_int = None
    if visible_to is not None:
        visible_to_int, error = convert_id_string(visible_to, "visible_to")
        if error:
            return format_tool_response(False, error_message=error)
    
    # Convert value to float if provided
    value_float = None
    if value is not None:
        try:
            value_float = float(value)
        except ValueError:
            return format_tool_response(
                False, 
                error_message=f"Invalid value format: {value}. Must be a valid number."
            )
    
    # Convert boolean parameters
    is_archived_bool = None
    if is_archived is not None:
        is_archived_bool = is_archived.lower() == "true"
    
    was_seen_bool = None
    if was_seen is not None:
        was_seen_bool = was_seen.lower() == "true"
    
    # Handle label_ids as a list
    label_ids_list = None
    if label_ids is not None:
        label_ids_list = safe_split_to_list(label_ids)
    
    # Check that at least one field is provided for update
    if all(param is None for param in [
        title, value, currency, person_id, organization_id, owner_id,
        label_ids, expected_close_date, visible_to, is_archived, was_seen
    ]):
        return format_tool_response(
            False, 
            error_message="At least one field must be provided for update"
        )
    
    try:
        # Use the Pipedrive client from the context
        pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
        client = pd_mcp_ctx.pipedrive_client
        
        try:
            updated_lead = await client.lead_client.update_lead(
                lead_id=validated_uuid,
                title=title,
                amount=value_float,
                currency=currency,
                person_id=person_id_int,
                organization_id=organization_id_int,
                owner_id=owner_id_int,
                label_ids=label_ids_list,
                expected_close_date=expected_close_date,
                visible_to=visible_to_int,
                is_archived=is_archived_bool,
                was_seen=was_seen_bool,
            )
            
            if not updated_lead:
                return format_tool_response(
                    False,
                    error_message=f"Lead with ID {lead_id} not found or could not be updated"
                )
            
            # Create a Lead model from the response for consistent formatting
            updated_lead_model = Lead.from_api_dict(updated_lead)
            
            return format_tool_response(True, data=updated_lead_model.model_dump())
            
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
        logger.error(f"Error updating lead: {str(e)}")
        return format_tool_response(False, error_message=f"Failed to update lead: {str(e)}")