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


@mcp.tool()
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

    This tool requires the deal's ID and at least one field to update.
    It can update basic information like title, value, currency,
    as well as linked entities like person, organization, and owner.

    args:
    ctx: Context
    id_str: str - The ID of the deal to update
    title: Optional[str] = None - The updated title of the deal
    value: Optional[str] = None - The updated value of the deal
    currency: Optional[str] = None - The updated currency of the deal
    person_id_str: Optional[str] = None - The ID of the person to link to the deal
    org_id_str: Optional[str] = None - The ID of the organization to link to the deal
    status: Optional[str] = None - The updated status of the deal (open, won, lost)
    owner_id_str: Optional[str] = None - The ID of the user who owns the deal
    stage_id_str: Optional[str] = None - The ID of the deal stage
    pipeline_id_str: Optional[str] = None - The ID of the pipeline
    expected_close_date: Optional[str] = None - The expected close date (YYYY-MM-DD)
    visible_to_str: Optional[str] = None - Visibility setting of the deal
    probability: Optional[str] = None - Success probability percentage (0-100)
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

    visible_to, visible_to_error = convert_id_string(visible_to_str, "visible_to")
    if visible_to_error:
        logger.error(visible_to_error)
        return format_tool_response(False, error_message=visible_to_error)

    # Convert value string to float
    value_float = None
    if value is not None:
        try:
            value_float = float(value)
        except ValueError:
            error_message = f"Invalid deal value format: '{value}'. Must be a valid number."
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)

    # Convert probability string to integer
    probability_int = None
    if probability is not None:
        try:
            probability_int = int(probability)
            if probability_int < 0 or probability_int > 100:
                error_message = f"Invalid probability value: {probability_int}. Must be between 0 and 100."
                logger.error(error_message)
                return format_tool_response(False, error_message=error_message)
        except ValueError:
            error_message = f"Invalid probability format: '{probability}'. Must be an integer."
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
        # Validate status and lost_reason if provided
        if status is not None and status not in ["open", "won", "lost"]:
            error_message = f"Invalid status: '{status}'. Must be one of: open, won, lost"
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)
        
        if lost_reason is not None and (status is None or status != "lost"):
            error_message = "Lost reason can only be provided when status is 'lost'"
            logger.error(error_message)
            return format_tool_response(False, error_message=error_message)

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