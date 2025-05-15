from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.item_search.models.search_result import ItemSearchResults
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list, sanitize_inputs
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def search_items_in_pipedrive(
    ctx: Context,
    term: str,
    item_types_str: Optional[str] = None,
    fields_str: Optional[str] = None,
    search_for_related_items: bool = False,
    exact_match: bool = False,
    include_fields_str: Optional[str] = None,
    limit_str: Optional[str] = "100",
    cursor: Optional[str] = None,
) -> str:
    """Searches for items across multiple types in Pipedrive CRM.
    
    This tool performs a comprehensive search across specified item types using
    the provided search term. It can search in specific fields and include related items.
    Results can be paginated for large result sets.
    
    Format requirements:
    - term: Must be at least 2 characters (1 character if exact_match=True). The search
      supports logical operators (AND, OR, NOT) when properly formatted.
      Example: "company AND technology" will find items containing both words.
    - item_types_str: Comma-separated list of item types. Valid types include: deal,
      person, organization, product, lead, file, mail_attachment, project.
      Example: "deal,person,organization"
    - fields_str: Comma-separated list of fields to search in. Valid fields depend on
      the item type and include: address, code, custom_fields, email, name, notes,
      organization_name, person_name, phone, title, description.
      Example: "name,email,notes"
    - include_fields_str: Comma-separated list of optional fields to include in results.
      Example: "deal.cc_email,person.picture,product.price"
    - limit_str: Numeric string for max results per page (max 500).
      Example: "250"
    - cursor: Opaque string for pagination (obtained from a previous search result).
      Example: "eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
    
    Example:
    ```
    search_items_in_pipedrive(
        term="acme corporation",
        item_types_str="deal,organization,person",
        fields_str="name,notes,title",
        exact_match=False,
        search_for_related_items=True,
        limit_str="100"
    )
    ```
    
    Args:
        ctx: Context object provided by the MCP server
        term: The search term to look for (min 2 chars, or 1 if exact_match=True)
        item_types_str: Comma-separated list of item types to search within
        fields_str: Comma-separated list of fields to search in
        search_for_related_items: When True, includes related leads/deals for found
            persons and organizations, and related persons for found organizations
        exact_match: When True, only full exact matches of the term are returned
            (not case sensitive)
        include_fields_str: Comma-separated list of optional fields to include in results
        limit_str: Maximum number of results to return per page (max 500)
        cursor: Pagination cursor for fetching the next page of results
    
    Returns:
        JSON formatted response with search results or error message
    """
    logger.debug(
        f"Tool 'search_items_in_pipedrive' ENTERED with raw args: "
        f"term='{term}', item_types_str='{item_types_str}', "
        f"fields_str='{fields_str}', search_for_related_items={search_for_related_items}, "
        f"exact_match={exact_match}, include_fields_str='{include_fields_str}', "
        f"limit_str='{limit_str}', cursor='{cursor}'"
    )

    # Sanitize inputs - convert empty strings to None
    inputs = {
        "term": term,
        "item_types_str": item_types_str,
        "fields_str": fields_str,
        "include_fields_str": include_fields_str,
        "limit_str": limit_str,
        "cursor": cursor
    }
    
    sanitized = sanitize_inputs(inputs)
    term = sanitized["term"]
    item_types_str = sanitized["item_types_str"]
    fields_str = sanitized["fields_str"]
    include_fields_str = sanitized["include_fields_str"]
    limit_str = sanitized["limit_str"]
    cursor = sanitized["cursor"]
    
    # Trim strings
    if term:
        term = term.strip()
        
    # Validate search term length
    if not term:
        error_msg = "Search term cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    elif not exact_match and len(term) < 2:
        error_msg = (f"Search term must be at least 2 characters when exact_match is False. "
                    f"Current term '{term}' is {len(term)} character(s).")
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    elif exact_match and len(term) < 1:
        error_msg = "Search term must be at least 1 character when exact_match is True."
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Process string parameters using the safe utility function
    item_types = safe_split_to_list(item_types_str)
    if item_types:
        logger.debug(f"Searching for item types: {item_types}")
        
        valid_item_types = [
            "deal", "person", "organization", "product", 
            "lead", "file", "mail_attachment", "project"
        ]
        for item_type in item_types:
            if item_type not in valid_item_types:
                error_msg = (f"Invalid item type: '{item_type}'. Must be one of: "
                            f"{', '.join(valid_item_types)}. Example: 'deal,person,organization'")
                logger.error(error_msg)
                return format_tool_response(False, error_message=error_msg)

    fields = safe_split_to_list(fields_str)
    if fields:
        logger.debug(f"Searching in fields: {fields}")
        
        valid_fields = [
            "address", "code", "custom_fields", "email", "name", 
            "notes", "organization_name", "person_name", "phone", 
            "title", "description"
        ]
        for field in fields:
            if field not in valid_fields:
                error_msg = (f"Invalid field: '{field}'. Must be one of: "
                            f"{', '.join(valid_fields)}. Example: 'name,email,notes'")
                logger.error(error_msg)
                return format_tool_response(False, error_message=error_msg)

    include_fields = safe_split_to_list(include_fields_str)
    if include_fields:
        logger.debug(f"Including fields: {include_fields}")
        valid_include_fields = [
            "deal.cc_email", "person.picture", "product.price"
        ]
        # This is informational only, not validation, as API might support
        # additional fields we don't explicitly list
        logger.debug(f"Supported include fields are: {', '.join(valid_include_fields)}")

    # Convert limit string to int
    try:
        limit = int(limit_str) if limit_str else 100
        if limit < 1:
            logger.warning(f"Invalid limit value: {limit}. Must be a positive integer. Using default value 100.")
            limit = 100
        elif limit > 500:
            logger.warning(f"Limit value {limit} exceeds maximum (500). The API allows a maximum of 500 results per page. Using maximum value 500.")
            limit = 500
    except ValueError:
        # Use default value for invalid limit string
        logger.warning(f"Invalid limit value: '{limit_str}'. Must be a numeric string (e.g., '100'). Using default value 100.")
        limit = 100

    try:
        # Call the item search API
        search_results, next_cursor = await pd_mcp_ctx.pipedrive_client.search_items(
            term=term,
            item_types=item_types,
            fields=fields,
            search_for_related_items=search_for_related_items,
            exact_match=exact_match,
            include_fields=include_fields,
            limit=limit,
            cursor=cursor
        )

        # Check if any results were found
        if not search_results:
            logger.info(f"No items found for search term '{term}'")
            return format_tool_response(
                True,
                data={
                    "items": [], 
                    "count": 0, 
                    "message": f"No items found matching '{term}'. Try refining your search term, checking different item types, or using a less specific term."
                }
            )
        
        try:
            # Process results into a structured format with type counts
            results_model = ItemSearchResults.from_api_response({
                "items": search_results,
                "next_cursor": next_cursor
            })
            
            # Convert to dict for JSON serialization
            response_data = results_model.model_dump()
            
            logger.info(
                f"Found {len(search_results)} items matching term '{term}'. "
                f"Deal: {response_data.get('deal_count', 0)}, "
                f"Person: {response_data.get('person_count', 0)}, "
                f"Organization: {response_data.get('organization_count', 0)}, "
                f"Product: {response_data.get('product_count', 0)}"
            )
            
            # Format and return the response
            return format_tool_response(True, data=response_data)
        except Exception as model_error:
            # If there's an error in model processing, fall back to a simpler response
            logger.warning(
                f"Error processing search results through model: {str(model_error)}. Falling back to simple format."
            )
            # Return a simplified response
            return format_tool_response(
                True, 
                data={
                    "items": search_results,
                    "count": len(search_results),
                    "next_cursor": next_cursor
                }
            )
        
    except PipedriveAPIError as e:
        error_msg = f"Error searching Pipedrive: {str(e)}"
        response_data = getattr(e, 'response_data', None)
        logger.error(
            f"PipedriveAPIError in tool 'search_items_in_pipedrive' for term '{term}': {str(e)} - Response Data: {response_data}"
        )
        
        # Add specific guidance for common search errors
        if "search term too short" in str(e).lower():
            error_msg += ". Search term must be at least 2 characters (or 1 character if exact_match=True)."
        elif "invalid field" in str(e).lower():
            error_msg += ". Check that all specified fields are valid for the selected item types."
        
        return format_tool_response(False, error_message=error_msg, data=response_data)
    except ValueError as e:
        error_msg = f"Invalid parameter: {str(e)}"
        logger.error(f"ValueError in tool 'search_items_in_pipedrive': {str(e)}")
        return format_tool_response(False, error_message=error_msg)
    except Exception as e:
        error_msg = f"An unexpected error occurred during search: {str(e)}"
        logger.exception(
            f"Unexpected error in tool 'search_items_in_pipedrive' for term '{term}': {str(e)}"
        )
        return format_tool_response(False, error_message=error_msg)