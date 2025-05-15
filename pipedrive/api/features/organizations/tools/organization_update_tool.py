from typing import Optional, List, Dict, Any

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.organizations.models.organization import Organization
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def update_organization_in_pipedrive(
    ctx: Context,
    id_str: str,
    name: Optional[str] = None,
    owner_id_str: Optional[str] = None,
    address: Optional[str] = None,
    visible_to_str: Optional[str] = None,
    industry: Optional[str] = None,
    custom_fields_dict: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Updates an existing organization in the Pipedrive CRM.
    
    This tool updates an existing organization with the specified details. At least one field
    must be provided for updating. Any fields not specified will remain unchanged.
    
    Format requirements:
    - address: Must be a physical address in text format. Will be automatically formatted
      for the API. Example: "123 Main Street, New York, NY 10001"
    - visible_to: Must be a value from 1-4 (1: Owner only, 2: Owner's visibility group,
      3: Entire company, 4: Specified users)
    - industry: Industry classification as a string (commonly used values include
      "Technology", "Finance", "Healthcare", "Manufacturing", etc.)
    - custom_fields_dict: JSON object containing custom field values, with field keys as defined
      in your Pipedrive account
    
    Usage example:
    ```
    update_organization_in_pipedrive(
        id_str="12345",
        name="Acme Corporation Updated",
        address="123 Main St, San Francisco, CA 94107",
        visible_to_str="3",
        industry="Technology"
    )
    ```
    
    Args:
        ctx: Context
        id_str: The ID of the organization to update (required)
        name: The updated name of the organization
        owner_id_str: The ID of the user who owns the organization. Example: "12345"
        address: The physical address of the organization. Will be properly formatted for the API.
            Example: "123 Main St, San Francisco, CA 94107"
        visible_to_str: Visibility setting of the organization (1-4).
            1: Owner only, 2: Owner's visibility group, 3: Entire company, 4: Specified users.
            Example: "3"
        industry: Industry classification for the organization.
            Example: "Technology", "Finance", "Healthcare", etc.
        custom_fields_dict: Dictionary of custom field values with field keys as defined in Pipedrive.
            Example: {"cf_annual_revenue": 1000000, "cf_company_size": "101-250"}
    
    Returns:
        JSON string containing the updated organization data if successful, or error details if failed
    """
    logger.debug(
        f"Tool 'update_organization_in_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', name='{name}', owner_id_str='{owner_id_str}', "
        f"address='{address}', visible_to_str='{visible_to_str}', "
        f"industry='{industry}', custom_fields_dict={custom_fields_dict}"
    )

    # Check if at least one update field is provided
    if all(param is None or param == "" for param in 
           [name, owner_id_str, address, visible_to_str, industry]) and not custom_fields_dict:
        error_message = "At least one field must be provided for updating an organization"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string IDs to integers using our utility function
    organization_id, id_error = convert_id_string(id_str, "organization_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)

    owner_id, owner_error = convert_id_string(owner_id_str, "owner_id")
    if owner_error:
        logger.error(owner_error)
        return format_tool_response(False, error_message=owner_error)

    visible_to, visible_error = convert_id_string(visible_to_str, "visible_to")
    if visible_error:
        logger.error(visible_error)
        return format_tool_response(False, error_message=visible_error)

    try:
        # Prepare update payload
        update_data = {}
        if name is not None and name != "":
            update_data["name"] = name
        if owner_id is not None:
            update_data["owner_id"] = owner_id
        if address is not None and address != "":
            # Format address using the Organization model's helper method
            address_dict = Organization.format_address(address)
            if address_dict:
                update_data["address"] = address_dict
            else:
                return format_tool_response(False, error_message="Invalid address format. Address cannot be empty.")
        if visible_to is not None:
            # Validate the visible_to value
            if visible_to not in [1, 2, 3, 4]:
                error_message = f"Invalid visibility value: {visible_to}. Must be one of: 1 (Owner only), 2 (Owner's visibility group), 3 (Entire company), or 4 (Specified users)"
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
            update_data["visible_to"] = visible_to
        if industry is not None and industry != "":
            update_data["industry"] = industry
            
        # Add any custom fields to the payload
        if custom_fields_dict:
            update_data.update(custom_fields_dict)

        # Call the Pipedrive API to update the organization
        updated_organization = await pd_mcp_ctx.pipedrive_client.organizations.update_organization(
            organization_id=organization_id,
            **update_data
        )

        logger.info(f"Successfully updated organization with ID: {organization_id}")
        return format_tool_response(True, data=updated_organization)

    except ValidationError as e:
        logger.error(f"Validation error updating organization with ID {organization_id}: {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'update_organization_in_pipedrive' for ID {organization_id}: {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'update_organization_in_pipedrive' for ID {organization_id}: {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )