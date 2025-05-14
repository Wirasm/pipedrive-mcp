from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("persons")
async def delete_person_from_pipedrive(
    ctx: Context,
    id_str: str,
) -> str:
    """Deletes a person from the Pipedrive CRM.

    This tool marks a person as deleted. After 30 days, the person will be 
    permanently deleted from Pipedrive. This operation cannot be undone through
    the API, so use it carefully.

    Format requirements:
        - id_str: Person ID as a string (required, will be converted to integer)

    Example:
        delete_person_from_pipedrive(
            id_str="123"
        )

    Args:
        ctx: Context object containing the Pipedrive client
        id_str: ID of the person to delete (required)

    Returns:
        JSON string containing success status or error message.
        When successful, the response includes:
        - id: The ID of the deleted person
        - message: Confirmation that the person was deleted
    """
    logger.debug(
        f"Tool 'delete_person_from_pipedrive' ENTERED with raw args: id_str='{id_str}'"
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

    try:
        # Call the Pipedrive API using the persons client
        delete_result = await pd_mcp_ctx.pipedrive_client.persons.delete_person(
            person_id=person_id
        )
        
        # Check if the delete operation was successful
        if "id" in delete_result and "error_details" not in delete_result:
            logger.info(f"Successfully deleted person with ID: {person_id}")
            return format_tool_response(
                True, 
                data={"id": person_id, "message": f"Person with ID {person_id} was successfully deleted"}
            )
        else:
            # If there's an error_details key, something went wrong
            logger.warning(f"Failed to delete person with ID {person_id}: {delete_result}")
            return format_tool_response(
                False, 
                error_message=f"Failed to delete person with ID {person_id}",
                data=delete_result
            )
        
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'delete_person_from_pipedrive' for ID {person_id}: {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'delete_person_from_pipedrive' for ID {person_id}: {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )