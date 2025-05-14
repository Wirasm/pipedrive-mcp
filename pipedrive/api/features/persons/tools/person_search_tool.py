from typing import Optional, List

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("persons")
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

    Format requirements:
        - term: Search term (minimum 2 characters, or 1 if exact_match=True)
        - fields_str: Optional comma-separated list of fields to search in:
          Available options: "name", "email", "phone", "notes", "custom_fields"
          Example: "name,email,phone"
        - exact_match: When True, only exact matches are returned
        - org_id_str: Optional organization ID as a string to filter persons by
        - include_fields_str: Optional comma-separated list of additional fields to include
          Example: "person.picture,open_deals_count"
        - limit_str: Maximum number of results to return (max 500)

    Example:
        search_persons_in_pipedrive(
            term="John Smith",
            fields_str="name,email",
            exact_match=false,
            org_id_str="42",
            include_fields_str="person.picture",
            limit_str="25"
        )

    Args:
        ctx: Context object containing the Pipedrive client
        term: The search term to look for
        fields_str: Comma-separated list of fields to search in
        exact_match: When True, only exact matches are returned
        org_id_str: Organization ID to filter persons by
        include_fields_str: Comma-separated list of additional fields to include
        limit_str: Maximum number of results to return (default: "100")

    Returns:
        JSON string containing success status and search results or error message.
        When successful, the response includes:
        - items: Array of matching person objects
        - count: Number of results found
        - next_cursor: Pagination cursor for fetching more results (if available)
    """
    logger.debug(
        f"Tool 'search_persons_in_pipedrive' ENTERED with raw args: "
        f"term='{term}', fields_str='{fields_str}', exact_match={exact_match}, "
        f"org_id_str='{org_id_str}', include_fields_str='{include_fields_str}', "
        f"limit_str='{limit_str}'"
    )

    # Validate search term length
    if not term or len(term.strip()) < 1:
        error_msg = "Search term cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    elif not exact_match and len(term.strip()) < 2:
        error_msg = "Search term must be at least 2 characters when exact_match is False"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Process fields_str if provided
    fields: Optional[List[str]] = None
    if fields_str and fields_str.strip():
        fields = [field.strip() for field in fields_str.split(",") if field.strip()]
        
        # Validate field values
        valid_fields = {"name", "email", "phone", "notes", "custom_fields"}
        invalid_fields = [f for f in fields if f not in valid_fields]
        if invalid_fields:
            error_msg = (
                f"Invalid search fields: {invalid_fields}. "
                f"Valid options are: {', '.join(valid_fields)}"
            )
            logger.error(error_msg)
            return format_tool_response(False, error_message=error_msg)
            
        logger.debug(f"Searching in fields: {fields}")

    # Process include_fields_str if provided
    include_fields: Optional[List[str]] = None
    if include_fields_str and include_fields_str.strip():
        include_fields = [field.strip() for field in include_fields_str.split(",") if field.strip()]
        logger.debug(f"Including additional fields: {include_fields}")

    # Convert organization ID if provided
    org_id = None
    if org_id_str:
        org_id, org_error = convert_id_string(org_id_str, "organization_id")
        if org_error:
            logger.error(org_error)
            return format_tool_response(False, error_message=org_error)

    # Convert limit to integer
    try:
        limit = int(limit_str) if limit_str else 100
        if limit < 1:
            error_msg = f"Limit must be a positive integer, got {limit}"
            logger.error(error_msg)
            return format_tool_response(False, error_message=error_msg)
        elif limit > 500:
            logger.warning(f"Limit value {limit} exceeds maximum (500). Using max value 500.")
            limit = 500
    except ValueError:
        error_msg = f"Invalid limit value: '{limit_str}'. Must be a valid integer."
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

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
                data={"items": [], "message": f"No persons found matching '{term}'", "count": 0}
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