from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator


class OrganizationFollower(BaseModel):
    """Organization follower entity model with Pydantic validation
    
    This model represents a user following an organization in Pipedrive CRM.
    When a user follows an organization, they receive notifications about changes
    to that organization.
    
    Format requirements:
    - user_id: Must be a valid user ID in your Pipedrive account
    
    Note: When adding a follower, only the user_id is required. The add_time
    field is returned by the API but not needed for creating a follower.
    """
    user_id: int
    add_time: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary representation suitable for the API
        
        Returns:
            Dictionary with non-None values for API requests
        """
        return self.model_dump(exclude_none=True)
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'OrganizationFollower':
        """Create OrganizationFollower from API response dictionary
        
        Args:
            data: API response data containing follower information
            
        Returns:
            Instantiated OrganizationFollower model
        """
        follower_data = {
            "user_id": data.get("user_id"),
            "add_time": data.get("add_time"),
        }
        return cls(**follower_data)
        
    @model_validator(mode='after')
    def validate_follower(self) -> 'OrganizationFollower':
        """Validate that the follower has a valid user_id
        
        Returns:
            The validated OrganizationFollower object
            
        Raises:
            ValueError: If user_id is not valid
        """
        if not self.user_id or self.user_id <= 0:
            raise ValueError("user_id must be a positive integer")
            
        return self