from typing import Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.activities.models.activity_type import ActivityType
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("activities")
async def create_activity_type_in_pipedrive(
    ctx: Context,
    name: str,
    icon_key: str,
    color: Optional[str] = None,
    order_nr_str: Optional[str] = None
):
    """Creates a new activity type in Pipedrive CRM.

    This tool creates a new custom activity type that can be used when creating activities.

    args:
    ctx: Context
    name: str - The name of the activity type
    icon_key: str - The icon key for the activity type (e.g., call, meeting, task, etc.)
    color: Optional[str] = None - The color for the activity type in 6-character HEX format (e.g., FFFFFF)
    order_nr_str: Optional[str] = None - The order number for sorting activity types (integer)
    """
    logger.info(f"Tool 'create_activity_type_in_pipedrive' ENTERED with raw args: name='{name}', icon_key='{icon_key}'")
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Sanitize empty strings to None
    name = name.strip() if name else name
    icon_key = icon_key.strip() if icon_key else icon_key
    color = None if color == "" else color
    order_nr_str = None if order_nr_str == "" else order_nr_str
    
    # Convert order_nr_str to integer if provided
    order_nr = None
    if order_nr_str:
        try:
            order_nr = int(order_nr_str)
            if order_nr < 0:
                logger.warning(f"Invalid order_nr value: {order_nr}. Must be a positive integer. Setting to None.")
                order_nr = None
        except ValueError:
            error_message = f"Invalid order_nr format: '{order_nr_str}'. Must be a valid integer."
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
    
    try:
        # Validate inputs with Pydantic model
        activity_type = ActivityType(
            name=name,
            icon_key=icon_key,
            color=color,
            order_nr=order_nr
        )
        
        # Convert model to API-compatible dict
        payload = activity_type.to_api_dict()
        
        logger.debug(f"Prepared payload for activity type creation: {payload}")
        
        # Call the Pipedrive API to create the activity type
        created_activity_type = await pd_mcp_ctx.pipedrive_client.activities.create_activity_type(
            name=name,
            icon_key=icon_key,
            color=color,
            order_nr=order_nr
        )
        
        logger.info(f"Successfully created activity type '{name}' with ID: {created_activity_type.get('id')}")
        
        # Return the API response
        return format_tool_response(True, data=created_activity_type)
        
    except ValidationError as e:
        logger.error(f"Validation error creating activity type '{name}': {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(f"Pipedrive API error creating activity type '{name}': {str(e)}")
        return format_tool_response(False, error_message=f"Pipedrive API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error creating activity type '{name}': {str(e)}")
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")