from typing import Optional
from datetime import date

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string, validate_date_string
from pipedrive.api.features.shared.utils import format_tool_response, format_validation_error
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("update_product_in_deal_in_pipedrive")
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

    This tool updates an existing product that is already attached to a deal. You must 
    provide both the deal ID and the product attachment ID (not the product ID), along with
    at least one field to update. It can modify pricing, quantity, tax settings, discount,
    and recurring billing options.
    
    Format requirements:
    - id_str: Required numeric ID of the deal (e.g. "123")
    - product_attachment_id_str: Required numeric ID of the product attachment (e.g. "456")
    - item_price: Positive numeric value (e.g. "99.99")
    - quantity: Positive integer (e.g. "1")
    - tax: Non-negative numeric percentage or amount (e.g. "10" for 10%)
    - discount: Non-negative numeric percentage or amount (e.g. "15" for 15%)
    - billing_start_date: ISO date format YYYY-MM-DD (e.g. "2025-12-31")
    
    Pricing Options:
    - discount_type: Controls how discount is applied ("percentage" or "amount")
    - tax_method: Controls how tax is calculated ("inclusive", "exclusive", or "none")
    
    Billing Options:
    - billing_frequency: Frequency for recurring billing ("one-time", "weekly", etc.)
    - billing_frequency_cycles: Number of billing cycles (1-208)
    - is_enabled: Whether the product is active on the deal (true or false)
    
    Special Validations:
    - One-time products can't have billing cycles
    - Weekly products must have billing cycles specified
    - When updating billing_frequency to "one-time", billing_frequency_cycles must be null
    - When updating billing_frequency to "weekly", billing_frequency_cycles must be provided
    
    Example usage:
    ```
    update_product_in_deal_in_pipedrive(
        id_str="123",
        product_attachment_id_str="456",
        item_price="249.99",
        quantity="3",
        discount="20",
        discount_type="percentage"
    )
    ```

    args:
    ctx: Context
    id_str: str - The ID of the deal (required)
    product_attachment_id_str: str - The ID of the product attachment to update (required)
    item_price: Optional[str] = None - The updated price of the product (positive number)
    quantity: Optional[str] = None - The updated quantity of the product (positive integer)
    tax: Optional[str] = None - The updated tax value (non-negative number)
    comments: Optional[str] = None - Updated comments about the product
    discount: Optional[str] = None - The updated discount value (non-negative number)
    discount_type: Optional[str] = None - Updated discount type ("percentage" or "amount")
    tax_method: Optional[str] = None - Updated tax method ("inclusive", "exclusive", "none")
    is_enabled: Optional[bool] = None - Whether the product is enabled for the deal
    product_variation_id_str: Optional[str] = None - The updated ID of the product variation
    billing_frequency: Optional[str] = None - Updated billing frequency ("one-time", "annually", etc.)
    billing_frequency_cycles: Optional[str] = None - Updated number of billing cycles (1-208)
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
        error_message = format_validation_error(
            "discount_type", discount_type, 
            "Must be 'percentage' (applies percentage discount) or 'amount' (applies fixed amount discount).", 
            "percentage"
        )
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    # Validate tax_method if provided
    if tax_method and tax_method not in ["inclusive", "exclusive", "none"]:
        error_message = format_validation_error(
            "tax_method", tax_method, 
            "Must be 'inclusive' (tax included in price), 'exclusive' (tax added to price), or 'none' (no tax).", 
            "inclusive"
        )
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    # Validate billing_frequency if provided
    if billing_frequency and billing_frequency not in [
        "one-time", "annually", "semi-annually", "quarterly", "monthly", "weekly"
    ]:
        error_message = format_validation_error(
            "billing_frequency", billing_frequency, 
            "Must be one of: one-time, annually, semi-annually, quarterly, monthly, weekly.", 
            "monthly"
        )
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
        
    # Validate billing_frequency and billing_frequency_cycles compatibility
    if billing_frequency == "one-time" and billing_cycles_int is not None:
        error_message = "When billing_frequency is 'one-time', billing_frequency_cycles must be null."
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
        
    if billing_frequency == "weekly" and billing_cycles_int is None:
        error_message = "When billing_frequency is 'weekly', billing_frequency_cycles must be specified."
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    # Validate billing_start_date format if provided
    if billing_start_date is not None:
        date_value, date_error = validate_date_string(
            billing_start_date, "billing_start_date", "YYYY-MM-DD", "2025-12-31"
        )
        if date_error:
            logger.error(date_error)
            return format_tool_response(False, error_message=date_error)
        billing_start_date = date_value
            
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