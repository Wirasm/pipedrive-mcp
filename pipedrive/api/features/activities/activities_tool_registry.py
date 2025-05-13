from pipedrive.api.features.tool_registry import registry, FeatureMetadata
from pipedrive.api.features.activities.tools.activity_create_tool import create_activity_in_pipedrive
from pipedrive.api.features.activities.tools.activity_get_tool import get_activity_from_pipedrive
from pipedrive.api.features.activities.tools.activity_list_tool import list_activities_from_pipedrive
from pipedrive.api.features.activities.tools.activity_update_tool import update_activity_in_pipedrive
from pipedrive.api.features.activities.tools.activity_delete_tool import delete_activity_from_pipedrive
from pipedrive.api.features.activities.tools.activity_type_list_tool import get_activity_types_from_pipedrive
from pipedrive.api.features.activities.tools.activity_type_create_tool import create_activity_type_in_pipedrive

# Register the feature
registry.register_feature(
    "activities",
    FeatureMetadata(
        name="Activities",
        description="Tools for managing activity entities in Pipedrive",
        version="1.0.0",
    )
)

# Register all activity tools for this feature
registry.register_tool("activities", create_activity_in_pipedrive)
registry.register_tool("activities", get_activity_from_pipedrive)
registry.register_tool("activities", list_activities_from_pipedrive)
registry.register_tool("activities", update_activity_in_pipedrive)
registry.register_tool("activities", delete_activity_from_pipedrive)

# Register all activity type tools for this feature
registry.register_tool("activities", get_activity_types_from_pipedrive)
registry.register_tool("activities", create_activity_type_in_pipedrive)