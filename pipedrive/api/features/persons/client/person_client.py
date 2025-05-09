import json
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from log_config import logger
from pipedrive.api.base_client import BaseClient


class PersonClient:
    """Client for Pipedrive Person API endpoints"""

    def __init__(self, base_client: BaseClient):
        """
        Initialize the Person client

        Args:
            base_client: BaseClient instance for making API requests
        """
        self.base_client = base_client
    
    async def create_person(
        self,
        name: str,
        owner_id: Optional[int] = None,
        org_id: Optional[int] = None,
        emails: Optional[List[Dict[str, Any]]] = None,
        phones: Optional[List[Dict[str, Any]]] = None,
        visible_to: Optional[int] = None,
        add_time: Optional[str] = None,  # Expected format "YYYY-MM-DD HH:MM:SS"
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new person in Pipedrive
        
        Args:
            name: Full name of the person
            owner_id: User ID of the owner
            org_id: Organization ID to link the person to
            emails: List of email objects
            phones: List of phone objects
            visible_to: Visibility setting
            add_time: Creation timestamp
            custom_fields: Custom field values
            
        Returns:
            Created person data
        """
        logger.info(f"PersonClient: Attempting to create person '{name}'")
        payload: Dict[str, Any] = {"name": name}
        
        if owner_id is not None:
            payload["owner_id"] = owner_id
        if org_id is not None:
            payload["org_id"] = org_id
        if emails:  # Should be a list of email objects
            payload["emails"] = emails
        if phones:  # Should be a list of phone objects
            payload["phones"] = phones
        if visible_to is not None:
            payload["visible_to"] = visible_to
        if add_time is not None:
            payload["add_time"] = add_time

        if custom_fields:
            payload.update(custom_fields)

        logger.debug(
            f"PersonClient: create_person payload: {json.dumps(payload, indent=2)}"
        )
        response_data = await self.base_client.request("POST", "/persons", json_payload=payload)
        return response_data.get("data", {})
    
    async def get_person(
        self,
        person_id: int,
        include_fields: Optional[List[str]] = None,
        custom_fields_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get a person by ID from Pipedrive
        
        Args:
            person_id: ID of the person to retrieve
            include_fields: Additional fields to include
            custom_fields_keys: Custom fields to include
            
        Returns:
            Person data
        """
        logger.info(f"PersonClient: Attempting to get person with ID {person_id}")
        query_params: Dict[str, Any] = {}
        
        if include_fields:
            query_params["include_fields"] = ",".join(include_fields)
        if custom_fields_keys:
            query_params["custom_fields"] = ",".join(custom_fields_keys)

        response_data = await self.base_client.request(
            "GET",
            f"/persons/{person_id}",
            query_params=query_params if query_params else None,
        )
        return response_data.get("data", {})
    
    async def update_person(
        self,
        person_id: int,
        name: Optional[str] = None,
        owner_id: Optional[int] = None,
        org_id: Optional[int] = None,
        emails: Optional[List[Dict[str, Any]]] = None,
        phones: Optional[List[Dict[str, Any]]] = None,
        visible_to: Optional[int] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing person in Pipedrive
        
        Args:
            person_id: ID of the person to update
            name: Updated name of the person
            owner_id: Updated owner user ID
            org_id: Updated organization ID
            emails: Updated list of email objects
            phones: Updated list of phone objects
            visible_to: Updated visibility setting
            custom_fields: Updated custom field values
            
        Returns:
            Updated person data
            
        Raises:
            ValueError: If no fields are provided to update
        """
        logger.info(f"PersonClient: Attempting to update person with ID {person_id}")
        payload: Dict[str, Any] = {}
        
        if name is not None:
            payload["name"] = name
        if owner_id is not None:
            payload["owner_id"] = owner_id
        if org_id is not None:
            payload["org_id"] = org_id
        if emails is not None:  # If None, Pipedrive won't update emails. To clear, send empty list [].
            payload["emails"] = emails
        if phones is not None:  # If None, Pipedrive won't update phones. To clear, send empty list [].
            payload["phones"] = phones
        if visible_to is not None:
            payload["visible_to"] = visible_to

        if custom_fields:
            payload.update(custom_fields)

        if not payload:
            logger.warning(
                f"PersonClient: update_person called with no fields to update for ID {person_id}."
            )
            # For safety, let's assume it's not intended if no fields are provided.
            raise ValueError(
                "At least one field must be provided for updating a person."
            )

        logger.debug(
            f"PersonClient: update_person payload for ID {person_id}: {json.dumps(payload, indent=2)}"
        )
        response_data = await self.base_client.request(
            "PATCH", f"/persons/{person_id}", json_payload=payload
        )
        return response_data.get("data", {})
    
    async def delete_person(self, person_id: int) -> Dict[str, Any]:
        """
        Delete a person from Pipedrive
        
        Args:
            person_id: ID of the person to delete
            
        Returns:
            Deletion result data
        """
        logger.info(f"PersonClient: Attempting to delete person with ID {person_id}")
        response_data = await self.base_client.request("DELETE", f"/persons/{person_id}")
        
        # Successful delete usually returns: {"success": true, "data": {"id": person_id}}
        return (
            response_data.get("data", {})
            if response_data.get("success")
            else {"id": person_id, "error_details": response_data}
        )
    
    async def list_persons(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        filter_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        org_id: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
        include_fields: Optional[List[str]] = None,
        custom_fields_keys: Optional[List[str]] = None,
        updated_since: Optional[str] = None,  # RFC3339 format, e.g. 2025-01-01T10:20:00Z
        updated_until: Optional[str] = None,  # RFC3339 format
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        List persons from Pipedrive with pagination
        
        Args:
            limit: Maximum number of results to return
            cursor: Pagination cursor for retrieving the next page
            filter_id: ID of the filter to apply
            owner_id: Filter by owner user ID
            org_id: Filter by organization ID
            sort_by: Field to sort by
            sort_direction: Sort direction (asc or desc)
            include_fields: Additional fields to include
            custom_fields_keys: Custom fields to include
            updated_since: Filter by update time (RFC3339 format)
            updated_until: Filter by update time (RFC3339 format)
            
        Returns:
            Tuple of (list of persons, next cursor)
        """
        logger.info(
            f"PersonClient: Attempting to list persons with limit {limit}, cursor '{cursor}'"
        )
        query_params: Dict[str, Any] = {
            "limit": limit,
            "cursor": cursor,
            "filter_id": filter_id,
            "owner_id": owner_id,
            "org_id": org_id,
            "sort_by": sort_by,
            "sort_direction": sort_direction,
            "updated_since": updated_since,
            "updated_until": updated_until,
        }
        if include_fields:
            query_params["include_fields"] = ",".join(include_fields)
        if custom_fields_keys:
            query_params["custom_fields"] = ",".join(custom_fields_keys)

        # Filter out None values from query_params before sending
        final_query_params = {k: v for k, v in query_params.items() if v is not None}
        logger.debug(
            f"PersonClient: list_persons query_params: {final_query_params}"
        )

        response_data = await self.base_client.request(
            "GET",
            "/persons",
            query_params=final_query_params if final_query_params else None,
        )

        persons_list = response_data.get("data", [])
        additional_data = response_data.get("additional_data", {})
        next_cursor = (
            additional_data.get("next_cursor")
            if isinstance(additional_data, dict)
            else None
        )
        logger.info(
            f"PersonClient: Listed {len(persons_list)} persons. Next cursor: '{next_cursor}'"
        )
        return persons_list, next_cursor

    async def search_persons(
        self,
        term: str,
        fields: Optional[List[str]] = None,
        exact_match: bool = False,
        organization_id: Optional[int] = None,
        include_fields: Optional[List[str]] = None,
        limit: int = 100,
        cursor: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Search for persons in Pipedrive

        Args:
            term: The search term to look for (min 2 chars, or 1 if exact_match=True)
            fields: Fields to search in (name, email, phone, notes, custom_fields)
            exact_match: When True, only exact matches are returned
            organization_id: Filter persons by organization ID
            include_fields: Additional fields to include in the results
            limit: Maximum number of results to return (max 500)
            cursor: Pagination cursor

        Returns:
            Tuple of (list of person results, next cursor)
        """
        logger.info(
            f"PersonClient: Searching for persons with term '{term}'"
        )

        # Build query parameters
        query_params: Dict[str, Any] = {
            "term": term,
            "exact_match": "true" if exact_match else "false",  # API expects string
            "limit": limit,
            "cursor": cursor,
            "organization_id": organization_id,
        }

        if fields:
            query_params["fields"] = ",".join(fields)

        if include_fields:
            query_params["include_fields"] = ",".join(include_fields)

        # Filter out None values
        final_query_params = {k: v for k, v in query_params.items() if v is not None}

        logger.debug(f"PersonClient: search_persons query_params: {final_query_params}")

        response_data = await self.base_client.request(
            "GET",
            "/persons/search",
            query_params=final_query_params
        )

        data = response_data.get("data", [])
        items = data.get("items", []) if isinstance(data, dict) else []

        # Extract the next cursor from additional_data
        additional_data = response_data.get("additional_data", {})
        next_cursor = (
            additional_data.get("next_cursor")
            if isinstance(additional_data, dict)
            else None
        )

        logger.info(
            f"PersonClient: Found {len(items)} persons. Next cursor: '{next_cursor}'"
        )

        return items, next_cursor