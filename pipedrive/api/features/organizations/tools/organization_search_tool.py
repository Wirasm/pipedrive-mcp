from typing import Optional, Dict, Any

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def search_organizations_in_pipedrive(
    ctx: Context,
    term: str,
    fields_str: Optional[str] = None,
    exact_match: bool = False,
    include_fields_str: Optional[str] = None,
    limit_str: Optional[str] = "100",
    cursor: Optional[str] = None,
) -> str:
    """
    Searches for organizations in the Pipedrive CRM by name, address, notes or custom fields.
    
    This tool searches across all organizations in Pipedrive using the provided term.
    Results can be filtered by specific fields to search in.
    
    args:
    ctx: Context
    term: str - The search term to look for (min 2 chars, or 1 if exact_match=True)
    
    fields_str: Optional[str] = None - Comma-separated list of fields to search in (name, address, notes, custom_fields)
    
    exact_match: bool = False - When True, only exact matches are returned
    
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
    
    limit_str: Optional[str] = "100" - Maximum number of results to return (max 500)
    
    cursor: Optional[str] = None - Pagination cursor for the next page
    """
    logger.debug(
        f"Tool 'search_organizations_in_pipedrive' ENTERED with raw args: "
        f"term='{term}', fields_str='{fields_str}', exact_match={exact_match}, "
        f"include_fields_str='{include_fields_str}', limit_str='{limit_str}', cursor='{cursor}'"
    )

    # Validate search term
    if not term:
        error_message = "Search term cannot be empty"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    if len(term) < 2 and not exact_match:
        error_message = "Search term must be at least 2 characters long when exact_match is False"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string parameters to their appropriate types
    limit, limit_error = convert_id_string(limit_str, "limit")
    if limit_error:
        logger.error(limit_error)
        return format_tool_response(False, error_message=limit_error)

    # Convert comma-separated strings to lists
    fields = safe_split_to_list(fields_str)
    include_fields = safe_split_to_list(include_fields_str)

    try:
        # Call the Pipedrive API to search organizations
        results, next_cursor = await pd_mcp_ctx.pipedrive_client.organizations.search_organizations(
            term=term,
            fields=fields,
            exact_match=exact_match,
            include_fields=include_fields,
            limit=limit or 100,  # Default to 100 if None
            cursor=cursor
        )

        logger.info(f"Successfully found {len(results)} organizations matching term '{term}'")
        
        # Format the response with pagination information
        response_data = {
            "items": results,
            "next_cursor": next_cursor,
            "count": len(results)
        }
        
        return format_tool_response(True, data=response_data)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'search_organizations_in_pipedrive' for term '{term}': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'search_organizations_in_pipedrive' for term '{term}': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )