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
async def update_organization_in_pipedrive(
    ctx: Context,
    id_str: str,
    name: Optional[str] = None,
    owner_id_str: Optional[str] = None,
    address: Optional[str] = None,
    visible_to_str: Optional[str] = None,
) -> str:
    """
    Updates an existing organization in the Pipedrive CRM.
    
    This tool requires the organization's ID and at least one field to update.
    It can update basic information like name, owner, address, and visibility settings.
    
    args:
    ctx: Context
    id_str: str - The ID of the organization to update
    
    name: Optional[str] = None - The updated name of the organization
    
    owner_id_str: Optional[str] = None - The ID of the user who owns the organization
    
    address: Optional[str] = None - The address of the organization
    
    visible_to_str: Optional[str] = None - Visibility setting of the organization (1-4)
    """
    logger.debug(
        f"Tool 'update_organization_in_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', name='{name}', owner_id_str='{owner_id_str}', "
        f"address='{address}', visible_to_str='{visible_to_str}'"
    )

    # Check if at least one update field is provided
    if all(param is None or param == "" for param in [name, owner_id_str, address, visible_to_str]):
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
            # Convert address string to dictionary format for the API
            update_data["address"] = {"value": address}
        if visible_to is not None:
            update_data["visible_to"] = visible_to

        # Validate the visible_to value if provided
        if "visible_to" in update_data and update_data["visible_to"] not in [1, 2, 3, 4]:
            error_message = f"Invalid visibility value: {visible_to}. Must be one of: 1, 2, 3, 4"
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)

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