from typing import Optional, List

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("persons")
async def get_person_from_pipedrive(
    ctx: Context,
    id_str: str,
    include_fields_str: Optional[str] = None,
    custom_fields_str: Optional[str] = None,
) -> str:
    """Gets the details of a specific person from Pipedrive CRM.

    This tool retrieves complete information about a person by their ID, with
    options to include additional fields and custom fields in the response.

    Format requirements:
        - id_str: Person ID as a string (required, will be converted to integer)
        - include_fields_str: Optional comma-separated list of additional fields to include:
          Example: "open_deals_count,files_count,activities_count"
          Available fields include:
            - next_activity_id, last_activity_id
            - open_deals_count, closed_deals_count
            - related_open_deals_count, related_closed_deals_count
            - participant_open_deals_count, participant_closed_deals_count
            - email_messages_count
            - activities_count, done_activities_count, undone_activities_count
            - files_count, notes_count, followers_count
            - won_deals_count, lost_deals_count
            - related_won_deals_count, related_lost_deals_count
            - last_incoming_mail_time, last_outgoing_mail_time
        - custom_fields_str: Optional comma-separated list of custom field keys to include
          Example: "customer_type,lead_source"
          Maximum of 15 keys allowed

    Example:
        get_person_from_pipedrive(
            id_str="123",
            include_fields_str="activities_count,files_count",
            custom_fields_str="customer_type,lead_source"
        )

    Args:
        ctx: Context object containing the Pipedrive client
        id_str: ID of the person to retrieve (required)
        include_fields_str: Comma-separated list of additional fields to include
        custom_fields_str: Comma-separated list of custom field keys to include (max 15)

    Returns:
        JSON string containing success status and person data or error message.
        When successful, the response includes all standard person fields such as:
        - name: Person's full name
        - emails: List of email addresses (each with value, label, and primary flag)
        - phones: List of phone numbers (each with value, label, and primary flag)
        - org_id: ID of the linked organization (if any)
        - owner_id: ID of the user who owns this person
        - visible_to: Visibility setting (1=Owner only, 2=Owner's group, 3=Entire company)
        - custom_fields: Any requested custom fields
    """
    logger.debug(
        f"Tool 'get_person_from_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', include_fields_str='{include_fields_str}', "
        f"custom_fields_str='{custom_fields_str}'"
    )

    # Validate that person ID is provided
    if not id_str:
        error_msg = "Person ID is required"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string ID to integer using our utility function
    person_id, id_error = convert_id_string(id_str, "person_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)

    # Process include_fields if provided
    include_fields: Optional[List[str]] = None
    if include_fields_str and include_fields_str.strip():
        include_fields = [field.strip() for field in include_fields_str.split(",") if field.strip()]
        
        # Validate the maximum number of include fields
        if len(include_fields) > 25:  # arbitrary limit to prevent abuse
            error_msg = f"Too many include_fields provided: {len(include_fields)}. Please limit to 25 fields."
            logger.error(error_msg)
            return format_tool_response(False, error_message=error_msg)
            
        logger.debug(f"Including additional fields: {include_fields}")

    # Process custom_fields if provided
    custom_fields_keys: Optional[List[str]] = None
    if custom_fields_str and custom_fields_str.strip():
        custom_fields_keys = [field.strip() for field in custom_fields_str.split(",") if field.strip()]
        
        # Validate the maximum number of custom fields (API limit is 15)
        if len(custom_fields_keys) > 15:
            error_msg = f"Too many custom fields provided: {len(custom_fields_keys)}. API limit is 15 keys."
            logger.error(error_msg)
            return format_tool_response(False, error_message=error_msg)
            
        logger.debug(f"Including custom fields: {custom_fields_keys}")

    try:
        # Call the Pipedrive API using the persons client
        person_data = await pd_mcp_ctx.pipedrive_client.persons.get_person(
            person_id=person_id,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys
        )
        
        if not person_data:
            logger.warning(f"Person with ID {person_id} not found")
            return format_tool_response(
                False, error_message=f"Person with ID {person_id} not found"
            )
        
        logger.info(f"Successfully retrieved person with ID: {person_id}")
        
        # Return the API response
        return format_tool_response(True, data=person_data)
        
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'get_person_from_pipedrive' for ID {person_id}: {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'get_person_from_pipedrive' for ID {person_id}: {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )