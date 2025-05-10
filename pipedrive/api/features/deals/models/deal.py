from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator, field_validator
from datetime import date, datetime


class Deal(BaseModel):
    """Deal entity model with Pydantic validation"""
    title: str
    value: Optional[float] = None
    currency: str = "USD"
    person_id: Optional[int] = None
    org_id: Optional[int] = None
    status: str = "open"
    owner_id: Optional[int] = None
    stage_id: Optional[int] = None
    pipeline_id: Optional[int] = None
    expected_close_date: Optional[date] = None
    visible_to: Optional[int] = None
    probability: Optional[int] = None
    lost_reason: Optional[str] = None
    id: Optional[int] = None

    # Field validators for ID fields
    @field_validator('person_id', 'org_id', 'owner_id', 'stage_id', 'pipeline_id', 'visible_to', 'id')
    @classmethod
    def validate_positive_id(cls, v: Optional[int], info) -> Optional[int]:
        """Validate that ID fields are positive integers if present"""
        if v is not None and v <= 0:
            raise ValueError(f"{info.field_name} must be a positive integer if provided")
        return v

    @field_validator('value')
    @classmethod
    def validate_non_negative_value(cls, v: Optional[float]) -> Optional[float]:
        """Validate that value is non-negative if present"""
        if v is not None and v < 0:
            raise ValueError("Deal value must be non-negative if provided")
        return v

    @field_validator('probability')
    @classmethod
    def validate_probability_range(cls, v: Optional[int]) -> Optional[int]:
        """Validate that probability is between 0 and 100 if present"""
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Deal probability must be between 0 and 100 if provided")
        return v

    @field_validator('currency')
    @classmethod
    def validate_currency(cls, v: str) -> str:
        """Validate that currency is a valid 3-letter ISO currency code"""
        if not v:
            return "USD"  # Default to USD if empty

        v = v.upper()  # Standardize to uppercase

        # List of common currency codes
        valid_currencies = {
            "USD", "EUR", "GBP", "JPY", "CNY", "AUD", "CAD", "CHF", "HKD", "SGD",
            "SEK", "NOK", "DKK", "NZD", "INR", "BRL", "RUB", "ZAR", "MXN", "AED",
            "PLN", "TRY", "SAR", "ILS", "KRW", "IDR", "THB", "MYR", "PHP"
        }

        if len(v) != 3:
            raise ValueError(f"Invalid currency code: {v}. Currency code must be 3 letters.")

        if v not in valid_currencies:
            # We don't strictly require a known currency, but we do warn about it
            # This allows for future currency codes or less common ones
            if not v.isalpha() or len(v) != 3:
                raise ValueError(f"Invalid currency code format: {v}. Must be a 3-letter code (e.g., USD, EUR).")

        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate that status is one of the valid values"""
        if not v:
            return "open"  # Default to 'open' if empty

        v = v.lower()  # Standardize to lowercase

        valid_statuses = {"open", "won", "lost"}
        if v not in valid_statuses:
            raise ValueError(f"Invalid status: {v}. Must be one of: {', '.join(valid_statuses)}")

        return v

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate that title is not empty"""
        if not v or not v.strip():
            raise ValueError("Deal title cannot be empty")
        return v.strip()  # Normalize by removing leading/trailing whitespace
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary"""
        # Start with the model dict excluding None values
        result = {k: v for k, v in self.model_dump().items() 
                  if v is not None and k != "id"}
        
        # Convert date objects to strings
        if self.expected_close_date:
            result["expected_close_date"] = self.expected_close_date.isoformat()
            
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'Deal':
        """Create Deal from API response dictionary"""
        # Extract basic fields
        deal_data = {
            "title": data.get("title", ""),
            "value": data.get("value"),
            "currency": data.get("currency", "USD"),
            "person_id": data.get("person_id"),
            "org_id": data.get("org_id"),
            "status": data.get("status", "open"),
            "owner_id": data.get("owner_id"),
            "stage_id": data.get("stage_id"),
            "pipeline_id": data.get("pipeline_id"),
            "visible_to": data.get("visible_to"),
            "probability": data.get("probability"),
            "lost_reason": data.get("lost_reason"),
            "id": data.get("id")
        }

        # Process date fields
        if "expected_close_date" in data and data["expected_close_date"]:
            try:
                deal_data["expected_close_date"] = date.fromisoformat(data["expected_close_date"])
            except ValueError:
                raise ValueError(
                    f"Invalid date format for expected_close_date: '{data['expected_close_date']}'. "
                    f"Expected ISO format (YYYY-MM-DD)."
                )
            except TypeError:
                raise ValueError(
                    f"Invalid date type for expected_close_date: {type(data['expected_close_date'])}. "
                    f"Expected string in ISO format (YYYY-MM-DD)."
                )

        return cls(**deal_data)
    
    @model_validator(mode='after')
    def validate_deal(self) -> 'Deal':
        """Validate that the deal has valid data - cross-field validations"""
        # Lost reason should only be set if status is 'lost'
        if self.status != "lost" and self.lost_reason:
            raise ValueError("Lost reason can only be set if deal status is 'lost'")

        return self