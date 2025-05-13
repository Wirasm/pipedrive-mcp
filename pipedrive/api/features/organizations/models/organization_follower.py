from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class OrganizationFollower(BaseModel):
    """Organization follower entity model with Pydantic validation"""
    user_id: int
    add_time: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary representation"""
        return self.model_dump(exclude_none=True)
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'OrganizationFollower':
        """Create OrganizationFollower from API response dictionary"""
        follower_data = {
            "user_id": data.get("user_id"),
            "add_time": data.get("add_time"),
        }
        return cls(**follower_data)