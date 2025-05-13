from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string, validate_uuid_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
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
):
    """Lists activities from Pipedrive CRM with filtering and pagination.

    This tool retrieves a list of activities with optional filtering.

    args:
    ctx: Context
    limit_str: Optional[str] = "100" - Maximum number of results to return (default 100, max 500)
    cursor: Optional[str] = None - Pagination cursor for the next page
    filter_id_str: Optional[str] = None - ID of the filter to apply
    owner_id_str: Optional[str] = None - Filter by activity owner ID
    deal_id_str: Optional[str] = None - Filter by associated deal ID
    lead_id_str: Optional[str] = None - Filter by associated lead ID
    person_id_str: Optional[str] = None - Filter by associated person ID
    org_id_str: Optional[str] = None - Filter by associated organization ID
    updated_since: Optional[str] = None - Filter by update time (RFC3339 format, e.g. 2025-01-01T10:20:00Z)
    updated_until: Optional[str] = None - Filter by update time (RFC3339 format, e.g. 2025-01-01T10:20:00Z)
    sort_by: Optional[str] = None - Field to sort by (id, update_time, add_time)
    sort_direction: Optional[str] = None - Sort direction (asc, desc)
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
    """
    logger.info(f"Tool 'list_activities_from_pipedrive' ENTERED with limit={limit_str}, cursor='{cursor}'")
    
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
            logger.warning(f"Invalid limit value: '{limit_str}'. Using default of 100.")
    
    # Convert ID strings to integers
    filter_id, filter_id_error = convert_id_string(filter_id_str, "filter_id")
    if filter_id_error:
        logger.error(filter_id_error)
        return format_tool_response(False, error_message=filter_id_error)
    
    owner_id, owner_id_error = convert_id_string(owner_id_str, "owner_id")
    if owner_id_error:
        logger.error(owner_id_error)
        return format_tool_response(False, error_message=owner_id_error)
    
    deal_id, deal_id_error = convert_id_string(deal_id_str, "deal_id")
    if deal_id_error:
        logger.error(deal_id_error)
        return format_tool_response(False, error_message=deal_id_error)
    
    person_id, person_id_error = convert_id_string(person_id_str, "person_id")
    if person_id_error:
        logger.error(person_id_error)
        return format_tool_response(False, error_message=person_id_error)
    
    org_id, org_id_error = convert_id_string(org_id_str, "org_id")
    if org_id_error:
        logger.error(org_id_error)
        return format_tool_response(False, error_message=org_id_error)
    
    # Validate lead_id as UUID
    lead_id, lead_id_error = validate_uuid_string(lead_id_str, "lead_id")
    if lead_id_error:
        logger.error(lead_id_error)
        return format_tool_response(False, error_message=lead_id_error)
    
    # Validate sort parameters
    if sort_by and sort_by not in ["id", "update_time", "add_time"]:
        error_message = f"Invalid sort_by value: '{sort_by}'. Must be one of: id, update_time, add_time."
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    if sort_direction and sort_direction not in ["asc", "desc"]:
        error_message = f"Invalid sort_direction value: '{sort_direction}'. Must be one of: asc, desc."
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