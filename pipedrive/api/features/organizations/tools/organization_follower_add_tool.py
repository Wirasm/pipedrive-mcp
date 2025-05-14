from typing import Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.organizations.models.organization_follower import OrganizationFollower
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def add_follower_to_organization_in_pipedrive(
    ctx: Context,
    organization_id_str: str,
    user_id_str: str,
) -> str:
    """
    Adds a user as a follower to an organization in Pipedrive CRM.
    
    This tool adds a user as a follower to the specified organization. When a user
    follows an organization, they receive notifications about changes and updates
    to that organization.
    
    Format requirements:
    - organization_id_str: Must be a numeric string representing the organization ID
    - user_id_str: Must be a numeric string representing the user ID
    
    Usage example:
    ```
    add_follower_to_organization_in_pipedrive(
        organization_id_str="12345", 
        user_id_str="6789"
    )
    ```
    
    Args:
        ctx: Context
        organization_id_str: The ID of the organization. Must be a numeric string.
            Example: "12345"
        user_id_str: The ID of the user to add as a follower. Must be a numeric string.
            Example: "6789"
    
    Returns:
        JSON string containing the result of the operation if successful, or error details if failed
    """
    logger.debug(
        f"Tool 'add_follower_to_organization_in_pipedrive' ENTERED with raw args: "
        f"organization_id_str='{organization_id_str}', user_id_str='{user_id_str}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string IDs to integers
    organization_id, org_id_error = convert_id_string(organization_id_str, "organization_id")
    if org_id_error:
        logger.error(org_id_error)
        return format_tool_response(False, error_message=org_id_error)

    user_id, user_id_error = convert_id_string(user_id_str, "user_id")
    if user_id_error:
        logger.error(user_id_error)
        return format_tool_response(False, error_message=user_id_error)

    try:
        # Create and validate OrganizationFollower model
        follower = OrganizationFollower(user_id=user_id)
        
        # Call the Pipedrive API to add a follower to the organization
        result = await pd_mcp_ctx.pipedrive_client.organizations.add_follower(
            organization_id=organization_id,
            user_id=user_id
        )

        logger.info(f"Successfully added user {user_id} as follower to organization {organization_id}")
        return format_tool_response(True, data=result)

    except ValidationError as e:
        logger.error(f"Validation error adding follower with user ID {user_id} to organization {organization_id}: {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
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