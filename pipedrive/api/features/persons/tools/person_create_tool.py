from typing import Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.persons.models.contact_info import Email, Phone
from pipedrive.api.features.persons.models.person import Person
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("persons")
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
        f"Tool 'create_person_in_pipedrive' ENTERED with raw args: "
        f"name='{name}', owner_id_str={owner_id_str}, org_id_str={org_id_str}, "
        f"email_address={email_address}, email_label={email_label}, "
        f"phone_number={phone_number}, phone_label={phone_label}, "
        f"visible_to_str={visible_to_str}"
    )

    # Sanitize empty strings to None
    owner_id_str = None if owner_id_str == "" else owner_id_str
    org_id_str = None if org_id_str == "" else org_id_str
    email_address = None if email_address == "" else email_address
    phone_number = None if phone_number == "" else phone_number
    visible_to_str = None if visible_to_str == "" else visible_to_str

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string IDs to integers using our utility function
    owner_id, owner_error = convert_id_string(owner_id_str, "owner_id")
    if owner_error:
        logger.error(owner_error)
        return format_tool_response(False, error_message=owner_error)

    org_id, org_error = convert_id_string(org_id_str, "org_id")
    if org_error:
        logger.error(org_error)
        return format_tool_response(False, error_message=org_error)

    visible_to, visible_error = convert_id_string(visible_to_str, "visible_to")
    if visible_error:
        logger.error(visible_error)
        return format_tool_response(False, error_message=visible_error)

    try:
        # Create Person model instance with validation
        person = Person(
            name=name, owner_id=owner_id, org_id=org_id, visible_to=visible_to
        )

        # Add email if provided
        if email_address and email_address.strip():
            person.emails.append(Email(value=email_address, label=email_label))

        # Add phone if provided
        if phone_number and phone_number.strip():
            person.phones.append(Phone(value=phone_number, label=phone_label))

        # Convert model to API-compatible dict
        payload = person.to_api_dict()

        logger.debug(f"Prepared payload for person creation: {payload}")

        # Call the Pipedrive API using the persons client
        created_person = await pd_mcp_ctx.pipedrive_client.persons.create_person(
            **payload
        )

        logger.info(
            f"Successfully created person '{name}' with ID: {created_person.get('id')}"
        )

        # Return the API response
        return format_tool_response(True, data=created_person)

    except ValidationError as e:
        logger.error(f"Validation error creating person '{name}': {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
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