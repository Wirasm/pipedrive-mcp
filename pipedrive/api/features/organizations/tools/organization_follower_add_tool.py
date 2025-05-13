from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def add_follower_to_organization_in_pipedrive(
    ctx: Context,
    id_str: str,
    user_id_str: str,
) -> str:
    """
    Adds a user as a follower to an organization in Pipedrive CRM.
    
    This tool adds a user as a follower to the specified organization.
    The user will receive notifications about changes to the organization.
    
    args:
    ctx: Context
    id_str: str - The ID of the organization
    
    user_id_str: str - The ID of the user to add as a follower
    """
    logger.debug(
        f"Tool 'add_follower_to_organization_in_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', user_id_str='{user_id_str}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string IDs to integers
    organization_id, org_id_error = convert_id_string(id_str, "organization_id")
    if org_id_error:
        logger.error(org_id_error)
        return format_tool_response(False, error_message=org_id_error)

    user_id, user_id_error = convert_id_string(user_id_str, "user_id")
    if user_id_error:
        logger.error(user_id_error)
        return format_tool_response(False, error_message=user_id_error)

    try:
        # Call the Pipedrive API to add a follower to the organization
        result = await pd_mcp_ctx.pipedrive_client.organizations.add_follower(
            organization_id=organization_id,
            user_id=user_id
        )

        logger.info(f"Successfully added user {user_id} as follower to organization {organization_id}")
        return format_tool_response(True, data=result)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'add_follower_to_organization_in_pipedrive' for org ID {organization_id} and user ID {user_id}: {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'add_follower_to_organization_in_pipedrive' for org ID {organization_id} and user ID {user_id}: {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )