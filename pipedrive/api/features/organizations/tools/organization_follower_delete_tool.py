from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def delete_follower_from_organization_in_pipedrive(
    ctx: Context,
    organization_id_str: str,
    follower_id_str: str,
) -> str:
    """
    Deletes a user follower from an organization in Pipedrive CRM.
    
    This tool removes a user follower from the specified organization. After removal,
    the user will no longer receive notifications about changes to the organization.
    
    Format requirements:
    - organization_id_str: Must be a numeric string representing the organization ID
    - follower_id_str: Must be a numeric string representing the follower ID
    
    Usage example:
    ```
    delete_follower_from_organization_in_pipedrive(
        organization_id_str="12345", 
        follower_id_str="6789"
    )
    ```
    
    Args:
        ctx: Context
        organization_id_str: The ID of the organization. Must be a numeric string.
            Example: "12345"
        follower_id_str: The ID of the follower to remove. Must be a numeric string.
            Example: "6789"
    
    Returns:
        JSON string containing the result of the operation if successful, or error details if failed
    """
    logger.debug(
        f"Tool 'delete_follower_from_organization_in_pipedrive' ENTERED with raw args: "
        f"organization_id_str='{organization_id_str}', follower_id_str='{follower_id_str}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string IDs to integers
    organization_id, org_id_error = convert_id_string(organization_id_str, "organization_id")
    if org_id_error:
        logger.error(org_id_error)
        return format_tool_response(False, error_message=org_id_error)

    follower_id, follower_id_error = convert_id_string(follower_id_str, "follower_id")
    if follower_id_error:
        logger.error(follower_id_error)
        return format_tool_response(False, error_message=follower_id_error)

    try:
        # Call the Pipedrive API to delete a follower from the organization
        result = await pd_mcp_ctx.pipedrive_client.organizations.delete_follower(
            organization_id=organization_id,
            follower_id=follower_id
        )

        logger.info(f"Successfully deleted follower {follower_id} from organization {organization_id}")
        return format_tool_response(True, data=result)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'delete_follower_from_organization_in_pipedrive' for org ID {organization_id} and follower ID {follower_id}: {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'delete_follower_from_organization_in_pipedrive' for org ID {organization_id} and follower ID {follower_id}: {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )