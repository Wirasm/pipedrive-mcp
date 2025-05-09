import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from .api.pipedrive_context import pipedrive_lifespan  # Relative import

load_dotenv()

mcp = FastMCP(
    "mcp-pipedrive",
    description="MCP server for Pipedrive API v2",
    lifespan=pipedrive_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=int(os.getenv("PORT", "8152")),
)
