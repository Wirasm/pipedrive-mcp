from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.item_search.models.search_result import FieldSearchResults
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def search_item_field_in_pipedrive(
    ctx: Context,
    term: str,
    entity_type: str,
    field: str,
    match: str = "exact",
    limit_str: Optional[str] = "100",
    cursor: Optional[str] = None,
) -> str:
    """
    Searches for values of a specific field in Pipedrive.
    
    This tool is useful for finding autocomplete values for specific fields.
    
    args:
    ctx: Context
    term: str - The search term to look for (min 2 chars, or 1 if match is not 'exact')
    
    entity_type: str - The type of entity to search (deal, person, organization, product, lead, project)
    
    field: str - The field key to search in
    
    match: str = "exact" - Type of match: exact, beginning, or middle
    
    limit_str: Optional[str] = "100" - Maximum number of results to return (max 500)
    
    cursor: Optional[str] = None - Pagination cursor for the next page
    """
    logger.debug(
        f"Tool 'search_item_field_in_pipedrive' ENTERED with raw args: "
        f"term='{term}', entity_type='{entity_type}', field='{field}', "
        f"match='{match}', limit_str='{limit_str}', cursor='{cursor}'"
    )

    # Validate required parameters
    if not term or len(term.strip()) < 1:
        error_msg = "Search term cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    # For exact match, we need at least 1 character
    term_length = len(term.strip())
    if match == "exact" and term_length < 1:
        error_msg = "Search term must be at least 1 character for exact matching"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    # For non-exact matches, we need at least 2 characters
    if match != "exact" and term_length < 2:
        error_msg = f"Search term must be at least 2 characters for '{match}' matching (current length: {term_length})"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    if not entity_type or not entity_type.strip():
        error_msg = "Entity type cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    if not field or not field.strip():
        error_msg = "Field key cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Validate entity_type
    valid_entity_types = ["deal", "person", "organization", "product", "lead", "project"]
    if entity_type not in valid_entity_types:
        error_msg = f"Invalid entity type: '{entity_type}'. Must be one of: {', '.join(valid_entity_types)}"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    # Validate match type
    valid_match_types = ["exact", "beginning", "middle"]
    if match not in valid_match_types:
        error_msg = f"Invalid match type: '{match}'. Must be one of: {', '.join(valid_match_types)}"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    # Sanitize empty strings to None
    cursor = None if cursor == "" else cursor

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
        # Call the field search API
        field_results, next_cursor = await pd_mcp_ctx.pipedrive_client.search_field(
            term=term,
            entity_type=entity_type,
            field=field,
            match=match,
            limit=limit,
            cursor=cursor
        )
        
        # Check if any results were found
        if not field_results:
            logger.info(f"No field values found for search term '{term}'")
            return format_tool_response(
                True,
                data={
                    "items": [], 
                    "count": 0, 
                    "message": f"No values found for field '{field}' matching '{term}'"
                }
            )
        
        try:
            # Process results into a structured format
            results_model = FieldSearchResults.from_api_response({
                "items": field_results,
                "next_cursor": next_cursor
            })
            
            # Convert to dict for JSON serialization
            response_data = results_model.model_dump()
            
            logger.info(f"Found {len(field_results)} field values matching term '{term}'")
            
            # Format and return the response
            return format_tool_response(True, data=response_data)
        except Exception as model_error:
            # If there's an error in model processing, fall back to a simpler response
            logger.warning(
                f"Error processing field search results through model: {str(model_error)}. Falling back to simple format."
            )
            # Return a simplified response
            return format_tool_response(
                True, 
                data={
                    "items": field_results,
                    "count": len(field_results),
                    "next_cursor": next_cursor
                }
            )
        
    except PipedriveAPIError as e:
        error_msg = f"Error searching field in Pipedrive: {str(e)}"
        response_data = getattr(e, 'response_data', None)
        logger.error(
            f"PipedriveAPIError in tool 'search_item_field_in_pipedrive' for term '{term}': {str(e)} - Response Data: {response_data}"
        )
        return format_tool_response(False, error_message=error_msg, data=response_data)
    except ValueError as e:
        error_msg = f"Invalid parameter: {str(e)}"
        logger.error(f"ValueError in tool 'search_item_field_in_pipedrive': {str(e)}")
        return format_tool_response(False, error_message=error_msg)
    except Exception as e:
        error_msg = f"An unexpected error occurred during field search"
        logger.exception(
            f"Unexpected error in tool 'search_item_field_in_pipedrive' for term '{term}': {str(e)}"
        )
        return format_tool_response(False, error_message=error_msg)