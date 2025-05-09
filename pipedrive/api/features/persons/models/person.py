from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator

from pipedrive.api.features.persons.models.contact_info import Email, Phone


class Person(BaseModel):
    """Person entity model with Pydantic validation"""
    name: str
    owner_id: Optional[int] = None
    org_id: Optional[int] = None
    emails: List[Email] = Field(default_factory=list)
    phones: List[Phone] = Field(default_factory=list)
    visible_to: Optional[int] = None
    id: Optional[int] = None
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary"""
        # Start with the model dict excluding None values
        result = {k: v for k, v in self.model_dump().items() 
                  if v is not None and k != "id"}
        
        # Handle nested objects
        if self.emails:
            result["emails"] = [email.to_dict() for email in self.emails]
        if self.phones:
            result["phones"] = [phone.to_dict() for phone in self.phones]
        
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'Person':
        """Create Person from API response dictionary"""
        # Extract basic fields
        person_data = {
            "name": data.get("name", ""),
            "owner_id": data.get("owner_id"),
            "org_id": data.get("org_id"),
            "visible_to": data.get("visible_to"),
            "id": data.get("id")
        }
        
        # Process emails
        emails = []
        if "emails" in data and data["emails"]:
            for email_data in data["emails"]:
                emails.append(Email(
                    value=email_data.get("value", ""),
                    label=email_data.get("label", "work"),
                    primary=email_data.get("primary", False)
                ))
        person_data["emails"] = emails
        
        # Process phones
        phones = []
        if "phones" in data and data["phones"]:
            for phone_data in data["phones"]:
                phones.append(Phone(
                    value=phone_data.get("value", ""),
                    label=phone_data.get("label", "work"),
                    primary=phone_data.get("primary", False)
                ))
        person_data["phones"] = phones
        
        return cls(**person_data)
    
    @model_validator(mode='after')
    def validate_person(self) -> 'Person':
        """Validate that the person has a valid name"""
        if not self.name or not self.name.strip():
            raise ValueError("Person name cannot be empty")
        return self