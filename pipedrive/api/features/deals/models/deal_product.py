from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator


class DealProduct(BaseModel):
    """Model representing a product attached to a deal"""
    product_id: int
    item_price: float
    quantity: int
    discount: float = 0
    tax: float = 0
    comments: Optional[str] = None
    currency: str = "USD"
    discount_type: str = "percentage"  # "percentage" or "amount"
    tax_method: str = "inclusive"  # "inclusive", "exclusive", or "none"
    is_enabled: bool = True
    product_variation_id: Optional[int] = None
    billing_frequency: str = "one-time"  # "one-time", "annually", "semi-annually", "quarterly", "monthly", "weekly"
    billing_frequency_cycles: Optional[int] = None
    billing_start_date: Optional[str] = None  # ISO format date: YYYY-MM-DD
    deal_id: Optional[int] = None
    id: Optional[int] = None  # Product attachment ID
    
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
    
    @model_validator(mode='after')
    def validate_deal_product(self) -> 'DealProduct':
        """Validate that the deal product has valid data"""
        # Item price should be a positive number
        if self.item_price <= 0:
            raise ValueError("Product price must be greater than zero")
        
        # Quantity should be a positive integer
        if self.quantity <= 0:
            raise ValueError("Product quantity must be greater than zero")
        
        # Validate discount type
        valid_discount_types = ["percentage", "amount"]
        if self.discount_type not in valid_discount_types:
            raise ValueError(f"Discount type must be one of: {', '.join(valid_discount_types)}")
        
        # Validate tax method
        valid_tax_methods = ["inclusive", "exclusive", "none"]
        if self.tax_method not in valid_tax_methods:
            raise ValueError(f"Tax method must be one of: {', '.join(valid_tax_methods)}")
        
        # Validate billing frequency
        valid_billing_frequencies = ["one-time", "annually", "semi-annually", "quarterly", "monthly", "weekly"]
        if self.billing_frequency not in valid_billing_frequencies:
            raise ValueError(f"Billing frequency must be one of: {', '.join(valid_billing_frequencies)}")
        
        # Billing frequency cycles validation
        if self.billing_frequency == "one-time" and self.billing_frequency_cycles is not None:
            raise ValueError("Billing frequency cycles must be null when billing frequency is 'one-time'")
        
        if self.billing_frequency == "weekly" and self.billing_frequency_cycles is None:
            raise ValueError("Billing frequency cycles cannot be null when billing frequency is 'weekly'")
        
        if self.billing_frequency_cycles is not None and (self.billing_frequency_cycles <= 0 or self.billing_frequency_cycles > 208):
            raise ValueError("Billing frequency cycles must be a positive integer less than or equal to 208")
        
        return self