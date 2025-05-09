from typing import Any, Dict, List, Optional, Tuple

import httpx

from log_config import logger
from pipedrive.api.base_client import BaseClient
from pipedrive.api.features.persons.client.person_client import PersonClient


class PipedriveClient:
    """
    Main client for Pipedrive API with access to all resources
    """
    
    def __init__(
        self, api_token: str, company_domain: str, http_client: httpx.AsyncClient
    ):
        """
        Initialize the Pipedrive client
        
        Args:
            api_token: Pipedrive API token
            company_domain: Pipedrive company domain
            http_client: AsyncClient for HTTP requests
        """
        # Initialize the base client
        self.base_client = BaseClient(api_token, company_domain, http_client)
        
        # Initialize resource-specific clients
        self.persons = PersonClient(self.base_client)
        
        logger.debug("PipedriveClient initialized.")
    
    # --- Person Methods (forwarding to persons client) ---
    
    async def create_person(
        self,
        name: str,
        owner_id: Optional[int] = None,
        org_id: Optional[int] = None,
        emails: Optional[List[Dict[str, Any]]] = None,
        phones: Optional[List[Dict[str, Any]]] = None,
        visible_to: Optional[int] = None,
        add_time: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Forward to persons client create_person method"""
        return await self.persons.create_person(
            name=name,
            owner_id=owner_id,
            org_id=org_id,
            emails=emails,
            phones=phones,
            visible_to=visible_to,
            add_time=add_time,
            custom_fields=custom_fields,
        )
    
    async def get_person(
        self,
        person_id: int,
        include_fields: Optional[List[str]] = None,
        custom_fields_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Forward to persons client get_person method"""
        return await self.persons.get_person(
            person_id=person_id,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys,
        )
    
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
        """Forward to persons client update_person method"""
        return await self.persons.update_person(
            person_id=person_id,
            name=name,
            owner_id=owner_id,
            org_id=org_id,
            emails=emails,
            phones=phones,
            visible_to=visible_to,
            custom_fields=custom_fields,
        )
    
    async def delete_person(self, person_id: int) -> Dict[str, Any]:
        """Forward to persons client delete_person method"""
        return await self.persons.delete_person(person_id=person_id)
    
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
        updated_since: Optional[str] = None,
        updated_until: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Forward to persons client list_persons method"""
        return await self.persons.list_persons(
            limit=limit,
            cursor=cursor,
            filter_id=filter_id,
            owner_id=owner_id,
            org_id=org_id,
            sort_by=sort_by,
            sort_direction=sort_direction,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys,
            updated_since=updated_since,
            updated_until=updated_until,
        )