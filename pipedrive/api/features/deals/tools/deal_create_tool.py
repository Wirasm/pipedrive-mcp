from typing import Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.deals.models.deal import Deal, VISIBILITY_PRIVATE, VISIBILITY_SHARED, VISIBILITY_TEAM, VISIBILITY_ENTIRE_COMPANY
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string, validate_date_string
from pipedrive.api.features.shared.utils import format_tool_response, format_validation_error
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
    owner_id_str: Optional[str] = None,
    stage_id_str: Optional[str] = None,
    pipeline_id_str: Optional[str] = None,
    expected_close_date: Optional[str] = None,
    visible_to_str: Optional[str] = None,
    probability: Optional[str] = None,
    lost_reason: Optional[str] = None
):
    """Creates a new deal in Pipedrive CRM.

    This tool creates a new deal with the specified attributes. A deal represents a sales
    opportunity in Pipedrive CRM and can be linked to persons, organizations, and products.
    
    Format requirements:
    - title: Required name for the deal
    - value: Numeric value (e.g. "1000" or "1500.50")
    - currency: 3-letter ISO currency code (e.g. "USD", "EUR")
    - *_id_str: Numeric ID strings (e.g. "123")
    - expected_close_date: ISO date format YYYY-MM-DD (e.g. "2025-12-31")
    - visible_to_str: Visibility level ID ("0"=private, "1"=shared, "3"=team, "7"=company)
    
    Stage and Pipeline Relationships:
    - If stage_id_str is provided, the deal will be placed in that stage
    - If pipeline_id_str is provided, the deal will be placed in that pipeline's first stage
    - If both are provided, the stage must belong to the specified pipeline
    
    Example usage:
    ```
    create_deal_in_pipedrive(
        title="New software license",
        value="5000",
        currency="USD",
        person_id_str="123",
        org_id_str="456",
        stage_id_str="7",
        expected_close_date="2025-06-30"
    )
    ```

    args:
    ctx: Context
    title: str - The title of the deal (required)
    value: Optional[str] = None - The monetary value of the deal (numeric string)
    currency: str = "USD" - The currency of the deal (3-letter ISO code)
    person_id_str: Optional[str] = None - The ID of the person associated with the deal
    org_id_str: Optional[str] = None - The ID of the organization associated with the deal
    status: str = "open" - The status of the deal (open, won, lost)
    owner_id_str: Optional[str] = None - The ID of the user who owns the deal
    stage_id_str: Optional[str] = None - The ID of the stage this deal belongs to
    pipeline_id_str: Optional[str] = None - The ID of the pipeline this deal belongs to
    expected_close_date: Optional[str] = None - The expected close date (YYYY-MM-DD)
    visible_to_str: Optional[str] = None - Visibility setting (0=private, 1=shared, 3=team, 7=company)
    probability: Optional[str] = None - Deal success probability percentage (0-100)
    lost_reason: Optional[str] = None - Reason for losing the deal (only if status is 'lost')
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
    owner_id_str = None if owner_id_str == "" else owner_id_str
    stage_id_str = None if stage_id_str == "" else stage_id_str
    pipeline_id_str = None if pipeline_id_str == "" else pipeline_id_str
    expected_close_date = None if expected_close_date == "" else expected_close_date
    visible_to_str = None if visible_to_str == "" else visible_to_str
    probability = None if probability == "" else probability
    lost_reason = None if lost_reason == "" else lost_reason
    
    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Validate date format
    if expected_close_date:
        date_value, date_error = validate_date_string(expected_close_date, "expected_close_date")
        if date_error:
            logger.error(date_error)
            return format_tool_response(False, error_message=date_error)
        expected_close_date = date_value

    # Safely convert value string to float with proper error handling
    value_float = None
    if value:
        try:
            value_float = float(value)
            if value_float < 0:
                error_message = format_validation_error(
                    "deal value", value, "Must be a non-negative number.", "1000"
                )
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
        except ValueError:
            error_message = format_validation_error(
                "deal value", value, "Must be a valid number.", "1000"
            )
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
    
    # Convert probability string to integer if provided
    probability_int = None
    if probability:
        try:
            probability_int = int(probability)
            if probability_int < 0 or probability_int > 100:
                error_message = format_validation_error(
                    "probability", probability, "Must be an integer between 0 and 100.", "75"
                )
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
        except ValueError:
            error_message = format_validation_error(
                "probability", probability, "Must be a valid integer.", "75"
            )
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
            
    # Validate status value is one of the allowed values
    valid_statuses = {"open", "won", "lost"}
    if status not in valid_statuses:
        error_message = format_validation_error(
            "status", status, f"Must be one of: {', '.join(valid_statuses)}.", "open"
        )
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)
        
    # Validate lost_reason is only provided when status is 'lost'
    if lost_reason and status != "lost":
        error_message = "Lost reason can only be provided when status is 'lost'"
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
        
    # Convert additional ID strings to integers
    owner_id, owner_error = convert_id_string(owner_id_str, "owner_id")
    if owner_error:
        logger.error(owner_error)
        return format_tool_response(False, error_message=owner_error)
        
    stage_id, stage_error = convert_id_string(stage_id_str, "stage_id")
    if stage_error:
        logger.error(stage_error)
        return format_tool_response(False, error_message=stage_error)
        
    pipeline_id, pipeline_error = convert_id_string(pipeline_id_str, "pipeline_id")
    if pipeline_error:
        logger.error(pipeline_error)
        return format_tool_response(False, error_message=pipeline_error)
        
    # Validate visible_to value if provided
    visible_to = None
    if visible_to_str:
        try:
            visible_to = int(visible_to_str)
            valid_visibility_values = {VISIBILITY_PRIVATE, VISIBILITY_SHARED, VISIBILITY_TEAM, VISIBILITY_ENTIRE_COMPANY}
            if visible_to not in valid_visibility_values:
                error_message = format_validation_error(
                    "visible_to", visible_to_str, 
                    f"Must be one of: {', '.join(map(str, valid_visibility_values))} (0=private, 1=shared, 3=team, 7=company).",
                    "3"
                )
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
        except ValueError:
            error_message = format_validation_error(
                "visible_to", visible_to_str, "Must be a valid integer.", "3"
            )
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)

    try:
        # Validate inputs with Pydantic model
        deal = Deal(
            title=title,
            value=value_float,
            currency=currency,
            person_id=person_id,
            org_id=org_id,
            status=status,
            owner_id=owner_id,
            stage_id=stage_id,
            pipeline_id=pipeline_id,
            expected_close_date=expected_close_date,
            visible_to=visible_to,
            probability=probability_int,
            lost_reason=lost_reason
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