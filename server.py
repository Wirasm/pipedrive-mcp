import asyncio
import os

from dotenv import load_dotenv

from log_config import logger

# tools and lifespan has to be imported here for the server to work, lets figure out how to handle it nicer later
from pipedrive.api.features.persons.tools.person_create_tool import (
    create_person_in_pipedrive,
)
from pipedrive.api.features.persons.tools.person_delete_tool import (
    delete_person_from_pipedrive,
)
from pipedrive.api.features.persons.tools.person_get_tool import (
    get_person_from_pipedrive,
)
from pipedrive.api.features.persons.tools.person_search_tool import (
    search_persons_in_pipedrive,
)
from pipedrive.api.features.persons.tools.person_update_tool import (
    update_person_in_pipedrive,
)
from pipedrive.api.pipedrive_context import pipedrive_lifespan
from pipedrive.mcp_instance import mcp

load_dotenv()


async def main():
    transport = os.getenv("TRANSPORT", "sse")
    server_host = os.getenv("HOST", "0.0.0.0")
    server_port = int(os.getenv("PORT", "8152"))

    logger.info(
        f"Starting Pipedrive MCP server. Transport: {transport}, Host: {server_host}, Port: {server_port}"
    )

    if transport == "sse":
        await mcp.run_sse_async()  # Assuming this is the correct method from FastMCP
    else:
        logger.info(
            "Stdio transport selected. Ensure your FastMCP setup supports this or modify."
        )
        # Example: await mcp.run_stdio_async() if it exists
        # For now, let's assume sse is the primary test method
        if hasattr(mcp, "run_stdio_async"):
            await mcp.run_stdio_async()
        else:
            logger.warning(
                "run_stdio_async method not found on mcp object. Defaulting to SSE behavior for this example if stdio is chosen."
            )
            await mcp.run_sse_async()


if __name__ == "__main__":
    asyncio.run(main())
