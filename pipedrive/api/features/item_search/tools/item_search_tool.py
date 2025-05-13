from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.item_search.models.search_result import ItemSearchResults
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
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
    """
    Searches for items across multiple types in Pipedrive CRM.
    
    This tool searches across specified item types using the provided term.
    
    args:
    ctx: Context
    term: str - The search term to look for (min 2 chars, or 1 if exact_match=True)
    
    item_types_str: Optional[str] = None - Comma-separated list of item types to search (deal, person, organization, product, lead, file, mail_attachment)
    
    fields_str: Optional[str] = None - Comma-separated list of fields to search in (depends on item types)
    
    search_for_related_items: bool = False - When True, includes related items in the results
    
    exact_match: bool = False - When True, only exact matches are returned
    
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
    
    limit_str: Optional[str] = "100" - Maximum number of results to return (max 500)
    
    cursor: Optional[str] = None - Pagination cursor for the next page
    """
    logger.debug(
        f"Tool 'search_items_in_pipedrive' ENTERED with raw args: "
        f"term='{term}', item_types_str='{item_types_str}', "
        f"fields_str='{fields_str}', search_for_related_items={search_for_related_items}, "
        f"exact_match={exact_match}, include_fields_str='{include_fields_str}', "
        f"limit_str='{limit_str}', cursor='{cursor}'"
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

    # Sanitize empty strings to None
    item_types_str = None if item_types_str == "" else item_types_str
    fields_str = None if fields_str == "" else fields_str
    include_fields_str = None if include_fields_str == "" else include_fields_str
    cursor = None if cursor == "" else cursor

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
                error_msg = f"Invalid item type: '{item_type}'. Must be one of: {', '.join(valid_item_types)}"
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
                error_msg = f"Invalid field: '{field}'. Must be one of: {', '.join(valid_fields)}"
                logger.error(error_msg)
                return format_tool_response(False, error_message=error_msg)

    include_fields = safe_split_to_list(include_fields_str)
    if include_fields:
        logger.debug(f"Including fields: {include_fields}")

    # Convert limit string to int
    try:
        limit = int(limit_str) if limit_str else 100
        if limit < 1:
            logger.warning(f"Invalid limit value: {limit}. Using default value 100.")
            limit = 100
        elif limit > 500:
            logger.warning(f"Limit value {limit} exceeds maximum (500). Using maximum value 500.")
            limit = 500
    except ValueError:
        logger.warning(f"Invalid limit value: {limit_str}. Using default value 100.")
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
                data={"items": [], "count": 0, "message": f"No items found matching '{term}'"}
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
        return format_tool_response(False, error_message=error_msg, data=response_data)
    except ValueError as e:
        error_msg = f"Invalid parameter: {str(e)}"
        logger.error(f"ValueError in tool 'search_items_in_pipedrive': {str(e)}")
        return format_tool_response(False, error_message=error_msg)
    except Exception as e:
        error_msg = f"An unexpected error occurred during search"
        logger.exception(
            f"Unexpected error in tool 'search_items_in_pipedrive' for term '{term}': {str(e)}"
        )
        return format_tool_response(False, error_message=error_msg)