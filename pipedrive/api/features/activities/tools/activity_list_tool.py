from typing import Optional, List, Dict, Any

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string, validate_uuid_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list, sanitize_inputs
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("activities")
async def list_activities_from_pipedrive(
    ctx: Context,
    limit_str: Optional[str] = "100",
    cursor: Optional[str] = None,
    filter_id_str: Optional[str] = None,
    owner_id_str: Optional[str] = None,
    deal_id_str: Optional[str] = None,
    lead_id_str: Optional[str] = None,
    person_id_str: Optional[str] = None,
    org_id_str: Optional[str] = None,
    updated_since: Optional[str] = None,
    updated_until: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = None,
    include_fields_str: Optional[str] = None
) -> str:
    """Lists activities from Pipedrive CRM with filtering and pagination.

    This tool retrieves a list of activities with optional filtering and pagination 
    capabilities. Results can be filtered by various criteria such as owner, 
    associated deals, persons, organizations, leads, and update times. Use the cursor 
    parameter for retrieving subsequent pages of results.

    Format requirements:
    - limit_str: Numeric string between 1-500 (e.g., "100")
    - filter_id_str, owner_id_str, deal_id_str, person_id_str, org_id_str: Must be numeric strings (e.g., "123")
    - lead_id_str: Must be a UUID string (e.g., "123e4567-e89b-12d3-a456-426614174000")
    - updated_since, updated_until: Must be in RFC3339 format (e.g., "2025-01-01T10:20:00Z")
    - sort_by: Must be one of: "id", "update_time", "add_time"
    - sort_direction: Must be one of: "asc", "desc"
    - include_fields_str: Comma-separated list of additional fields to include (e.g., "field1,field2")

    Example:
    ```
    list_activities_from_pipedrive(
        limit_str="50",
        owner_id_str="123",
        updated_since="2025-01-01T00:00:00Z",
        sort_by="update_time",
        sort_direction="desc",
        include_fields_str="subject,note"
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        limit_str: Maximum number of results to return (default "100", max "500")
        cursor: Pagination cursor for the next page
        filter_id_str: Numeric ID of the filter to apply
        owner_id_str: Numeric ID of the activity owner to filter by
        deal_id_str: Numeric ID of the deal to filter by
        lead_id_str: UUID string of the lead to filter by
        person_id_str: Numeric ID of the person to filter by
        org_id_str: Numeric ID of the organization to filter by
        updated_since: Filter by update time, in RFC3339 format (e.g., "2025-01-01T10:20:00Z")
        updated_until: Filter by update time, in RFC3339 format (e.g., "2025-01-01T10:20:00Z")
        sort_by: Field to sort by ("id", "update_time", "add_time")
        sort_direction: Sort direction ("asc", "desc")
        include_fields_str: Comma-separated list of additional fields to include

    Returns:
        JSON formatted response with activity list, pagination information, or error message
    """
    logger.info(f"Tool 'list_activities_from_pipedrive' ENTERED with limit={limit_str}, cursor='{cursor}'")
    
    # Sanitize inputs - convert empty strings to None
    inputs = {
        "limit_str": limit_str,
        "cursor": cursor,
        "filter_id_str": filter_id_str,
        "owner_id_str": owner_id_str,
        "deal_id_str": deal_id_str,
        "lead_id_str": lead_id_str,
        "person_id_str": person_id_str,
        "org_id_str": org_id_str,
        "updated_since": updated_since,
        "updated_until": updated_until,
        "sort_by": sort_by,
        "sort_direction": sort_direction,
        "include_fields_str": include_fields_str
    }
    
    sanitized = sanitize_inputs(inputs)
    limit_str = sanitized["limit_str"] 
    cursor = sanitized["cursor"]
    filter_id_str = sanitized["filter_id_str"]
    owner_id_str = sanitized["owner_id_str"]
    deal_id_str = sanitized["deal_id_str"]
    lead_id_str = sanitized["lead_id_str"]
    person_id_str = sanitized["person_id_str"]
    org_id_str = sanitized["org_id_str"]
    updated_since = sanitized["updated_since"]
    updated_until = sanitized["updated_until"]
    sort_by = sanitized["sort_by"]
    sort_direction = sanitized["sort_direction"]
    include_fields_str = sanitized["include_fields_str"]
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Convert limit string to integer
    limit = 100  # Default
    if limit_str:
        try:
            limit = int(limit_str)
            if limit < 1 or limit > 500:
                limit = min(max(limit, 1), 500)  # Clamp between 1 and 500
                logger.warning(f"Limit adjusted to valid range: {limit}")
        except ValueError:
            error_message = f"Invalid limit value: '{limit_str}'. Must be a numeric string between 1 and 500. Example: '100'"
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
    
    # Convert ID strings to integers with proper error handling
    filter_id, filter_id_error = convert_id_string(filter_id_str, "filter_id", "123")
    if filter_id_error:
        logger.error(filter_id_error)
        return format_tool_response(False, error_message=filter_id_error)
    
    owner_id, owner_id_error = convert_id_string(owner_id_str, "owner_id", "123")
    if owner_id_error:
        logger.error(owner_id_error)
        return format_tool_response(False, error_message=owner_id_error)
    
    deal_id, deal_id_error = convert_id_string(deal_id_str, "deal_id", "123")
    if deal_id_error:
        logger.error(deal_id_error)
        return format_tool_response(False, error_message=deal_id_error)
    
    person_id, person_id_error = convert_id_string(person_id_str, "person_id", "123")
    if person_id_error:
        logger.error(person_id_error)
        return format_tool_response(False, error_message=person_id_error)
    
    org_id, org_id_error = convert_id_string(org_id_str, "org_id", "123")
    if org_id_error:
        logger.error(org_id_error)
        return format_tool_response(False, error_message=org_id_error)
    
    # Validate lead_id as UUID
    lead_id, lead_id_error = validate_uuid_string(
        lead_id_str, 
        "lead_id", 
        "123e4567-e89b-12d3-a456-426614174000"
    )
    if lead_id_error:
        logger.error(lead_id_error)
        return format_tool_response(False, error_message=lead_id_error)
    
    # Validate updated_since and updated_until formats if provided
    if updated_since and not updated_since.endswith('Z'):
        error_message = f"Invalid updated_since format: '{updated_since}'. Must be in RFC3339 format. Example: '2025-01-01T10:20:00Z'"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
        
    if updated_until and not updated_until.endswith('Z'):
        error_message = f"Invalid updated_until format: '{updated_until}'. Must be in RFC3339 format. Example: '2025-01-01T10:20:00Z'"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    # Validate sort parameters
    valid_sort_fields = ["id", "update_time", "add_time"]
    if sort_by and sort_by not in valid_sort_fields:
        error_message = f"Invalid sort_by value: '{sort_by}'. Must be one of: {', '.join(valid_sort_fields)}"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    valid_sort_directions = ["asc", "desc"]
    if sort_direction and sort_direction not in valid_sort_directions:
        error_message = f"Invalid sort_direction value: '{sort_direction}'. Must be one of: {', '.join(valid_sort_directions)}"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    # Convert include_fields_str to list
    include_fields = safe_split_to_list(include_fields_str)
    
    try:
        # Call Pipedrive API to list activities
        activities_list, next_cursor = await pd_mcp_ctx.pipedrive_client.activities.list_activities(
            limit=limit,
            cursor=cursor,
            filter_id=filter_id,
            owner_id=owner_id,
            deal_id=deal_id,
            lead_id=lead_id,
            person_id=person_id,
            org_id=org_id,
            updated_since=updated_since,
            updated_until=updated_until,
            sort_by=sort_by,
            sort_direction=sort_direction,
            include_fields=include_fields
        )
        
        logger.info(f"Successfully retrieved {len(activities_list)} activities. Next cursor: '{next_cursor}'")
        
        # Return the results with next_cursor in additional_data
        result_data = {
            "items": activities_list,
            "additional_data": {"next_cursor": next_cursor} if next_cursor else {}
        }
        
        return format_tool_response(True, data=result_data)
        
    except PipedriveAPIError as e:
        logger.error(f"Pipedrive API error listing activities: {str(e)}")
        return format_tool_response(False, error_message=f"Pipedrive API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error listing activities: {str(e)}")
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")