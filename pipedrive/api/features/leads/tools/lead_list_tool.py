from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.leads.models.lead import Lead
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("leads")
async def list_leads_from_pipedrive(
    ctx: Context,
    limit: Optional[str] = "100",
    start: Optional[str] = None,
    archived_status: Optional[str] = None,
    owner_id: Optional[str] = None,
    person_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    filter_id: Optional[str] = None,
    sort: Optional[str] = None,
) -> str:
    """Lists leads from Pipedrive with filtering and pagination options.
    
    This tool retrieves a paginated list of leads from Pipedrive. You can filter the results by
    various criteria such as owner, associated person or organization, archive status, and more.
    The results include complete lead details along with pagination information.
    
    Format requirements:
        - limit: Maximum number of leads to return (integer as string, default: 100)
        - start: Pagination offset (integer as string)
        - archived_status: One of: "archived", "not_archived", "all"
        - owner_id: Owner user ID as string (will be converted to integer)
        - person_id: Associated person ID as string (will be converted to integer)
        - organization_id: Associated organization ID as string (will be converted to integer) 
        - filter_id: Filter ID as string (will be converted to integer)
        - sort: Sorting specification as string in format "field_name direction"
          Valid fields: id, title, owner_id, creator_id, was_seen, expected_close_date, add_time, update_time
          Valid directions: ASC, DESC
          Examples: "title ASC", "add_time DESC"
    
    Example:
        list_leads_from_pipedrive(
            limit="50",
            archived_status="not_archived",
            owner_id="123",
            sort="add_time DESC"
        )
    
    Args:
        ctx: Context object containing the Pipedrive client
        limit: Maximum number of results to return (default: 100)
        start: Pagination start offset
        archived_status: Filter by archive status (archived, not_archived, all)
        owner_id: Filter by owner user ID
        person_id: Filter by associated person ID
        organization_id: Filter by associated organization ID
        filter_id: ID of the filter to apply
        sort: Field to sort by with direction (e.g., "title ASC" or "add_time DESC")
    
    Returns:
        JSON string containing success status with leads list and pagination info, or error message.
    """
    logger.debug(
        f"Tool 'list_leads_from_pipedrive' ENTERED with raw args: "
        f"limit='{limit}', start='{start}', archived_status='{archived_status}', "
        f"owner_id='{owner_id}', person_id='{person_id}', organization_id='{organization_id}', "
        f"filter_id='{filter_id}', sort='{sort}'"
    )
    
    # Sanitize empty strings to None
    limit = None if limit == "" else limit
    start = None if start == "" else start
    archived_status = None if archived_status == "" else archived_status
    owner_id = None if owner_id == "" else owner_id
    person_id = None if person_id == "" else person_id
    organization_id = None if organization_id == "" else organization_id
    filter_id = None if filter_id == "" else filter_id
    sort = None if sort == "" else sort
    
    # Convert string parameters to appropriate types
    try:
        limit_int = int(limit) if limit else 100
        if limit_int < 1:
            return format_tool_response(
                False, 
                error_message=f"Invalid limit: {limit}. Must be a positive integer."
            )
        if limit_int > 500:
            # API typically has a max limit, usually capping at 500 items
            logger.warning(f"Large limit value: {limit_int}. API may cap results.")
            
        start_int = int(start) if start else None
        if start_int is not None and start_int < 0:
            return format_tool_response(
                False, 
                error_message=f"Invalid start: {start}. Must be a non-negative integer."
            )
    except ValueError:
        return format_tool_response(
            False, 
            error_message="Invalid pagination parameters. Limit and start must be integers (e.g., '100', '50')."
        )
    
    # Validate archived_status
    if archived_status and archived_status not in ["archived", "not_archived", "all"]:
        return format_tool_response(
            False,
            error_message=f"Invalid archived_status: '{archived_status}'. Must be one of: archived, not_archived, all"
        )
        
    # Validate sort parameter if provided
    if sort:
        # Check if the sort format is valid
        sort_parts = sort.split()
        if len(sort_parts) != 2:
            return format_tool_response(
                False,
                error_message=f"Invalid sort format: '{sort}'. Must be in format: 'field_name direction' (e.g., 'title ASC')"
            )
            
        field_name, direction = sort_parts
        valid_fields = ["id", "title", "owner_id", "creator_id", "was_seen", 
                      "expected_close_date", "add_time", "update_time", "next_activity_id"]
        valid_directions = ["ASC", "DESC"]
        
        if field_name not in valid_fields:
            return format_tool_response(
                False,
                error_message=f"Invalid sort field: '{field_name}'. Must be one of: {', '.join(valid_fields)}"
            )
            
        if direction.upper() not in valid_directions:
            return format_tool_response(
                False,
                error_message=f"Invalid sort direction: '{direction}'. Must be one of: {', '.join(valid_directions)}"
            )
    
    # Convert ID parameters to integers
    owner_id_int = None
    if owner_id:
        owner_id_int, error = convert_id_string(owner_id, "owner_id")
        if error:
            return format_tool_response(False, error_message=error)
    
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
    
    filter_id_int = None
    if filter_id:
        filter_id_int, error = convert_id_string(filter_id, "filter_id")
        if error:
            return format_tool_response(False, error_message=error)
    
    try:
        # Use the Pipedrive client from the context
        pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
        client = pd_mcp_ctx.pipedrive_client
        
        try:
            leads_list, total_count, next_start = await client.lead_client.list_leads(
                limit=limit_int,
                start=start_int,
                archived_status=archived_status,
                owner_id=owner_id_int,
                person_id=person_id_int,
                organization_id=organization_id_int,
                filter_id=filter_id_int,
                sort=sort,
            )
            
            # Convert each lead to a Lead model for consistent formatting
            leads_data = []
            for lead_data in leads_list:
                try:
                    lead_model = Lead.from_api_dict(lead_data)
                    leads_data.append(lead_model.model_dump())
                except Exception as e:
                    logger.warning(f"Error processing lead data: {str(e)}")
                    # Include the raw data if we can't parse it
                    leads_data.append(lead_data)
            
            # Prepare the response with pagination info
            response_data = {
                "leads": leads_data,
                "pagination": {
                    "total_count": total_count,
                    "start": start_int or 0,
                    "limit": limit_int,
                    "next_start": next_start,
                    "more_items_available": next_start > 0
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
        logger.error(f"Validation error listing leads: {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'list_leads_from_pipedrive': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        # Handle other errors
        logger.exception(
            f"Unexpected error in tool 'list_leads_from_pipedrive': {str(e)}"
        )
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")