from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.leads.models.lead import Lead
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("list_leads_from_pipedrive")
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
    """
    List leads from Pipedrive with filtering and pagination.
    
    Args:
        limit: 
            Maximum number of results to return (default: 100).
            
        start: 
            Pagination start offset.
            
        archived_status: 
            Filter by archive status (archived, not_archived, all).
            
        owner_id: 
            Filter by owner user ID.
            
        person_id: 
            Filter by associated person ID.
            
        organization_id: 
            Filter by associated organization ID.
            
        filter_id: 
            ID of the filter to apply.
            
        sort: 
            Field to sort by with direction (e.g., "title ASC" or "add_time DESC").
    
    Returns:
        JSON response with a list of leads and pagination information.
    """
    logger.info(f"Listing leads with limit: {limit}, start: {start}")
    
    # Convert string parameters to appropriate types
    try:
        limit_int = int(limit) if limit else 100
        start_int = int(start) if start else None
    except ValueError:
        return format_tool_response(
            False, 
            error_message="Invalid pagination parameters. Limit and start must be integers."
        )
    
    # Validate archived_status
    if archived_status and archived_status not in ["archived", "not_archived", "all"]:
        return format_tool_response(
            False,
            error_message="Invalid archived_status. Must be one of: archived, not_archived, all"
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
        return format_tool_response(False, error_message=str(e))
    except Exception as e:
        # Handle other errors
        logger.error(f"Error listing leads: {str(e)}")
        return format_tool_response(False, error_message=f"Failed to list leads: {str(e)}")