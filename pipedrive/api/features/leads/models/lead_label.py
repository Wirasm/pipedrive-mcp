from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime


class LeadLabel(BaseModel):
    """Lead label entity model with Pydantic validation"""
    name: str
    color: str
    id: Optional[str] = None  # UUID string
    add_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    
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
            raise ValueError(f"Invalid UUID format for lead label ID: '{v}'")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is not empty"""
        if not v or not v.strip():
            raise ValueError("Lead label name cannot be empty")
        return v.strip()  # Normalize by removing leading/trailing whitespace
    
    @field_validator('color')
    @classmethod
    def validate_color(cls, v: str) -> str:
        """Validate that color is one of the valid options"""
        if not v or not v.strip():
            raise ValueError("Lead label color cannot be empty")
        
        v = v.lower()  # Standardize to lowercase
        
        valid_colors = {
            "blue", "brown", "dark-gray", "gray", "green", 
            "orange", "pink", "purple", "red", "yellow"
        }
        
        if v not in valid_colors:
            raise ValueError(f"Invalid color: {v}. Must be one of: {', '.join(valid_colors)}")
            
        return v
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary"""
        # Start with the model dict excluding None values and ID
        result = {k: v for k, v in self.model_dump().items() 
                  if v is not None and k not in ["id", "add_time", "update_time"]}
        
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'LeadLabel':
        """Create LeadLabel from API response dictionary"""
        # Extract basic fields
        label_data = {
            "name": data.get("name", ""),
            "color": data.get("color", ""),
            "id": data.get("id"),
        }
        
        # Process datetime fields
        if "add_time" in data and data["add_time"]:
            try:
                label_data["add_time"] = datetime.fromisoformat(data["add_time"].replace('Z', '+00:00'))
            except ValueError:
                # If the format is not ISO, try parsing with other formats
                try:
                    label_data["add_time"] = datetime.strptime(data["add_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                except ValueError:
                    try:
                        label_data["add_time"] = datetime.strptime(data["add_time"], "%Y-%m-%dT%H:%M:%SZ")
                    except ValueError:
                        raise ValueError(f"Unsupported datetime format for add_time: {data['add_time']}")
                        
        if "update_time" in data and data["update_time"]:
            try:
                label_data["update_time"] = datetime.fromisoformat(data["update_time"].replace('Z', '+00:00'))
            except ValueError:
                # If the format is not ISO, try parsing with other formats
                try:
                    label_data["update_time"] = datetime.strptime(data["update_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                except ValueError:
                    try:
                        label_data["update_time"] = datetime.strptime(data["update_time"], "%Y-%m-%dT%H:%M:%SZ")
                    except ValueError:
                        raise ValueError(f"Unsupported datetime format for update_time: {data['update_time']}")

        return cls(**label_data)