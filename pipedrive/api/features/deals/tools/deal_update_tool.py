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


@mcp.tool("update_deal_in_pipedrive")
async def update_deal_in_pipedrive(
    ctx: Context,
    id_str: str,
    title: Optional[str] = None,
    value: Optional[str] = None,
    currency: Optional[str] = None,
    person_id_str: Optional[str] = None,
    org_id_str: Optional[str] = None,
    status: Optional[str] = None,
    owner_id_str: Optional[str] = None,
    stage_id_str: Optional[str] = None,
    pipeline_id_str: Optional[str] = None,
    expected_close_date: Optional[str] = None,
    visible_to_str: Optional[str] = None,
    probability: Optional[str] = None,
    lost_reason: Optional[str] = None,
) -> str:
    """Updates an existing deal in the Pipedrive CRM.

    This tool updates a deal identified by its ID. You must provide at least one field to update.
    It can modify basic information like title and value, as well as the deal's relationships,
    stage, status, and other attributes.
    
    Format requirements:
    - id_str: Required numeric ID of the deal to update (e.g. "123")
    - value: Numeric value (e.g. "1000" or "1500.50")
    - currency: 3-letter ISO currency code (e.g. "USD", "EUR")
    - *_id_str: Numeric ID strings (e.g. "123")
    - expected_close_date: ISO date format YYYY-MM-DD (e.g. "2025-12-31")
    - visible_to_str: Visibility level ID ("0"=private, "1"=shared, "3"=team, "7"=company)
    - probability: Integer between 0-100 (e.g. "75")
    
    Stage and Pipeline Relationships:
    - When updating stage_id_str and/or pipeline_id_str, ensure the stage belongs to the pipeline
    - Changing just the pipeline_id will place the deal in the first stage of that pipeline
    - Changing just the stage_id will update the pipeline_id automatically to match the stage's pipeline
    
    Status and Lost Reason:
    - status can be "open", "won", or "lost"
    - lost_reason can only be provided when status is "lost"
    
    Example usage:
    ```
    update_deal_in_pipedrive(
        id_str="42",
        title="Updated software license deal",
        value="7500",
        status="won",
        stage_id_str="3"
    )
    ```

    args:
    ctx: Context
    id_str: str - The ID of the deal to update (required)
    title: Optional[str] = None - The updated title of the deal
    value: Optional[str] = None - The updated monetary value of the deal (numeric string)
    currency: Optional[str] = None - The updated currency of the deal (3-letter ISO code)
    person_id_str: Optional[str] = None - The ID of the person to link to the deal
    org_id_str: Optional[str] = None - The ID of the organization to link to the deal
    status: Optional[str] = None - The updated status of the deal (open, won, lost)
    owner_id_str: Optional[str] = None - The ID of the user who owns the deal
    stage_id_str: Optional[str] = None - The ID of the stage this deal belongs to
    pipeline_id_str: Optional[str] = None - The ID of the pipeline this deal belongs to
    expected_close_date: Optional[str] = None - The expected close date (YYYY-MM-DD)
    visible_to_str: Optional[str] = None - Visibility setting (0=private, 1=shared, 3=team, 7=company)
    probability: Optional[str] = None - Deal success probability percentage (0-100)
    lost_reason: Optional[str] = None - Reason for losing the deal (only if status is 'lost')
    """
    logger.debug(
        f"Tool 'update_deal_in_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', title='{title}', "
        f"status='{status}', expected_close_date='{expected_close_date}'"
    )

    # Sanitize empty strings to None
    title = None if title == "" else title
    value = None if value == "" else value
    currency = None if currency == "" else currency
    person_id_str = None if person_id_str == "" else person_id_str
    org_id_str = None if org_id_str == "" else org_id_str
    status = None if status == "" else status
    owner_id_str = None if owner_id_str == "" else owner_id_str
    stage_id_str = None if stage_id_str == "" else stage_id_str
    pipeline_id_str = None if pipeline_id_str == "" else pipeline_id_str
    expected_close_date = None if expected_close_date == "" else expected_close_date
    visible_to_str = None if visible_to_str == "" else visible_to_str
    probability = None if probability == "" else probability
    lost_reason = None if lost_reason == "" else lost_reason

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string IDs to integers
    deal_id, id_error = convert_id_string(id_str, "deal_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)

    person_id, person_id_error = convert_id_string(person_id_str, "person_id")
    if person_id_error:
        logger.error(person_id_error)
        return format_tool_response(False, error_message=person_id_error)

    org_id, org_id_error = convert_id_string(org_id_str, "org_id")
    if org_id_error:
        logger.error(org_id_error)
        return format_tool_response(False, error_message=org_id_error)

    owner_id, owner_id_error = convert_id_string(owner_id_str, "owner_id")
    if owner_id_error:
        logger.error(owner_id_error)
        return format_tool_response(False, error_message=owner_id_error)

    stage_id, stage_id_error = convert_id_string(stage_id_str, "stage_id")
    if stage_id_error:
        logger.error(stage_id_error)
        return format_tool_response(False, error_message=stage_id_error)

    pipeline_id, pipeline_id_error = convert_id_string(pipeline_id_str, "pipeline_id")
    if pipeline_id_error:
        logger.error(pipeline_id_error)
        return format_tool_response(False, error_message=pipeline_id_error)

    # Validate visible_to value if provided
    visible_to = None
    if visible_to_str is not None:
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

    # Validate date format
    if expected_close_date is not None:
        date_value, date_error = validate_date_string(expected_close_date, "expected_close_date")
        if date_error:
            logger.error(date_error)
            return format_tool_response(False, error_message=date_error)
        expected_close_date = date_value
            
    # Convert value string to float with improved error handling
    value_float = None
    if value is not None:
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

    # Convert probability string to integer with improved error handling
    probability_int = None
    if probability is not None:
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

    # Check if at least one field is being updated
    if all(param is None for param in [
        title, value_float, currency, person_id, org_id, status,
        owner_id, stage_id, pipeline_id, expected_close_date,
        visible_to, probability_int, lost_reason
    ]):
        error_message = "At least one field must be provided for updating a deal"
        logger.error(error_message)
        return format_tool_response(False, error_message=error_message)

    try:
        # Validate status and lost_reason if provided with improved error messaging
        if status is not None:
            valid_statuses = {"open", "won", "lost"}
            if status not in valid_statuses:
                error_message = format_validation_error(
                    "status", status, f"Must be one of: {', '.join(valid_statuses)}.", "open"
                )
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
        
            # Validate stage/pipeline consistency based on status
            if status == "won" and stage_id_str is not None:
                logger.debug("Deal status is 'won' - stage will be set to the final win stage of the deal's pipeline")
            elif status == "lost" and stage_id_str is not None:
                logger.debug("Deal status is 'lost' - stage will be set to the final lost stage of the deal's pipeline")
        
        # Validate lost_reason is only provided when status is 'lost'
        if lost_reason is not None and (status is None or status != "lost"):
            error_message = "Lost reason can only be provided when status is 'lost'"
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
            
        # Validate stage and pipeline compatibility if both are provided
        if stage_id is not None and pipeline_id is not None:
            logger.debug(f"Both stage_id ({stage_id}) and pipeline_id ({pipeline_id}) provided - API will validate compatibility")
            # Note: actual validation happens server-side since we don't have stage/pipeline mapping locally

        # Call the Pipedrive API
        updated_deal = await pd_mcp_ctx.pipedrive_client.deals.update_deal(
            deal_id=deal_id,
            title=title,
            value=value_float,
            currency=currency,
            person_id=person_id,
            org_id=org_id,
            status=status,
            expected_close_date=expected_close_date,
            owner_id=owner_id,
            stage_id=stage_id,
            pipeline_id=pipeline_id,
            visible_to=visible_to,
            probability=probability_int,
            lost_reason=lost_reason
        )

        logger.info(f"Successfully updated deal with ID: {deal_id}")

        # Return the API response
        return format_tool_response(True, data=updated_deal)

    except ValidationError as e:
        logger.error(f"Validation error updating deal with ID '{id_str}': {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'update_deal_in_pipedrive' for ID '{id_str}': {str(e)}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'update_deal_in_pipedrive' for ID '{id_str}': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )