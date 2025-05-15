from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.leads.models.lead import Lead
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("leads")
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
    """Creates a new lead entity within the Pipedrive CRM.
    
    This tool creates a new lead record with the provided information. A lead represents
    an early-stage sales opportunity in Pipedrive. Each lead must have a title and be linked
    to either a person or an organization (or both).
    
    Format requirements:
        - title: Required lead name/title (cannot be empty)
        - value: Numeric value as a string (will be converted to float)
        - currency: 3-letter currency code (default: "USD")
        - person_id: Person ID as a string (will be converted to integer)
        - organization_id: Organization ID as a string (will be converted to integer)
        - owner_id: User ID as a string for the lead owner (will be converted to integer)
        - label_ids: Comma-separated list of lead label UUIDs (e.g., "uuid1,uuid2")
          Note: You can get available label IDs using the get_lead_labels_from_pipedrive tool
        - expected_close_date: Date in ISO format (YYYY-MM-DD)
        - visible_to: Visibility setting as a string, where:
          "1" = Owner only 
          "3" = Owner's visibility group
          "5" = Owner's visibility group and sub-groups
          "7" = Entire company
    
    Example:
        create_lead_in_pipedrive(
            title="Potential Client ABC",
            value="5000",
            currency="USD",
            person_id="123",
            label_ids="f08b42a0-4e75-11ea-9643-03698ef1cfd6,f08b42a1-4e75-11ea-9643-03698ef1cfd6",
            visible_to="3"
        )
    
    Args:
        ctx: Context object containing the Pipedrive client
        title: The title/name of the lead to create (required)
        value: The monetary value of the lead (numeric string)
        currency: Currency code for the lead value (default: USD)
        person_id: ID of the person to associate with this lead
        organization_id: ID of the organization to associate with this lead
        owner_id: ID of the user who will own this lead
        label_ids: Comma-separated list of lead label UUIDs to apply
        expected_close_date: Expected close date in ISO format (YYYY-MM-DD)
        visible_to: Visibility setting (1=Owner only, 3=Owner's group, 5=Owner's group & sub-groups, 7=Entire company)
    
    Returns:
        JSON string containing success status and created lead data or error message.
    """
    logger.debug(
        f"Tool 'create_lead_in_pipedrive' ENTERED with raw args: "
        f"title='{title}', value={value}, currency={currency}, "
        f"person_id={person_id}, organization_id={organization_id}, "
        f"owner_id={owner_id}, label_ids={label_ids}, "
        f"expected_close_date={expected_close_date}, visible_to={visible_to}"
    )
    
    # Validate required fields
    if not title or not title.strip():
        error_msg = "Lead title is required and cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    # Sanitize empty strings to None
    value = None if value == "" else value
    person_id = None if person_id == "" else person_id
    organization_id = None if organization_id == "" else organization_id
    owner_id = None if owner_id == "" else owner_id
    label_ids = None if label_ids == "" else label_ids
    expected_close_date = None if expected_close_date == "" else expected_close_date
    visible_to = None if visible_to == "" else visible_to
    
    # Convert value from string to float if provided
    value_float = None
    if value is not None:
        try:
            value_float = float(value)
            if value_float < 0:
                return format_tool_response(
                    False, 
                    error_message=f"Lead value cannot be negative: {value}. Please provide a non-negative number."
                )
        except ValueError:
            return format_tool_response(
                False, 
                error_message=f"Invalid value format: {value}. Must be a valid number (e.g., '1000', '1500.50')."
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
        
        # Validate visibility setting
        if visible_to_int not in {1, 3, 5, 7}:
            error_msg = (
                f"Invalid visible_to value: {visible_to_int}. "
                f"Must be one of [1, 3, 5, 7] (1=Owner only, 3=Owner's group, 5=Owner's group & sub-groups, 7=Entire company)"
            )
            logger.error(error_msg)
            return format_tool_response(False, error_message=error_msg)
            
    # Handle label_ids as a list
    label_ids_list = None
    if label_ids:
        label_ids_list = safe_split_to_list(label_ids)
        # Validate UUID format for label_ids
        for label_id in label_ids_list:
            try:
                from uuid import UUID
                UUID(label_id)
            except ValueError:
                return format_tool_response(
                    False,
                    error_message=f"Invalid label_id format: '{label_id}'. Label IDs must be valid UUIDs."
                )
    
    # Check that either person_id or organization_id is provided
    if not person_id_int and not organization_id_int:
        return format_tool_response(
            False, 
            error_message="Association error: Either person_id or organization_id (or both) must be provided. A lead must be linked to a person or organization."
        )
    
    # Validate date format if provided
    if expected_close_date:
        try:
            from datetime import date
            date.fromisoformat(expected_close_date)
        except ValueError:
            return format_tool_response(
                False,
                error_message=f"Invalid expected_close_date format: '{expected_close_date}'. Must be in ISO format (YYYY-MM-DD)."
            )
    
    # Validate currency format
    if currency and len(currency) != 3:
        return format_tool_response(
            False,
            error_message=f"Invalid currency format: '{currency}'. Must be a 3-letter currency code (e.g., 'USD', 'EUR')."
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
        logger.error(f"Validation error creating lead '{title}': {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'create_lead_in_pipedrive' for '{title}': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        # Handle other errors
        logger.exception(
            f"Unexpected error in tool 'create_lead_in_pipedrive' for '{title}': {str(e)}"
        )
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")