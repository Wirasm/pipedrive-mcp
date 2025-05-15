from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator


class ContactInfo(BaseModel):
    """Base class for contact information
    
    Represents a piece of contact information with its value, label, and primary status.
    Pipedrive requires contact information to be formatted as objects with these fields.
    
    Format requirements:
        - value: The actual contact value (email address, phone number, etc.)
        - label: A descriptor for this contact info (work, home, mobile, etc.)
        - primary: Whether this is the primary contact method
        
    Example:
        {
            "value": "contact@example.com",
            "label": "work",
            "primary": true
        }
    """
    value: str = Field(..., description="The contact information value")
    label: str = Field("work", description="Label describing the contact information type (work, home, etc.)")
    primary: bool = Field(False, description="Whether this is the primary contact method")
    
    @model_validator(mode='after')
    def validate_value_not_empty(self) -> 'ContactInfo':
        """Validate that the value is not empty"""
        if not self.value or not self.value.strip():
            raise ValueError(f"Contact {type(self).__name__} value cannot be empty")
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary format
        
        Returns:
            Dictionary representation for API requests
        """
        return {
            "value": self.value,
            "label": self.label,
            "primary": self.primary
        }


class Email(ContactInfo):
    """Email contact information
    
    Represents an email address with its label and primary status.
    Pipedrive expects emails to be formatted as objects with value, label, and primary fields.
    
    Format requirements:
        - value: A valid email address
        - label: Email type descriptor (work, home, etc.)
        - primary: Whether this is the primary email
        
    Example:
        {
            "value": "contact@example.com",
            "label": "work",
            "primary": true
        }
    """
    label: str = Field("work", description="Label for the email (work, home, etc.)")
    primary: bool = Field(True, description="Whether this is the primary email address")
    
    @field_validator('value')
    @classmethod
    def validate_email_format(cls, value: str) -> str:
        """Validate email format"""
        if not value or '@' not in value:
            raise ValueError("Invalid email format. Must contain '@' symbol.")
        return value


class Phone(ContactInfo):
    """Phone contact information
    
    Represents a phone number with its label and primary status.
    Pipedrive expects phone numbers to be formatted as objects with value, label, and primary fields.
    
    Format requirements:
        - value: A valid phone number (any format accepted by Pipedrive)
        - label: Phone type descriptor (work, home, mobile, etc.)
        - primary: Whether this is the primary phone number
        
    Example:
        {
            "value": "+1 (555) 123-4567",
            "label": "work",
            "primary": true
        }
    """
    label: str = Field("work", description="Label for the phone number (work, home, mobile, etc.)")
    primary: bool = Field(True, description="Whether this is the primary phone number")