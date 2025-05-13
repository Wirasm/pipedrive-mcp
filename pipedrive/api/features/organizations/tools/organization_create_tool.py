from typing import Optional, List

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
) -> str:
    """
    Creates a new organization entity within the Pipedrive CRM.
    
    This tool requires the organization's name and can optionally take details
    like owner ID, address, and visibility settings.
    It returns the details of the created organization upon success.
    
    args:
    ctx: Context
    name: str - The name of the organization
    
    owner_id_str: Optional[str] = None - The ID of the user who owns the organization
    
    address: Optional[str] = None - The address of the organization
    
    visible_to_str: Optional[str] = None - Visibility setting of the organization (1-4)
    """
    logger.debug(
        f"Tool 'create_organization_in_pipedrive' ENTERED with raw args: "
        f"name='{name}', owner_id_str={owner_id_str}, "
        f"address={address}, visible_to_str={visible_to_str}"
    )

    # Sanitize empty strings to None
    owner_id_str = None if owner_id_str == "" else owner_id_str
    address = None if address == "" else address
    visible_to_str = None if visible_to_str == "" else visible_to_str

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
        # Create Organization model instance with validation
        organization = Organization(
            name=name, owner_id=owner_id, address=address, visible_to=visible_to
        )

        # Convert model to API-compatible dict
        payload = organization.to_api_dict()

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