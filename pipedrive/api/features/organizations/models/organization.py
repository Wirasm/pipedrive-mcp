from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field, model_validator


class Organization(BaseModel):
    """Organization entity model with Pydantic validation
    
    The Organization model represents a company or organization in Pipedrive CRM.
    It handles validation of required fields and proper formatting for API calls.
    
    Format requirements:
    - address: Must be a dictionary with a 'value' key for proper API handling
      Example: {"value": "123 Main St, City, Country"}
    - visible_to: Must be an integer between 1-4 representing visibility level
      1: Owner only, 2: Owner's visibility group, 3: Entire company, 4: Specified users
    - label_ids: Must be an array even for a single label
      Example: [12345] not 12345
    """
    name: str
    owner_id: Optional[int] = None
    address: Optional[Dict[str, str]] = None  # Address should be a dictionary for the API
    visible_to: Optional[int] = None
    id: Optional[int] = None
    label_ids: Optional[List[int]] = Field(default_factory=list)
    industry: Optional[str] = None  # Industry classification as a string
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary
        
        Returns:
            A dictionary suitable for sending to the Pipedrive API with proper formatting
        """
        # Start with the model dict excluding None values
        result = {k: v for k, v in self.model_dump().items() 
                  if v is not None and k != "id"}
        
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'Organization':
        """Create Organization from API response dictionary
        
        Args:
            data: The API response dictionary containing organization data
            
        Returns:
            Organization: A properly instantiated Organization model
        """
        # Extract basic fields
        org_data = {
            "name": data.get("name", ""),
            "owner_id": data.get("owner_id"),
            "visible_to": data.get("visible_to"),
            "id": data.get("id"),
        }
        
        # Process address - convert from string to dict if needed
        address = data.get("address")
        if address:
            if isinstance(address, str):
                org_data["address"] = {"value": address}
            else:
                org_data["address"] = address
        
        # Process label IDs
        if "label_ids" in data and data["label_ids"]:
            org_data["label_ids"] = data["label_ids"]
            
        # Process industry if present
        if "industry" in data and data["industry"]:
            org_data["industry"] = data["industry"]
        
        return cls(**org_data)
    
    @staticmethod
    def format_address(address: Optional[Union[str, Dict[str, str]]]) -> Optional[Dict[str, str]]:
        """Format an address string or dict to the API-required format
        
        The Pipedrive API requires organization addresses to be in a dict format with
        a 'value' key, not a plain string. This utility handles the conversion.
        
        Args:
            address: Address as either a string or already-formatted dict
            
        Returns:
            Properly formatted address dict or None if input is None/empty
        
        Examples:
            >>> Organization.format_address("123 Main St, City, Country")
            {"value": "123 Main St, City, Country"}
            >>> Organization.format_address({"value": "123 Main St"})
            {"value": "123 Main St"}
        """
        if address is None:
            return None
            
        if isinstance(address, str) and address.strip():
            return {"value": address.strip()}
            
        if isinstance(address, dict) and "value" in address and address["value"].strip():
            return address
        
        return None
    
    @model_validator(mode='after')
    def validate_organization(self) -> 'Organization':
        """Validate that the organization has valid field formats
        
        Performs validation on:
        - Name (required and non-empty)
        - Address (properly formatted as a dict)
        - Visibility settings (must be a valid option)
        
        Returns:
            The validated Organization object
            
        Raises:
            ValueError: If any validation fails
        """
        # Validate name
        if not self.name or not self.name.strip():
            raise ValueError("Organization name cannot be empty")
        
        # Validate visible_to if it's provided
        if self.visible_to is not None and self.visible_to not in [1, 2, 3, 4]:
            raise ValueError(f"Invalid visibility value: {self.visible_to}. Must be one of: 1 (Owner only), 2 (Owner's visibility group), 3 (Entire company), or 4 (Specified users)")
        
        # Validate address format if provided
        if self.address is not None:
            if not isinstance(self.address, dict) or "value" not in self.address:
                raise ValueError("Address must be a dictionary with a 'value' key. Example: {\"value\": \"123 Main St, City, Country\"}")
            if not self.address["value"] or not isinstance(self.address["value"], str) or not self.address["value"].strip():
                raise ValueError("Address value cannot be empty and must be a string")
        
        # Validate industry if provided
        if self.industry is not None and not isinstance(self.industry, str):
            raise ValueError("Industry must be a string value")
        
        return self