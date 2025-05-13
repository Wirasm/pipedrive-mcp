from typing import Any, Dict, List, Optional, Tuple

import httpx

from log_config import logger
from pipedrive.api.base_client import BaseClient
from pipedrive.api.features.deals.client.deal_client import DealClient
from pipedrive.api.features.item_search.client.item_search_client import (
    ItemSearchClient,
)
from pipedrive.api.features.organizations.client.organization_client import (
    OrganizationClient,
)
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
        self.deals = DealClient(self.base_client)
        self.organizations = OrganizationClient(self.base_client)
        self.item_search = ItemSearchClient(self.base_client)

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

    # --- Deal Methods (forwarding to deals client) ---

    async def create_deal(
        self,
        title: str,
        value: Optional[float] = None,
        currency: str = "USD",
        person_id: Optional[int] = None,
        org_id: Optional[int] = None,
        status: str = "open",
        expected_close_date: Optional[str] = None,
        owner_id: Optional[int] = None,
        stage_id: Optional[int] = None,
        pipeline_id: Optional[int] = None,
        visible_to: Optional[int] = None,
        probability: Optional[int] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Forward to deals client create_deal method"""
        return await self.deals.create_deal(
            title=title,
            value=value,
            currency=currency,
            person_id=person_id,
            org_id=org_id,
            status=status,
            expected_close_date=expected_close_date,
            owner_id=owner_id,
            stage_id=stage_id,
            pipeline_id=pipeline_id,
            visible_to=visible_to,
            probability=probability,
            custom_fields=custom_fields,
        )

    async def get_deal(
        self,
        deal_id: int,
        include_fields: Optional[List[str]] = None,
        custom_fields_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Forward to deals client get_deal method"""
        return await self.deals.get_deal(
            deal_id=deal_id,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys,
        )

    async def update_deal(
        self,
        deal_id: int,
        title: Optional[str] = None,
        value: Optional[float] = None,
        currency: Optional[str] = None,
        person_id: Optional[int] = None,
        org_id: Optional[int] = None,
        status: Optional[str] = None,
        expected_close_date: Optional[str] = None,
        owner_id: Optional[int] = None,
        stage_id: Optional[int] = None,
        pipeline_id: Optional[int] = None,
        visible_to: Optional[int] = None,
        probability: Optional[int] = None,
        lost_reason: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Forward to deals client update_deal method"""
        return await self.deals.update_deal(
            deal_id=deal_id,
            title=title,
            value=value,
            currency=currency,
            person_id=person_id,
            org_id=org_id,
            status=status,
            expected_close_date=expected_close_date,
            owner_id=owner_id,
            stage_id=stage_id,
            pipeline_id=pipeline_id,
            visible_to=visible_to,
            probability=probability,
            lost_reason=lost_reason,
            custom_fields=custom_fields,
        )

    async def delete_deal(self, deal_id: int) -> Dict[str, Any]:
        """Forward to deals client delete_deal method"""
        return await self.deals.delete_deal(deal_id=deal_id)

    # --- Item Search Methods (forwarding to item_search client) ---

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
        """Forward to item_search client search_items method"""
        return await self.item_search.search_items(
            term=term,
            item_types=item_types,
            fields=fields,
            search_for_related_items=search_for_related_items,
            exact_match=exact_match,
            include_fields=include_fields,
            limit=limit,
            cursor=cursor,
        )

    async def search_field(
        self,
        term: str,
        entity_type: str,
        field: str,
        match: str = "exact",
        limit: int = 100,
        cursor: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Forward to item_search client search_field method"""
        return await self.item_search.search_field(
            term=term,
            entity_type=entity_type,
            field=field,
            match=match,
            limit=limit,
            cursor=cursor,
        )

    # --- Organization Methods (forwarding to organizations client) ---

    async def create_organization(
        self,
        name: str,
        owner_id: Optional[int] = None,
        address: Optional[str] = None,
        visible_to: Optional[int] = None,
        label_ids: Optional[List[int]] = None,
        add_time: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Forward to organizations client create_organization method"""
        return await self.organizations.create_organization(
            name=name,
            owner_id=owner_id,
            address=address,
            visible_to=visible_to,
            label_ids=label_ids,
            add_time=add_time,
            custom_fields=custom_fields,
        )

    async def get_organization(
        self,
        organization_id: int,
        include_fields: Optional[List[str]] = None,
        custom_fields_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Forward to organizations client get_organization method"""
        return await self.organizations.get_organization(
            organization_id=organization_id,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys,
        )

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
        """Forward to organizations client update_organization method"""
        return await self.organizations.update_organization(
            organization_id=organization_id,
            name=name,
            owner_id=owner_id,
            address=address,
            visible_to=visible_to,
            label_ids=label_ids,
            custom_fields=custom_fields,
        )

    async def delete_organization(self, organization_id: int) -> Dict[str, Any]:
        """Forward to organizations client delete_organization method"""
        return await self.organizations.delete_organization(
            organization_id=organization_id
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
        updated_since: Optional[str] = None,
        updated_until: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Forward to organizations client list_organizations method"""
        return await self.organizations.list_organizations(
            limit=limit,
            cursor=cursor,
            filter_id=filter_id,
            owner_id=owner_id,
            sort_by=sort_by,
            sort_direction=sort_direction,
            include_fields=include_fields,
            custom_fields_keys=custom_fields_keys,
            updated_since=updated_since,
            updated_until=updated_until,
        )

    async def add_organization_follower(
        self, organization_id: int, user_id: int
    ) -> Dict[str, Any]:
        """Forward to organizations client add_follower method"""
        return await self.organizations.add_follower(
            organization_id=organization_id, user_id=user_id
        )

    async def delete_organization_follower(
        self, organization_id: int, follower_id: int
    ) -> Dict[str, Any]:
        """Forward to organizations client delete_follower method"""
        return await self.organizations.delete_follower(
            organization_id=organization_id, follower_id=follower_id
        )
