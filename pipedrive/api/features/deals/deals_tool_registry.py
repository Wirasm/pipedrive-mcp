from pipedrive.api.features.tool_registry import registry, FeatureMetadata
from pipedrive.api.features.deals.tools.deal_create_tool import create_deal_in_pipedrive
from pipedrive.api.features.deals.tools.deal_get_tool import get_deal_from_pipedrive
from pipedrive.api.features.deals.tools.deal_update_tool import update_deal_in_pipedrive
from pipedrive.api.features.deals.tools.deal_delete_tool import delete_deal_from_pipedrive
from pipedrive.api.features.deals.tools.deal_search_tool import search_deals_in_pipedrive
from pipedrive.api.features.deals.tools.deal_list_tool import list_deals_from_pipedrive
from pipedrive.api.features.deals.tools.deal_product_add_tool import add_product_to_deal_in_pipedrive
from pipedrive.api.features.deals.tools.deal_product_update_tool import update_product_in_deal_in_pipedrive
from pipedrive.api.features.deals.tools.deal_product_delete_tool import delete_product_from_deal_in_pipedrive

# Register the feature
registry.register_feature(
    "deals",
    FeatureMetadata(
        name="Deals",
        description="Tools for managing deal entities in Pipedrive",
        version="1.0.0",
    )
)

# Register all deal tools for this feature
registry.register_tool("deals", create_deal_in_pipedrive)
registry.register_tool("deals", get_deal_from_pipedrive)
registry.register_tool("deals", update_deal_in_pipedrive)
registry.register_tool("deals", delete_deal_from_pipedrive)
registry.register_tool("deals", search_deals_in_pipedrive)
registry.register_tool("deals", list_deals_from_pipedrive)

# Register all deal product tools for this feature
registry.register_tool("deals", add_product_to_deal_in_pipedrive)
registry.register_tool("deals", update_product_in_deal_in_pipedrive)
registry.register_tool("deals", delete_product_from_deal_in_pipedrive)