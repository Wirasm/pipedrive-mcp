from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("search_deals_in_pipedrive")
async def search_deals_in_pipedrive(
    ctx: Context,
    term: str,
    fields_str: Optional[str] = None,
    exact_match: bool = False,
    person_id_str: Optional[str] = None,
    organization_id_str: Optional[str] = None,
    status: Optional[str] = None,
    include_fields_str: Optional[str] = None,
    limit_str: Optional[str] = "100",
    cursor: Optional[str] = None,
) -> str:
    """Searches for deals in the Pipedrive CRM by title, notes or custom fields.

    This tool performs a full-text search across deals in Pipedrive using the provided search term.
    The search can be focused on specific fields and filtered by person, organization, and status.
    Results are returned in pages, with cursor-based pagination for handling large result sets.
    
    Format requirements:
    - term: Required search text (minimum 2 characters, or 1 character with exact_match=True)
    - fields_str: Optional comma-separated list of fields to search in (defaults to all searchable fields)
    - person_id_str, organization_id_str: Optional numeric ID strings (e.g. "123")
    - status: Optional filter by status ("open", "won", or "lost")
    - limit_str: Maximum results per page (1-500, default 100)
    
    Search Fields:
    You can specify which fields to search in with the fields_str parameter:
    - "title": Search in deal titles only
    - "notes": Search in deal notes only
    - "custom_fields": Search in custom fields only
    - Leave empty to search in all searchable fields
    
    Search Behavior:
    - By default, performs a partial match search (matches terms within words)
    - With exact_match=True, only complete word matches are returned
    - Searches are case-insensitive
    - Only searchable custom field types are included: address, text, varchar, numeric, phone
    
    Filtering:
    - person_id_str: Find deals associated with a specific person
    - organization_id_str: Find deals associated with a specific organization
    - status: Filter to only "open", "won", or "lost" deals
    
    Example usage:
    ```
    search_deals_in_pipedrive(
        term="software license",
        fields_str="title,notes",
        status="open",
        organization_id_str="123"
    )
    ```

    args:
    ctx: Context
    term: str - The search term to look for (min 2 chars, or 1 if exact_match=True)
    fields_str: Optional[str] = None - Comma-separated list of fields to search in ("title", "notes", "custom_fields")
    exact_match: bool = False - When True, only exact matches are returned
    person_id_str: Optional[str] = None - Filter deals by person ID
    organization_id_str: Optional[str] = None - Filter deals by organization ID
    status: Optional[str] = None - Filter deals by status ("open", "won", "lost")
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
    limit_str: Optional[str] = "100" - Maximum number of results to return (1-500)
    cursor: Optional[str] = None - Pagination cursor for retrieving the next page
    """
    logger.debug(
        f"Tool 'search_deals_in_pipedrive' ENTERED with raw args: "
        f"term='{term}', fields_str='{fields_str}', "
        f"exact_match={exact_match}, person_id_str='{person_id_str}', "
        f"organization_id_str='{organization_id_str}', status='{status}', "
        f"include_fields_str='{include_fields_str}', limit_str='{limit_str}', "
        f"cursor='{cursor}'"
    )
    
    # Validate required fields
    if not term or not term.strip():
        error_message = "Search term cannot be empty"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    term = term.strip()
    if not exact_match and len(term) < 2:
        error_message = "Search term must be at least 2 characters long (or 1 if exact_match=True)"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    # Sanitize empty strings to None
    fields_str = None if fields_str == "" else fields_str
    person_id_str = None if person_id_str == "" else person_id_str
    organization_id_str = None if organization_id_str == "" else organization_id_str
    status = None if status == "" else status
    include_fields_str = None if include_fields_str == "" else include_fields_str
    cursor = None if cursor == "" else cursor

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    try:
        # Parse the limit string to an integer
        limit = 100  # Default
        if limit_str:
            try:
                limit = int(limit_str)
                if limit < 1:
                    limit = 100
                elif limit > 500:
                    limit = 500
            except ValueError:
                logger.warning(f"Invalid limit format: '{limit_str}'. Using default of 100.")

        # Convert string IDs to integers
        person_id, person_id_error = convert_id_string(person_id_str, "person_id")
        if person_id_error:
            logger.error(person_id_error)
            return format_tool_response(False, error_message=person_id_error)

        organization_id, org_id_error = convert_id_string(organization_id_str, "organization_id")
        if org_id_error:
            logger.error(org_id_error)
            return format_tool_response(False, error_message=org_id_error)

        # Convert fields and include_fields from comma-separated strings to lists
        fields = None
        if fields_str:
            fields = [field.strip() for field in fields_str.split(",")]

        include_fields = None
        if include_fields_str:
            include_fields = [field.strip() for field in include_fields_str.split(",")]

        # Validate status if provided
        if status and status not in ["open", "won", "lost"]:
            error_message = f"Invalid status: '{status}'. Must be one of: open, won, lost"
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)

        # Call the Pipedrive API
        deals_list, next_cursor = await pd_mcp_ctx.pipedrive_client.deals.search_deals(
            term=term,
            fields=fields,
            exact_match=exact_match,
            person_id=person_id,
            organization_id=organization_id,
            status=status,
            include_fields=include_fields,
            limit=limit,
            cursor=cursor
        )

        logger.info(f"Successfully found {len(deals_list)} deals for term '{term}'")

        # Format and return the response with next cursor information
        response_data = {
            "items": deals_list,
            "next_cursor": next_cursor
        }
        return format_tool_response(True, data=response_data)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'search_deals_in_pipedrive' for term '{term}': {str(e)}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'search_deals_in_pipedrive' for term '{term}': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )