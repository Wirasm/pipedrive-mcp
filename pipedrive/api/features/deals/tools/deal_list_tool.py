from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("list_deals_from_pipedrive")
async def list_deals_from_pipedrive(
    ctx: Context,
    limit_str: Optional[str] = "100",
    cursor: Optional[str] = None,
    filter_id_str: Optional[str] = None,
    owner_id_str: Optional[str] = None,
    person_id_str: Optional[str] = None,
    org_id_str: Optional[str] = None,
    pipeline_id_str: Optional[str] = None,
    stage_id_str: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_direction: Optional[str] = None,
    include_fields_str: Optional[str] = None,
    custom_fields_str: Optional[str] = None,
    updated_since: Optional[str] = None,
    updated_until: Optional[str] = None,
) -> str:
    """Lists deals from Pipedrive CRM with filtering and pagination.

    This tool retrieves a list of deals from Pipedrive with powerful filtering options.
    Results are returned in pages, with cursor-based pagination for handling large result sets.
    You can filter deals by owner, person, organization, pipeline, stage, status, and more.
    
    Format requirements:
    - limit_str: Maximum number of deals to return (1-500, default 100)
    - cursor: Opaque pagination cursor from a previous response
    - *_id_str: Numeric ID strings (e.g. "123")
    - status: One of "open", "won", "lost", or "deleted"
    - sort_by: One of "id", "update_time", or "add_time"
    - sort_direction: Either "asc" or "desc"
    - updated_since/updated_until: RFC3339 format (e.g. "2025-01-01T10:20:00Z")
    
    Pipeline and Stage Filtering:
    - Use pipeline_id_str to filter deals in a specific pipeline
    - Use stage_id_str to filter deals in a specific stage 
    - You can use both together to filter deals that are in a specific stage of a specific pipeline
    
    Including Additional Fields:
    - include_fields_str: Comma-separated list of additional fields to include
      (e.g. "products_count,activities_count,participants_count")
    - custom_fields_str: Comma-separated list of custom field keys to include
    
    Pagination:
    - The response includes a next_cursor value when there are more results
    - To get the next page, pass this cursor value in your next request
    
    Example usage:
    ```
    list_deals_from_pipedrive(
        limit_str="50",
        pipeline_id_str="1",
        status="open",
        sort_by="update_time",
        sort_direction="desc"
    )
    ```

    args:
    ctx: Context
    limit_str: Optional[str] = "100" - Maximum number of results to return (1-500)
    cursor: Optional[str] = None - Pagination cursor for retrieving the next page
    filter_id_str: Optional[str] = None - ID of the filter to apply
    owner_id_str: Optional[str] = None - Filter by owner user ID
    person_id_str: Optional[str] = None - Filter by person ID
    org_id_str: Optional[str] = None - Filter by organization ID
    pipeline_id_str: Optional[str] = None - Filter by pipeline ID
    stage_id_str: Optional[str] = None - Filter by stage ID
    status: Optional[str] = None - Filter by status ("open", "won", "lost", or "deleted")
    sort_by: Optional[str] = None - Field to sort by ("id", "update_time", "add_time")
    sort_direction: Optional[str] = None - Sort direction ("asc" or "desc")
    include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
    custom_fields_str: Optional[str] = None - Comma-separated list of custom fields to include
    updated_since: Optional[str] = None - Filter by update time (RFC3339 format, e.g. "2025-01-01T10:20:00Z")
    updated_until: Optional[str] = None - Filter by update time (RFC3339 format)
    """
    logger.debug(
        f"Tool 'list_deals_from_pipedrive' ENTERED with raw args: "
        f"limit_str='{limit_str}', cursor='{cursor}', filter_id_str='{filter_id_str}', "
        f"owner_id_str='{owner_id_str}', person_id_str='{person_id_str}', "
        f"org_id_str='{org_id_str}', pipeline_id_str='{pipeline_id_str}', "
        f"stage_id_str='{stage_id_str}', status='{status}'"
    )

    # Sanitize empty strings to None
    cursor = None if cursor == "" else cursor
    filter_id_str = None if filter_id_str == "" else filter_id_str
    owner_id_str = None if owner_id_str == "" else owner_id_str
    person_id_str = None if person_id_str == "" else person_id_str
    org_id_str = None if org_id_str == "" else org_id_str
    pipeline_id_str = None if pipeline_id_str == "" else pipeline_id_str
    stage_id_str = None if stage_id_str == "" else stage_id_str
    status = None if status == "" else status
    sort_by = None if sort_by == "" else sort_by
    sort_direction = None if sort_direction == "" else sort_direction
    include_fields_str = None if include_fields_str == "" else include_fields_str
    custom_fields_str = None if custom_fields_str == "" else custom_fields_str
    updated_since = None if updated_since == "" else updated_since
    updated_until = None if updated_until == "" else updated_until

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
        filter_id, filter_id_error = convert_id_string(filter_id_str, "filter_id")
        if filter_id_error:
            logger.error(filter_id_error)
            return format_tool_response(False, error_message=filter_id_error)

        owner_id, owner_id_error = convert_id_string(owner_id_str, "owner_id")
        if owner_id_error:
            logger.error(owner_id_error)
            return format_tool_response(False, error_message=owner_id_error)

        person_id, person_id_error = convert_id_string(person_id_str, "person_id")
        if person_id_error:
            logger.error(person_id_error)
            return format_tool_response(False, error_message=person_id_error)

        org_id, org_id_error = convert_id_string(org_id_str, "org_id")
        if org_id_error:
            logger.error(org_id_error)
            return format_tool_response(False, error_message=org_id_error)

        pipeline_id, pipeline_id_error = convert_id_string(pipeline_id_str, "pipeline_id")
        if pipeline_id_error:
            logger.error(pipeline_id_error)
            return format_tool_response(False, error_message=pipeline_id_error)

        stage_id, stage_id_error = convert_id_string(stage_id_str, "stage_id")
        if stage_id_error:
            logger.error(stage_id_error)
            return format_tool_response(False, error_message=stage_id_error)

        # Convert include_fields and custom_fields from comma-separated strings to lists
        include_fields = None
        if include_fields_str:
            include_fields = [field.strip() for field in include_fields_str.split(",")]

        custom_fields_keys = None
        if custom_fields_str:
            custom_fields_keys = [field.strip() for field in custom_fields_str.split(",")]

        # Call the Pipedrive API
        deals_list, next_cursor = await pd_mcp_ctx.pipedrive_client.deals.list_deals(
            limit=limit,
            cursor=cursor,
            filter_id=filter_id,
            owner_id=owner_id,
            person_id=person_id,
            org_id=org_id,
            pipeline_id=pipeline_id,
            stage_id=stage_id,
            status=status,
            sort_by=sort_by,
            sort_direction=sort_direction,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys,
            updated_since=updated_since,
            updated_until=updated_until,
        )

        logger.info(f"Successfully retrieved {len(deals_list)} deals")

        # Format and return the response with next cursor information
        response_data = {
            "items": deals_list,
            "next_cursor": next_cursor
        }
        return format_tool_response(True, data=response_data)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'list_deals_from_pipedrive': {str(e)}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'list_deals_from_pipedrive': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )