from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, model_validator


class Organization(BaseModel):
    """Organization entity model with Pydantic validation"""
    name: str
    owner_id: Optional[int] = None
    address: Optional[str] = None
    visible_to: Optional[int] = None
    id: Optional[int] = None
    label_ids: Optional[List[int]] = Field(default_factory=list)
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary"""
        # Start with the model dict excluding None values
        result = {k: v for k, v in self.model_dump().items() 
                  if v is not None and k != "id"}
        
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'Organization':
        """Create Organization from API response dictionary"""
        # Extract basic fields
        org_data = {
            "name": data.get("name", ""),
            "owner_id": data.get("owner_id"),
            "address": data.get("address"),
            "visible_to": data.get("visible_to"),
            "id": data.get("id"),
        }
        
        # Process label IDs
        if "label_ids" in data and data["label_ids"]:
            org_data["label_ids"] = data["label_ids"]
        
        return cls(**org_data)
    
    @model_validator(mode='after')
    def validate_organization(self) -> 'Organization':
        """Validate that the organization has a valid name"""
        if not self.name or not self.name.strip():
            raise ValueError("Organization name cannot be empty")
        
        # Validate visible_to if it's provided
        if self.visible_to is not None and self.visible_to not in [1, 2, 3, 4]:
            raise ValueError(f"Invalid visibility value: {self.visible_to}. Must be one of: 1, 2, 3, 4")
        
        return self