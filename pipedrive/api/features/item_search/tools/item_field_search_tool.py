from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.item_search.models.search_result import FieldSearchResults
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list, sanitize_inputs
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("item_search")
async def search_item_field_in_pipedrive(
    ctx: Context,
    term: str,
    entity_type: str,
    field: str,
    match: str = "exact",
    limit_str: Optional[str] = "100",
    cursor: Optional[str] = None,
) -> str:
    """Performs a field-specific search across a particular entity type in Pipedrive CRM.
    
    This tool allows you to search for values in a specific field within deals, leads, persons, 
    organizations, products, or projects. It's particularly useful for finding exact matches, 
    retrieving autocomplete values, or searching for specific field values within a given entity type.
    
    Format requirements:
    - term: Minimum 2 characters (or 1 character if match is "exact")
      Case-insensitive
      Example: "smith" will search for names containing "smith"
    - entity_type: The type of entity to search in
      Valid values: "deal", "lead", "person", "organization", "product", "project"
      Example: "person"
    - field: The field key to search within
      Common fields include: "name", "title", "email", etc.
      Field keys can be obtained from the Pipedrive API
      Only the following custom field types are searchable: address, varchar, text, varchar_auto, double, monetary and phone
      Example: "name"
    - match: The type of match to perform against the term
      Default: "exact"
      Options:
        - "exact": Only exact matches (case insensitive)
        - "beginning": Matches starting with the term
        - "middle": Matches containing the term
      
      Examples:
      For a field value "Smith":
        - "exact" match with term "Smith" will find it
        - "beginning" match with term "Sm" will find it
        - "middle" match with term "mi" will find it
    - limit_str: Maximum number of results to return per page
      Default: "100"
      Maximum value: "500"
      Example: "50"
    - cursor: Pagination cursor for fetching the next page of results
      Obtained from previous search result response
      Example: "eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
    
    Example:
    ```
    search_item_field_in_pipedrive(
        term="smith",
        entity_type="person",
        field="name",
        match="beginning",
        limit_str="50"
    )
    ```
    
    Args:
        ctx: Context object provided by the MCP server
        term: The search term to look for (min 2 chars, or 1 if match is 'exact')
        entity_type: The type of entity to search (deal, lead, person, organization, product, project)
        field: The field key to search in
        match: Type of match: exact, beginning, or middle
        limit_str: Maximum number of results to return per page (max 500)
        cursor: Pagination cursor for fetching the next page of results
    
    Returns:
        JSON formatted response with field search results or error message. When successful, the response includes:
        - A list of matching items with their IDs and names
        - Pagination information (next_cursor) if more results are available
    """
    logger.debug(
        f"Tool 'search_item_field_in_pipedrive' ENTERED with raw args: "
        f"term='{term}', entity_type='{entity_type}', field='{field}', "
        f"match='{match}', limit_str='{limit_str}', cursor='{cursor}'"
    )

    # Sanitize inputs - convert empty strings to None
    inputs = {
        "term": term,
        "entity_type": entity_type,
        "field": field,
        "match": match,
        "limit_str": limit_str,
        "cursor": cursor
    }
    
    sanitized = sanitize_inputs(inputs)
    term = sanitized["term"]
    entity_type = sanitized["entity_type"]
    field = sanitized["field"]
    match = sanitized["match"]
    limit_str = sanitized["limit_str"]
    cursor = sanitized["cursor"]
    
    # Trim strings
    if term:
        term = term.strip()
    if entity_type:
        entity_type = entity_type.strip()
    if field:
        field = field.strip()
    if match:
        match = match.strip()
        
    # Validate required parameters
    if not term:
        error_msg = "Search term cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    # For exact match, we need at least 1 character
    term_length = len(term)
    if match == "exact" and term_length < 1:
        error_msg = "Search term must be at least 1 character for exact matching"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    # For non-exact matches, we need at least 2 characters
    if match != "exact" and term_length < 2:
        error_msg = (f"Search term must be at least 2 characters for '{match}' matching. "
                    f"Current term '{term}' is {term_length} character(s).")
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    if not entity_type:
        error_msg = "Entity type cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    if not field:
        error_msg = "Field key cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Validate entity_type
    valid_entity_types = ["deal", "person", "organization", "product", "lead", "project"]
    if entity_type not in valid_entity_types:
        error_msg = (f"Invalid entity type: '{entity_type}'. Must be one of: "
                    f"{', '.join(valid_entity_types)}. Example: 'person'")
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    # Validate match type
    valid_match_types = ["exact", "beginning", "middle"]
    if match not in valid_match_types:
        error_msg = (f"Invalid match type: '{match}'. Must be one of: "
                    f"{', '.join(valid_match_types)}. Example: 'beginning'")
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)
    
    # Field validation note - we don't validate field keys here as they are dynamic
    # and depend on the entity type. The API will validate them.
    logger.debug(f"Using field key: '{field}'. Note that available field keys depend on entity type.")

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
                    "message": (f"No values found for field '{field}' matching '{term}'. "
                               f"Try a different match type (e.g., 'beginning' or 'middle'), "
                               f"check the field key, or use a less specific term.")
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
        
        # Add specific guidance for common field search errors
        if "search term too short" in str(e).lower():
            error_msg += ". Search term must be at least 2 characters (or 1 character if match is 'exact')."
        elif "invalid field" in str(e).lower():
            error_msg += f". The field key '{field}' may not be valid for entity type '{entity_type}'. Check available fields for this entity type."
        elif "not found" in str(e).lower() and "field" in str(e).lower():
            error_msg += f". Field '{field}' was not found for entity type '{entity_type}'. Check the field key."
        
        return format_tool_response(False, error_message=error_msg, data=response_data)
    except ValueError as e:
        error_msg = f"Invalid parameter: {str(e)}"
        logger.error(f"ValueError in tool 'search_item_field_in_pipedrive': {str(e)}")
        return format_tool_response(False, error_message=error_msg)
    except Exception as e:
        error_msg = f"An unexpected error occurred during field search: {str(e)}"
        logger.exception(
            f"Unexpected error in tool 'search_item_field_in_pipedrive' for term '{term}': {str(e)}"
        )
        return format_tool_response(False, error_message=error_msg)