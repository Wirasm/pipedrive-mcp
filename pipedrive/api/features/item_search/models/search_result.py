from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class SearchResult(BaseModel):
    """Model representing an item search result from Pipedrive"""

    id: int
    type: str
    result_score: float

    # Common fields across all item types (not all items have all fields)
    name: Optional[str] = None
    title: Optional[str] = None
    email: Optional[List[Dict[str, Any]]] = None
    phone: Optional[List[Dict[str, Any]]] = None
    organization_name: Optional[str] = None
    person_name: Optional[str] = None
    address: Optional[str] = None
    code: Optional[str] = None
    visible_to: Optional[int] = None
    notes: Optional[List[Dict[str, Any]]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    
    # Deal-specific fields
    value: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    
    # File-specific fields
    url: Optional[str] = None
    
    # Related items 
    person: Optional[Dict[str, Any]] = None
    organization: Optional[Dict[str, Any]] = None
    deal: Optional[Dict[str, Any]] = None
    
    @field_validator('type')
    def validate_type(cls, v):
        """Validate the item type"""
        valid_types = [
            'deal', 'person', 'organization', 'product', 
            'lead', 'file', 'mail_attachment', 'project'
        ]
        if v not in valid_types:
            raise ValueError(f"Invalid item type: {v}. Must be one of: {', '.join(valid_types)}")
        return v
    
    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "SearchResult":
        """Create a SearchResult instance from Pipedrive API response data
        
        Args:
            api_data: Item search result data from Pipedrive API
            
        Returns:
            SearchResult instance with parsed data
        """
        # Extract type-specific data
        result = dict(api_data) if isinstance(api_data, dict) else {}
        
        # Handle related items if present
        if "person" in result and isinstance(result["person"], dict) and "id" in result["person"]:
            # Person might already be properly formatted, keep as is
            pass
        elif "person_id" in result and result["person_id"] is not None:
            # For deal results, person might be referenced by ID and name
            result["person"] = {
                "id": result.pop("person_id", None),
                "name": result.pop("person_name", None) 
            }
            
        if "organization" in result and isinstance(result["organization"], dict) and "id" in result["organization"]:
            # Organization might already be properly formatted, keep as is
            pass
        elif "org_id" in result and result["org_id"] is not None:
            # For deal or person results, organization might be referenced by ID and name
            result["organization"] = {
                "id": result.pop("org_id", None),
                "name": result.pop("org_name", None)
            }
        
        # Create the model
        return cls(**result)


class ItemSearchResults(BaseModel):
    """Model representing a collection of search results with metadata"""
    
    items: List[SearchResult]
    total_count: Optional[int] = None
    next_cursor: Optional[str] = None
    
    # Summary counts by type
    deal_count: Optional[int] = 0
    person_count: Optional[int] = 0
    organization_count: Optional[int] = 0
    product_count: Optional[int] = 0
    lead_count: Optional[int] = 0
    file_count: Optional[int] = 0
    mail_attachment_count: Optional[int] = 0
    project_count: Optional[int] = 0
    
    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "ItemSearchResults":
        """Create an ItemSearchResults instance from Pipedrive API response data
        
        Args:
            api_data: Item search results data from Pipedrive API
            
        Returns:
            ItemSearchResults instance with parsed data
        """
        # Process items array
        items_data = api_data.get("items", [])
        search_results = [SearchResult.from_api_response(item_data) for item_data in items_data]
        
        # Count items by type
        type_counts = {}
        for item in search_results:
            type_counts[f"{item.type}_count"] = type_counts.get(f"{item.type}_count", 0) + 1
        
        # Create the model
        return cls(
            items=search_results,
            total_count=len(search_results),
            next_cursor=api_data.get("next_cursor"),
            **type_counts
        )


class FieldSearchResult(BaseModel):
    """Model representing a field search result from Pipedrive"""
    
    id: int
    name: str
    
    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "FieldSearchResult":
        """Create a FieldSearchResult instance from Pipedrive API response data
        
        Args:
            api_data: Field search result data from Pipedrive API
            
        Returns:
            FieldSearchResult instance with parsed data
        """
        return cls(**api_data)


class FieldSearchResults(BaseModel):
    """Model representing a collection of field search results with metadata"""
    
    items: List[FieldSearchResult]
    next_cursor: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "FieldSearchResults":
        """Create a FieldSearchResults instance from Pipedrive API response data
        
        Args:
            api_data: Field search results data from Pipedrive API
            
        Returns:
            FieldSearchResults instance with parsed data
        """
        # Process items array
        items_data = api_data.get("items", [])
        field_results = [FieldSearchResult.from_api_response(item_data) for item_data in items_data]
        
        # Create the model
        return cls(
            items=field_results,
            next_cursor=api_data.get("next_cursor")
        )