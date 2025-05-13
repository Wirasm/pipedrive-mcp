import json
from typing import Any, Dict, List, Optional, Tuple, Union, cast
from uuid import UUID

from log_config import logger
from pipedrive.api.base_client import BaseClient


class LeadClient:
    """Client for Pipedrive Lead API endpoints"""

    def __init__(self, base_client: BaseClient):
        """
        Initialize the Lead client

        Args:
            base_client: BaseClient instance for making API requests
        """
        self.base_client = base_client

    async def create_lead(
        self,
        title: str,
        amount: Optional[float] = None,
        currency: str = "USD",
        person_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        label_ids: Optional[List[str]] = None,
        expected_close_date: Optional[str] = None,  # ISO format YYYY-MM-DD
        visible_to: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Create a new lead in Pipedrive

        Args:
            title: Title of the lead
            amount: Monetary value of the lead
            currency: Currency of the lead value (3-letter code, e.g., USD, EUR)
            person_id: ID of the person linked to the lead
            organization_id: ID of the organization linked to the lead
            owner_id: User ID of the lead owner
            label_ids: List of lead label UUIDs
            expected_close_date: Expected close date in ISO format (YYYY-MM-DD)
            visible_to: Visibility setting

        Returns:
            Created lead data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"LeadClient: Attempting to create lead '{title}'")

        try:
            payload: Dict[str, Any] = {"title": title}

            if person_id is not None:
                payload["person_id"] = person_id
            if organization_id is not None:
                payload["organization_id"] = organization_id
            if owner_id is not None:
                payload["owner_id"] = owner_id
            if label_ids is not None:
                payload["label_ids"] = label_ids
            if expected_close_date:
                payload["expected_close_date"] = expected_close_date
            if visible_to is not None:
                payload["visible_to"] = visible_to

            # Value needs to be an object with amount and currency
            if amount is not None:
                payload["value"] = {"amount": amount, "currency": currency or "USD"}

            # Validate required fields
            if not title or not title.strip():
                raise ValueError("Lead title cannot be empty")

            # Either person_id or organization_id must be provided
            if person_id is None and organization_id is None:
                raise ValueError("Either person_id or organization_id must be provided")

            # Log the payload without sensitive information
            safe_log_payload = payload.copy()
            if "value" in safe_log_payload:
                safe_log_payload["value"] = "[REDACTED]"

            logger.debug(
                f"LeadClient: create_lead payload: {json.dumps(safe_log_payload, indent=2)}"
            )

            # Use v1 endpoint for leads
            response_data = await self.base_client.request(
                "POST", "/leads", json_payload=payload, version="v1"
            )
            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in create_lead: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in create_lead: {str(e)}")
            raise

    async def get_lead(
        self,
        lead_id: str,
    ) -> Dict[str, Any]:
        """
        Get a lead by ID from Pipedrive

        Args:
            lead_id: UUID of the lead to retrieve (string format)

        Returns:
            Lead data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"LeadClient: Attempting to get lead with ID {lead_id}")

        try:
            # Validate lead_id as UUID
            try:
                uuid_obj = UUID(lead_id)
                # Normalize the UUID format
                lead_id = str(uuid_obj)
            except ValueError:
                raise ValueError(
                    f"Invalid lead ID: {lead_id}. Must be a valid UUID string."
                )

            # Use v1 endpoint for leads
            response_data = await self.base_client.request(
                "GET",
                f"/leads/{lead_id}",
                version="v1",
            )
            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in get_lead: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in get_lead: {str(e)}")
            raise

    async def update_lead(
        self,
        lead_id: str,
        title: Optional[str] = None,
        amount: Optional[float] = None,
        currency: Optional[str] = None,
        person_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        label_ids: Optional[List[str]] = None,
        expected_close_date: Optional[str] = None,
        visible_to: Optional[int] = None,
        is_archived: Optional[bool] = None,
        was_seen: Optional[bool] = None,
        channel: Optional[int] = None,
        channel_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing lead in Pipedrive

        Args:
            lead_id: UUID of the lead to update (string format)
            title: Updated title of the lead
            amount: Updated monetary value
            currency: Updated currency
            person_id: Updated person ID
            organization_id: Updated organization ID
            owner_id: Updated owner ID
            label_ids: Updated list of lead label UUIDs
            expected_close_date: Updated expected close date
            visible_to: Updated visibility setting
            is_archived: Whether the lead is archived
            was_seen: Whether the lead was seen
            channel: Updated marketing channel ID
            channel_id: Updated marketing channel specific ID

        Returns:
            Updated lead data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails or no fields are provided to update
        """
        logger.info(f"LeadClient: Attempting to update lead with ID {lead_id}")

        try:
            # Validate lead_id as UUID
            try:
                uuid_obj = UUID(lead_id)
                # Normalize the UUID format
                lead_id = str(uuid_obj)
            except ValueError:
                raise ValueError(
                    f"Invalid lead ID: {lead_id}. Must be a valid UUID string."
                )

            payload: Dict[str, Any] = {}

            if title is not None:
                payload["title"] = title
            if person_id is not None:
                payload["person_id"] = person_id
            if organization_id is not None:
                payload["organization_id"] = organization_id
            if owner_id is not None:
                payload["owner_id"] = owner_id
            if label_ids is not None:
                payload["label_ids"] = label_ids
            if expected_close_date is not None:
                payload["expected_close_date"] = expected_close_date
            if visible_to is not None:
                payload["visible_to"] = visible_to
            if is_archived is not None:
                payload["is_archived"] = is_archived
            if was_seen is not None:
                payload["was_seen"] = was_seen
            if channel is not None:
                payload["channel"] = channel
            if channel_id is not None:
                payload["channel_id"] = channel_id

            # Value handling - must include both amount and currency when provided
            if amount is not None:
                value_obj = {"amount": amount, "currency": currency or "USD"}
                payload["value"] = value_obj
            elif currency is not None and amount is None:
                # If only currency is provided but no amount, we need the current amount
                current_lead = await self.get_lead(lead_id)
                current_amount = None

                # Extract the current amount from the response
                if "value" in current_lead and current_lead["value"]:
                    if isinstance(current_lead["value"], dict):
                        current_amount = current_lead["value"].get("amount")
                    else:
                        current_amount = float(current_lead["value"])

                if current_amount is not None:
                    payload["value"] = {"amount": current_amount, "currency": currency}

            if not payload:
                logger.warning(
                    f"LeadClient: update_lead called with no fields to update for ID {lead_id}."
                )
                # For safety, let's assume it's not intended if no fields are provided.
                raise ValueError(
                    "At least one field must be provided for updating a lead."
                )

            # Additional validations
            if title is not None and not title.strip():
                raise ValueError("Lead title cannot be empty if provided")

            # Log the payload without sensitive information
            safe_log_payload = payload.copy()
            if "value" in safe_log_payload:
                safe_log_payload["value"] = "[REDACTED]"

            logger.debug(
                f"LeadClient: update_lead payload for ID {lead_id}: {json.dumps(safe_log_payload, indent=2)}"
            )

            # Use v1 endpoint for leads
            response_data = await self.base_client.request(
                "PATCH", f"/leads/{lead_id}", json_payload=payload, version="v1"
            )
            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in update_lead: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in update_lead: {str(e)}")
            raise

    async def delete_lead(self, lead_id: str) -> Dict[str, Any]:
        """
        Delete a lead from Pipedrive

        Args:
            lead_id: UUID of the lead to delete (string format)

        Returns:
            Deletion result data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"LeadClient: Attempting to delete lead with ID {lead_id}")

        try:
            # Validate lead_id as UUID
            try:
                uuid_obj = UUID(lead_id)
                # Normalize the UUID format
                lead_id = str(uuid_obj)
            except ValueError:
                raise ValueError(
                    f"Invalid lead ID: {lead_id}. Must be a valid UUID string."
                )

            # Use v1 endpoint for leads
            response_data = await self.base_client.request(
                "DELETE", f"/leads/{lead_id}", version="v1"
            )

            # Successful delete usually returns: {"success": true, "data": {"id": lead_id}}
            return (
                response_data.get("data", {})
                if response_data.get("success")
                else {"id": lead_id, "error_details": response_data}
            )

        except ValueError as e:
            logger.error(f"Validation error in delete_lead: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in delete_lead: {str(e)}")
            raise

    async def list_leads(
        self,
        limit: int = 100,
        start: Optional[int] = None,
        archived_status: Optional[str] = None,
        owner_id: Optional[int] = None,
        person_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        filter_id: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], int, int]:
        """
        List leads from Pipedrive with pagination

        Args:
            limit: Maximum number of results to return
            start: Pagination start index
            archived_status: Filter by archive status (archived, not_archived, all)
            owner_id: Filter by owner user ID
            person_id: Filter by person ID
            organization_id: Filter by organization ID
            filter_id: ID of the filter to apply
            sort: Field to sort by with direction

        Returns:
            Tuple of (list of leads, total count, pagination info)

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"LeadClient: Listing leads with limit {limit}, start {start}")

        try:
            # Validate limit
            if limit < 1:
                raise ValueError(f"Invalid limit: {limit}. Must be a positive integer.")

            # Validate archived_status if provided
            if archived_status is not None and archived_status not in [
                "archived",
                "not_archived",
                "all",
            ]:
                raise ValueError(
                    f"Invalid archived_status: {archived_status}. Must be one of: archived, not_archived, all"
                )

            query_params: Dict[str, Any] = {
                "limit": limit,
                "start": start,
                "archived_status": archived_status,
                "owner_id": owner_id,
                "person_id": person_id,
                "organization_id": organization_id,
                "filter_id": filter_id,
                "sort": sort,
            }

            # Filter out None values from query_params before sending
            final_query_params = {
                k: v for k, v in query_params.items() if v is not None
            }
            logger.debug(f"LeadClient: list_leads query_params: {final_query_params}")

            # Use v1 endpoint for leads
            response_data = await self.base_client.request(
                "GET",
                "/leads",
                query_params=final_query_params if final_query_params else None,
                version="v1",
            )

            leads_list = response_data.get("data", [])

            # Get pagination info from additional_data
            additional_data = response_data.get("additional_data", {})
            pagination = (
                additional_data.get("pagination", {})
                if isinstance(additional_data, dict)
                else {}
            )

            total_count = (
                pagination.get("total_count", 0) if isinstance(pagination, dict) else 0
            )
            more_items_in_collection = (
                pagination.get("more_items_in_collection", False)
                if isinstance(pagination, dict)
                else False
            )
            next_start = (
                pagination.get("next_start", None)
                if isinstance(pagination, dict)
                else None
            )

            logger.info(
                f"LeadClient: Listed {len(leads_list)} leads out of {total_count} total."
            )

            return leads_list, total_count, next_start or 0

        except ValueError as e:
            logger.error(f"Validation error in list_leads: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in list_leads: {str(e)}")
            raise

    async def search_leads(
        self,
        term: str,
        fields: Optional[List[str]] = None,
        exact_match: bool = False,
        person_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        include_fields: Optional[List[str]] = None,
        limit: int = 100,
        cursor: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Search for leads in Pipedrive

        Args:
            term: The search term to look for (min 2 chars, or 1 if exact_match=True)
            fields: Fields to search in (title, notes, custom_fields)
            exact_match: When True, only exact matches are returned
            person_id: Filter leads by person ID
            organization_id: Filter leads by organization ID
            include_fields: Additional fields to include in the results
            limit: Maximum number of results to return (max 500)
            cursor: Pagination cursor

        Returns:
            Tuple of (list of search results, next cursor)

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"LeadClient: Searching for leads with term '{term}'")

        try:
            # Validate required parameters
            if not term:
                raise ValueError("Search term cannot be empty")

            if not exact_match and len(term) < 2:
                raise ValueError(
                    "Search term must be at least 2 characters long when exact_match is False"
                )

            if exact_match and len(term) < 1:
                raise ValueError(
                    "Search term must be at least 1 character long when exact_match is True"
                )

            # Validate limit
            if limit < 1 or limit > 500:
                raise ValueError(
                    f"Invalid limit: {limit}. Must be a positive integer between 1 and 500."
                )

            # Build query parameters
            query_params: Dict[str, Any] = {
                "term": term,
                "exact_match": exact_match,
                "limit": limit,
                "cursor": cursor,
                "person_id": person_id,
                "organization_id": organization_id,
            }

            if fields:
                query_params["fields"] = ",".join(fields)

            if include_fields:
                query_params["include_fields"] = ",".join(include_fields)

            # Filter out None values
            final_query_params = {
                k: v for k, v in query_params.items() if v is not None
            }

            logger.debug(f"LeadClient: search_leads query_params: {final_query_params}")

            # Use v2 endpoint for lead search
            response_data = await self.base_client.request(
                "GET", "/leads/search", query_params=final_query_params, version="v2"
            )

            items = response_data.get("data", {}).get("items", [])

            # Extract the next cursor from additional_data
            additional_data = response_data.get("additional_data", {})
            next_cursor = (
                additional_data.get("next_cursor")
                if isinstance(additional_data, dict)
                else None
            )

            logger.info(
                f"LeadClient: Found {len(items)} leads. Next cursor: '{next_cursor}'"
            )

            return items, next_cursor

        except ValueError as e:
            logger.error(f"Validation error in search_leads: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in search_leads: {str(e)}")
            raise

    async def get_lead_labels(self) -> List[Dict[str, Any]]:
        """
        Get all lead labels from Pipedrive

        Returns:
            List of lead labels

        Raises:
            PipedriveAPIError: If the API call fails
        """
        logger.info("LeadClient: Getting all lead labels")

        try:
            # Use v1 endpoint for lead labels
            response_data = await self.base_client.request(
                "GET", "/leadLabels", version="v1"
            )

            labels = response_data.get("data", [])
            logger.info(f"LeadClient: Got {len(labels)} lead labels")

            return labels

        except Exception as e:
            logger.error(f"Error in get_lead_labels: {str(e)}")
            raise

    async def get_lead_sources(self) -> List[Dict[str, Any]]:
        """
        Get all lead sources from Pipedrive

        Returns:
            List of lead sources

        Raises:
            PipedriveAPIError: If the API call fails
        """
        logger.info("LeadClient: Getting all lead sources")

        try:
            # Use v1 endpoint for lead sources
            response_data = await self.base_client.request(
                "GET", "/leadSources", version="v1"
            )

            sources = response_data.get("data", [])
            logger.info(f"LeadClient: Got {len(sources)} lead sources")

            return sources

        except Exception as e:
            logger.error(f"Error in get_lead_sources: {str(e)}")
            raise
