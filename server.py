import asyncio
import os

from dotenv import load_dotenv

from log_config import logger

# Import feature registry and discovery
from pipedrive.api.features.tool_registry import registry
from pipedrive.api.features import discover_features
from pipedrive.feature_config import FeatureConfig
from pipedrive.api.pipedrive_context import pipedrive_lifespan
from pipedrive.mcp_instance import mcp

load_dotenv()

# Discover and register all features
discover_features()

# Load feature configuration
feature_config = FeatureConfig()

async def main():
    transport = os.getenv("TRANSPORT", "sse")
    server_host = os.getenv("HOST", "0.0.0.0")
    server_port = int(os.getenv("PORT", "8152"))
    
    # Log enabled features
    enabled_features = feature_config.get_enabled_features()
    logger.info(f"Enabled features: {', '.join(enabled_features.keys())}")
    
    # Log registered tools
    tool_count = registry.get_tool_count()
    logger.info(f"Registered tools: {tool_count}")
    
    logger.info(
        f"Starting Pipedrive MCP server. Transport: {transport}, Host: {server_host}, Port: {server_port}"
    )
    
    if transport == "sse":
        await mcp.run_sse_async()
    else:
        logger.info(
            "Stdio transport selected. Ensure your FastMCP setup supports this or modify."
        )
        if hasattr(mcp, "run_stdio_async"):
            await mcp.run_stdio_async()
        else:
            logger.warning(
                "run_stdio_async method not found on mcp object. Defaulting to SSE behavior for this example if stdio is chosen."
            )
            await mcp.run_sse_async()


if __name__ == "__main__":
    asyncio.run(main())