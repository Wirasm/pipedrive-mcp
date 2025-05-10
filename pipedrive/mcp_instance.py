import os
from typing import List, Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from .api.pipedrive_context import pipedrive_lifespan  # Relative import

load_dotenv()


# Use 127.0.0.1 as the default host instead of 0.0.0.0 for better security
default_host = "127.0.0.1"
# If running in a container, we need to use 0.0.0.0 to expose the port
if os.getenv("CONTAINER_MODE", "false").lower() == "true":
    default_host = "0.0.0.0"

# Create the FastMCP instance
mcp = FastMCP(
    "mcp-pipedrive",
    description="MCP server for Pipedrive API v2",
    lifespan=pipedrive_lifespan,
    host=os.getenv("HOST", default_host),
    port=int(os.getenv("PORT", "8152")),
)
