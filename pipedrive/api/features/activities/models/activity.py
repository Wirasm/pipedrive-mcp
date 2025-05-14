from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date, datetime


class ParticipantModel(BaseModel):
    """Model for activity participants"""
    person_id: int
    primary_flag: Optional[bool] = None


class Activity(BaseModel):
    """Activity entity model with Pydantic validation"""
    subject: str
    type: str
    due_date: Optional[str] = None  # ISO format YYYY-MM-DD
    due_time: Optional[str] = None  # HH:MM format (not HH:MM:SS as previously thought)
    duration: Optional[str] = None  # HH:MM format (not HH:MM:SS as previously thought)
    owner_id: Optional[int] = None
    deal_id: Optional[int] = None
    lead_id: Optional[str] = None  # UUID string
    person_id: Optional[int] = None  # Read-only field in Pipedrive API
    org_id: Optional[int] = None
    project_id: Optional[int] = None
    busy: Optional[bool] = None
    done: Optional[bool] = None
    note: Optional[str] = None
    location: Optional[Dict[str, Any]] = None  # Location is an object, not a string
    public_description: Optional[str] = None
    priority: Optional[int] = None
    participants: Optional[List[Dict[str, Any]]] = None  # List of participant objects
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
    
    @field_validator('due_time')
    @classmethod
    def validate_due_time(cls, v: Optional[str]) -> Optional[str]:
        """Validate that due_time is in HH:MM format if provided"""
        if v is None or not v.strip():
            return None
            
        v = v.strip()
        # Pipedrive API expects time in HH:MM format (not HH:MM:SS)
        time_format = r"^([01]\d|2[0-3]):([0-5]\d)$"
        import re
        if re.match(time_format, v):
            return v
            
        # If it's in HH:MM:SS format, convert to HH:MM
        hhmmss_format = r"^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$"
        if re.match(hhmmss_format, v):
            return v[:5]  # Take just the HH:MM part
                
        # If it's a single-digit hour with no leading zero
        single_digit_hour = re.match(r"^(\d):([0-5]\d)(?::([0-5]\d))?$", v)
        if single_digit_hour:
            if v.count(':') == 1:
                return f"0{v}"  # Add leading zero to hour
            elif v.count(':') == 2:
                return f"0{v[:3]}"  # Add leading zero to hour and truncate seconds
        
        # Check if it's in ISO datetime format and extract HH:MM
        iso_datetime_pattern = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:Z|[+-][0-9]{2}:[0-9]{2})?$'
        if re.match(iso_datetime_pattern, v):
            try:
                # Extract time part (HH:MM) from ISO format
                if 'T' in v:
                    time_part = v.split('T')[1]
                    if ':' in time_part:
                        return time_part[:5]
            except Exception:
                pass
                    
        raise ValueError(f"Invalid due_time format: {v}. Must be in HH:MM format (e.g., '14:30')")
        return v
    
    @field_validator('duration')
    @classmethod
    def validate_duration(cls, v: Optional[str]) -> Optional[str]:
        """Validate that duration is in HH:MM format if provided"""
        if v is None or not v.strip():
            return None
            
        v = v.strip()
        # Pipedrive API expects duration in HH:MM format
        time_format = r"^([01]\d|2[0-3]):([0-5]\d)$"
        import re
        if not re.match(time_format, v):
            # If it's in HH:MM:SS format, convert to HH:MM
            hhmmss_format = r"^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$"
            if re.match(hhmmss_format, v):
                return v[:5]  # Take just the HH:MM part
                
            # If it's a single-digit hour with no leading zero
            single_digit_hour = re.match(r"^(\d):([0-5]\d)(?::([0-5]\d))?$", v)
            if single_digit_hour:
                if v.count(':') == 1:
                    return f"0{v}"  # Add leading zero to hour
                elif v.count(':') == 2:
                    return f"0{v[:3]}"  # Add leading zero to hour and truncate seconds
                    
            # If it's seconds as an integer
            seconds_pattern = r'^\d+$'
            if re.match(seconds_pattern, v):
                try:
                    seconds = int(v)
                    hours, remainder = divmod(seconds, 3600)
                    minutes = remainder // 60
                    return f"{hours:02d}:{minutes:02d}"
                except ValueError:
                    pass
                    
            raise ValueError(f"Invalid duration format: {v}. Must be in HH:MM format (e.g., '01:30') or seconds (e.g., '5400')")
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
    
    @field_validator('participants')
    @classmethod
    def validate_participants(cls, v: Optional[List[Dict[str, Any]]]) -> Optional[List[Dict[str, Any]]]:
        """Validate participants format if provided"""
        if v is None:
            return None
            
        # Ensure it's a list
        if not isinstance(v, list):
            raise ValueError("participants must be a list of participant objects with person_id")
            
        # Validate each participant
        for i, participant in enumerate(v):
            if not isinstance(participant, dict):
                raise ValueError(f"Each participant must be an object. Invalid participant at position {i}")
                
            # Check for required person_id
            if 'person_id' not in participant:
                raise ValueError(f"Each participant must have a 'person_id' field. Missing in participant at position {i}")
                
            # Ensure person_id is an integer
            if not isinstance(participant['person_id'], int) or participant['person_id'] <= 0:
                raise ValueError(f"person_id must be a positive integer in participant at position {i}")
        
        return v
    
    @model_validator(mode='after')
    def validate_activity(self) -> 'Activity':
        """Validate that the activity has valid data - cross-field validations"""
        # Ensure at least one related entity is provided
        if all(getattr(self, field) is None for field in ['deal_id', 'lead_id', 'person_id', 'org_id']) and not self.participants:
            # This is a soft warning, as it's valid in Pipedrive to have an activity without relations
            pass
            
        # If an activity is marked as done, ensure due_date is set
        if self.done and not self.due_date:
            # Pipedrive might allow this, so just a warning in logs would be appropriate
            # For now, we'll allow it in the model
            pass
            
        # If person_id is provided but no participants, warn about read-only field
        if self.person_id is not None and not self.participants:
            pass  # We'll handle this warning in the tool, not the model
            
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
        # Extract basic activity data
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
            "public_description": data.get("public_description"),
            "priority": data.get("priority")
        }
        
        # Handle location data which could be structured differently in API response
        location_data = data.get("location")
        if isinstance(location_data, str):
            activity_data["location"] = {"value": location_data}
        elif isinstance(location_data, dict):
            activity_data["location"] = location_data
            
        # Extract participants if available
        participants = data.get("participants")
        if participants:
            activity_data["participants"] = participants
            
        return cls(**activity_data)