from typing import Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.deals.models.deal import Deal
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool("create_deal_in_pipedrive")
async def create_deal_in_pipedrive(
    ctx: Context,
    title: str,
    value: Optional[str] = None,
    currency: str = "USD",
    person_id_str: Optional[str] = None,
    org_id_str: Optional[str] = None,
    status: str = "open",
    expected_close_date: Optional[str] = None
):
    """Creates a new deal in Pipedrive CRM.

    This tool creates a new deal with the specified attributes.

    args:
    ctx: Context
    title: str - The title of the deal
    value: Optional[str] = None - The value of the deal
    currency: str = "USD" - The currency of the deal
    person_id_str: Optional[str] = None - The ID of the person associated with the deal
    org_id_str: Optional[str] = None - The ID of the organization associated with the deal
    status: str = "open" - The status of the deal
    expected_close_date: Optional[str] = None - The expected close date in ISO format (YYYY-MM-DD)
    """
    # Log inputs with appropriate redaction of sensitive data
    logger.debug(
        f"Tool 'create_deal_in_pipedrive' ENTERED with raw args: "
        f"title='{title}', currency='{currency}', "
        f"status='{status}', expected_close_date='{expected_close_date}'"
    )

    # Sanitize empty strings to None
    title = title.strip() if title else title
    value = None if value == "" else value
    currency = currency.upper() if currency else "USD"
    person_id_str = None if person_id_str == "" else person_id_str
    org_id_str = None if org_id_str == "" else org_id_str
    status = status.lower() if status else "open"
    expected_close_date = None if expected_close_date == "" else expected_close_date
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Safely convert value string to float with proper error handling
    value_float = None
    if value:
        try:
            value_float = float(value)
        except ValueError:
            error_message = f"Invalid deal value format: '{value}'. Must be a valid number."
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
    
    # Convert string IDs to integers with proper error handling
    person_id, person_error = convert_id_string(person_id_str, "person_id")
    if person_error:
        logger.error(person_error)
        return format_tool_response(False, error_message=person_error)
    
    org_id, org_error = convert_id_string(org_id_str, "org_id")
    if org_error:
        logger.error(org_error)
        return format_tool_response(False, error_message=org_error)

    try:
        # Validate inputs with Pydantic model
        deal = Deal(
            title=title,
            value=value_float,
            currency=currency,
            person_id=person_id,
            org_id=org_id,
            status=status,
            expected_close_date=expected_close_date
        )
        
        # Convert model to API-compatible dict
        payload = deal.to_api_dict()
        
        # Log the payload with sensitive information redacted
        safe_log_payload = payload.copy()
        if "value" in safe_log_payload:
            safe_log_payload["value"] = "[REDACTED]"
            
        logger.debug(f"Prepared payload for deal creation: {safe_log_payload}")
        
        # Call the Pipedrive API using the deals client
        created_deal = await pd_mcp_ctx.pipedrive_client.deals.create_deal(**payload)
        
        logger.info(
            f"Successfully created deal '{title}' with ID: {created_deal.get('id')}"
        )
        
        # Return the API response with sensitive information redacted in logs
        return format_tool_response(True, data=created_deal)
        
    except ValidationError as e:
        logger.error(f"Validation error creating deal '{title}': {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(f"Pipedrive API error creating deal '{title}': {str(e)}")
        return format_tool_response(
            False, error_message=f"Pipedrive API error: {str(e)}"
        )
    except Exception as e:
        logger.error(
            f"Unexpected error creating deal '{title}': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )