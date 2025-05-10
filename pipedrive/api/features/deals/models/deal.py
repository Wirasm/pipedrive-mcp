from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator
from datetime import date, datetime


class Deal(BaseModel):
    """Deal entity model with Pydantic validation"""
    title: str
    value: Optional[float] = None
    currency: str = "USD"
    person_id: Optional[int] = None
    org_id: Optional[int] = None
    status: str = "open"
    owner_id: Optional[int] = None
    stage_id: Optional[int] = None
    pipeline_id: Optional[int] = None
    expected_close_date: Optional[date] = None
    visible_to: Optional[int] = None
    probability: Optional[int] = None
    lost_reason: Optional[str] = None
    id: Optional[int] = None
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary"""
        # Start with the model dict excluding None values
        result = {k: v for k, v in self.model_dump().items() 
                  if v is not None and k != "id"}
        
        # Convert date objects to strings
        if self.expected_close_date:
            result["expected_close_date"] = self.expected_close_date.isoformat()
            
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'Deal':
        """Create Deal from API response dictionary"""
        # Extract basic fields
        deal_data = {
            "title": data.get("title", ""),
            "value": data.get("value"),
            "currency": data.get("currency", "USD"),
            "person_id": data.get("person_id"),
            "org_id": data.get("org_id"),
            "status": data.get("status", "open"),
            "owner_id": data.get("owner_id"),
            "stage_id": data.get("stage_id"),
            "pipeline_id": data.get("pipeline_id"),
            "visible_to": data.get("visible_to"),
            "probability": data.get("probability"),
            "lost_reason": data.get("lost_reason"),
            "id": data.get("id")
        }
        
        # Process date fields
        if "expected_close_date" in data and data["expected_close_date"]:
            try:
                deal_data["expected_close_date"] = date.fromisoformat(data["expected_close_date"])
            except (ValueError, TypeError):
                # Handle invalid date format gracefully
                pass
        
        return cls(**deal_data)
    
    @model_validator(mode='after')
    def validate_deal(self) -> 'Deal':
        """Validate that the deal has valid data"""
        # Title must not be empty
        if not self.title or not self.title.strip():
            raise ValueError("Deal title cannot be empty")
        
        # Status must be one of the valid values
        valid_statuses = ["open", "won", "lost"]
        if self.status not in valid_statuses:
            raise ValueError(f"Deal status must be one of: {', '.join(valid_statuses)}")
        
        # Lost reason should only be set if status is 'lost'
        if self.status != "lost" and self.lost_reason:
            raise ValueError("Lost reason can only be set if deal status is 'lost'")
        
        # Probability must be between 0 and 100
        if self.probability is not None and (self.probability < 0 or self.probability > 100):
            raise ValueError("Deal probability must be between 0 and 100")
            
        return self