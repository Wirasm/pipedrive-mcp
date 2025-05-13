from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("delete_deal_from_pipedrive")
async def delete_deal_from_pipedrive(
    ctx: Context,
    id_str: str,
) -> str:
    """Deletes a deal from the Pipedrive CRM.

    This tool marks a deal as deleted in Pipedrive. The deal will initially be moved to 
    the "deleted" state and can be restored within 30 days. After 30 days, the deal will 
    be permanently deleted from Pipedrive's servers.
    
    Format requirements:
    - id_str: Required numeric ID of the deal to delete (e.g. "123")
    
    Important Considerations:
    - Deleting a deal cannot be undone after 30 days
    - Any products associated with the deal will be detached
    - Deal followers will be removed
    - Activities linked to the deal will remain but will no longer show the deal association
    
    Example usage:
    ```
    delete_deal_from_pipedrive(
        id_str="123"
    )
    ```

    args:
    ctx: Context
    id_str: str - The ID of the deal to delete (required)
    """
    logger.debug(
        f"Tool 'delete_deal_from_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string ID to integer
    deal_id, id_error = convert_id_string(id_str, "deal_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)

    try:
        # Call the Pipedrive API
        result = await pd_mcp_ctx.pipedrive_client.deals.delete_deal(deal_id=deal_id)

        logger.info(f"Successfully deleted deal with ID: {deal_id}")

        # Return the API response
        return format_tool_response(True, data=result)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'delete_deal_from_pipedrive' for ID '{id_str}': {str(e)}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'delete_deal_from_pipedrive' for ID '{id_str}': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )