import json
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from log_config import logger
from pipedrive.api.base_client import BaseClient


class DealClient:
    """Client for Pipedrive Deal API endpoints"""

    def __init__(self, base_client: BaseClient):
        """
        Initialize the Deal client

        Args:
            base_client: BaseClient instance for making API requests
        """
        self.base_client = base_client

    async def create_deal(
        self,
        title: str,
        value: Optional[float] = None,
        currency: str = "USD",
        person_id: Optional[int] = None,
        org_id: Optional[int] = None,
        status: str = "open",
        expected_close_date: Optional[str] = None,  # ISO format YYYY-MM-DD
        owner_id: Optional[int] = None,
        stage_id: Optional[int] = None,
        pipeline_id: Optional[int] = None,
        visible_to: Optional[int] = None,
        probability: Optional[int] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new deal in Pipedrive

        Args:
            title: Title of the deal
            value: Monetary value of the deal
            currency: Currency of the deal value (3-letter code, e.g., USD, EUR)
            person_id: ID of the person linked to the deal
            org_id: ID of the organization linked to the deal
            status: Status of the deal (open, won, lost)
            expected_close_date: Expected close date in ISO format (YYYY-MM-DD)
            owner_id: User ID of the deal owner
            stage_id: ID of the stage the deal is in
            pipeline_id: ID of the pipeline the deal is in
            visible_to: Visibility setting
            probability: Deal success probability percentage (0-100)
            custom_fields: Custom field values

        Returns:
            Created deal data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"DealClient: Attempting to create deal '{title}'")

        try:
            payload: Dict[str, Any] = {"title": title}

            if value is not None:
                payload["value"] = value
            if currency:
                payload["currency"] = currency
            if person_id is not None:
                payload["person_id"] = person_id
            if org_id is not None:
                payload["org_id"] = org_id
            if status:
                payload["status"] = status
            if expected_close_date:
                payload["expected_close_date"] = expected_close_date
            if owner_id is not None:
                payload["owner_id"] = owner_id
            if stage_id is not None:
                payload["stage_id"] = stage_id
            if pipeline_id is not None:
                payload["pipeline_id"] = pipeline_id
            if visible_to is not None:
                payload["visible_to"] = visible_to
            if probability is not None:
                payload["probability"] = probability

            if custom_fields:
                payload.update(custom_fields)

            # Validate required fields
            if not title or not title.strip():
                raise ValueError("Deal title cannot be empty")

            # Log the payload without sensitive information
            safe_log_payload = payload.copy()
            if "value" in safe_log_payload:
                safe_log_payload["value"] = "[REDACTED]"

            logger.debug(
                f"DealClient: create_deal payload: {json.dumps(safe_log_payload, indent=2)}"
            )

            response_data = await self.base_client.request("POST", "/deals", json_payload=payload)
            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in create_deal: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in create_deal: {str(e)}")
            raise

    async def get_deal(
        self,
        deal_id: int,
        include_fields: Optional[List[str]] = None,
        custom_fields_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get a deal by ID from Pipedrive

        Args:
            deal_id: ID of the deal to retrieve
            include_fields: Additional fields to include
            custom_fields_keys: Custom fields to include

        Returns:
            Deal data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"DealClient: Attempting to get deal with ID {deal_id}")

        try:
            # Validate deal_id
            if deal_id <= 0:
                raise ValueError(f"Invalid deal ID: {deal_id}. Must be a positive integer.")

            query_params: Dict[str, Any] = {}

            if include_fields:
                query_params["include_fields"] = ",".join(include_fields)
            if custom_fields_keys:
                query_params["custom_fields"] = ",".join(custom_fields_keys)

            response_data = await self.base_client.request(
                "GET",
                f"/deals/{deal_id}",
                query_params=query_params if query_params else None,
            )
            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in get_deal: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in get_deal: {str(e)}")
            raise

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
        """
        Update an existing deal in Pipedrive

        Args:
            deal_id: ID of the deal to update
            title: Updated title of the deal
            value: Updated monetary value
            currency: Updated currency
            person_id: Updated person ID
            org_id: Updated organization ID
            status: Updated status
            expected_close_date: Updated expected close date
            owner_id: Updated owner ID
            stage_id: Updated stage ID
            pipeline_id: Updated pipeline ID
            visible_to: Updated visibility setting
            probability: Updated success probability
            lost_reason: Reason if the deal was lost
            custom_fields: Updated custom field values

        Returns:
            Updated deal data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails or no fields are provided to update
        """
        logger.info(f"DealClient: Attempting to update deal with ID {deal_id}")

        try:
            # Validate deal_id
            if deal_id <= 0:
                raise ValueError(f"Invalid deal ID: {deal_id}. Must be a positive integer.")

            payload: Dict[str, Any] = {}

            if title is not None:
                payload["title"] = title
            if value is not None:
                payload["value"] = value
            if currency is not None:
                payload["currency"] = currency
            if person_id is not None:
                payload["person_id"] = person_id
            if org_id is not None:
                payload["org_id"] = org_id
            if status is not None:
                payload["status"] = status
            if expected_close_date is not None:
                payload["expected_close_date"] = expected_close_date
            if owner_id is not None:
                payload["owner_id"] = owner_id
            if stage_id is not None:
                payload["stage_id"] = stage_id
            if pipeline_id is not None:
                payload["pipeline_id"] = pipeline_id
            if visible_to is not None:
                payload["visible_to"] = visible_to
            if probability is not None:
                payload["probability"] = probability
            if lost_reason is not None:
                payload["lost_reason"] = lost_reason

            if custom_fields:
                payload.update(custom_fields)

            if not payload:
                logger.warning(
                    f"DealClient: update_deal called with no fields to update for ID {deal_id}."
                )
                # For safety, let's assume it's not intended if no fields are provided.
                raise ValueError(
                    "At least one field must be provided for updating a deal."
                )

            # Additional validations
            if status is not None and status not in ["open", "won", "lost"]:
                raise ValueError(f"Invalid status value: {status}. Must be one of: open, won, lost")

            if status != "lost" and lost_reason is not None:
                raise ValueError("Lost reason can only be set when status is 'lost'")

            if probability is not None and (probability < 0 or probability > 100):
                raise ValueError(f"Invalid probability value: {probability}. Must be between 0 and 100")

            # Log the payload without sensitive information
            safe_log_payload = payload.copy()
            if "value" in safe_log_payload:
                safe_log_payload["value"] = "[REDACTED]"

            logger.debug(
                f"DealClient: update_deal payload for ID {deal_id}: {json.dumps(safe_log_payload, indent=2)}"
            )

            response_data = await self.base_client.request(
                "PATCH", f"/deals/{deal_id}", json_payload=payload
            )
            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in update_deal: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in update_deal: {str(e)}")
            raise

    async def delete_deal(self, deal_id: int) -> Dict[str, Any]:
        """
        Delete a deal from Pipedrive

        Args:
            deal_id: ID of the deal to delete

        Returns:
            Deletion result data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"DealClient: Attempting to delete deal with ID {deal_id}")

        try:
            # Validate deal_id
            if deal_id <= 0:
                raise ValueError(f"Invalid deal ID: {deal_id}. Must be a positive integer.")

            response_data = await self.base_client.request("DELETE", f"/deals/{deal_id}")

            # Successful delete usually returns: {"success": true, "data": {"id": deal_id}}
            return (
                response_data.get("data", {})
                if response_data.get("success")
                else {"id": deal_id, "error_details": response_data}
            )

        except ValueError as e:
            logger.error(f"Validation error in delete_deal: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in delete_deal: {str(e)}")
            raise

    async def list_deals(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        filter_id: Optional[int] = None,
        owner_id: Optional[int] = None,
        person_id: Optional[int] = None,
        org_id: Optional[int] = None,
        pipeline_id: Optional[int] = None,
        stage_id: Optional[int] = None,
        status: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_direction: Optional[str] = None,
        include_fields: Optional[List[str]] = None,
        custom_fields_keys: Optional[List[str]] = None,
        updated_since: Optional[str] = None,  # RFC3339 format, e.g. 2025-01-01T10:20:00Z
        updated_until: Optional[str] = None,  # RFC3339 format
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        List deals from Pipedrive with pagination

        Args:
            limit: Maximum number of results to return
            cursor: Pagination cursor for retrieving the next page
            filter_id: ID of the filter to apply
            owner_id: Filter by owner user ID
            person_id: Filter by person ID
            org_id: Filter by organization ID
            pipeline_id: Filter by pipeline ID
            stage_id: Filter by stage ID
            status: Filter by status (open, won, lost)
            sort_by: Field to sort by (id, update_time, add_time)
            sort_direction: Sort direction (asc or desc)
            include_fields: Additional fields to include
            custom_fields_keys: Custom fields to include
            updated_since: Filter by update time (RFC3339 format)
            updated_until: Filter by update time (RFC3339 format)

        Returns:
            Tuple of (list of deals, next cursor)

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(
            f"DealClient: Attempting to list deals with limit {limit}, cursor '{cursor}'"
        )

        try:
            # Validate limit
            if limit < 1:
                raise ValueError(f"Invalid limit: {limit}. Must be a positive integer.")

            # Validate status if provided
            if status is not None and status not in ["open", "won", "lost"]:
                raise ValueError(f"Invalid status value: {status}. Must be one of: open, won, lost")

            # Validate sort_direction if provided
            if sort_direction is not None and sort_direction not in ["asc", "desc"]:
                raise ValueError(f"Invalid sort_direction: {sort_direction}. Must be 'asc' or 'desc'.")

            query_params: Dict[str, Any] = {
                "limit": limit,
                "cursor": cursor,
                "filter_id": filter_id,
                "owner_id": owner_id,
                "person_id": person_id,
                "org_id": org_id,
                "pipeline_id": pipeline_id,
                "stage_id": stage_id,
                "status": status,
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
                f"DealClient: list_deals query_params: {final_query_params}"
            )

            response_data = await self.base_client.request(
                "GET",
                "/deals",
                query_params=final_query_params if final_query_params else None,
            )

            deals_list = response_data.get("data", [])
            additional_data = response_data.get("additional_data", {})
            next_cursor = (
                additional_data.get("next_cursor")
                if isinstance(additional_data, dict)
                else None
            )
            logger.info(
                f"DealClient: Listed {len(deals_list)} deals. Next cursor: '{next_cursor}'"
            )
            return deals_list, next_cursor

        except ValueError as e:
            logger.error(f"Validation error in list_deals: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in list_deals: {str(e)}")
            raise

    async def search_deals(
        self,
        term: str,
        fields: Optional[List[str]] = None,
        exact_match: bool = False,
        person_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        status: Optional[str] = None,
        include_fields: Optional[List[str]] = None,
        limit: int = 100,
        cursor: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        Search for deals in Pipedrive

        Args:
            term: The search term to look for (min 2 chars, or 1 if exact_match=True)
            fields: Fields to search in (title, notes, custom_fields)
            exact_match: When True, only exact matches are returned
            person_id: Filter deals by person ID
            organization_id: Filter deals by organization ID
            status: Filter deals by status (open, won, lost)
            include_fields: Additional fields to include in the results
            limit: Maximum number of results to return (max 500)
            cursor: Pagination cursor

        Returns:
            Tuple of (list of deal results, next cursor)

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(
            f"DealClient: Searching for deals with term '{term}'"
        )

        try:
            # Validate required parameters
            if not term:
                raise ValueError("Search term cannot be empty")

            if not exact_match and len(term) < 2:
                raise ValueError("Search term must be at least 2 characters long when exact_match is False")

            if exact_match and len(term) < 1:
                raise ValueError("Search term must be at least 1 character long when exact_match is True")

            # Validate limit
            if limit < 1:
                raise ValueError(f"Invalid limit: {limit}. Must be a positive integer.")

            # Validate status if provided
            if status is not None and status not in ["open", "won", "lost"]:
                raise ValueError(f"Invalid status value: {status}. Must be one of: open, won, lost")

            # Build query parameters
            query_params: Dict[str, Any] = {
                "term": term,
                "exact_match": "true" if exact_match else "false",
                "limit": limit,
                "cursor": cursor,
                "person_id": person_id,
                "organization_id": organization_id,
                "status": status,
            }

            if fields:
                query_params["fields"] = ",".join(fields)

            if include_fields:
                query_params["include_fields"] = ",".join(include_fields)

            # Filter out None values
            final_query_params = {k: v for k, v in query_params.items() if v is not None}

            logger.debug(f"DealClient: search_deals query_params: {final_query_params}")

            response_data = await self.base_client.request(
                "GET",
                "/deals/search",
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
                f"DealClient: Found {len(items)} deals. Next cursor: '{next_cursor}'"
            )

            return items, next_cursor

        except ValueError as e:
            logger.error(f"Validation error in search_deals: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in search_deals: {str(e)}")
            raise

    async def add_product_to_deal(
        self,
        deal_id: int,
        product_id: int,
        item_price: float,
        quantity: int,
        tax: float = 0,
        comments: Optional[str] = None,
        discount: float = 0,
        discount_type: str = "percentage",
        tax_method: Optional[str] = None,
        product_variation_id: Optional[int] = None,
        billing_frequency: str = "one-time",
        billing_frequency_cycles: Optional[int] = None,
        billing_start_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add a product to a deal, creating a new item called a deal-product

        Args:
            deal_id: ID of the deal
            product_id: ID of the product to add
            item_price: Price value of the product
            quantity: Quantity of the product
            tax: Product tax
            comments: Comments about the product
            discount: Discount value
            discount_type: Discount type (percentage or amount)
            tax_method: Tax method (inclusive, exclusive, none)
            product_variation_id: ID of the product variation
            billing_frequency: Billing frequency (one-time, annually, etc.)
            billing_frequency_cycles: Number of billing cycles
            billing_start_date: Start date for billing (YYYY-MM-DD)

        Returns:
            Created deal-product data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(f"DealClient: Adding product {product_id} to deal {deal_id}")

        try:
            # Validate required parameters
            if deal_id <= 0:
                raise ValueError(f"Invalid deal ID: {deal_id}. Must be a positive integer.")

            if product_id <= 0:
                raise ValueError(f"Invalid product ID: {product_id}. Must be a positive integer.")

            if item_price < 0:
                raise ValueError(f"Invalid item price: {item_price}. Must be a non-negative number.")

            if quantity <= 0:
                raise ValueError(f"Invalid quantity: {quantity}. Must be a positive integer.")

            if tax < 0:
                raise ValueError(f"Invalid tax value: {tax}. Must be a non-negative number.")

            if discount < 0:
                raise ValueError(f"Invalid discount value: {discount}. Must be a non-negative number.")

            # Validate enum values
            valid_discount_types = ["percentage", "amount"]
            if discount_type not in valid_discount_types:
                raise ValueError(f"Invalid discount type: {discount_type}. Must be one of: {', '.join(valid_discount_types)}")

            if tax_method is not None:
                valid_tax_methods = ["inclusive", "exclusive", "none"]
                if tax_method not in valid_tax_methods:
                    raise ValueError(f"Invalid tax method: {tax_method}. Must be one of: {', '.join(valid_tax_methods)}")

            valid_billing_frequencies = ["one-time", "weekly", "monthly", "quarterly", "semi-annually", "annually"]
            if billing_frequency not in valid_billing_frequencies:
                raise ValueError(f"Invalid billing frequency: {billing_frequency}. Must be one of: {', '.join(valid_billing_frequencies)}")

            if billing_frequency_cycles is not None and (billing_frequency_cycles <= 0 or billing_frequency_cycles > 208):
                raise ValueError(f"Invalid billing frequency cycles: {billing_frequency_cycles}. Must be a positive integer less than or equal to 208.")

            payload: Dict[str, Any] = {
                "product_id": product_id,
                "item_price": item_price,
                "quantity": quantity,
            }

            if tax is not None:
                payload["tax"] = tax
            if comments:
                payload["comments"] = comments
            if discount is not None:
                payload["discount"] = discount
            if discount_type:
                payload["discount_type"] = discount_type
            if tax_method:
                payload["tax_method"] = tax_method
            if product_variation_id is not None:
                payload["product_variation_id"] = product_variation_id
            if billing_frequency:
                payload["billing_frequency"] = billing_frequency
            if billing_frequency_cycles is not None:
                payload["billing_frequency_cycles"] = billing_frequency_cycles
            if billing_start_date:
                payload["billing_start_date"] = billing_start_date

            # Log the payload without sensitive information
            safe_log_payload = payload.copy()
            if "item_price" in safe_log_payload:
                safe_log_payload["item_price"] = "[REDACTED]"

            logger.debug(
                f"DealClient: add_product_to_deal payload: {json.dumps(safe_log_payload, indent=2)}"
            )

            response_data = await self.base_client.request(
                "POST",
                f"/deals/{deal_id}/products",
                json_payload=payload
            )

            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in add_product_to_deal: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in add_product_to_deal: {str(e)}")
            raise

    async def update_product_in_deal(
        self,
        deal_id: int,
        product_attachment_id: int,
        item_price: Optional[float] = None,
        quantity: Optional[int] = None,
        tax: Optional[float] = None,
        comments: Optional[str] = None,
        discount: Optional[float] = None,
        discount_type: Optional[str] = None,
        tax_method: Optional[str] = None,
        is_enabled: Optional[bool] = None,
        product_variation_id: Optional[int] = None,
        billing_frequency: Optional[str] = None,
        billing_frequency_cycles: Optional[int] = None,
        billing_start_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a product attached to a deal

        Args:
            deal_id: ID of the deal
            product_attachment_id: ID of the product attachment (deal-product)
            item_price: Updated price value
            quantity: Updated quantity
            tax: Updated tax value
            comments: Updated comments
            discount: Updated discount value
            discount_type: Updated discount type
            tax_method: Updated tax method
            is_enabled: Whether the product is enabled
            product_variation_id: Updated product variation ID
            billing_frequency: Updated billing frequency
            billing_frequency_cycles: Updated billing cycles
            billing_start_date: Updated billing start date

        Returns:
            Updated deal-product data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails or no fields are provided to update
        """
        logger.info(f"DealClient: Updating product {product_attachment_id} in deal {deal_id}")

        try:
            # Validate IDs
            if deal_id <= 0:
                raise ValueError(f"Invalid deal ID: {deal_id}. Must be a positive integer.")

            if product_attachment_id <= 0:
                raise ValueError(f"Invalid product attachment ID: {product_attachment_id}. Must be a positive integer.")

            payload: Dict[str, Any] = {}

            if item_price is not None:
                if item_price < 0:
                    raise ValueError(f"Invalid item price: {item_price}. Must be a non-negative number.")
                payload["item_price"] = item_price

            if quantity is not None:
                if quantity <= 0:
                    raise ValueError(f"Invalid quantity: {quantity}. Must be a positive integer.")
                payload["quantity"] = quantity

            if tax is not None:
                if tax < 0:
                    raise ValueError(f"Invalid tax value: {tax}. Must be a non-negative number.")
                payload["tax"] = tax

            if comments is not None:
                payload["comments"] = comments

            if discount is not None:
                if discount < 0:
                    raise ValueError(f"Invalid discount value: {discount}. Must be a non-negative number.")
                payload["discount"] = discount

            if discount_type is not None:
                valid_discount_types = ["percentage", "amount"]
                if discount_type not in valid_discount_types:
                    raise ValueError(f"Invalid discount type: {discount_type}. Must be one of: {', '.join(valid_discount_types)}")
                payload["discount_type"] = discount_type

            if tax_method is not None:
                valid_tax_methods = ["inclusive", "exclusive", "none"]
                if tax_method not in valid_tax_methods:
                    raise ValueError(f"Invalid tax method: {tax_method}. Must be one of: {', '.join(valid_tax_methods)}")
                payload["tax_method"] = tax_method

            if is_enabled is not None:
                payload["is_enabled"] = is_enabled

            if product_variation_id is not None:
                if product_variation_id <= 0:
                    raise ValueError(f"Invalid product variation ID: {product_variation_id}. Must be a positive integer.")
                payload["product_variation_id"] = product_variation_id

            if billing_frequency is not None:
                valid_billing_frequencies = ["one-time", "weekly", "monthly", "quarterly", "semi-annually", "annually"]
                if billing_frequency not in valid_billing_frequencies:
                    raise ValueError(f"Invalid billing frequency: {billing_frequency}. Must be one of: {', '.join(valid_billing_frequencies)}")
                payload["billing_frequency"] = billing_frequency

            if billing_frequency_cycles is not None:
                if billing_frequency_cycles <= 0 or billing_frequency_cycles > 208:
                    raise ValueError(f"Invalid billing frequency cycles: {billing_frequency_cycles}. Must be a positive integer less than or equal to 208.")
                payload["billing_frequency_cycles"] = billing_frequency_cycles

            if billing_start_date is not None:
                # Could add date validation here in the future
                payload["billing_start_date"] = billing_start_date

            if not payload:
                logger.warning(
                    f"DealClient: update_product_in_deal called with no fields to update."
                )
                raise ValueError(
                    "At least one field must be provided for updating a product in a deal."
                )

            # Log the payload without sensitive information
            safe_log_payload = payload.copy()
            if "item_price" in safe_log_payload:
                safe_log_payload["item_price"] = "[REDACTED]"

            logger.debug(
                f"DealClient: update_product_in_deal payload: {json.dumps(safe_log_payload, indent=2)}"
            )

            response_data = await self.base_client.request(
                "PATCH",
                f"/deals/{deal_id}/products/{product_attachment_id}",
                json_payload=payload
            )

            return response_data.get("data", {})

        except ValueError as e:
            logger.error(f"Validation error in update_product_in_deal: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in update_product_in_deal: {str(e)}")
            raise

    async def delete_product_from_deal(
        self,
        deal_id: int,
        product_attachment_id: int
    ) -> Dict[str, Any]:
        """
        Delete a product attachment from a deal

        Args:
            deal_id: ID of the deal
            product_attachment_id: ID of the product attachment to delete

        Returns:
            Deletion result data

        Raises:
            PipedriveAPIError: If the API call fails
            ValueError: If input validation fails
        """
        logger.info(
            f"DealClient: Deleting product {product_attachment_id} from deal {deal_id}"
        )

        try:
            # Validate IDs
            if deal_id <= 0:
                raise ValueError(f"Invalid deal ID: {deal_id}. Must be a positive integer.")

            if product_attachment_id <= 0:
                raise ValueError(f"Invalid product attachment ID: {product_attachment_id}. Must be a positive integer.")

            response_data = await self.base_client.request(
                "DELETE",
                f"/deals/{deal_id}/products/{product_attachment_id}"
            )

            return (
                response_data.get("data", {})
                if response_data.get("success")
                else {"id": product_attachment_id, "error_details": response_data}
            )

        except ValueError as e:
            logger.error(f"Validation error in delete_product_from_deal: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in delete_product_from_deal: {str(e)}")
            raise