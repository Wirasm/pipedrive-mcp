from typing import Optional, Dict, Any, List

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.persons.models.person import Person
from pipedrive.api.features.persons.models.contact_info import Email, Phone
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("persons")
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
    custom_fields_str: Optional[str] = None,
) -> str:
    """Updates an existing person in the Pipedrive CRM.

    This tool updates a person record with the provided information. Only the fields
    that are explicitly provided will be updated; others remain unchanged. For contact
    information, the provided email/phone will replace any existing ones.

    Format requirements:
        - id_str: Person ID as a string (required, will be converted to integer)
        - name: Updated person name (if not provided, remains unchanged)
        - owner_id_str: User ID as a string (will be converted to integer)
        - org_id_str: Organization ID as a string (will be converted to integer)
          Set to "null" to remove organization association
        - email_address: Email address string (replaces current email)
          Set to "" (empty string) to remove all emails
        - email_label: Label for the email (work, home, etc.)
        - phone_number: Phone number string (replaces current phone)
          Set to "" (empty string) to remove all phones
        - phone_label: Label for the phone number (work, home, mobile, etc.)
        - visible_to_str: Visibility setting as a string (1-3), where:
          "1" = Owner only
          "2" = Owner's visibility group
          "3" = Entire company
        - custom_fields_str: JSON string of custom fields (optional)

    Example:
        update_person_in_pipedrive(
            id_str="123",
            name="Jane Smith",
            email_address="jane@example.com",
            org_id_str="42"
        )

    Args:
        ctx: Context object containing the Pipedrive client
        id_str: ID of the person to update (required)
        name: Updated name of the person
        owner_id_str: Updated owner user ID
        org_id_str: Updated organization ID (set to "null" to remove organization)
        email_address: Updated primary email address (replaces current email)
        email_label: Label for the email (default: "work")
        phone_number: Updated primary phone number (replaces current phone)
        phone_label: Label for the phone (default: "work")
        visible_to_str: Updated visibility setting (1=Owner only, 2=Owner's group, 3=Entire company)
        custom_fields_str: JSON string of custom fields to update

    Returns:
        JSON string containing success status and updated person data or error message.
    """
    logger.debug(
        f"Tool 'update_person_in_pipedrive' ENTERED with raw args: "
        f"id_str='{id_str}', name='{name}', owner_id_str='{owner_id_str}', "
        f"org_id_str='{org_id_str}', email_address='{email_address}', "
        f"phone_number='{phone_number}', visible_to_str='{visible_to_str}', "
        f"custom_fields_str='{custom_fields_str}'"
    )

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Verify that person ID is provided
    if not id_str:
        error_msg = "Person ID is required"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    # Verify that at least one update field is provided
    if all(param is None for param in [
        name, owner_id_str, org_id_str, email_address, phone_number, visible_to_str, custom_fields_str
    ]):
        error_msg = "At least one field must be provided to update a person"
        logger.error(error_msg)
        return format_tool_response(False, error_message=error_msg)

    # Handle special case for org_id: "null" string means to remove organization association
    if org_id_str == "null":
        org_id_str = None
        org_id = None
        remove_org = True
    else:
        remove_org = False

    # Convert string IDs to integers using our utility function
    person_id, id_error = convert_id_string(id_str, "person_id")
    if id_error:
        logger.error(id_error)
        return format_tool_response(False, error_message=id_error)
    
    owner_id, owner_error = convert_id_string(owner_id_str, "owner_id")
    if owner_error:
        logger.error(owner_error)
        return format_tool_response(False, error_message=owner_error)
    
    if not remove_org:  # Only convert org_id if not removing
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
        # Build an update payload
        update_data: Dict[str, Any] = {}
        
        if name is not None:
            if not name.strip():
                error_msg = "Person name cannot be empty"
                logger.error(error_msg)
                return format_tool_response(False, error_message=error_msg)
            update_data["name"] = name
            
        if owner_id is not None:
            update_data["owner_id"] = owner_id
            
        # Handle org_id update (including removal)
        update_data["org_id"] = org_id
            
        if visible_to is not None:
            update_data["visible_to"] = visible_to
            
        # Handle email update if provided (even empty string to clear emails)
        if email_address is not None:
            if email_address == "":
                # Empty string means clear all emails
                update_data["emails"] = []
            else:
                # Otherwise add the provided email
                if '@' not in email_address:
                    error_msg = f"Invalid email format for '{email_address}'. Email must contain '@' symbol."
                    logger.error(error_msg)
                    return format_tool_response(False, error_message=error_msg)
                
                email = Email(
                    value=email_address,
                    label=email_label,
                    primary=True
                )
                update_data["emails"] = [email.to_dict()]
        
        # Handle phone update if provided (even empty string to clear phones)
        if phone_number is not None:
            if phone_number == "":
                # Empty string means clear all phones
                update_data["phones"] = []
            else:
                # Otherwise add the provided phone
                phone = Phone(
                    value=phone_number,
                    label=phone_label,
                    primary=True
                )
                update_data["phones"] = [phone.to_dict()]
        
        # Add custom fields if provided
        if custom_fields:
            update_data.update(custom_fields)
        
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