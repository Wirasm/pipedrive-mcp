from pipedrive.api.features.tool_registry import registry, FeatureMetadata
from pipedrive.api.features.leads.tools.lead_create_tool import create_lead_in_pipedrive
from pipedrive.api.features.leads.tools.lead_get_tool import get_lead_from_pipedrive
from pipedrive.api.features.leads.tools.lead_update_tool import update_lead_in_pipedrive
from pipedrive.api.features.leads.tools.lead_delete_tool import delete_lead_from_pipedrive
from pipedrive.api.features.leads.tools.lead_search_tool import search_leads_in_pipedrive
from pipedrive.api.features.leads.tools.lead_list_tool import list_leads_from_pipedrive
from pipedrive.api.features.leads.tools.lead_label_get_tool import get_lead_labels_from_pipedrive
from pipedrive.api.features.leads.tools.lead_source_get_tool import get_lead_sources_from_pipedrive

# Register the feature
registry.register_feature(
    "leads",
    FeatureMetadata(
        name="Leads",
        description="Tools for managing lead entities in Pipedrive",
        version="1.0.0",
    )
)

# Register all tools for this feature
registry.register_tool("leads", create_lead_in_pipedrive)
registry.register_tool("leads", get_lead_from_pipedrive)
registry.register_tool("leads", update_lead_in_pipedrive)
registry.register_tool("leads", delete_lead_from_pipedrive)
registry.register_tool("leads", search_leads_in_pipedrive)
registry.register_tool("leads", list_leads_from_pipedrive)
registry.register_tool("leads", get_lead_labels_from_pipedrive)
registry.register_tool("leads", get_lead_sources_from_pipedrive)