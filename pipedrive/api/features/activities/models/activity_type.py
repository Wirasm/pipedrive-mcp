from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, field_validator


class ActivityType(BaseModel):
    """ActivityType entity model with Pydantic validation"""
    name: str
    icon_key: str
    color: Optional[str] = None
    order_nr: Optional[int] = None
    id: Optional[int] = None
    key_string: Optional[str] = None
    active_flag: Optional[bool] = True
    is_custom_flag: Optional[bool] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is not empty"""
        if not v or not v.strip():
            raise ValueError("Activity type name cannot be empty")
        return v.strip()
    
    @field_validator('icon_key')
    @classmethod
    def validate_icon_key(cls, v: str) -> str:
        """Validate that icon_key is one of the valid values"""
        if not v or not v.strip():
            raise ValueError("Activity type icon_key cannot be empty")
            
        valid_icons = {
            "task", "email", "meeting", "deadline", "call", "lunch", "calendar", 
            "downarrow", "document", "smartphone", "camera", "scissors", "cogs", 
            "bubble", "uparrow", "checkbox", "signpost", "shuffle", "addressbook", 
            "linegraph", "picture", "car", "world", "search", "clip", "sound", 
            "brush", "key", "padlock", "pricetag", "suitcase", "finish", "plane", 
            "loop", "wifi", "truck", "cart", "bulb", "bell", "presentation"
        }
        
        v = v.strip()
        if v not in valid_icons:
            raise ValueError(f"Invalid icon_key: {v}. Must be one of the valid Pipedrive icon keys.")
        return v
    
    @field_validator('color')
    @classmethod
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        """Validate that color is a valid HEX color if provided"""
        if v is None or not v.strip():
            return None
            
        v = v.strip().upper()
        # Check for valid 6-character hex color
        if not (len(v) == 6 and all(c in '0123456789ABCDEF' for c in v)):
            raise ValueError(f"Invalid color format: {v}. Must be a 6-character HEX color (e.g., FFFFFF)")
        return v
    
    @field_validator('order_nr', 'id')
    @classmethod
    def validate_positive_integer(cls, v: Optional[int]) -> Optional[int]:
        """Validate that numeric fields are positive integers if provided"""
        if v is not None and v < 0:
            raise ValueError(f"Field must be a positive integer if provided")
        return v
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary for creation/updates"""
        # Start with the model dict excluding None values and ID
        result = {k: v for k, v in self.model_dump().items() 
                 if v is not None and k not in ["id", "key_string", "is_custom_flag"]}
        
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'ActivityType':
        """Create ActivityType from API response dictionary"""
        activity_type_data = {
            "id": data.get("id"),
            "name": data.get("name", ""),
            "icon_key": data.get("icon_key", ""),
            "color": data.get("color"),
            "order_nr": data.get("order_nr"),
            "key_string": data.get("key_string"),
            "active_flag": data.get("active_flag", True),
            "is_custom_flag": data.get("is_custom_flag")
        }
        
        return cls(**activity_type_data)