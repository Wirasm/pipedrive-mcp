from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def search_persons_in_pipedrive(
    ctx: Context,
    term: str,
    fields_str: Optional[str] = None,
    exact_match: bool = False,
    org_id_str: Optional[str] = None,
    include_fields_str: Optional[str] = None,
    limit_str: Optional[str] = "100",
) -> str:
    """Searches for persons in the Pipedrive CRM by name, email, phone, notes or custom fields.

    This tool searches across all persons in Pipedrive using the provided term.
    Results can be filtered by organization and specific fields to search in.

    args:
    ctx: Context
    term: str - The search term to look for (min 2 chars, or 1 if exact_match=True)
    fields_str: Optional[str] = None - Comma-separated list of fields to search in (name, email, phone, notes, custom_fields)
    exact_match: bool = False - When True, only exact matches are returned
    org_id_str: Optional[str] = None - Organization ID to filter persons by
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
    limit_str: Optional[str] = "100" - Maximum number of results to return (max 500)
    """
    logger.debug(
        f"Tool 'search_persons_in_pipedrive' ENTERED with raw args: term='{term}'"
    )

    # Validate search term length
    if len(term.strip()) < 1:
        error_msg = "Search term cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    elif not exact_match and len(term.strip()) < 2:
        error_msg = "Search term must be at least 2 characters when exact_match is False"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Process fields_str if provided
    fields = None
    if fields_str and fields_str.strip():
        fields = [field.strip() for field in fields_str.split(",")]
        logger.debug(f"Searching in fields: {fields}")

    # Process include_fields_str if provided
    include_fields = None
    if include_fields_str and include_fields_str.strip():
        include_fields = [field.strip() for field in include_fields_str.split(",")]
        logger.debug(f"Including additional fields: {include_fields}")

    # Convert organization ID if provided
    org_id, org_error = convert_id_string(org_id_str, "organization_id")
    if org_error:
        logger.error(org_error)
        return format_tool_response(False, error_message=org_error)

    # Convert limit to integer
    try:
        limit = int(limit_str) if limit_str else 100
        if limit < 1 or limit > 500:
            logger.warning(f"Invalid limit value: {limit}. Using default value 100.")
            limit = 100
    except ValueError:
        logger.warning(f"Invalid limit value: {limit_str}. Using default value 100.")
        limit = 100

    try:
        # Call the Pipedrive API using the persons client
        search_results, next_cursor = await pd_mcp_ctx.pipedrive_client.persons.search_persons(
            term=term,
            fields=fields,
            exact_match=exact_match,
            organization_id=org_id,
            include_fields=include_fields,
            limit=limit
        )
        
        # Check if any results were found
        if not search_results:
            logger.info(f"No persons found for search term '{term}'")
            return format_tool_response(
                True,
                data={"items": [], "message": f"No persons found matching '{term}'"}
            )
        
        logger.info(f"Found {len(search_results)} persons matching term '{term}'")
        
        # Return the search results
        return format_tool_response(
            True, 
            data={
                "items": search_results,
                "count": len(search_results),
                "next_cursor": next_cursor
            }
        )
        
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'search_persons_in_pipedrive' for term '{term}': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'search_persons_in_pipedrive' for term '{term}': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )