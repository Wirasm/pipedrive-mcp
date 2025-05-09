from typing import Optional

from mcp.server.fastmcp import Context

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def create_person_in_pipedrive(
    ctx: Context,
    name: str,
    owner_id_str: Optional[str] = None,
    org_id_str: Optional[str] = None,
    email_address: Optional[str] = None,
    email_label: str = "work",
    phone_number: Optional[str] = None,
    phone_label: str = "work",
    visible_to_str: Optional[str] = None,
) -> str:
    """Creates a new person entity within the Pipedrive CRM.

    This tool requires the person's name and can optionally take details
    like owner ID, organization ID, email, phone, and visibility settings.
    It returns the details of the created person upon success.

    args:
    ctx: Context
    name: str
    owner_id_str: Optional[str] = None
    org_id_str: Optional[str] = None
    email_address: Optional[str] = None
    email_label: str = "work"
    phone_number: Optional[str] = None
    phone_label: str = "work"
    visible_to_str: Optional[str] = None
    """
    logger.debug(
        f"Tool 'create_person_in_pipedrive' ENTERED with raw args: name='{name}' (type: {type(name)}), "
        f"owner_id_str='{owner_id_str}' (type: {type(owner_id_str)}), "
        f"org_id_str='{org_id_str}' (type: {type(org_id_str)}), "
        f"email_address='{email_address}' (type: {type(email_address)}), "
        f"email_label='{email_label}' (type: {type(email_label)}), "
        f"phone_number='{phone_number}' (type: {type(phone_number)}), "
        f"phone_label='{phone_label}' (type: {type(phone_label)}), "
        f"visible_to_str='{visible_to_str}' (type: {type(visible_to_str)})"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # --- Manual Type Conversion and Validation ---
    owner_id: Optional[int] = None
    if (
        owner_id_str is not None and owner_id_str.strip()
    ):  # Check if not None and not empty/whitespace
        try:
            owner_id = int(owner_id_str)
        except ValueError:
            err_msg = (
                f"Invalid owner_id format: '{owner_id_str}'. Must be an integer string."
            )
            logger.error(err_msg)
            return format_tool_response(False, error_message=err_msg)

    org_id: Optional[int] = None
    if org_id_str is not None and org_id_str.strip():
        try:
            org_id = int(org_id_str)
        except ValueError:
            err_msg = (
                f"Invalid org_id format: '{org_id_str}'. Must be an integer string."
            )
            logger.error(err_msg)
            return format_tool_response(False, error_message=err_msg)

    visible_to: Optional[int] = None
    if visible_to_str is not None and visible_to_str.strip():
        try:
            visible_to = int(visible_to_str)
        except ValueError:
            err_msg = f"Invalid visible_to format: '{visible_to_str}'. Must be an integer string."
            logger.error(err_msg)
            return format_tool_response(False, error_message=err_msg)

    logger.debug(
        f"Converted args: owner_id={owner_id}, org_id={org_id}, visible_to={visible_to}"
    )

    emails_payload = None
    if email_address is not None and email_address.strip():
        emails_payload = [
            {"value": email_address, "label": email_label, "primary": True}
        ]
    elif email_address == "":  # Explicitly empty string might mean "no email"
        logger.debug(
            "email_address is an empty string, treating as no email for payload."
        )

    phones_payload = None
    if phone_number is not None and phone_number.strip():
        phones_payload = [
            {"value": phone_number, "label": phone_label, "primary": True}
        ]
    elif phone_number == "":
        logger.debug(
            "phone_number is an empty string, treating as no phone for payload."
        )

    logger.debug(f"Constructed emails_payload: {emails_payload}")
    logger.debug(f"Constructed phones_payload: {phones_payload}")

    try:
        created_person = await pd_mcp_ctx.pipedrive_client.create_person(
            name=name,
            owner_id=owner_id,
            org_id=org_id,
            emails=emails_payload,
            phones=phones_payload,
            visible_to=visible_to,
        )
        logger.info(
            f"Successfully created person '{name}' with ID: {created_person.get('id')}"
        )
        return format_tool_response(True, data=created_person)
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'create_person_in_pipedrive' for '{name}': {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'create_person_in_pipedrive' for '{name}': {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )
