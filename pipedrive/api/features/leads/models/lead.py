from typing import List, Dict, Any, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field, model_validator, field_validator
from datetime import date, datetime


class Lead(BaseModel):
    """Lead entity model with Pydantic validation"""
    title: str
    amount: Optional[float] = None
    currency: str = "USD"
    person_id: Optional[int] = None
    organization_id: Optional[int] = None
    owner_id: Optional[int] = None
    expected_close_date: Optional[date] = None
    visible_to: Optional[int] = None
    id: Optional[str] = None  # UUID string
    label_ids: Optional[List[str]] = None  # List of UUID strings
    source_name: Optional[str] = None
    is_archived: Optional[bool] = False
    was_seen: Optional[bool] = False
    channel: Optional[int] = None
    channel_id: Optional[str] = None
    
    # Field validators for ID fields
    @field_validator('owner_id', 'person_id', 'organization_id', 'channel')
    @classmethod
    def validate_positive_id(cls, v: Optional[int], info) -> Optional[int]:
        """Validate that ID fields are positive integers if present"""
        if v is not None and v <= 0:
            raise ValueError(f"{info.field_name} must be a positive integer if provided")
        return v

    @field_validator('amount')
    @classmethod
    def validate_non_negative_value(cls, v: Optional[float]) -> Optional[float]:
        """Validate that value is non-negative if present"""
        if v is not None and v < 0:
            raise ValueError("Lead amount must be non-negative if provided")
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

    @field_validator('id')
    @classmethod
    def validate_uuid(cls, v: Optional[str]) -> Optional[str]:
        """Validate that ID is a valid UUID string if present"""
        if v is None:
            return v

        try:
            # Convert to UUID and back to string for standardization
            return str(UUID(v))
        except ValueError:
            raise ValueError(f"Invalid UUID format for lead ID: '{v}'")

    @field_validator('label_ids')
    @classmethod
    def validate_label_ids(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate that label_ids are valid UUID strings if present"""
        if v is None:
            return v

        if not isinstance(v, list):
            raise ValueError("label_ids must be a list")

        # Validate each UUID in the list
        validated_uuids = []
        for uuid_str in v:
            try:
                validated_uuids.append(str(UUID(uuid_str)))
            except ValueError:
                raise ValueError(f"Invalid UUID format in label_ids: '{uuid_str}'")

        return validated_uuids

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate that title is not empty"""
        if not v or not v.strip():
            raise ValueError("Lead title cannot be empty")
        return v.strip()  # Normalize by removing leading/trailing whitespace
    
    @field_validator('visible_to')
    @classmethod
    def validate_visible_to(cls, v: Optional[int]) -> Optional[int]:
        """Validate that visible_to is one of the valid visibility levels"""
        if v is None:
            return v
            
        valid_values = {1, 3, 5, 7}
        if v not in valid_values:
            raise ValueError(f"Invalid visible_to value: {v}. Must be one of: {', '.join(map(str, valid_values))}")
            
        return v
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary"""
        # Start with the model dict excluding None values
        result = {k: v for k, v in self.model_dump().items() 
                  if v is not None and k != "id"}
        
        # Convert date objects to strings
        if self.expected_close_date:
            result["expected_close_date"] = self.expected_close_date.isoformat()
            
        # Handle value field properly (amount + currency)
        if self.amount is not None:
            result["value"] = {"amount": self.amount, "currency": self.currency}
            # Remove the separate fields since they're now in the value object
            if "amount" in result:
                del result["amount"]
            if "currency" in result:
                del result["currency"]
            
        # Ensure label_ids is a list if provided
        if self.label_ids is not None:
            result["label_ids"] = self.label_ids
            
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'Lead':
        """Create Lead from API response dictionary"""
        # Extract basic fields
        lead_data = {
            "title": data.get("title", ""),
            "person_id": data.get("person_id"),
            "organization_id": data.get("organization_id"),
            "owner_id": data.get("owner_id"),
            "visible_to": data.get("visible_to"),
            "id": data.get("id"),
            "is_archived": data.get("is_archived", False),
            "was_seen": data.get("was_seen", False),
            "source_name": data.get("source_name"),
            "channel": data.get("channel"),
            "channel_id": data.get("channel_id"),
        }
        
        # Handle label_ids - ensure it's a list
        if "label_ids" in data and data["label_ids"] is not None:
            if isinstance(data["label_ids"], list):
                lead_data["label_ids"] = data["label_ids"]
            else:
                # If it's a single value, convert to a list
                lead_data["label_ids"] = [data["label_ids"]]
        
        # Process amount and currency
        # The API might provide them separately or as a 'value' object
        if "value" in data and data["value"]:
            if isinstance(data["value"], dict):
                lead_data["amount"] = data["value"].get("amount")
                lead_data["currency"] = data["value"].get("currency", "USD")
            else:
                # Handle cases where value might be a simple number
                lead_data["amount"] = float(data["value"]) if data["value"] else None
                lead_data["currency"] = data.get("currency", "USD")
        else:
            # Handle cases where amount and currency are provided separately
            lead_data["amount"] = data.get("amount")
            lead_data["currency"] = data.get("currency", "USD")

        # Process date fields
        if "expected_close_date" in data and data["expected_close_date"]:
            try:
                lead_data["expected_close_date"] = date.fromisoformat(data["expected_close_date"])
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

        return cls(**lead_data)
    
    @model_validator(mode='after')
    def validate_lead(self) -> 'Lead':
        """Validate that the lead has valid data - cross-field validations"""
        # A lead must be linked to either a person or an organization or both
        if self.person_id is None and self.organization_id is None:
            raise ValueError("A lead must be linked to either a person, an organization, or both")
        
        return self