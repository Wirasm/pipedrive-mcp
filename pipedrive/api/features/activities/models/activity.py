from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date, datetime


class Activity(BaseModel):
    """Activity entity model with Pydantic validation"""
    subject: str
    type: str
    due_date: Optional[str] = None  # ISO format YYYY-MM-DD
    due_time: Optional[str] = None  # HH:MM:SS
    duration: Optional[str] = None  # HH:MM:SS
    owner_id: Optional[int] = None
    deal_id: Optional[int] = None
    lead_id: Optional[str] = None  # UUID string
    person_id: Optional[int] = None
    org_id: Optional[int] = None
    project_id: Optional[int] = None
    busy: Optional[bool] = None
    done: Optional[bool] = None
    note: Optional[str] = None
    location: Optional[str] = None
    public_description: Optional[str] = None
    priority: Optional[int] = None
    id: Optional[int] = None
    
    # Field validators
    @field_validator('subject')
    @classmethod
    def validate_subject(cls, v: str) -> str:
        """Validate that subject is not empty"""
        if not v or not v.strip():
            raise ValueError("Activity subject cannot be empty")
        return v.strip()
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate that type is not empty"""
        if not v or not v.strip():
            raise ValueError("Activity type cannot be empty")
        return v.strip()
    
    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v: Optional[str]) -> Optional[str]:
        """Validate that due_date is in YYYY-MM-DD format if provided"""
        if v is None or not v.strip():
            return None
            
        v = v.strip()
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError(f"Invalid due_date format: {v}. Must be in ISO format (YYYY-MM-DD)")
    
    @field_validator('due_time', 'duration')
    @classmethod
    def validate_time_format(cls, v: Optional[str], info) -> Optional[str]:
        """Validate that time values are in HH:MM:SS format if provided"""
        if v is None or not v.strip():
            return None
            
        v = v.strip()
        time_format = r"^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$"
        import re
        if not re.match(time_format, v):
            # Convert single-digit hour with no leading zero (1:00 or 1:00:00)
            single_digit_hour = re.match(r"^(\d):([0-5]\d)(?::([0-5]\d))?$", v)
            if info.field_name == 'duration' and single_digit_hour:
                if v.count(':') == 1:
                    return f"0{v}:00"  # Add seconds and leading zero
                elif v.count(':') == 2:
                    return f"0{v}"  # Just add leading zero
            # Allow HH:MM format and convert to HH:MM:SS for duration
            elif info.field_name == 'duration' and re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", v):
                return f"{v}:00"  # Add seconds if only HH:MM was provided for duration
            raise ValueError(f"Invalid {info.field_name} format: {v}. Must be in HH:MM:SS format")
        return v
    
    @field_validator('owner_id', 'deal_id', 'person_id', 'org_id', 'project_id', 'id')
    @classmethod
    def validate_positive_id(cls, v: Optional[int]) -> Optional[int]:
        """Validate that ID fields are positive integers if present"""
        if v is not None and v <= 0:
            raise ValueError(f"ID fields must be positive integers if provided")
        return v
    
    @field_validator('lead_id')
    @classmethod
    def validate_lead_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate lead_id format if provided"""
        if v is None or not v.strip():
            return None
            
        v = v.strip()
        # UUID pattern (RFC 4122)
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        import re
        if not re.match(uuid_pattern, v.lower()):
            raise ValueError(f"Invalid lead_id format: {v}. Must be a valid UUID string.")
        return v
    
    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: Optional[int]) -> Optional[int]:
        """Validate priority range if provided"""
        if v is not None and (v < 0 or v > 999):
            raise ValueError(f"Priority must be between 0 and 999 if provided")
        return v
    
    @model_validator(mode='after')
    def validate_activity(self) -> 'Activity':
        """Validate that the activity has valid data - cross-field validations"""
        # Ensure at least one related entity is provided
        if all(getattr(self, field) is None for field in ['deal_id', 'lead_id', 'person_id', 'org_id']):
            # This is a soft warning, as it's valid in Pipedrive to have an activity without relations
            pass
            
        # If an activity is marked as done, ensure due_date is set
        if self.done and not self.due_date:
            # Pipedrive might allow this, so just a warning in logs would be appropriate
            # For now, we'll allow it in the model
            pass
            
        return self
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary for creation/updates"""
        # Start with the model dict excluding None values and ID
        result = {k: v for k, v in self.model_dump().items() 
                 if v is not None and k != "id"}
        
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'Activity':
        """Create Activity from API response dictionary"""
        activity_data = {
            "id": data.get("id"),
            "subject": data.get("subject", ""),
            "type": data.get("type", ""),
            "due_date": data.get("due_date"),
            "due_time": data.get("due_time"),
            "duration": data.get("duration"),
            "owner_id": data.get("owner_id"),
            "deal_id": data.get("deal_id"),
            "lead_id": data.get("lead_id"),
            "person_id": data.get("person_id"),
            "org_id": data.get("org_id"),
            "project_id": data.get("project_id"),
            "busy": data.get("busy", False) if "busy" in data else None,
            "done": data.get("done", False) if "done" in data else None,
            "note": data.get("note"),
            "location": data.get("location"),
            "public_description": data.get("public_description"),
            "priority": data.get("priority")
        }
        
        return cls(**activity_data)