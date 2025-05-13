from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def get_organization_from_pipedrive(
    ctx: Context,
    id_str: str,
    include_fields_str: Optional[str] = None,
    custom_fields_str: Optional[str] = None,
) -> str:
    """
    Gets the details of a specific organization from Pipedrive CRM.
    
    This tool retrieves complete information about an organization by its ID, with
    options to include additional fields and custom fields in the response.
    
    args:
    ctx: Context
    id_str: str - The ID of the organization to retrieve
    
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
    
    custom_fields_str: Optional[str] = None - Comma-separated list of custom fields to include
    """
    logger.debug(
        f"Tool 'get_organization_from_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', include_fields_str={include_fields_str}, "
        f"custom_fields_str={custom_fields_str}"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string ID to integer
    organization_id, id_error = convert_id_string(id_str, "organization_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)

    # Parse comma-separated strings to lists
    include_fields = safe_split_to_list(include_fields_str)
    custom_fields_keys = safe_split_to_list(custom_fields_str)

    try:
        # Call the Pipedrive API to get the organization
        organization = await pd_mcp_ctx.pipedrive_client.organizations.get_organization(
            organization_id=organization_id,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys
        )

        if not organization:
            error_message = f"Organization with ID {organization_id} not found"
            logger.warning(error_message)
            return format_tool_response(False, error_message=error_message)

        logger.info(f"Successfully retrieved organization with ID: {organization_id}")
        return format_tool_response(True, data=organization)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'get_organization_from_pipedrive' for ID {organization_id}: {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'get_organization_from_pipedrive' for ID {organization_id}: {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )