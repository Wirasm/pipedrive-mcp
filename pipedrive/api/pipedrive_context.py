from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

import httpx
from mcp.server.fastmcp import FastMCP

from log_config import logger
from pipedrive.api.pipedrive_client import PipedriveClient
from pipedrive.pipedrive_config import settings


@dataclass
class PipedriveMCPContext:
    pipedrive_client: PipedriveClient


@asynccontextmanager
async def pipedrive_lifespan(server: FastMCP) -> AsyncIterator[PipedriveMCPContext]:
    logger.info("Attempting to initialize Pipedrive MCP Context...")

    # Use the settings singleton to get configuration
    if not settings.verify_ssl:
        logger.warning("SSL verification is disabled. This should only be used in development environments.")

    async with httpx.AsyncClient(timeout=settings.timeout, verify=settings.verify_ssl) as client:
        pd_client = PipedriveClient(
            api_token=settings.api_token,
            company_domain=settings.company_domain,
            http_client=client,
        )
        mcp_context = PipedriveMCPContext(pipedrive_client=pd_client)
        try:
            logger.info("Pipedrive MCP Context initialized successfully.")
            yield mcp_context
        finally:
            logger.info("Pipedrive MCP Context cleaned up.")
