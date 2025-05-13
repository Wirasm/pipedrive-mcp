from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("persons")
async def get_person_from_pipedrive(
    ctx: Context,
    id_str: str,
    include_fields_str: Optional[str] = None,
    custom_fields_str: Optional[str] = None,
) -> str:
    """Gets the details of a specific person from Pipedrive CRM.

    This tool retrieves complete information about a person by their ID, with
    options to include additional fields and custom fields in the response.

    args:
    ctx: Context
    id_str: str - The ID of the person to retrieve
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
    custom_fields_str: Optional[str] = None - Comma-separated list of custom fields to include
    """
    logger.debug(
        f"Tool 'get_person_from_pipedrive' ENTERED with raw args: id_str='{id_str}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string ID to integer using our utility function
    person_id, id_error = convert_id_string(id_str, "person_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)

    # Process include_fields if provided
    include_fields = None
    if include_fields_str and include_fields_str.strip():
        include_fields = [field.strip() for field in include_fields_str.split(",")]
        logger.debug(f"Including additional fields: {include_fields}")

    # Process custom_fields if provided
    custom_fields_keys = None
    if custom_fields_str and custom_fields_str.strip():
        custom_fields_keys = [field.strip() for field in custom_fields_str.split(",")]
        logger.debug(f"Including custom fields: {custom_fields_keys}")

    try:
        # Call the Pipedrive API using the persons client
        person_data = await pd_mcp_ctx.pipedrive_client.persons.get_person(
            person_id=person_id,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys
        )
        
        if not person_data:
            logger.warning(f"Person with ID {person_id} not found")
            return format_tool_response(
                False, error_message=f"Person with ID {person_id} not found"
            )
        
        logger.info(f"Successfully retrieved person with ID: {person_id}")
        
        # Return the API response
        return format_tool_response(True, data=person_data)
        
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'get_person_from_pipedrive' for ID {person_id}: {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'get_person_from_pipedrive' for ID {person_id}: {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )