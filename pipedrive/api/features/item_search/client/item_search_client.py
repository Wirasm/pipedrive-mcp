import json
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from log_config import logger
from pipedrive.api.base_client import BaseClient


class ItemSearchClient:
    """Client for Pipedrive itemSearch API endpoints"""
    
    def __init__(self, base_client: BaseClient):
        """
        Initialize the ItemSearch client
        
        Args:
            base_client: BaseClient instance for making API requests
        """
        self.base_client = base_client
    
    async def search_items(
        self,
        term: str,
        item_types: Optional[List[str]] = None,
        fields: Optional[List[str]] = None,
        search_for_related_items: bool = False,
        exact_match: bool = False,
        include_fields: Optional[List[str]] = None,
        limit: int = 100,
        cursor: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Search for items across multiple types in Pipedrive
        
        Args:
            term: The search term to look for (min 2 chars, or 1 if exact_match=True)
            item_types: List of item types to search (deal, person, organization, product, lead, file, mail_attachment, project)
            fields: List of fields to search in (depends on item types)
            search_for_related_items: When True, includes related items in the results
            exact_match: When True, only exact matches are returned
            include_fields: List of additional fields to include
            limit: Maximum number of results to return (max 500)
            cursor: Pagination cursor for the next page
            
        Returns:
            Tuple of (list of search results, next cursor)
            
        Raises:
            ValueError: If validation fails
        """
        logger.info(f"ItemSearchClient: Attempting to search for items with term '{term}'")

        # Validate required parameters
        if not term or not term.strip():
            raise ValueError("Search term cannot be empty")
            
        if not exact_match and len(term.strip()) < 2:
            raise ValueError("Search term must be at least 2 characters when exact_match is False")
            
        if exact_match and len(term.strip()) < 1:
            raise ValueError("Search term must be at least 1 character when exact_match is True")
        
        # Build query parameters
        query_params: Dict[str, Any] = {
            "term": term,
            "exact_match": "true" if exact_match else "false",
            "search_for_related_items": "true" if search_for_related_items else "false",
            "limit": limit,
            "cursor": cursor,
        }
        
        # Add optional parameters if provided
        if item_types:
            query_params["item_types"] = ",".join(item_types)
            
        if fields:
            query_params["fields"] = ",".join(fields)
            
        if include_fields:
            query_params["include_fields"] = ",".join(include_fields)
        
        # Filter out None values
        final_query_params = {k: v for k, v in query_params.items() if v is not None}
        
        logger.debug(f"ItemSearchClient: search_items query_params: {final_query_params}")
        
        # Make the API request
        response_data = await self.base_client.request(
            "GET",
            "/itemSearch",
            query_params=final_query_params
        )
        
        # Extract data and pagination cursor
        items = response_data.get("data", [])
        additional_data = response_data.get("additional_data", {})
        next_cursor = (
            additional_data.get("next_cursor")
            if isinstance(additional_data, dict)
            else None
        )
        
        logger.info(f"ItemSearchClient: Found {len(items)} items matching term '{term}'")
        
        return items, next_cursor
    
    async def search_field(
        self,
        term: str,
        entity_type: str,
        field: str,
        match: str = "exact",
        limit: int = 100,
        cursor: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Search for items using a specific field
        
        Args:
            term: The search term to look for (min 2 chars, or 1 if match is not 'exact')
            entity_type: The type of entity to search (deal, person, organization, product, lead, project)
            field: The field key to search in
            match: Type of match: exact, beginning, or middle
            limit: Maximum number of results to return (max 500)
            cursor: Pagination cursor for the next page
            
        Returns:
            Tuple of (list of field search results, next cursor)
            
        Raises:
            ValueError: If validation fails
        """
        logger.info(f"ItemSearchClient: Attempting to search field '{field}' with term '{term}'")
        
        # Validate required parameters
        if not term or not term.strip():
            raise ValueError("Search term cannot be empty")
            
        if match == "exact" and len(term.strip()) < 1:
            raise ValueError("Search term must be at least 1 character for exact matching")
            
        if match != "exact" and len(term.strip()) < 2:
            raise ValueError("Search term must be at least 2 characters for beginning or middle matching")
        
        if not entity_type:
            raise ValueError("Entity type cannot be empty")
            
        if not field:
            raise ValueError("Field key cannot be empty")
        
        # Validate entity_type
        valid_entity_types = ["deal", "person", "organization", "product", "lead", "project"]
        if entity_type not in valid_entity_types:
            raise ValueError(f"Invalid entity type: {entity_type}. Must be one of: {', '.join(valid_entity_types)}")
        
        # Validate match type
        valid_match_types = ["exact", "beginning", "middle"]
        if match not in valid_match_types:
            raise ValueError(f"Invalid match type: {match}. Must be one of: {', '.join(valid_match_types)}")
        
        # Build query parameters
        query_params: Dict[str, Any] = {
            "term": term,
            "entity_type": entity_type,
            "field": field,
            "match": match,
            "limit": limit,
            "cursor": cursor,
        }
        
        # Filter out None values
        final_query_params = {k: v for k, v in query_params.items() if v is not None}
        
        logger.debug(f"ItemSearchClient: search_field query_params: {final_query_params}")
        
        # Make the API request
        response_data = await self.base_client.request(
            "GET",
            "/itemSearch/field",
            query_params=final_query_params
        )
        
        # Extract data and pagination cursor
        items = response_data.get("data", [])
        additional_data = response_data.get("additional_data", {})
        next_cursor = (
            additional_data.get("next_cursor")
            if isinstance(additional_data, dict)
            else None
        )
        
        logger.info(f"ItemSearchClient: Found {len(items)} field values matching term '{term}'")
        
        return items, next_cursor