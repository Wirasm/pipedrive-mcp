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
async def create_organization_in_pipedrive(
    ctx: Context,
    name: str,
    owner_id_str: Optional[str] = None,
    address: Optional[str] = None,
    visible_to_str: Optional[str] = None,
    industry: Optional[str] = None,
    custom_fields_dict: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Creates a new organization entity within the Pipedrive CRM.
    
    This tool creates a new organization with the specified details. Organization 
    records represent companies and other organizations you interact with in Pipedrive.
    
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
    create_organization_in_pipedrive(
        name="Acme Corporation",
        owner_id_str="12345",
        address="123 Main St, San Francisco, CA 94107",
        visible_to_str="3",
        industry="Technology"
    )
    ```
    
    Args:
        ctx: Context
        name: The name of the organization (required)
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
        JSON string containing the created organization data if successful, or error details if failed
    """
    logger.debug(
        f"Tool 'create_organization_in_pipedrive' ENTERED with raw args: "
        f"name='{name}', owner_id_str={owner_id_str}, "
        f"address={address}, visible_to_str={visible_to_str}, "
        f"industry={industry}, custom_fields_dict={custom_fields_dict}"
    )

    # Sanitize empty strings to None
    owner_id_str = None if owner_id_str == "" else owner_id_str
    address = None if address == "" else address
    visible_to_str = None if visible_to_str == "" else visible_to_str
    industry = None if industry == "" else industry

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string IDs to integers using our utility function
    owner_id, owner_error = convert_id_string(owner_id_str, "owner_id")
    if owner_error:
        logger.error(owner_error)
        return format_tool_response(False, error_message=owner_error)

    visible_to, visible_error = convert_id_string(visible_to_str, "visible_to")
    if visible_error:
        logger.error(visible_error)
        return format_tool_response(False, error_message=visible_error)

    try:
        # Format address using the organization model's helper method
        address_dict = Organization.format_address(address)
        
        # Create organization model instance with validation
        organization = Organization(
            name=name, 
            owner_id=owner_id, 
            address=address_dict, 
            visible_to=visible_to,
            industry=industry
        )

        # Convert model to API-compatible dict
        payload = organization.to_api_dict()
        
        # Add any custom fields to the payload
        if custom_fields_dict:
            payload.update(custom_fields_dict)

        logger.debug(f"Prepared payload for organization creation: {payload}")

        # Call the Pipedrive API using the organizations client
        created_organization = await pd_mcp_ctx.pipedrive_client.organizations.create_organization(
            **payload
        )

        logger.info(
            f"Successfully created organization '{name}' with ID: {created_organization.get('id')}"
        )

        # Return the API response
        return format_tool_response(True, data=created_organization)

    except ValidationError as e:
        logger.error(f"Validation error creating organization '{name}': {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'create_organization_in_pipedrive' for '{name}': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'create_organization_in_pipedrive' for '{name}': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )