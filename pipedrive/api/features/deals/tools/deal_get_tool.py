from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def get_deal_from_pipedrive(
    ctx: Context,
    id_str: str,
    include_fields_str: Optional[str] = None,
    custom_fields_str: Optional[str] = None,
) -> str:
    """Gets the details of a specific deal from Pipedrive CRM.

    This tool retrieves complete information about a deal by its ID, with
    options to include additional fields and custom fields in the response.

    args:
    ctx: Context
    id_str: str - The ID of the deal to retrieve
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
    custom_fields_str: Optional[str] = None - Comma-separated list of custom fields to include
    """
    logger.debug(
        f"Tool 'get_deal_from_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', include_fields_str='{include_fields_str}', "
        f"custom_fields_str='{custom_fields_str}'"
    )

    # Sanitize empty strings to None
    include_fields_str = None if include_fields_str == "" else include_fields_str
    custom_fields_str = None if custom_fields_str == "" else custom_fields_str

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string ID to integer
    deal_id, id_error = convert_id_string(id_str, "deal_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)

    try:
        # Process include_fields from comma-separated string to list
        include_fields = None
        if include_fields_str:
            include_fields = [field.strip() for field in include_fields_str.split(",")]

        # Process custom_fields from comma-separated string to list
        custom_fields_keys = None
        if custom_fields_str:
            custom_fields_keys = [field.strip() for field in custom_fields_str.split(",")]

        # Call the Pipedrive API
        deal_data = await pd_mcp_ctx.pipedrive_client.deals.get_deal(
            deal_id=deal_id,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys,
        )

        logger.info(f"Successfully retrieved deal with ID: {deal_id}")

        # Return the API response
        return format_tool_response(True, data=deal_data)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'get_deal_from_pipedrive' for ID '{id_str}': {str(e)}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'get_deal_from_pipedrive' for ID '{id_str}': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )