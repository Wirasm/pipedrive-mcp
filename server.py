import asyncio
import json
import os
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any, Optional, Dict, List 

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP

from pipedrive_client import PipedriveAPIError, PipedriveClient
import logging

load_dotenv()

# --- Configure Logging ---
logging.basicConfig(
    level=logging.DEBUG, # Ensure this is DEBUG for testing
    format="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@dataclass
class PipedriveMCPContext:
    pipedrive_client: PipedriveClient


@asynccontextmanager
async def pipedrive_lifespan(server: FastMCP) -> AsyncIterator[PipedriveMCPContext]:
    logger.info("Attempting to initialize Pipedrive MCP Context...")
    pipedrive_api_token = os.getenv("PIPEDRIVE_API_TOKEN")
    pipedrive_company_domain = os.getenv("PIPEDRIVE_COMPANY_DOMAIN")

    if not pipedrive_api_token:
        logger.error("PIPEDRIVE_API_TOKEN environment variable not set.")
        raise ValueError("PIPEDRIVE_API_TOKEN environment variable not set.")
    if not pipedrive_company_domain:
        logger.error("PIPEDRIVE_COMPANY_DOMAIN environment variable not set.")
        raise ValueError("PIPEDRIVE_COMPANY_DOMAIN environment variable not set.")

    async with httpx.AsyncClient(timeout=30.0) as client:
        pd_client = PipedriveClient(
            api_token=pipedrive_api_token,
            company_domain=pipedrive_company_domain,
            http_client=client,
        )
        mcp_context = PipedriveMCPContext(pipedrive_client=pd_client)
        try:
            logger.info("Pipedrive MCP Context initialized successfully.")
            yield mcp_context
        finally:
            logger.info("Pipedrive MCP Context cleaned up.")


mcp = FastMCP(
    "mcp-pipedrive",
    description="MCP server for Pipedrive API v2",
    lifespan=pipedrive_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=int(os.getenv("PORT", "8152")),
)

def format_tool_response(
    success: bool, data: Optional[Any] = None, error_message: Optional[str] = None
) -> str:
    return json.dumps(
        {"success": success, "data": data, "error": error_message}, indent=2
    )

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
    visible_to_str: Optional[str] = None
) -> str:
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
    actual_owner_id: Optional[int] = None
    if owner_id_str is not None and owner_id_str.strip(): # Check if not None and not empty/whitespace
        try:
            actual_owner_id = int(owner_id_str)
        except ValueError:
            err_msg = f"Invalid owner_id format: '{owner_id_str}'. Must be an integer string."
            logger.error(err_msg)
            return format_tool_response(False, error_message=err_msg)

    actual_org_id: Optional[int] = None
    if org_id_str is not None and org_id_str.strip():
        try:
            actual_org_id = int(org_id_str)
        except ValueError:
            err_msg = f"Invalid org_id format: '{org_id_str}'. Must be an integer string."
            logger.error(err_msg)
            return format_tool_response(False, error_message=err_msg)

    actual_visible_to: Optional[int] = None
    if visible_to_str is not None and visible_to_str.strip():
        try:
            actual_visible_to = int(visible_to_str)
        except ValueError:
            err_msg = f"Invalid visible_to format: '{visible_to_str}'. Must be an integer string."
            logger.error(err_msg)
            return format_tool_response(False, error_message=err_msg)

    logger.debug(f"Converted args: owner_id={actual_owner_id}, org_id={actual_org_id}, visible_to={actual_visible_to}")

    emails_payload = None
    if email_address is not None and email_address.strip():
        emails_payload = [{"value": email_address, "label": email_label, "primary": True}]
    elif email_address == "": # Explicitly empty string might mean "no email"
        logger.debug("email_address is an empty string, treating as no email for payload.")


    phones_payload = None
    if phone_number is not None and phone_number.strip():
        phones_payload = [{"value": phone_number, "label": phone_label, "primary": True}]
    elif phone_number == "":
        logger.debug("phone_number is an empty string, treating as no phone for payload.")
    
    logger.debug(f"Constructed emails_payload: {emails_payload}")
    logger.debug(f"Constructed phones_payload: {phones_payload}")

    try:
        created_person = await pd_mcp_ctx.pipedrive_client.create_person(
            name=name,
            owner_id=actual_owner_id,
            org_id=actual_org_id,    
            emails=emails_payload,
            phones=phones_payload,
            visible_to=actual_visible_to,
        )
        logger.info(f"Successfully created person '{name}' with ID: {created_person.get('id')}")
        return format_tool_response(True, data=created_person)
    except PipedriveAPIError as e:
        logger.error(f"PipedriveAPIError in tool 'create_person_in_pipedrive' for '{name}': {str(e)} - Response Data: {e.response_data}")
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(f"Unexpected error in tool 'create_person_in_pipedrive' for '{name}': {str(e)}")
        return format_tool_response(
            False, error_message=f"An unexpected error occurred: {str(e)}"
        )

# --- Other tools (get, update, delete, list) would follow a similar pattern ---
# For brevity, I'm only showing the create tool. You'd adapt the others:
# - Change Optional[int] in signatures to Optional[str] for IDs.
# - Add manual int() conversion with error handling.

async def main():
    transport = os.getenv("TRANSPORT", "stdio")
    server_host = os.getenv("HOST", "0.0.0.0")
    server_port = int(os.getenv("PORT", "8152"))

    logger.info(f"Starting Pipedrive MCP server. Transport: {transport}, Host: {server_host}, Port: {server_port}")

    if transport == "sse":
        await mcp.run_sse_async() # Assuming this is the correct method from FastMCP
    else:
        # If you have a stdio run method, use it, otherwise this might need adjustment
        logger.info("Stdio transport selected. Ensure your FastMCP setup supports this or modify.")
        # Example: await mcp.run_stdio_async() if it exists
        # For now, let's assume sse is the primary test method
        if hasattr(mcp, 'run_stdio_async'):
            await mcp.run_stdio_async()
        else:
            logger.warning("run_stdio_async method not found on mcp object. Defaulting to SSE behavior for this example if stdio is chosen.")
            await mcp.run_sse_async()


if __name__ == "__main__":
    asyncio.run(main())