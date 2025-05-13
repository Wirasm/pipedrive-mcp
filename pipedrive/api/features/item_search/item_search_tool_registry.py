from pipedrive.api.features.tool_registry import registry, FeatureMetadata
from pipedrive.api.features.item_search.tools.item_search_tool import search_items_in_pipedrive
from pipedrive.api.features.item_search.tools.item_field_search_tool import search_item_field_in_pipedrive

# Register the feature
registry.register_feature(
    "item_search",
    FeatureMetadata(
        name="Item Search",
        description="Tools for searching across different item types in Pipedrive",
        version="1.0.0",
    )
)

# Register all tools for this feature
registry.register_tool("item_search", search_items_in_pipedrive)
registry.register_tool("item_search", search_item_field_in_pipedrive)