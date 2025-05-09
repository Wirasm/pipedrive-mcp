from typing import Optional, Dict, Any

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.persons.models.person import Person
from pipedrive.api.features.persons.models.contact_info import Email, Phone
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.mcp_instance import mcp


@mcp.tool()
async def update_person_in_pipedrive(
    ctx: Context,
    id_str: str,
    name: Optional[str] = None,
    owner_id_str: Optional[str] = None,
    org_id_str: Optional[str] = None,
    email_address: Optional[str] = None,
    email_label: str = "work",
    phone_number: Optional[str] = None,
    phone_label: str = "work",
    visible_to_str: Optional[str] = None,
) -> str:
    """Updates an existing person in the Pipedrive CRM.

    This tool requires the person's ID and at least one field to update.
    It can update basic information like name, owner, organization,
    as well as contact details like email and phone.

    args:
    ctx: Context
    id_str: str - The ID of the person to update
    name: Optional[str] = None - The updated name of the person
    owner_id_str: Optional[str] = None - The ID of the user who owns the person
    org_id_str: Optional[str] = None - The ID of the organization linked to the person
    email_address: Optional[str] = None - Email address to update/add
    email_label: str = "work" - Label for the email (work, home, etc.)
    phone_number: Optional[str] = None - Phone number to update/add
    phone_label: str = "work" - Label for the phone number (work, home, mobile, etc.)
    visible_to_str: Optional[str] = None - Visibility setting of the person
    """
    logger.debug(
        f"Tool 'update_person_in_pipedrive' ENTERED with raw args: id_str='{id_str}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Verify that at least one update field is provided
    if all(param is None for param in [
        name, owner_id_str, org_id_str, email_address, phone_number, visible_to_str
    ]):
        error_msg = "At least one field must be provided to update a person"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    # Convert string IDs to integers using our utility function
    person_id, id_error = convert_id_string(id_str, "person_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)
    
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
        # Build an update payload
        update_data: Dict[str, Any] = {}
        
        if name is not None:
            update_data["name"] = name
        if owner_id is not None:
            update_data["owner_id"] = owner_id
        if org_id is not None:
            update_data["org_id"] = org_id
        if visible_to is not None:
            update_data["visible_to"] = visible_to
            
        # Handle email update if provided
        emails = None
        if email_address and email_address.strip():
            email = Email(
                value=email_address,
                label=email_label,
                primary=True
            )
            emails = [email.to_dict()]
            update_data["emails"] = emails
        
        # Handle phone update if provided
        phones = None
        if phone_number and phone_number.strip():
            phone = Phone(
                value=phone_number,
                label=phone_label,
                primary=True
            )
            phones = [phone.to_dict()]
            update_data["phones"] = phones
        
        logger.debug(f"Prepared payload for person update: {update_data}")
        
        # Call the Pipedrive API using the persons client
        updated_person = await pd_mcp_ctx.pipedrive_client.persons.update_person(
            person_id=person_id,
            **update_data
        )
        
        logger.info(f"Successfully updated person with ID: {person_id}")
        
        # Return the API response
        return format_tool_response(True, data=updated_person)
        
    except ValidationError as e:
        logger.error(f"Validation error updating person {id_str}: {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except ValueError as e:
        logger.error(f"Value error updating person {id_str}: {str(e)}")
        return format_tool_response(False, error_message=str(e))
    except PipedriveAPIError as e:
        logger.error(
            f"PipedriveAPIError in tool 'update_person_in_pipedrive' for ID {id_str}: {str(e)} - Response Data: {e.response_data}"
        )
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(
            f"Unexpected error in tool 'update_person_in_pipedrive' for ID {id_str}: {str(e)}"
        )
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )