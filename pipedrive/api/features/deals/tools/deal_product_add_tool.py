from typing import Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.deals.models.deal_product import DealProduct
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def add_product_to_deal_in_pipedrive(
    ctx: Context,
    id_str: str,
    product_id_str: str,
    item_price: str,
    quantity: str,
    tax: Optional[str] = "0",
    comments: Optional[str] = None,
    discount: Optional[str] = "0",
    discount_type: str = "percentage",
    tax_method: Optional[str] = "inclusive",
    product_variation_id_str: Optional[str] = None,
    billing_frequency: str = "one-time",
    billing_frequency_cycles: Optional[str] = None,
    billing_start_date: Optional[str] = None,
) -> str:
    """Adds a product to a deal in Pipedrive CRM, creating a new deal-product.

    This tool requires the deal ID, product ID, price and quantity. You can
    optionally provide details like tax, discount, comments, and billing options.

    args:
    ctx: Context
    id_str: str - The ID of the deal
    product_id_str: str - The ID of the product to add
    item_price: str - The price value of the product
    quantity: str - The quantity of the product
    tax: Optional[str] = "0" - The product tax value
    comments: Optional[str] = None - Additional comments about the product
    discount: Optional[str] = "0" - The discount value
    discount_type: str = "percentage" - Discount type (percentage or amount)
    tax_method: Optional[str] = "inclusive" - Tax method (inclusive, exclusive, none)
    product_variation_id_str: Optional[str] = None - The ID of the product variation
    billing_frequency: str = "one-time" - Billing frequency (one-time, annually, semi-annually, quarterly, monthly, weekly)
    billing_frequency_cycles: Optional[str] = None - Number of billing cycles
    billing_start_date: Optional[str] = None - Start date for billing in YYYY-MM-DD format
    """
    logger.debug(
        f"Tool 'add_product_to_deal_in_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', product_id_str='{product_id_str}', "
        f"item_price='{item_price}', quantity='{quantity}'"
    )

    # Sanitize empty strings to None
    comments = None if comments == "" else comments
    product_variation_id_str = None if product_variation_id_str == "" else product_variation_id_str
    billing_frequency_cycles = None if billing_frequency_cycles == "" else billing_frequency_cycles
    billing_start_date = None if billing_start_date == "" else billing_start_date

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string IDs to integers
    deal_id, deal_id_error = convert_id_string(id_str, "deal_id")
    if deal_id_error:
        logger.error(deal_id_error)
        return format_tool_response(False, error_message=deal_id_error)

    product_id, product_id_error = convert_id_string(product_id_str, "product_id")
    if product_id_error:
        logger.error(product_id_error)
        return format_tool_response(False, error_message=product_id_error)

    product_variation_id, variation_id_error = convert_id_string(
        product_variation_id_str, "product_variation_id"
    )
    if variation_id_error:
        logger.error(variation_id_error)
        return format_tool_response(False, error_message=variation_id_error)

    # Convert numeric string values to appropriate types
    try:
        item_price_float = float(item_price)
    except ValueError:
        error_message = f"Invalid item price format: '{item_price}'. Must be a valid number."
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

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

    try:
        tax_float = float(tax) if tax else 0
    except ValueError:
        error_message = f"Invalid tax format: '{tax}'. Must be a valid number."
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    try:
        discount_float = float(discount) if discount else 0
    except ValueError:
        error_message = f"Invalid discount format: '{discount}'. Must be a valid number."
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    # Convert billing_frequency_cycles to integer if provided
    billing_cycles_int = None
    if billing_frequency_cycles:
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

    try:
        # Create deal product through validation model
        deal_product = DealProduct(
            product_id=product_id,
            item_price=item_price_float,
            quantity=quantity_int,
            tax=tax_float,
            comments=comments,
            discount=discount_float,
            discount_type=discount_type,
            tax_method=tax_method,
            product_variation_id=product_variation_id,
            billing_frequency=billing_frequency,
            billing_frequency_cycles=billing_cycles_int,
            billing_start_date=billing_start_date,
            deal_id=deal_id
        )

        # Convert model to API-compatible dict
        payload = deal_product.to_api_dict()
        
        # Log the payload without sensitive information
        safe_log_payload = payload.copy()
        if "item_price" in safe_log_payload:
            safe_log_payload["item_price"] = "[REDACTED]"
            
        logger.debug(f"Prepared payload for product addition: {safe_log_payload}")
        
        # Call the Pipedrive API
        result = await pd_mcp_ctx.pipedrive_client.deals.add_product_to_deal(
            deal_id=deal_id,
            **payload
        )

        logger.info(
            f"Successfully added product {product_id} to deal {deal_id}"
        )

        # Return the API response
        return format_tool_response(True, data=result)

    except ValidationError as e:
        logger.error(f"Validation error adding product to deal: {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'add_product_to_deal_in_pipedrive': {str(e)}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'add_product_to_deal_in_pipedrive': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )