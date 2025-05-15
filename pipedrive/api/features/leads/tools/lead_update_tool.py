from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.leads.models.lead import Lead
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string, validate_uuid_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("leads")
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
    """Updates an existing lead entity within the Pipedrive CRM.
    
    This tool updates a lead with the provided information. Only the fields you specify will be updated;
    all other fields will remain unchanged. At least one field must be provided for update.
    
    Format requirements:
        - lead_id: Required UUID of the lead to update (example: "adf21080-0e10-11eb-879b-05d71fb426ec")
        - title: Updated lead name/title (cannot be empty if provided) 
        - value: Updated monetary value as a string (will be converted to float)
        - currency: Updated 3-letter currency code
        - person_id: Updated person ID as a string (will be converted to integer)
          Note: At least one of person_id or organization_id must remain associated with the lead
        - organization_id: Updated organization ID as a string (will be converted to integer)
          Note: At least one of person_id or organization_id must remain associated with the lead
        - owner_id: Updated user ID as a string for the lead owner (will be converted to integer)
        - label_ids: Updated comma-separated list of lead label UUIDs (e.g., "uuid1,uuid2")
          Note: You can get available label IDs using the get_lead_labels_from_pipedrive tool
        - expected_close_date: Updated date in ISO format (YYYY-MM-DD)
        - visible_to: Updated visibility setting as a string, where:
          "1" = Owner only 
          "3" = Owner's visibility group
          "5" = Owner's visibility group and sub-groups
          "7" = Entire company
        - is_archived: Whether the lead is archived ("true" or "false")
        - was_seen: Whether the lead was seen ("true" or "false")
    
    Example:
        update_lead_in_pipedrive(
            lead_id="adf21080-0e10-11eb-879b-05d71fb426ec",
            title="Updated Client XYZ",
            value="10000",
            visible_to="7",
            is_archived="false"
        )
    
    Args:
        ctx: Context object containing the Pipedrive client
        lead_id: The UUID of the lead to update (required)
        title: The updated title/name of the lead
        value: The updated monetary value of the lead (numeric string)
        currency: Updated currency code for the lead value
        person_id: Updated ID of the person to associate with this lead
        organization_id: Updated ID of the organization to associate with this lead
        owner_id: Updated ID of the user who will own this lead
        label_ids: Updated comma-separated list of lead label UUIDs to apply
        expected_close_date: Updated expected close date in ISO format (YYYY-MM-DD)
        visible_to: Updated visibility setting (1=Owner only, 3=Owner's group, 5=Owner's group & sub-groups, 7=Entire company)
        is_archived: Whether the lead is archived ("true" or "false")
        was_seen: Whether the lead was seen ("true" or "false")
    
    Returns:
        JSON string containing success status and updated lead data or error message.
    """
    logger.debug(
        f"Tool 'update_lead_in_pipedrive' ENTERED with raw args: "
        f"lead_id='{lead_id}', title='{title}', value={value}, currency={currency}, "
        f"person_id={person_id}, organization_id={organization_id}, "
        f"owner_id={owner_id}, label_ids={label_ids}, "
        f"expected_close_date={expected_close_date}, visible_to={visible_to}, "
        f"is_archived={is_archived}, was_seen={was_seen}"
    )
    
    # Validate required fields
    if not lead_id or not lead_id.strip():
        error_msg = "Lead ID is required and cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    # Validate UUID format
    validated_uuid, error = validate_uuid_string(lead_id, "lead_id")
    if error:
        logger.error(f"Invalid lead_id format: {error}")
        return format_tool_response(False, error_message=error)
        
    # Sanitize empty strings to None
    title = None if title == "" else title
    value = None if value == "" else value
    currency = None if currency == "" else currency
    person_id = None if person_id == "" else person_id
    organization_id = None if organization_id == "" else organization_id
    owner_id = None if owner_id == "" else owner_id
    label_ids = None if label_ids == "" else label_ids
    expected_close_date = None if expected_close_date == "" else expected_close_date
    visible_to = None if visible_to == "" else visible_to
    is_archived = None if is_archived == "" else is_archived
    was_seen = None if was_seen == "" else was_seen
    
    # Convert string parameters to appropriate types
    person_id_int = None
    if person_id is not None:
        person_id_int, error = convert_id_string(person_id, "person_id")
        if error:
            logger.error(f"Invalid person_id: {error}")
            return format_tool_response(False, error_message=error)
    
    organization_id_int = None
    if organization_id is not None:
        organization_id_int, error = convert_id_string(organization_id, "organization_id")
        if error:
            logger.error(f"Invalid organization_id: {error}")
            return format_tool_response(False, error_message=error)
    
    owner_id_int = None
    if owner_id is not None:
        owner_id_int, error = convert_id_string(owner_id, "owner_id")
        if error:
            logger.error(f"Invalid owner_id: {error}")
            return format_tool_response(False, error_message=error)
    
    visible_to_int = None
    if visible_to is not None:
        visible_to_int, error = convert_id_string(visible_to, "visible_to")
        if error:
            logger.error(f"Invalid visible_to: {error}")
            return format_tool_response(False, error_message=error)
        
        # Validate visibility setting
        if visible_to_int not in {1, 3, 5, 7}:
            error_msg = (
                f"Invalid visible_to value: {visible_to_int}. "
                f"Must be one of [1, 3, 5, 7] (1=Owner only, 3=Owner's group, 5=Owner's group & sub-groups, 7=Entire company)"
            )
            logger.error(error_msg)
            return format_tool_response(False, error_message=error_msg)
    
    # Convert value to float if provided
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
    
    # Convert boolean parameters
    is_archived_bool = None
    if is_archived is not None:
        if is_archived.lower() not in ["true", "false"]:
            return format_tool_response(
                False, 
                error_message=f"Invalid is_archived format: {is_archived}. Must be 'true' or 'false'."
            )
        is_archived_bool = is_archived.lower() == "true"
    
    was_seen_bool = None
    if was_seen is not None:
        if was_seen.lower() not in ["true", "false"]:
            return format_tool_response(
                False, 
                error_message=f"Invalid was_seen format: {was_seen}. Must be 'true' or 'false'."
            )
        was_seen_bool = was_seen.lower() == "true"
    
    # Handle label_ids as a list
    label_ids_list = None
    if label_ids is not None:
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
    
    # Check that at least one field is provided for update
    if all(param is None for param in [
        title, value, currency, person_id, organization_id, owner_id,
        label_ids, expected_close_date, visible_to, is_archived, was_seen
    ]):
        return format_tool_response(
            False, 
            error_message="At least one field must be provided for update. Please specify which lead properties you want to change."
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
        logger.error(f"Validation error updating lead with ID '{lead_id}': {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'update_lead_in_pipedrive' for ID '{lead_id}': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        # Handle other errors
        logger.exception(
            f"Unexpected error in tool 'update_lead_in_pipedrive' for ID '{lead_id}': {str(e)}"
        )
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")