from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def delete_organization_from_pipedrive(
    ctx: Context,
    id_str: str,
) -> str:
    """
    Deletes an organization from the Pipedrive CRM.
    
    This tool marks an organization as deleted. After 30 days, the organization will be 
    permanently deleted from Pipedrive.
    
    args:
    ctx: Context
    id_str: str - The ID of the organization to delete
    """
    logger.debug(
        f"Tool 'delete_organization_from_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string ID to integer
    organization_id, id_error = convert_id_string(id_str, "organization_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)

    try:
        # Call the Pipedrive API to delete the organization
        result = await pd_mcp_ctx.pipedrive_client.organizations.delete_organization(
            organization_id=organization_id
        )

        logger.info(f"Successfully deleted organization with ID: {organization_id}")
        return format_tool_response(True, data=result)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'delete_organization_from_pipedrive' for ID {organization_id}: {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'delete_organization_from_pipedrive' for ID {organization_id}: {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )