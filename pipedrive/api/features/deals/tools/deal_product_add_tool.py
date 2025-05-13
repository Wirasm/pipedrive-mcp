from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

from mcp.server.fastmcp import Context
from pydantic import BaseModel, Field, ValidationError

from log_config import logger
from pipedrive.api.features.deals.models.deal_product import DealProduct
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string, validate_date_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


# Parameter groups to organize related parameters
class DealProductIdentifiers(BaseModel):
    """Required identifiers for adding a product to a deal"""
    id_str: str = Field(..., description="The ID of the deal")
    product_id_str: str = Field(..., description="The ID of the product to add")

    def validate_and_convert(self) -> Dict[str, Union[int, str]]:
        """Validate and convert string IDs to integers"""
        result = {}

        # Convert deal ID
        deal_id, deal_id_error = convert_id_string(self.id_str, "deal_id")
        if deal_id_error:
            raise ValueError(deal_id_error)
        result["deal_id"] = deal_id

        # Convert product ID
        product_id, product_id_error = convert_id_string(self.product_id_str, "product_id")
        if product_id_error:
            raise ValueError(product_id_error)
        result["product_id"] = product_id

        return result


class DealProductBasicInfo(BaseModel):
    """Basic product information"""
    item_price: str = Field(..., description="The price value of the product")
    quantity: str = Field(..., description="The quantity of the product")
    comments: Optional[str] = Field(None, description="Additional comments about the product")

    def validate_and_convert(self) -> Dict[str, Union[float, int, str, None]]:
        """Validate and convert string values to appropriate types"""
        result = {}

        # Convert and validate item_price
        try:
            item_price_float = float(self.item_price)
            if item_price_float < 0:
                raise ValueError(f"Item price must be non-negative, got: {item_price_float}")
            result["item_price"] = item_price_float
        except ValueError as e:
            if "must be non-negative" in str(e):
                raise
            raise ValueError(f"Invalid item price format: '{self.item_price}'. Must be a valid number.")

        # Convert and validate quantity
        try:
            quantity_int = int(self.quantity)
            if quantity_int <= 0:
                raise ValueError("Quantity must be greater than zero.")
            result["quantity"] = quantity_int
        except ValueError as e:
            if "must be greater than zero" in str(e):
                raise
            raise ValueError(f"Invalid quantity format: '{self.quantity}'. Must be a valid integer.")

        # Handle comments (already the right type, just sanitize empty string)
        result["comments"] = None if self.comments == "" else self.comments

        return result


class DealProductPricing(BaseModel):
    """Pricing related parameters"""
    tax: Optional[str] = Field("0", description="The product tax value")
    discount: Optional[str] = Field("0", description="The discount value")
    discount_type: str = Field("percentage", description="Discount type (percentage or amount)")
    tax_method: Optional[str] = Field("inclusive", description="Tax method (inclusive, exclusive, none)")

    def validate_and_convert(self) -> Dict[str, Union[float, str, None]]:
        """Validate and convert string values to appropriate types"""
        result = {}

        # Convert and validate tax
        try:
            tax_float = float(self.tax) if self.tax else 0
            if tax_float < 0:
                raise ValueError(f"Tax value must be non-negative, got: {tax_float}")
            result["tax"] = tax_float
        except ValueError as e:
            if "must be non-negative" in str(e):
                raise
            raise ValueError(f"Invalid tax format: '{self.tax}'. Must be a valid number.")

        # Convert and validate discount
        try:
            discount_float = float(self.discount) if self.discount else 0
            if discount_float < 0:
                raise ValueError(f"Discount value must be non-negative, got: {discount_float}")
            result["discount"] = discount_float
        except ValueError as e:
            if "must be non-negative" in str(e):
                raise
            raise ValueError(f"Invalid discount format: '{self.discount}'. Must be a valid number.")

        # Validate discount_type
        valid_discount_types = ["percentage", "amount"]
        if self.discount_type not in valid_discount_types:
            raise ValueError(
                f"Invalid discount type: '{self.discount_type}'. Must be one of: {', '.join(valid_discount_types)}"
            )
        result["discount_type"] = self.discount_type

        # Validate tax_method
        if self.tax_method:
            valid_tax_methods = ["inclusive", "exclusive", "none"]
            if self.tax_method not in valid_tax_methods:
                raise ValueError(
                    f"Invalid tax method: '{self.tax_method}'. Must be one of: {', '.join(valid_tax_methods)}"
                )
        result["tax_method"] = self.tax_method

        return result


