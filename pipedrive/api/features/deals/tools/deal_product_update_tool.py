from typing import Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def update_product_in_deal_in_pipedrive(
    ctx: Context,
    id_str: str,
    product_attachment_id_str: str,
    item_price: Optional[str] = None,
    quantity: Optional[str] = None,
    tax: Optional[str] = None,
    comments: Optional[str] = None,
    discount: Optional[str] = None,
    discount_type: Optional[str] = None,
    tax_method: Optional[str] = None,
    is_enabled: Optional[bool] = None,
    product_variation_id_str: Optional[str] = None,
    billing_frequency: Optional[str] = None,
    billing_frequency_cycles: Optional[str] = None,
    billing_start_date: Optional[str] = None,
) -> str:
    """Updates a product attached to a deal in Pipedrive CRM.

    This tool requires the deal ID and product attachment ID, and at least
    one field to update. It allows updating properties like price, quantity,
    tax, discount, and billing options.

    args:
    ctx: Context
    id_str: str - The ID of the deal
    product_attachment_id_str: str - The ID of the product attachment to update
    item_price: Optional[str] = None - The updated price of the product
    quantity: Optional[str] = None - The updated quantity of the product
    tax: Optional[str] = None - The updated tax value
    comments: Optional[str] = None - Updated comments about the product
    discount: Optional[str] = None - The updated discount value
    discount_type: Optional[str] = None - Updated discount type (percentage or amount)
    tax_method: Optional[str] = None - Updated tax method (inclusive, exclusive, none)
    is_enabled: Optional[bool] = None - Whether the product is enabled for the deal
    product_variation_id_str: Optional[str] = None - The updated ID of the product variation
    billing_frequency: Optional[str] = None - Updated billing frequency
    billing_frequency_cycles: Optional[str] = None - Updated number of billing cycles
    billing_start_date: Optional[str] = None - Updated start date for billing (YYYY-MM-DD)
    """
    logger.debug(
        f"Tool 'update_product_in_deal_in_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', product_attachment_id_str='{product_attachment_id_str}'"
    )

    # Sanitize empty strings to None
    item_price = None if item_price == "" else item_price
    quantity = None if quantity == "" else quantity
    tax = None if tax == "" else tax
    comments = None if comments == "" else comments
    discount = None if discount == "" else discount
    discount_type = None if discount_type == "" else discount_type
    tax_method = None if tax_method == "" else tax_method
    product_variation_id_str = None if product_variation_id_str == "" else product_variation_id_str
    billing_frequency = None if billing_frequency == "" else billing_frequency
    billing_frequency_cycles = None if billing_frequency_cycles == "" else billing_frequency_cycles
    billing_start_date = None if billing_start_date == "" else billing_start_date

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

    product_variation_id, variation_id_error = convert_id_string(
        product_variation_id_str, "product_variation_id"
    )
    if variation_id_error:
        logger.error(variation_id_error)
        return format_tool_response(False, error_message=variation_id_error)

    # Convert string values to appropriate types if provided
    item_price_float = None
    if item_price is not None:
        try:
            item_price_float = float(item_price)
            if item_price_float <= 0:
                error_message = "Item price must be greater than zero."
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
        except ValueError:
            error_message = f"Invalid item price format: '{item_price}'. Must be a valid number."
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)

    quantity_int = None
    if quantity is not None:
        try:
            quantity_int = int(quantity)
            if quantity_int <= 0:
                error_message = "Quantity must be greater than zero."
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
        except ValueError:
            error_message = f"Invalid quantity format: '{quantity}'. Must be a valid integer."
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)

    tax_float = None
    if tax is not None:
        try:
            tax_float = float(tax)
        except ValueError:
            error_message = f"Invalid tax format: '{tax}'. Must be a valid number."
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)

    discount_float = None
    if discount is not None:
        try:
            discount_float = float(discount)
        except ValueError:
            error_message = f"Invalid discount format: '{discount}'. Must be a valid number."
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)

    billing_cycles_int = None
    if billing_frequency_cycles is not None:
        try:
            billing_cycles_int = int(billing_frequency_cycles)
            if billing_cycles_int <= 0 or billing_cycles_int > 208:
                error_message = "Billing frequency cycles must be a positive integer less than or equal to 208."
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
        except ValueError:
            error_message = f"Invalid billing frequency cycles format: '{billing_frequency_cycles}'. Must be a valid integer."
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)

    # Validate discount_type if provided
    if discount_type and discount_type not in ["percentage", "amount"]:
        error_message = f"Invalid discount type: '{discount_type}'. Must be 'percentage' or 'amount'."
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    # Validate tax_method if provided
    if tax_method and tax_method not in ["inclusive", "exclusive", "none"]:
        error_message = f"Invalid tax method: '{tax_method}'. Must be 'inclusive', 'exclusive', or 'none'."
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    # Validate billing_frequency if provided
    if billing_frequency and billing_frequency not in [
        "one-time", "annually", "semi-annually", "quarterly", "monthly", "weekly"
    ]:
        error_message = (
            f"Invalid billing frequency: '{billing_frequency}'. "
            f"Must be one of: one-time, annually, semi-annually, quarterly, monthly, weekly."
        )
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    # Check if at least one field is being updated
    if all(param is None for param in [
        item_price_float, quantity_int, tax_float, comments, discount_float,
        discount_type, tax_method, is_enabled, product_variation_id,
        billing_frequency, billing_cycles_int, billing_start_date
    ]):
        error_message = "At least one field must be provided for updating a product in a deal"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    try:
        # Call the Pipedrive API
        result = await pd_mcp_ctx.pipedrive_client.deals.update_product_in_deal(
            deal_id=deal_id,
            product_attachment_id=product_attachment_id,
            item_price=item_price_float,
            quantity=quantity_int,
            tax=tax_float,
            comments=comments,
            discount=discount_float,
            discount_type=discount_type,
            tax_method=tax_method,
            is_enabled=is_enabled,
            product_variation_id=product_variation_id,
            billing_frequency=billing_frequency,
            billing_frequency_cycles=billing_cycles_int,
            billing_start_date=billing_start_date
        )

        logger.info(
            f"Successfully updated product {product_attachment_id} in deal {deal_id}"
        )

        # Return the API response
        return format_tool_response(True, data=result)

    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'update_product_in_deal_in_pipedrive': {str(e)}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'update_product_in_deal_in_pipedrive': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )