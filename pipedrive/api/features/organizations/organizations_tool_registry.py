from pipedrive.api.features.tool_registry import registry, FeatureMetadata
from pipedrive.api.features.organizations.tools.organization_create_tool import create_organization_in_pipedrive
from pipedrive.api.features.organizations.tools.organization_get_tool import get_organization_from_pipedrive
from pipedrive.api.features.organizations.tools.organization_update_tool import update_organization_in_pipedrive
from pipedrive.api.features.organizations.tools.organization_delete_tool import delete_organization_from_pipedrive
from pipedrive.api.features.organizations.tools.organization_search_tool import search_organizations_in_pipedrive
from pipedrive.api.features.organizations.tools.organization_list_tool import list_organizations_from_pipedrive
from pipedrive.api.features.organizations.tools.organization_follower_add_tool import add_follower_to_organization_in_pipedrive
from pipedrive.api.features.organizations.tools.organization_follower_delete_tool import delete_follower_from_organization_in_pipedrive

# Register the feature
registry.register_feature(
    "organizations",
    FeatureMetadata(
        name="Organizations",
        description="Tools for managing organization entities in Pipedrive",
        version="1.0.0",
    )
)

# Register all tools for this feature
registry.register_tool("organizations", create_organization_in_pipedrive)
registry.register_tool("organizations", get_organization_from_pipedrive)
registry.register_tool("organizations", update_organization_in_pipedrive)
registry.register_tool("organizations", delete_organization_from_pipedrive)
registry.register_tool("organizations", search_organizations_in_pipedrive)
registry.register_tool("organizations", list_organizations_from_pipedrive)
registry.register_tool("organizations", add_follower_to_organization_in_pipedrive)
registry.register_tool("organizations", delete_follower_from_organization_in_pipedrive)