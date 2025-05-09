import json
import logging
from typing import Any, Dict, List, Optional, Tuple

import httpx

logger = logging.getLogger(__name__)


# Custom Exception for Pipedrive API errors
class PipedriveAPIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_info: Optional[str] = None,
        response_data: Optional[
            Dict[str, Any]
        ] = None,  # Changed from Dict to Dict[str, Any]
    ):
        super().__init__(message)
        self.status_code = status_code
        self.error_info = error_info
        self.response_data = response_data

    def __str__(self):
        base_message = super().__str__()
        details = []
        if self.status_code is not None:
            details.append(f"Status: {self.status_code}")
        if self.error_info:
            details.append(f"Info: {self.error_info}")
        if self.response_data:
            details.append(
                f"Response Data Keys: {list(self.response_data.keys()) if isinstance(self.response_data, dict) else 'Present'}"
            )
        return f"PipedriveAPIError: {base_message} ({', '.join(details)})"


class PipedriveClient:
    def __init__(
        self, api_token: str, company_domain: str, http_client: httpx.AsyncClient
    ):
        if not api_token:
            raise ValueError("Pipedrive API token is required.")
        if not company_domain:
            raise ValueError("Pipedrive company domain is required.")
        if not http_client:
            raise ValueError("httpx.AsyncClient is required.")

        self.api_token = api_token
        self.base_url = f"https://{company_domain}.pipedrive.com/api/v2"
        self.http_client = http_client
        logger.debug("PipedriveClient initialized.")

    async def _request(
        self,
        method: str,
        endpoint: str,
        query_params: Optional[Dict[str, Any]] = None,
        json_payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"

        params_to_send = {"api_token": self.api_token}
        if query_params:
            filtered_query_params = {
                k: v for k, v in query_params.items() if v is not None
            }
            params_to_send.update(filtered_query_params)

        headers = {}
        if json_payload:
            headers["Content-Type"] = "application/json"

        logger.debug(f"PipedriveClient Request: {method} {url}")
        if params_to_send:
            logger.debug(f"PipedriveClient URL Params: {params_to_send}")
        if json_payload:
            logger.debug(
                f"PipedriveClient JSON Payload: {json.dumps(json_payload, indent=2)}"
            )

        try:
            response = await self.http_client.request(
                method, url, params=params_to_send, json=json_payload, headers=headers
            )
            logger.debug(f"Pipedrive API Response Status: {response.status_code}")

            try:
                # Attempt to log raw response for better debugging, especially errors
                raw_response_text = (
                    response.text
                )  # Use .text for already decoded string
                logger.debug(
                    f"Pipedrive API Raw Response Text: {raw_response_text[:1000]}..."
                )  # Log snippet
            except Exception as read_err:
                logger.warning(f"Could not log raw response text: {read_err}")

            response.raise_for_status()  # Check for HTTP errors

            response_data = response.json()  # Parse JSON
            logger.debug(
                f"Pipedrive API Parsed JSON Response: {json.dumps(response_data, indent=2)}"
            )

            if not response_data.get("success"):
                error_message = response_data.get(
                    "error", "Unknown Pipedrive API error"
                )
                error_info = response_data.get("error_info", "")
                logger.warning(
                    f"Pipedrive API call not successful: {error_message}, Info: {error_info}"
                )
                raise PipedriveAPIError(
                    message=error_message,
                    status_code=response.status_code,
                    error_info=error_info,
                    response_data=response_data,
                )

            logger.debug("Pipedrive API call successful, success flag was true.")
            return response_data

        except httpx.HTTPStatusError as e:
            error_body_text = e.response.text  # Default to text
            error_details_from_response = None
            try:
                error_details_from_response = (
                    e.response.json()
                )  # Attempt to parse as JSON
                error_message = error_details_from_response.get("error", str(e))
                error_info = error_details_from_response.get("error_info", "")
            except json.JSONDecodeError:
                # If not JSON, error_body_text is already set to e.response.text
                error_message = str(e)  # Use the general HTTP error message
                error_info = "Response body was not valid JSON."

            logger.error(
                f"HTTPStatusError from Pipedrive: {e.response.status_code} - {error_message}. Raw Body: {error_body_text[:500]}..."
            )
            raise PipedriveAPIError(
                message=f"HTTP error {e.response.status_code}: {error_message}",
                status_code=e.response.status_code,
                error_info=error_info,
                response_data=error_details_from_response
                or {"raw_error": error_body_text},
            ) from e
        except httpx.RequestError as e:  # Network errors, timeouts
            logger.error(f"RequestError during Pipedrive call: {str(e)}")
            raise PipedriveAPIError(message=f"Request failed: {str(e)}") from e
        except Exception as e:  # Catch-all for other unexpected errors
            logger.exception(f"Unexpected error in PipedriveClient._request: {str(e)}")
            raise PipedriveAPIError(
                message=f"An unexpected error occurred in _request: {str(e)}"
            )

    # --- Person Methods ---
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
        logger.info(f"PipedriveClient: Attempting to create person '{name}'")
        payload: Dict[str, Any] = {"name": name}  # Ensure payload is typed for clarity
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
            f"PipedriveClient: create_person payload: {json.dumps(payload, indent=2)}"
        )
        response_data = await self._request("POST", "/persons", json_payload=payload)
        return response_data.get("data", {})  # Return the 'data' part of the response

    async def get_person(
        self,
        person_id: int,
        include_fields: Optional[List[str]] = None,
        custom_fields_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        logger.info(f"PipedriveClient: Attempting to get person with ID {person_id}")
        query_params: Dict[str, Any] = {}
        if include_fields:
            query_params["include_fields"] = ",".join(include_fields)
        if custom_fields_keys:
            query_params["custom_fields"] = ",".join(custom_fields_keys)

        response_data = await self._request(
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
        logger.info(f"PipedriveClient: Attempting to update person with ID {person_id}")
        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if owner_id is not None:
            payload["owner_id"] = owner_id
        if org_id is not None:
            payload["org_id"] = org_id
        if (
            emails is not None
        ):  # If None, Pipedrive won't update emails. To clear, send empty list [].
            payload["emails"] = emails
        if (
            phones is not None
        ):  # If None, Pipedrive won't update phones. To clear, send empty list [].
            payload["phones"] = phones
        if visible_to is not None:
            payload["visible_to"] = visible_to

        if custom_fields:
            payload.update(custom_fields)

        if not payload:
            logger.warning(
                "PipedriveClient: update_person called with no fields to update for ID {person_id}."
            )
            # Depending on API, an empty patch might be an error or a no-op.
            # For safety, let's assume it's not intended if no fields are provided.
            raise ValueError(
                "At least one field must be provided for updating a person."
            )

        logger.debug(
            f"PipedriveClient: update_person payload for ID {person_id}: {json.dumps(payload, indent=2)}"
        )
        response_data = await self._request(
            "PATCH", f"/persons/{person_id}", json_payload=payload
        )
        return response_data.get("data", {})

    async def delete_person(self, person_id: int) -> Dict[str, Any]:
        logger.info(f"PipedriveClient: Attempting to delete person with ID {person_id}")
        response_data = await self._request("DELETE", f"/persons/{person_id}")
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
        updated_since: Optional[
            str
        ] = None,  # RFC3339 format, e.g. 2025-01-01T10:20:00Z
        updated_until: Optional[str] = None,  # RFC3339 format
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        logger.info(
            f"PipedriveClient: Attempting to list persons with limit {limit}, cursor '{cursor}'"
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
            f"PipedriveClient: list_persons query_params: {final_query_params}"
        )

        response_data = await self._request(
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
            f"PipedriveClient: Listed {len(persons_list)} persons. Next cursor: '{next_cursor}'"
        )
        return persons_list, next_cursor
