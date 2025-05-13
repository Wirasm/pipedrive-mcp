from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def list_organizations_from_pipedrive(
    ctx: Context,
    limit_str: Optional[str] = "100",
    cursor: Optional[str] = None,
    filter_id_str: Optional[str] = None,
    owner_id_str: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = None,
    include_fields_str: Optional[str] = None,
    custom_fields_str: Optional[str] = None,
    updated_since: Optional[str] = None,
    updated_until: Optional[str] = None,
) -> str:
    """
    Lists organizations from Pipedrive CRM with filtering and pagination.
    
    Returns a list of organizations with optional filtering based on various criteria.
    Results can be paginated using the cursor parameter.
    
    args:
    ctx: Context
    limit_str: Optional[str] = "100" - Maximum number of results to return (max 500)
    
    cursor: Optional[str] = None - Pagination cursor for retrieving the next page
    
    filter_id_str: Optional[str] = None - ID of the filter to apply
    
    owner_id_str: Optional[str] = None - Filter by owner user ID
    
    sort_by: Optional[str] = None - Field to sort by (id, update_time, add_time)
    
    sort_direction: Optional[str] = None - Sort direction (asc or desc)
    
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
    
    custom_fields_str: Optional[str] = None - Comma-separated list of custom fields to include
    
    updated_since: Optional[str] = None - Filter by update time (RFC3339 format, e.g. 2025-01-01T10:20:00Z)
    
    updated_until: Optional[str] = None - Filter by update time (RFC3339 format)
    """
    logger.debug(
        f"Tool 'list_organizations_from_pipedrive' ENTERED with raw args: "
        f"limit_str='{limit_str}', cursor='{cursor}', filter_id_str='{filter_id_str}', "
        f"owner_id_str='{owner_id_str}', sort_by='{sort_by}', sort_direction='{sort_direction}', "
        f"include_fields_str='{include_fields_str}', custom_fields_str='{custom_fields_str}', "
        f"updated_since='{updated_since}', updated_until='{updated_until}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string parameters to their appropriate types
    limit, limit_error = convert_id_string(limit_str, "limit")
    if limit_error:
        logger.error(limit_error)
        return format_tool_response(False, error_message=limit_error)

    filter_id, filter_id_error = convert_id_string(filter_id_str, "filter_id")
    if filter_id_error:
        logger.error(filter_id_error)
        return format_tool_response(False, error_message=filter_id_error)

    owner_id, owner_id_error = convert_id_string(owner_id_str, "owner_id")
    if owner_id_error:
        logger.error(owner_id_error)
        return format_tool_response(False, error_message=owner_id_error)

    # Parse comma-separated strings to lists
    include_fields = safe_split_to_list(include_fields_str)
    custom_fields_keys = safe_split_to_list(custom_fields_str)

    try:
        # Call the Pipedrive API to list organizations
        organizations, next_cursor = await pd_mcp_ctx.pipedrive_client.organizations.list_organizations(
            limit=limit or 100,  # Default to 100 if None
            cursor=cursor,
            filter_id=filter_id,
            owner_id=owner_id,
            sort_by=sort_by,
            sort_direction=sort_direction,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys,
            updated_since=updated_since,
            updated_until=updated_until
        )

        logger.info(f"Successfully listed {len(organizations)} organizations")
        
        # Format the response with pagination information
        response_data = {
            "items": organizations,
            "next_cursor": next_cursor,
            "count": len(organizations)
        }
        
        return format_tool_response(True, data=response_data)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'list_organizations_from_pipedrive': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'list_organizations_from_pipedrive': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )