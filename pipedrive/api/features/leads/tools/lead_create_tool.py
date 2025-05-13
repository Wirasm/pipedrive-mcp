from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.leads.models.lead import Lead
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("create_lead_in_pipedrive")
async def create_lead_in_pipedrive(
    ctx: Context,
    title: str,
    value: Optional[str] = None,
    currency: str = "USD",
    person_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    owner_id: Optional[str] = None,
    label_ids: Optional[str] = None,
    expected_close_date: Optional[str] = None,
    visible_to: Optional[str] = None,
) -> str:
    """
    Create a new lead in Pipedrive.
    
    Args:
        title: 
            The title of the lead.
            
        value: 
            The monetary value of the lead.
            
        currency: 
            Currency for the lead value (default: USD).
            
        person_id: 
            The ID of the person to associate with this lead.
            
        organization_id: 
            The ID of the organization to associate with this lead.
            
        owner_id: 
            The ID of the user who will be the owner of the lead.
            
        label_ids: 
            Comma-separated list of lead label IDs to apply.
            
        expected_close_date: 
            The expected close date in ISO format (YYYY-MM-DD).
            
        visible_to: 
            Visibility setting (1 = Owner only, 3 = Entire company).
    
    Returns:
        JSON response with lead details or error information.
    """
    logger.info(f"Creating lead with title: {title}")
    
    # Convert value from string to float if provided
    value_float = None
    if value is not None:
        try:
            value_float = float(value)
        except ValueError:
            return format_tool_response(
                False, 
                error_message=f"Invalid value format: {value}. Must be a valid number."
            )
    
    # Convert string parameters to appropriate types
    person_id_int = None
    if person_id:
        person_id_int, error = convert_id_string(person_id, "person_id")
        if error:
            return format_tool_response(False, error_message=error)
    
    organization_id_int = None
    if organization_id:
        organization_id_int, error = convert_id_string(organization_id, "organization_id")
        if error:
            return format_tool_response(False, error_message=error)
    
    owner_id_int = None
    if owner_id:
        owner_id_int, error = convert_id_string(owner_id, "owner_id")
        if error:
            return format_tool_response(False, error_message=error)
    
    visible_to_int = None
    if visible_to:
        visible_to_int, error = convert_id_string(visible_to, "visible_to")
        if error:
            return format_tool_response(False, error_message=error)
            
    # Handle label_ids as a list
    label_ids_list = None
    if label_ids:
        label_ids_list = safe_split_to_list(label_ids)
    
    # Check that either person_id or organization_id is provided
    if not person_id_int and not organization_id_int:
        return format_tool_response(
            False, 
            error_message="Either person_id or organization_id must be provided"
        )
    
    try:
        # Create a Lead model for validation
        lead = Lead(
            title=title,
            amount=value_float,
            currency=currency,
            person_id=person_id_int,
            organization_id=organization_id_int,
            owner_id=owner_id_int,
            label_ids=label_ids_list,
            expected_close_date=expected_close_date,
            visible_to=visible_to_int,
        )
        
        # Use the Pipedrive client from the context
        pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
        client = pd_mcp_ctx.pipedrive_client
        
        try:
            created_lead = await client.lead_client.create_lead(
                title=lead.title,
                amount=lead.amount,
                currency=lead.currency,
                person_id=lead.person_id,
                organization_id=lead.organization_id,
                owner_id=lead.owner_id,
                label_ids=lead.label_ids,
                expected_close_date=lead.expected_close_date.isoformat() if lead.expected_close_date else None,
                visible_to=lead.visible_to,
            )
            
            # Create a Lead model from the response for consistent formatting
            created_lead_model = Lead.from_api_dict(created_lead)
            
            return format_tool_response(True, data=created_lead_model.model_dump())
            
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
        logger.error(f"Error creating lead: {str(e)}")
        return format_tool_response(False, error_message=f"Failed to create lead: {str(e)}")