class DealProductBilling(BaseModel):
    """Billing related parameters"""
    product_variation_id_str: Optional[str] = Field(None, description="The ID of the product variation")
    billing_frequency: str = Field("one-time", description="Billing frequency (one-time, annually, semi-annually, quarterly, monthly, weekly)")
    billing_frequency_cycles: Optional[str] = Field(None, description="Number of billing cycles")
    billing_start_date: Optional[str] = Field(None, description="Start date for billing in YYYY-MM-DD format")

    def validate_and_convert(self) -> Dict[str, Union[int, str, None]]:
        """Validate and convert string values to appropriate types"""
        result = {}

        # Convert product variation ID if provided
        if self.product_variation_id_str and self.product_variation_id_str != "":
            product_variation_id, variation_id_error = convert_id_string(
                self.product_variation_id_str, "product_variation_id"
            )
            if variation_id_error:
                raise ValueError(variation_id_error)
            result["product_variation_id"] = product_variation_id
        else:
            result["product_variation_id"] = None

        # Validate billing_frequency
        valid_frequencies = ["one-time", "weekly", "monthly", "quarterly", "semi-annually", "annually"]
        if self.billing_frequency not in valid_frequencies:
            raise ValueError(
                f"Invalid billing frequency: '{self.billing_frequency}'. "
                f"Must be one of: {', '.join(valid_frequencies)}"
            )
        result["billing_frequency"] = self.billing_frequency

        # Convert billing_frequency_cycles to integer if provided
        if self.billing_frequency_cycles and self.billing_frequency_cycles != "":
            try:
                billing_cycles_int = int(self.billing_frequency_cycles)
                if billing_cycles_int <= 0 or billing_cycles_int > 208:
                    raise ValueError(
                        "Billing frequency cycles must be a positive integer less than or equal to 208."
                    )
                result["billing_frequency_cycles"] = billing_cycles_int
            except ValueError as e:
                if "must be a positive integer" in str(e):
                    raise
                raise ValueError(
                    f"Invalid billing frequency cycles format: '{self.billing_frequency_cycles}'. "
                    f"Must be a valid integer."
                )
        else:
            result["billing_frequency_cycles"] = None

        # Validate billing_start_date format
        if self.billing_start_date and self.billing_start_date.strip():
            date_value, date_error = validate_date_string(
                self.billing_start_date, "billing_start_date", "YYYY-MM-DD", "2025-12-31"
            )
            if date_error:
                raise ValueError(date_error)
            result["billing_start_date"] = date_value
        else:
            result["billing_start_date"] = None

        return result


