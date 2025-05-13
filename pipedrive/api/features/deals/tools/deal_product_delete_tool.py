from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("delete_product_from_deal_in_pipedrive")
async def delete_product_from_deal_in_pipedrive(
    ctx: Context,
    id_str: str,
    product_attachment_id_str: str,
) -> str:
    """Removes a product from a deal in Pipedrive CRM.

    This tool removes a product that has been previously attached to a deal. The removal
    affects the deal's value calculation and removes any billing configurations associated 
    with this product-deal association. Note that this is a permanent action that cannot be 
    undone.
    
    Format requirements:
    - id_str: Required numeric ID of the deal (e.g. "123")
    - product_attachment_id_str: Required numeric ID of the product attachment (e.g. "456")
      Note: This is NOT the product ID, but the ID of the specific deal-product association
    
    Important Distinctions:
    - The product_attachment_id is different from the product_id
    - The product_attachment_id is created when a product is added to a deal
    - You can get product_attachment_ids by querying the deal's products
    
    Important Considerations:
    - If the deal has installments, you cannot delete the last enabled product
    - Deal value will automatically update when products are deleted
    - Deletion cannot be undone
    
    Example usage:
    ```
    delete_product_from_deal_in_pipedrive(
        id_str="123",
        product_attachment_id_str="456"
    )
    ```

    args:
    ctx: Context
    id_str: str - The ID of the deal (required)
    product_attachment_id_str: str - The ID of the product attachment to delete (required)
    """
    logger.debug(
        f"Tool 'delete_product_from_deal_in_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', product_attachment_id_str='{product_attachment_id_str}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string IDs to integers
    deal_id, deal_id_error = convert_id_string(id_str, "deal_id")
    if deal_id_error:
        logger.error(deal_id_error)
        return format_tool_response(False, error_message=deal_id_error)

    product_attachment_id, attachment_id_error = convert_id_string(
        product_attachment_id_str, "product_attachment_id"
    )
    if attachment_id_error:
        logger.error(attachment_id_error)
        return format_tool_response(False, error_message=attachment_id_error)

    try:
        # Call the Pipedrive API
        result = await pd_mcp_ctx.pipedrive_client.deals.delete_product_from_deal(
            deal_id=deal_id,
            product_attachment_id=product_attachment_id
        )

        logger.info(
            f"Successfully deleted product {product_attachment_id} from deal {deal_id}"
        )

        # Return the API response
        return format_tool_response(True, data=result)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'delete_product_from_deal_in_pipedrive': {str(e)}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'delete_product_from_deal_in_pipedrive': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )