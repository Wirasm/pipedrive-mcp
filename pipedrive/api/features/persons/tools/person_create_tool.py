from typing import Optional, Dict, Any, List

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
    custom_fields_str: Optional[str] = None,
) -> str:
    """Creates a new person entity within the Pipedrive CRM.

    This tool creates a new person record with the provided information, including
    contact details, organization association, visibility settings, and custom fields.
    It returns the full details of the created person upon success.

    Format requirements:
        - name: Required person name (cannot be empty)
        - owner_id_str: User ID as a string (will be converted to integer)
        - org_id_str: Organization ID as a string (will be converted to integer)
        - email_address: Valid email address string
        - email_label: Label for the email (work, home, etc.)
        - phone_number: Phone number string in any format accepted by Pipedrive
        - phone_label: Label for the phone number (work, home, mobile, etc.)
        - visible_to_str: Visibility setting as a string (1-3), where:
          "1" = Owner only
          "2" = Owner's visibility group
          "3" = Entire company
        - custom_fields_str: JSON string of custom fields (optional)

    Example:
        create_person_in_pipedrive(
            name="John Doe",
            email_address="john@example.com",
            phone_number="+1 234 567 8901",
            org_id_str="42",
            visible_to_str="3"
        )

    Args:
        ctx: Context object containing the Pipedrive client
        name: Full name of the person to create (required)
        owner_id_str: ID of the user who will own this person record
        org_id_str: ID of the organization to link this person to
        email_address: Primary email address for this person
        email_label: Label for the email address (default: "work")
        phone_number: Primary phone number for this person
        phone_label: Label for the phone number (default: "work")
        visible_to_str: Visibility setting as string (1=Owner only, 2=Owner's group, 3=Entire company)
        custom_fields_str: JSON string of custom fields to set

    Returns:
        JSON string containing success status and created person data or error message.
    """
    logger.debug(
        f"Tool 'create_person_in_pipedrive' ENTERED with raw args: "
        f"name='{name}', owner_id_str={owner_id_str}, org_id_str={org_id_str}, "
        f"email_address={email_address}, email_label={email_label}, "
        f"phone_number={phone_number}, phone_label={phone_label}, "
        f"visible_to_str={visible_to_str}, custom_fields_str={custom_fields_str}"
    )

    # Validate required fields
    if not name or not name.strip():
        error_msg = "Person name is required and cannot be empty"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    # Sanitize empty strings to None
    owner_id_str = None if owner_id_str == "" else owner_id_str
    org_id_str = None if org_id_str == "" else org_id_str
    email_address = None if email_address == "" else email_address
    phone_number = None if phone_number == "" else phone_number
    visible_to_str = None if visible_to_str == "" else visible_to_str
    custom_fields_str = None if custom_fields_str == "" else custom_fields_str

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

    # Validate visibility setting
    if visible_to is not None and visible_to not in {1, 2, 3}:
        error_msg = (
            f"Invalid visible_to value: {visible_to}. "
            f"Must be one of [1, 2, 3] (1=Owner only, 2=Owner's group, 3=Entire company)"
        )
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    # Parse custom fields if provided
    custom_fields = None
    if custom_fields_str:
        try:
            import json
            custom_fields = json.loads(custom_fields_str)
            if not isinstance(custom_fields, dict):
                raise ValueError("Custom fields must be a JSON object")
        except Exception as e:
            error_msg = f"Invalid custom_fields_str format: {str(e)}"
            logger.error(error_msg)
            return format_tool_response(False, error_message=error_msg)

    try:
        # Create Person model instance with validation
        person = Person(
            name=name, owner_id=owner_id, org_id=org_id, visible_to=visible_to
        )

        # Add email if provided
        if email_address and email_address.strip():
            if '@' not in email_address:
                error_msg = f"Invalid email format for '{email_address}'. Email must contain '@' symbol."
                logger.error(error_msg)
                return format_tool_response(False, error_message=error_msg)
                
            person.emails.append(Email(value=email_address, label=email_label, primary=True))

        # Add phone if provided
        if phone_number and phone_number.strip():
            person.phones.append(Phone(value=phone_number, label=phone_label, primary=True))

        # Convert model to API-compatible dict
        payload = person.to_api_dict()

        # Add custom fields if provided
        if custom_fields:
            payload.update(custom_fields)

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