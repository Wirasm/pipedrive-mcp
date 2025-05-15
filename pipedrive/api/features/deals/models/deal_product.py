from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator, field_validator
from datetime import date, datetime


class DealProduct(BaseModel):
    """Model representing a product attached to a deal
    
    This model defines all parameters needed when attaching a product to a deal.
    
    Key components:
    - Basic product information (product_id, price, quantity)
    - Pricing details (discounts, taxes)
    - Billing configuration (frequency, cycles, start date)
    
    Important requirements:
    - All monetary values must be positive numbers
    - Tax and discount values must be non-negative
    - Billing frequencies affect required billing frequency cycles
    - One-time products can't have billing cycles
    - Weekly products must have billing cycles specified
    
    Format requirements:
    - Monetary values (item_price, discount): Numeric values (float)
    - Dates (billing_start_date): ISO-8601 format (YYYY-MM-DD)
    - IDs (product_id, product_variation_id): Positive integers
    """
    product_id: int = Field(..., description="The ID of the product to add to the deal")
    item_price: float = Field(..., description="The price value of the product (must be positive)")
    quantity: int = Field(..., description="The quantity of the product (must be positive)")
    discount: float = Field(0, description="The discount value (must be non-negative)")
    tax: float = Field(0, description="The product tax value (must be non-negative)")
    comments: Optional[str] = Field(None, description="Additional comments about the product")
    currency: str = Field("USD", description="The currency of the deal (3-letter ISO code)")
    discount_type: str = Field("percentage", description="Discount type: 'percentage' or 'amount'")
    tax_method: str = Field("inclusive", description="Tax method: 'inclusive', 'exclusive', or 'none'")
    is_enabled: bool = Field(True, description="Whether this product is enabled for the deal")
    product_variation_id: Optional[int] = Field(None, description="The ID of the product variation")
    billing_frequency: str = Field("one-time", description="How often a customer is billed: 'one-time', 'weekly', 'monthly', 'quarterly', 'semi-annually', 'annually'")
    billing_frequency_cycles: Optional[int] = Field(None, description="Number of billing cycles (required for 'weekly', optional for others except 'one-time')")
    billing_start_date: Optional[str] = Field(None, description="Start date for billing in YYYY-MM-DD format")
    deal_id: Optional[int] = Field(None, description="The ID of the deal this product is attached to")
    id: Optional[int] = Field(None, description="Product attachment ID (only used in responses)")
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary"""
        # Start with the model dict excluding None values and specific fields
        result = {k: v for k, v in self.model_dump().items() 
                  if v is not None and k not in ["id", "deal_id"]}
        
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'DealProduct':
        """Create DealProduct from API response dictionary"""
        # Extract fields from API response
        product_data = {
            "product_id": data.get("product_id"),
            "item_price": data.get("item_price"),
            "quantity": data.get("quantity"),
            "discount": data.get("discount", 0),
            "tax": data.get("tax", 0),
            "comments": data.get("comments"),
            "currency": data.get("currency", "USD"),
            "discount_type": data.get("discount_type", "percentage"),
            "tax_method": data.get("tax_method", "inclusive"),
            "is_enabled": data.get("is_enabled", True),
            "product_variation_id": data.get("product_variation_id"),
            "billing_frequency": data.get("billing_frequency", "one-time"),
            "billing_frequency_cycles": data.get("billing_frequency_cycles"),
            "billing_start_date": data.get("billing_start_date"),
            "deal_id": data.get("deal_id"),
            "id": data.get("id")
        }
        
        return cls(**product_data)
    
        # Field validators
    @field_validator('product_id', 'product_variation_id', mode='after')
    @classmethod
    def validate_positive_id(cls, v: Optional[int], info) -> Optional[int]:
        """Validate that ID fields are positive integers if present"""
        if v is not None and v <= 0:
            raise ValueError(f"{info.field_name} must be a positive integer. Example: 123")
        return v

    @field_validator('item_price', mode='after')
    @classmethod
    def validate_positive_price(cls, v: float) -> float:
        """Validate that price is a positive number"""
        if v <= 0:
            raise ValueError("Item price must be greater than zero. Example: 99.99")
        return v

    @field_validator('quantity', mode='after')
    @classmethod
    def validate_positive_quantity(cls, v: int) -> int:
        """Validate that quantity is a positive integer"""
        if v <= 0:
            raise ValueError("Quantity must be greater than zero. Example: 1")
        return v

    @field_validator('discount', 'tax', mode='after')
    @classmethod
    def validate_non_negative_value(cls, v: float, info) -> float:
        """Validate that discount and tax are non-negative"""
        if v < 0:
            raise ValueError(f"{info.field_name} must be non-negative. Example: 10")
        return v

    @field_validator('billing_start_date', mode='after')
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate that billing_start_date is in YYYY-MM-DD format"""
        if v is None:
            return None
            
        try:
            # Attempt to parse the date string
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid billing_start_date format: '{v}'. Must be in YYYY-MM-DD format. Example: '2025-12-31'")

    @model_validator(mode='after')
    def validate_deal_product(self) -> 'DealProduct':
        """Validate that the deal product has valid data - cross-field validations"""
        # Validate discount type
        valid_discount_types = ["percentage", "amount"]
        if self.discount_type not in valid_discount_types:
            raise ValueError(
                f"Invalid discount_type: '{self.discount_type}'. " 
                f"Must be one of: {', '.join(valid_discount_types)}. " 
                f"Example: 'percentage' (applies percentage discount) or 'amount' (applies fixed amount discount)"
            )
        
        # Validate tax method
        valid_tax_methods = ["inclusive", "exclusive", "none"]
        if self.tax_method not in valid_tax_methods:
            raise ValueError(
                f"Invalid tax_method: '{self.tax_method}'. " 
                f"Must be one of: {', '.join(valid_tax_methods)}. " 
                f"'inclusive' means tax is included in price, 'exclusive' means tax is added to price, 'none' means no tax"
            )
        
        # Validate billing frequency
        valid_billing_frequencies = ["one-time", "annually", "semi-annually", "quarterly", "monthly", "weekly"]
        if self.billing_frequency not in valid_billing_frequencies:
            raise ValueError(
                f"Invalid billing_frequency: '{self.billing_frequency}'. " 
                f"Must be one of: {', '.join(valid_billing_frequencies)}."
            )
        
        # Billing frequency cycles validation
        if self.billing_frequency == "one-time" and self.billing_frequency_cycles is not None:
            raise ValueError(
                "When billing_frequency is 'one-time', billing_frequency_cycles must be null. "
                "One-time products are charged only once and do not have recurring cycles."
            )
        
        if self.billing_frequency == "weekly" and self.billing_frequency_cycles is None:
            raise ValueError(
                "When billing_frequency is 'weekly', billing_frequency_cycles must be specified. "
                "This defines how many weeks the billing will continue."
            )
        
        if self.billing_frequency_cycles is not None:
            if self.billing_frequency_cycles <= 0 or self.billing_frequency_cycles > 208:
                raise ValueError(
                    f"Invalid billing_frequency_cycles: {self.billing_frequency_cycles}. "
                    "Must be a positive integer less than or equal to 208. Example: 12 (for 12 billing cycles)"
                )
        
        return self