import json
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from log_config import logger
from pipedrive.api.base_client import BaseClient


class OrganizationClient:
    """Client for Pipedrive Organization API endpoints"""

    def __init__(self, base_client: BaseClient):
        """
        Initialize the Organization client

        Args:
            base_client: BaseClient instance for making API requests
        """
        self.base_client = base_client
    
    async def create_organization(
        self,
        name: str,
        owner_id: Optional[int] = None,
        address: Optional[str] = None,
        visible_to: Optional[int] = None,
        label_ids: Optional[List[int]] = None,
        add_time: Optional[str] = None,  # Expected format "YYYY-MM-DD HH:MM:SS"
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new organization in Pipedrive
        
        Args:
            name: Name of the organization
            owner_id: User ID of the owner
            address: Physical address of the organization
            visible_to: Visibility setting
            label_ids: IDs of labels to assign to the organization
            add_time: Creation timestamp
            custom_fields: Custom field values
            
        Returns:
            Created organization data
        """
        logger.info(f"OrganizationClient: Attempting to create organization '{name}'")
        payload: Dict[str, Any] = {"name": name}
        
        if owner_id is not None:
            payload["owner_id"] = owner_id
        if address is not None:
            payload["address"] = address
        if visible_to is not None:
            payload["visible_to"] = visible_to
        if label_ids is not None:
            payload["label_ids"] = label_ids
        if add_time is not None:
            payload["add_time"] = add_time

        if custom_fields:
            payload.update(custom_fields)

        logger.debug(
            f"OrganizationClient: create_organization payload: {json.dumps(payload, indent=2)}"
        )
        response_data = await self.base_client.request("POST", "/organizations", json_payload=payload)
        return response_data.get("data", {})
    
    async def get_organization(
        self,
        organization_id: int,
        include_fields: Optional[List[str]] = None,
        custom_fields_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get an organization by ID from Pipedrive
        
        Args:
            organization_id: ID of the organization to retrieve
            include_fields: Additional fields to include
            custom_fields_keys: Custom fields to include
            
        Returns:
            Organization data
        """
        logger.info(f"OrganizationClient: Attempting to get organization with ID {organization_id}")
        query_params: Dict[str, Any] = {}
        
        if include_fields:
            query_params["include_fields"] = ",".join(include_fields)
        if custom_fields_keys:
            query_params["custom_fields"] = ",".join(custom_fields_keys)

        response_data = await self.base_client.request(
            "GET",
            f"/organizations/{organization_id}",
            query_params=query_params if query_params else None,
        )
        return response_data.get("data", {})
    
    async def update_organization(
        self,
        organization_id: int,
        name: Optional[str] = None,
        owner_id: Optional[int] = None,
        address: Optional[str] = None,
        visible_to: Optional[int] = None,
        label_ids: Optional[List[int]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing organization in Pipedrive
        
        Args:
            organization_id: ID of the organization to update
            name: Updated name of the organization
            owner_id: Updated owner user ID
            address: Updated address of the organization
            visible_to: Updated visibility setting
            label_ids: Updated label IDs
            custom_fields: Updated custom field values
            
        Returns:
            Updated organization data
            
        Raises:
            ValueError: If no fields are provided to update
        """
        logger.info(f"OrganizationClient: Attempting to update organization with ID {organization_id}")
        payload: Dict[str, Any] = {}
        
        if name is not None:
            payload["name"] = name
        if owner_id is not None:
            payload["owner_id"] = owner_id
        if address is not None:
            payload["address"] = address
        if visible_to is not None:
            payload["visible_to"] = visible_to
        if label_ids is not None:
            payload["label_ids"] = label_ids

        if custom_fields:
            payload.update(custom_fields)

        if not payload:
            logger.warning(
                f"OrganizationClient: update_organization called with no fields to update for ID {organization_id}."
            )
            # For safety, let's assume it's not intended if no fields are provided.
            raise ValueError(
                "At least one field must be provided for updating an organization."
            )

        logger.debug(
            f"OrganizationClient: update_organization payload for ID {organization_id}: {json.dumps(payload, indent=2)}"
        )
        response_data = await self.base_client.request(
            "PATCH", f"/organizations/{organization_id}", json_payload=payload
        )
        return response_data.get("data", {})
    
    async def delete_organization(self, organization_id: int) -> Dict[str, Any]:
        """
        Delete an organization from Pipedrive
        
        Args:
            organization_id: ID of the organization to delete
            
        Returns:
            Deletion result data
        """
        logger.info(f"OrganizationClient: Attempting to delete organization with ID {organization_id}")
        response_data = await self.base_client.request("DELETE", f"/organizations/{organization_id}")
        
        # Successful delete usually returns: {"success": true, "data": {"id": organization_id}}
        return (
            response_data.get("data", {})
            if response_data.get("success")
            else {"id": organization_id, "error_details": response_data}
        )
    
    async def list_organizations(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        filter_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
        include_fields: Optional[List[str]] = None,
        custom_fields_keys: Optional[List[str]] = None,
        updated_since: Optional[str] = None,  # RFC3339 format, e.g. 2025-01-01T10:20:00Z
        updated_until: Optional[str] = None,  # RFC3339 format
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        List organizations from Pipedrive with pagination
        
        Args:
            limit: Maximum number of results to return
            cursor: Pagination cursor for retrieving the next page
            filter_id: ID of the filter to apply
            owner_id: Filter by owner user ID
            sort_by: Field to sort by
            sort_direction: Sort direction (asc or desc)
            include_fields: Additional fields to include
            custom_fields_keys: Custom fields to include
            updated_since: Filter by update time (RFC3339 format)
            updated_until: Filter by update time (RFC3339 format)
            
        Returns:
            Tuple of (list of organizations, next cursor)
        """
        logger.info(
            f"OrganizationClient: Attempting to list organizations with limit {limit}, cursor '{cursor}'"
        )
        query_params: Dict[str, Any] = {
            "limit": limit,
            "cursor": cursor,
            "filter_id": filter_id,
            "owner_id": owner_id,
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
            f"OrganizationClient: list_organizations query_params: {final_query_params}"
        )

        response_data = await self.base_client.request(
            "GET",
            "/organizations",
            query_params=final_query_params if final_query_params else None,
        )

        organizations_list = response_data.get("data", [])
        additional_data = response_data.get("additional_data", {})
        next_cursor = (
            additional_data.get("next_cursor")
            if isinstance(additional_data, dict)
            else None
        )
        logger.info(
            f"OrganizationClient: Listed {len(organizations_list)} organizations. Next cursor: '{next_cursor}'"
        )
        return organizations_list, next_cursor

    async def search_organizations(
        self,
        term: str,
        fields: Optional[List[str]] = None,
        exact_match: bool = False,
        include_fields: Optional[List[str]] = None,
        limit: int = 100,
        cursor: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Search for organizations in Pipedrive

        Args:
            term: The search term to look for (min 2 chars, or 1 if exact_match=True)
            fields: Fields to search in (name, address, notes, custom_fields)
            exact_match: When True, only exact matches are returned
            include_fields: Additional fields to include in the results
            limit: Maximum number of results to return (max 500)
            cursor: Pagination cursor

        Returns:
            Tuple of (list of organization results, next cursor)
        """
        logger.info(
            f"OrganizationClient: Searching for organizations with term '{term}'"
        )

        # Build query parameters
        query_params: Dict[str, Any] = {
            "term": term,
            "exact_match": "true" if exact_match else "false",  # API expects string
            "limit": limit,
            "cursor": cursor,
        }

        if fields:
            query_params["fields"] = ",".join(fields)

        if include_fields:
            query_params["include_fields"] = ",".join(include_fields)

        # Filter out None values
        final_query_params = {k: v for k, v in query_params.items() if v is not None}

        logger.debug(f"OrganizationClient: search_organizations query_params: {final_query_params}")

        response_data = await self.base_client.request(
            "GET",
            "/organizations/search",
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
            f"OrganizationClient: Found {len(items)} organizations. Next cursor: '{next_cursor}'"
        )

        return items, next_cursor
    
    async def add_follower(
        self,
        organization_id: int,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Add a follower to an organization
        
        Args:
            organization_id: ID of the organization
            user_id: ID of the user to add as a follower
            
        Returns:
            Added follower data
        """
        logger.info(f"OrganizationClient: Adding follower user ID {user_id} to organization {organization_id}")
        
        payload = {"user_id": user_id}
        
        response_data = await self.base_client.request(
            "POST", 
            f"/organizations/{organization_id}/followers",
            json_payload=payload
        )
        
        return response_data.get("data", {})
    
    async def delete_follower(
        self,
        organization_id: int,
        follower_id: int
    ) -> Dict[str, Any]:
        """
        Delete a follower from an organization
        
        Args:
            organization_id: ID of the organization
            follower_id: ID of the follower to delete
            
        Returns:
            Deletion result data
        """
        logger.info(f"OrganizationClient: Removing follower ID {follower_id} from organization {organization_id}")
        
        response_data = await self.base_client.request(
            "DELETE",
            f"/organizations/{organization_id}/followers/{follower_id}"
        )
        
        # Successful delete usually returns: {"success": true, "data": ...}
        return (
            response_data.get("data", {})
            if response_data.get("success")
            else {"error_details": response_data}
        )