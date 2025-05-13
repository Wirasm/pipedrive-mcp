import asyncio
import os

from dotenv import load_dotenv

from log_config import logger

# tools and lifespan has to be imported here for the server to work, lets figure out how to handle it nicer later
# Person tools
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

# Deal tools
from pipedrive.api.features.deals.tools.deal_create_tool import (
    create_deal_in_pipedrive,
)
from pipedrive.api.features.deals.tools.deal_get_tool import (
    get_deal_from_pipedrive,
)
from pipedrive.api.features.deals.tools.deal_list_tool import (
    list_deals_from_pipedrive,
)
from pipedrive.api.features.deals.tools.deal_search_tool import (
    search_deals_in_pipedrive,
)
from pipedrive.api.features.deals.tools.deal_update_tool import (
    update_deal_in_pipedrive,
)
from pipedrive.api.features.deals.tools.deal_delete_tool import (
    delete_deal_from_pipedrive,
)

# Deal product tools
from pipedrive.api.features.deals.tools.deal_product_add_tool import (
    add_product_to_deal_in_pipedrive,
)
from pipedrive.api.features.deals.tools.deal_product_update_tool import (
    update_product_in_deal_in_pipedrive,
)
from pipedrive.api.features.deals.tools.deal_product_delete_tool import (
    delete_product_from_deal_in_pipedrive,
)

# Organization tools
from pipedrive.api.features.organizations.tools.organization_create_tool import (
    create_organization_in_pipedrive,
)
from pipedrive.api.features.organizations.tools.organization_get_tool import (
    get_organization_from_pipedrive,
)
from pipedrive.api.features.organizations.tools.organization_list_tool import (
    list_organizations_from_pipedrive,
)
from pipedrive.api.features.organizations.tools.organization_search_tool import (
    search_organizations_in_pipedrive,
)
from pipedrive.api.features.organizations.tools.organization_update_tool import (
    update_organization_in_pipedrive,
)
from pipedrive.api.features.organizations.tools.organization_delete_tool import (
    delete_organization_from_pipedrive,
)

# Organization follower tools
from pipedrive.api.features.organizations.tools.organization_follower_add_tool import (
    add_follower_to_organization_in_pipedrive,
)
from pipedrive.api.features.organizations.tools.organization_follower_delete_tool import (
    delete_follower_from_organization_in_pipedrive,
)

# Item Search tools
from pipedrive.api.features.item_search.tools.item_search_tool import (
    search_items_in_pipedrive,
)
from pipedrive.api.features.item_search.tools.item_field_search_tool import (
    search_item_field_in_pipedrive,
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
