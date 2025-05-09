import json
from typing import Any, Dict, Optional

import httpx

from log_config import logger
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class BaseClient:
    """Base client for Pipedrive API interactions"""
    
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
        logger.debug("BaseClient initialized.")

    async def request(
        self,
        method: str,
        endpoint: str,
        query_params: Optional[Dict[str, Any]] = None,
        json_payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the Pipedrive API
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (e.g., /persons)
            query_params: URL query parameters
            json_payload: JSON request body
            
        Returns:
            API response data
            
        Raises:
            PipedriveAPIError: If the API request fails
        """
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

        logger.debug(f"BaseClient Request: {method} {url}")
        if params_to_send:
            logger.debug(f"URL Params: {params_to_send}")
        if json_payload:
            logger.debug(
                f"JSON Payload: {json.dumps(json_payload, indent=2)}"
            )

        try:
            response = await self.http_client.request(
                method, url, params=params_to_send, json=json_payload, headers=headers
            )
            logger.debug(f"Pipedrive API Response Status: {response.status_code}")

            try:
                # Attempt to log raw response for better debugging
                raw_response_text = response.text
                logger.debug(
                    f"Pipedrive API Raw Response Text: {raw_response_text[:1000]}..."
                )
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
            logger.exception(f"Unexpected error in BaseClient.request: {str(e)}")
            raise PipedriveAPIError(
                message=f"An unexpected error occurred in request: {str(e)}"
            )