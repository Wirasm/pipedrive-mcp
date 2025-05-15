from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class SearchResult(BaseModel):
    """Model representing an item search result from Pipedrive API.
    
    This model captures all possible fields that can be returned for different
    entity types in Pipedrive search results. Not all fields will be present
    for all entity types.
    
    Fields:
        id: Unique identifier of the found item
        type: Type of the found item (deal, person, organization, etc.)
        result_score: Relevance score of this search result
        name: Name of the item (present for most entity types)
        title: Title of the item (present for deals, leads)
        email: Email addresses (for persons, may include multiple entries)
        phone: Phone numbers (for persons, may include multiple entries)
        organization_name: Name of related organization
        person_name: Name of related person
        address: Address information
        code: Product code (for products)
        visible_to: Visibility setting (1-4)
        notes: Notes associated with the item (may include multiple entries)
        custom_fields: Custom fields defined for this entity type
        value: Deal value (for deals)
        currency: Deal currency (for deals)
        status: Deal status (for deals)
        url: URL for file download (for files and mail attachments)
        person: Related person details
        organization: Related organization details
        deal: Related deal details
    """

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
        """Validate the item type against allowable Pipedrive entity types."""
        valid_types = [
            'deal', 'person', 'organization', 'product', 
            'lead', 'file', 'mail_attachment', 'project'
        ]
        if v not in valid_types:
            raise ValueError(f"Invalid item type: {v}. Must be one of: {', '.join(valid_types)}")
        return v
    
    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "SearchResult":
        """Create a SearchResult instance from Pipedrive API response data.
        
        This method normalizes the API response data to fit the model structure,
        handling various edge cases and data format inconsistencies that may be
        present in the Pipedrive API response.
        
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
    """Model representing a collection of search results with metadata.
    
    This model organizes search results by item type and provides counts
    for each type for easier analysis and filtering.
    
    Fields:
        items: List of individual search results
        total_count: Total number of found items across all types
        next_cursor: Pagination cursor for retrieving the next page of results
        deal_count: Number of deals in the results
        person_count: Number of persons in the results
        organization_count: Number of organizations in the results
        product_count: Number of products in the results
        lead_count: Number of leads in the results
        file_count: Number of files in the results
        mail_attachment_count: Number of mail attachments in the results
        project_count: Number of projects in the results
    """
    
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
        """Create an ItemSearchResults instance from Pipedrive API response data.
        
        This method processes the API response data to build a structured
        collection of search results with type-specific counts.
        
        Args:
            api_data: Item search results data from Pipedrive API,
                should contain 'items' array and optional 'next_cursor'
            
        Returns:
            ItemSearchResults instance with parsed and categorized data
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
    """Model representing a field search result from Pipedrive API.
    
    This model represents an individual item found when searching
    for specific field values.
    
    Fields:
        id: Unique identifier of the entity containing this field value
        name: The matched field value
    """
    
    id: int
    name: str
    
    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "FieldSearchResult":
        """Create a FieldSearchResult instance from Pipedrive API response data.
        
        Args:
            api_data: Field search result data from Pipedrive API
            
        Returns:
            FieldSearchResult instance with parsed data
        """
        return cls(**api_data)


class FieldSearchResults(BaseModel):
    """Model representing a collection of field search results with metadata.
    
    This model organizes field-specific search results and provides
    pagination support.
    
    Fields:
        items: List of individual field search results
        next_cursor: Pagination cursor for retrieving the next page of results
    """
    
    items: List[FieldSearchResult]
    next_cursor: Optional[str] = None
    
    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any]) -> "FieldSearchResults":
        """Create a FieldSearchResults instance from Pipedrive API response data.
        
        This method processes the API response data to build a structured
        collection of field search results.
        
        Args:
            api_data: Field search results data from Pipedrive API,
                should contain 'items' array and optional 'next_cursor'
            
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