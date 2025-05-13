from pipedrive.api.features.tool_registry import registry, FeatureMetadata
from pipedrive.api.features.persons.tools.person_create_tool import create_person_in_pipedrive
from pipedrive.api.features.persons.tools.person_get_tool import get_person_from_pipedrive
from pipedrive.api.features.persons.tools.person_update_tool import update_person_in_pipedrive
from pipedrive.api.features.persons.tools.person_delete_tool import delete_person_from_pipedrive
from pipedrive.api.features.persons.tools.person_search_tool import search_persons_in_pipedrive

# Register the feature
registry.register_feature(
    "persons",
    FeatureMetadata(
        name="Persons",
        description="Tools for managing person entities in Pipedrive",
        version="1.0.0",
    )
)

# Register all tools for this feature
registry.register_tool("persons", create_person_in_pipedrive)
registry.register_tool("persons", get_person_from_pipedrive)
registry.register_tool("persons", update_person_in_pipedrive)
registry.register_tool("persons", delete_person_from_pipedrive)
registry.register_tool("persons", search_persons_in_pipedrive)