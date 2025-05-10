import os
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

import httpx
from mcp.server.fastmcp import FastMCP

from log_config import logger
from pipedrive.api.pipedrive_client import PipedriveClient


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

    # For development environments, allow disabling SSL verification
    verify_ssl = os.getenv("VERIFY_SSL", "true").lower() != "false"
    if not verify_ssl:
        logger.warning("SSL verification is disabled. This should only be used in development environments.")

    async with httpx.AsyncClient(timeout=30.0, verify=verify_ssl) as client:
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
