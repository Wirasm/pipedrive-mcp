from typing import List, Dict, Any, Optional, Union, Set
from pydantic import BaseModel, Field, model_validator, field_validator

from pipedrive.api.features.persons.models.contact_info import Email, Phone


class Person(BaseModel):
    """Person entity model with Pydantic validation
    
    Represents a person entity in Pipedrive CRM with full validation.
    The Person model supports all standard Pipedrive person fields, including
    contact information (emails and phones), organization association,
    visibility settings and more.
    
    Format requirements:
        - name: Required person name (cannot be empty)
        - owner_id: Integer ID of the user who owns the person
        - org_id: Integer ID of the organization linked to the person
        - emails: List of email objects with value, label, and primary fields
        - phones: List of phone objects with value, label, and primary fields
        - visible_to: Integer visibility setting (1-4), where:
            1 = Owner only
            2 = Owner's visibility group
            3 = Entire company
            4 = Shared with specific users (not implementable via API)
        - custom_fields: Handled via the API client directly
    
    Examples:
        Basic person: 
            {
                "name": "John Doe",
                "owner_id": 123,
                "org_id": 456
            }
            
        Person with contact info:
            {
                "name": "Jane Smith",
                "emails": [
                    {"value": "jane@example.com", "label": "work", "primary": true},
                    {"value": "jsmith@personal.com", "label": "home", "primary": false}
                ],
                "phones": [
                    {"value": "+1 555-123-4567", "label": "work", "primary": true}
                ]
            }
    """
    name: str = Field(..., description="The name of the person (required)")
    owner_id: Optional[int] = Field(None, description="User ID of the owner of the person")
    org_id: Optional[int] = Field(None, description="Organization ID this person is associated with")
    emails: List[Email] = Field(default_factory=list, description="List of email addresses for this person")
    phones: List[Phone] = Field(default_factory=list, description="List of phone numbers for this person")
    visible_to: Optional[int] = Field(None, description="Visibility setting (1-4): 1=Owner, 2=Owner's group, 3=Entire company")
    id: Optional[int] = Field(None, description="Person ID (set by Pipedrive)")
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary
        
        Transforms the Person model into a dictionary format suitable for Pipedrive API requests.
        This includes properly formatting nested objects like emails and phones.
        
        Returns:
            Dictionary representation for API requests
        """
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
        """Create Person from API response dictionary
        
        Parses a Pipedrive API response dictionary into a Person model,
        handling nested objects like emails and phones.
        
        Args:
            data: Dictionary from Pipedrive API response
            
        Returns:
            Person model populated with API data
        """
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
        """Validates the Person model with all business rules
        
        Performs comprehensive validation including:
        - Name cannot be empty
        - Visibility settings must be in valid range
        - Organization ID is properly formatted
        - Contact information is valid
        
        Returns:
            Validated Person instance
            
        Raises:
            ValueError: If any validation fails
        """
        # Validate name
        if not self.name or not self.name.strip():
            raise ValueError("Person name cannot be empty")
        
        # Validate visible_to if provided
        if self.visible_to is not None:
            valid_visibility = {1, 2, 3}  # 1=Owner, 2=Owner's group, 3=Entire company
            if self.visible_to not in valid_visibility:
                raise ValueError(
                    f"Invalid visible_to value: {self.visible_to}. "
                    f"Must be one of {valid_visibility} (1=Owner only, 2=Owner's group, 3=Entire company)"
                )
        
        # Validate org_id if provided
        if self.org_id is not None:
            if not isinstance(self.org_id, int) or self.org_id <= 0:
                raise ValueError(f"Organization ID must be a positive integer, got {self.org_id}")
        
        # Ensure at most one primary email
        primary_emails = [email for email in self.emails if email.primary]
        if len(primary_emails) > 1:
            raise ValueError("Only one email can be set as primary")
        
        # Ensure at most one primary phone
        primary_phones = [phone for phone in self.phones if phone.primary]
        if len(primary_phones) > 1:
            raise ValueError("Only one phone can be set as primary")
        
        return self