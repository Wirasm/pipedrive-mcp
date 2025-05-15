from typing import Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.activities.models.activity_type import ActivityType
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response, sanitize_inputs
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("activities")
async def create_activity_type_in_pipedrive(
    ctx: Context,
    name: str,
    icon_key: str,
    color: Optional[str] = None,
    order_nr: Optional[str] = None
) -> str:
    """Creates a new activity type in Pipedrive CRM.

    This tool creates a new custom activity type that can be used when creating activities.
    Activity types define the different kinds of activities that can be logged in Pipedrive
    (e.g., call, meeting, email, etc.). Each activity type has a specific icon and
    can have a custom color.

    Format requirements:
    - name: Name of the activity type (e.g., "Video Call")
    - icon_key: Must be one of the valid Pipedrive icon keys (e.g., "call", "meeting", "task")
      Valid values include: task, email, meeting, deadline, call, lunch, calendar, downarrow,
      document, smartphone, camera, scissors, cogs, bubble, uparrow, checkbox, signpost,
      shuffle, addressbook, linegraph, picture, car, world, search, clip, sound, brush,
      key, padlock, pricetag, suitcase, finish, plane, loop, wifi, truck, cart, bulb,
      bell, presentation
    - color: Must be a 6-character HEX color code without the # symbol (e.g., "FFFFFF" for white)
    - order_nr: Order number as a numeric string (e.g., "1") for sorting activity types

    Example:
    ```
    create_activity_type_in_pipedrive(
        name="Video Call",
        icon_key="camera",
        color="FF5500",
        order_nr="1"
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        name: Name of the activity type
        icon_key: Icon key for the activity type
        color: Optional color for the activity type in 6-character HEX format
        order_nr: Optional order number for sorting activity types

    Returns:
        JSON formatted response with the created activity type data or error message
    """
    logger.info(f"Tool 'create_activity_type_in_pipedrive' ENTERED with raw args: name='{name}', icon_key='{icon_key}'")
    
    # Sanitize inputs
    inputs = {"name": name, "icon_key": icon_key, "color": color, "order_nr": order_nr}
    sanitized = sanitize_inputs(inputs)
    name = sanitized["name"]
    icon_key = sanitized["icon_key"]
    color = sanitized["color"]
    order_nr_str = sanitized["order_nr"]
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
    
    # Validate required parameters
    if not name:
        error_message = "Activity type name is required"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
        
    if not icon_key:
        error_message = "Activity type icon_key is required"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
    
    # Convert order_nr_str to integer if provided
    order_nr_int = None
    if order_nr_str:
        try:
            order_nr_int = int(order_nr_str)
            if order_nr_int < 0:
                error_message = f"Invalid order_nr value: {order_nr_int}. Must be a positive integer."
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
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
            order_nr=order_nr_int
        )
        
        # Convert model to API-compatible dict
        payload = activity_type.to_api_dict()
        
        logger.debug(f"Prepared payload for activity type creation: {payload}")
        
        # Call the Pipedrive API to create the activity type
        created_activity_type = await pd_mcp_ctx.pipedrive_client.activities.create_activity_type(
            name=name,
            icon_key=icon_key,
            color=color,
            order_nr=order_nr_int
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