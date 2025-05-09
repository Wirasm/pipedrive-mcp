from typing import Dict, Any
from pydantic import BaseModel, Field


class ContactInfo(BaseModel):
    """Base class for contact information"""
    value: str
    label: str
    primary: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "label": self.label,
            "primary": self.primary
        }


class Email(ContactInfo):
    """Email contact information"""
    label: str = "work"
    primary: bool = True


class Phone(ContactInfo):
    """Phone contact information"""
    label: str = "work"
    primary: bool = True