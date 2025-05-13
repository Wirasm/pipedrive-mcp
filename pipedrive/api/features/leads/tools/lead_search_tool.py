from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.leads.models.lead import Lead
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("search_leads_in_pipedrive")
async def search_leads_in_pipedrive(
    ctx: Context,
    term: str,
    fields: Optional[str] = None,
    exact_match: Optional[str] = "false",
    person_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    include_fields: Optional[str] = None,
    limit: Optional[str] = "100",
    cursor: Optional[str] = None,
) -> str:
    """
    Search for leads in Pipedrive by title, notes, and/or custom fields.
    
    Args:
        term: 
            The search term to look for (min 2 chars, or 1 with exact_match).
            
        fields: 
            Comma-separated list of fields to search in (title, notes, custom_fields).
            
        exact_match: 
            When "true", only exact matches are returned (default: "false").
            
        person_id: 
            Filter leads by person ID.
            
        organization_id: 
            Filter leads by organization ID.
            
        include_fields: 
            Comma-separated list of additional fields to include in results.
            
        limit: 
            Maximum number of results to return (max 500, default: 100).
            
        cursor: 
            Pagination cursor for retrieving additional results.
    
    Returns:
        JSON response with search results and pagination information.
    """
    logger.info(f"Searching leads with term: {term}")
    
    # Validate required parameters
    if not term:
        return format_tool_response(False, error_message="Search term cannot be empty")
    
    # Convert boolean parameters
    exact_match_bool = exact_match.lower() == "true"
    
    # Validate term length based on exact_match
    if not exact_match_bool and len(term) < 2:
        return format_tool_response(
            False, 
            error_message="Search term must be at least 2 characters long when exact_match is false"
        )
    
    if exact_match_bool and len(term) < 1:
        return format_tool_response(
            False, 
            error_message="Search term must be at least 1 character long when exact_match is true"
        )
    
    # Convert numeric parameters
    try:
        limit_int = int(limit) if limit else 100
        if limit_int < 1 or limit_int > 500:
            return format_tool_response(
                False, 
                error_message="Limit must be between 1 and 500"
            )
    except ValueError:
        return format_tool_response(
            False, 
            error_message="Invalid limit parameter. Must be an integer."
        )
    
    # Convert ID parameters
    person_id_int = None
    if person_id:
        person_id_int, error = convert_id_string(person_id, "person_id")
        if error:
            return format_tool_response(False, error_message=error)
    
    organization_id_int = None
    if organization_id:
        organization_id_int, error = convert_id_string(organization_id, "organization_id")
        if error:
            return format_tool_response(False, error_message=error)
    
    # Process comma-separated lists
    fields_list = safe_split_to_list(fields)
    include_fields_list = safe_split_to_list(include_fields)
    
    try:
        # Use the Pipedrive client from the context
        pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
        client = pd_mcp_ctx.pipedrive_client
        
        try:
            results, next_cursor = await client.lead_client.search_leads(
                term=term,
                fields=fields_list,
                exact_match=exact_match_bool,
                person_id=person_id_int,
                organization_id=organization_id_int,
                include_fields=include_fields_list,
                limit=limit_int,
                cursor=cursor,
            )
            
            # Format the response data
            leads_data = []
            for result in results:
                try:
                    # Extract lead data from the search result
                    lead_data = result.get("item", {})
                    if lead_data:
                        # Add any top-level fields that might be useful
                        lead_data["result_score"] = result.get("result_score")
                        
                        # Try to convert to a Lead model for consistent formatting
                        try:
                            lead_model = Lead.from_api_dict(lead_data)
                            leads_data.append(lead_model.model_dump())
                        except Exception as e:
                            # If conversion fails, use the raw data
                            logger.warning(f"Error converting lead search result: {str(e)}")
                            leads_data.append(lead_data)
                except Exception as e:
                    logger.warning(f"Error processing search result: {str(e)}")
                    # Include the raw result if we can't parse it
                    leads_data.append(result)
            
            # Prepare the response with pagination info
            response_data = {
                "leads": leads_data,
                "pagination": {
                    "next_cursor": next_cursor,
                    "more_items_available": next_cursor is not None
                }
            }
            
            return format_tool_response(True, data=response_data)
            
        except PipedriveAPIError as e:
            return format_tool_response(
                False, 
                error_message=f"Pipedrive API error: {str(e)}"
            )
            
    except ValueError as e:
        # Handle validation errors
        return format_tool_response(False, error_message=str(e))
    except Exception as e:
        # Handle other errors
        logger.error(f"Error searching leads: {str(e)}")
        return format_tool_response(False, error_message=f"Failed to search leads: {str(e)}")