@mcp.tool("add_product_to_deal_in_pipedrive")
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

    This tool adds a product to an existing deal with specified pricing and billing details.
    A deal-product association is created in Pipedrive, linking the product to the deal
    with the given price, quantity, and other attributes.
    
    Format requirements:
    - id_str: Numeric ID of the deal (e.g. "123")
    - product_id_str: Numeric ID of the product (e.g. "456")
    - item_price: Positive numeric value (e.g. "99.99")
    - quantity: Positive integer (e.g. "1")
    - tax: Numeric percentage or amount (e.g. "10" for 10%)
    - discount: Numeric percentage or amount (e.g. "15" for 15% or 15 units)
    - billing_start_date: ISO date format YYYY-MM-DD (e.g. "2025-12-31")
    
    Pricing Options:
    - discount_type: Controls how discount is applied ("percentage" or "amount")
      - "percentage": Applies discount as percentage of total (e.g. "10" = 10% off)
      - "amount": Applies fixed amount discount (e.g. "50" = $50 off)
    
    - tax_method: Controls how tax is calculated ("inclusive", "exclusive", or "none")
      - "inclusive": Tax is already included in the item_price
      - "exclusive": Tax will be added to the item_price
      - "none": No tax applied
    
    Billing Options:
    - billing_frequency: How often customer is billed ("one-time", "weekly", etc.)
    - billing_frequency_cycles: Number of billing cycles (required for "weekly", optional for others)
    - billing_start_date: When billing should begin (YYYY-MM-DD)
    
    Special Validations:
    - When billing_frequency is "one-time", billing_frequency_cycles must be null
    - When billing_frequency is "weekly", billing_frequency_cycles is required
    - For recurring billing, cycles must be between 1 and 208
    
    Example usage:
    ```
    add_product_to_deal_in_pipedrive(
        id_str="123",
        product_id_str="456",
        item_price="199.99",
        quantity="2",
        discount="10",
        discount_type="percentage"
    )
    ```

    args:
    ctx: Context
    id_str: str - The ID of the deal (required)
    product_id_str: str - The ID of the product to add (required)
    item_price: str - The price value of the product (positive number, required)
    quantity: str - The quantity of the product (positive integer, required)
    tax: Optional[str] = "0" - The product tax value (percentage or amount)
    comments: Optional[str] = None - Additional comments about the product
    discount: Optional[str] = "0" - The discount value (percentage or amount)
    discount_type: str = "percentage" - Discount type ("percentage" or "amount")
    tax_method: Optional[str] = "inclusive" - Tax method ("inclusive", "exclusive", "none")
    product_variation_id_str: Optional[str] = None - The ID of the product variation
    billing_frequency: str = "one-time" - Billing frequency ("one-time", "annually", "semi-annually", "quarterly", "monthly", "weekly")
    billing_frequency_cycles: Optional[str] = None - Number of billing cycles (1-208, required for weekly billing)
    billing_start_date: Optional[str] = None - Start date for billing in YYYY-MM-DD format
    """
    logger.debug(
        f"Tool 'add_product_to_deal_in_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', product_id_str='{product_id_str}', "
        f"item_price='{item_price}', quantity='{quantity}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    try:
        # Create and validate all parameter groups
        identifiers = DealProductIdentifiers(
            id_str=id_str,
            product_id_str=product_id_str
        )

        basic_info = DealProductBasicInfo(
            item_price=item_price,
            quantity=quantity,
            comments=comments
        )

        pricing = DealProductPricing(
            tax=tax,
            discount=discount,
            discount_type=discount_type,
            tax_method=tax_method
        )

        billing = DealProductBilling(
            product_variation_id_str=product_variation_id_str,
            billing_frequency=billing_frequency,
            billing_frequency_cycles=billing_frequency_cycles,
            billing_start_date=billing_start_date
        )

        # Validate and convert all parameters
        id_data = identifiers.validate_and_convert()
        basic_data = basic_info.validate_and_convert()
        pricing_data = pricing.validate_and_convert()
        billing_data = billing.validate_and_convert()

        # Merge all parameter data
        deal_id = id_data.pop("deal_id")
        all_params = {**id_data, **basic_data, **pricing_data, **billing_data}

        # Create deal product through validation model
        deal_product = DealProduct(
            deal_id=deal_id,
            **all_params
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
            f"Successfully added product {all_params['product_id']} to deal {deal_id}"
        )

        # Return the API response
        return format_tool_response(True, data=result)

    except ValidationError as e:
        logger.error(f"Validation error adding product to deal: {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except ValueError as e:
        logger.error(f"Value error adding product to deal: {str(e)}")
        return format_tool_response(False, error_message=str(e))
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