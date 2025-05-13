name: "Lead API MCP Tools"
description: |

  ## Goal
  Implement a complete set of MCP tools for managing leads in Pipedrive, utilizing the new API version abstraction to handle the different API versions needed for lead endpoints.

  ## Why
  - Provide a complete CRUD interface for Lead entity management through MCP
  - Allow Claude to interact with Pipedrive leads without needing additional development
  - Complete the ecosystem of Pipedrive entity management (persons, deals, organizations, leads)
  - Demonstrate usage of our new API version abstraction for mixed v1/v2 endpoints

  ## What
  The project will create MCP tools to:
  1. Get all leads (with filtering options)
  2. Get lead details
  3. Search for leads
  4. Create a lead
  5. Update a lead
  6. Delete a lead
  7. Get lead labels
  8. Get lead sources

  ## Endpoints to Implement

  **Get All Leads**
  - GET /v1/leads
  - Returns multiple leads with optional filtering and pagination

  **Get Lead Details**
  - GET /v1/leads/{id}
  - Returns details of a specific lead

  **Search Leads**
  - GET /api/v2/leads/search
  - Searches all leads by title, notes, and/or custom fields

  **Create Lead**
  - POST /v1/leads
  - Creates a new lead with the provided details

  **Update Lead**
  - PATCH /v1/leads/{id}
  - Updates one or more properties of a lead

  **Delete Lead**
  - DELETE /v1/leads/{id}
  - Deletes a specific lead

  **Get Lead Labels**
  - GET /v1/leadLabels
  - Returns details of all lead labels

  **Get Lead Sources**
  - GET /v1/leadSources
  - Returns all lead sources

  ## Current Directory Structure
  ```
  ├── pipedrive
  │   ├── api
  │   │   ├── base_client.py        # Enhanced with API version abstraction
  │   │   ├── features
  │   │   │   ├── persons/
  │   │   │   ├── deals/
  │   │   │   ├── organizations/
  │   │   │   ├── item_search/
  │   │   │   └── shared/
  │   │   ├── pipedrive_api_error.py
  │   │   ├── pipedrive_client.py
  │   │   └── pipedrive_context.py
  │   ├── mcp_instance.py
  ```

  ## Proposed Directory Structure
  ```
  ├── pipedrive
  │   ├── api
  │   │   ├── features
  │   │   │   ├── leads
  │   │   │   │   ├── __init__.py
  │   │   │   │   ├── client
  │   │   │   │   │   ├── __init__.py
  │   │   │   │   │   ├── lead_client.py       # Uses version parameter from BaseClient
  │   │   │   │   │   └── tests
  │   │   │   │   │       ├── __init__.py
  │   │   │   │   │       └── test_lead_client.py
  │   │   │   │   ├── models
  │   │   │   │   │   ├── __init__.py
  │   │   │   │   │   ├── lead.py              # Main Lead model
  │   │   │   │   │   ├── lead_label.py        # Lead label model
  │   │   │   │   │   └── tests
  │   │   │   │   │       ├── __init__.py
  │   │   │   │   │       ├── test_lead.py
  │   │   │   │   │       └── test_lead_label.py
  │   │   │   │   └── tools
  │   │   │   │       ├── __init__.py
  │   │   │   │       ├── lead_create_tool.py
  │   │   │   │       ├── lead_get_tool.py
  │   │   │   │       ├── lead_list_tool.py
  │   │   │   │       ├── lead_search_tool.py
  │   │   │   │       ├── lead_update_tool.py
  │   │   │   │       ├── lead_delete_tool.py
  │   │   │   │       ├── lead_label_get_tool.py
  │   │   │   │       ├── lead_source_get_tool.py
  │   │   │   │       └── tests
  │   │   │   │           ├── __init__.py
  │   │   │   │           ├── test_lead_create_tool.py
  │   │   │   │           ├── test_lead_get_tool.py
  │   │   │   │           ├── test_lead_list_tool.py
  │   │   │   │           ├── test_lead_search_tool.py
  │   │   │   │           ├── test_lead_update_tool.py
  │   │   │   │           ├── test_lead_delete_tool.py
  │   │   │   │           ├── test_lead_label_get_tool.py
  │   │   │   │           └── test_lead_source_get_tool.py
  │   │   ├── pipedrive_client.py              # Updated to include lead_client
  ```

  ## Files to Reference
  - PRPs/api_version_abstraction.md (read_only) - Details on the API version abstraction to use
  - ai_docs/pipedrive_leads.md (read_only) - API reference for leads endpoints
  - ai_docs/pipedrive_basics.md (read_only) - general API information
  - ai_docs/pipedrive_v2_migrate.md (read_only) - details about v1 vs v2 API differences
  - pipedrive/api/features/deals/ (directory to MIRROR for leads implementation)
  - pipedrive/api/base_client.py (with API version abstraction implemented)
  - pipedrive/api/pipedrive_client.py (for integrating the lead client)
  - pipedrive/api/features/shared/conversion/id_conversion.py (for ID validation)
  - pipedrive/api/features/shared/utils.py (for response formatting)

  ## Files to Implement (concept)

  ### Models
  1. `lead.py` - Pydantic model representing a lead
  2. `lead_label.py` - Pydantic model for lead labels

  ### Client
  1. `lead_client.py` - API client that uses the version parameter from BaseClient

  ### Tools
  1. `lead_create_tool.py` - Create a new lead
  2. `lead_get_tool.py` - Get lead details
  3. `lead_list_tool.py` - List/get all leads with filtering
  4. `lead_search_tool.py` - Search for leads
  5. `lead_update_tool.py` - Update a lead
  6. `lead_delete_tool.py` - Delete a lead
  7. `lead_label_get_tool.py` - Get all lead labels
  8. `lead_source_get_tool.py` - Get all lead sources

  ## Implementation Notes

  ### Using the API Version Abstraction
  The enhanced BaseClient now supports version specification, simplifying implementation of lead endpoints. Example:

  ```python
  class LeadClient:
      """Client for Pipedrive Lead API endpoints"""

      def __init__(self, base_client: BaseClient):
          """
          Initialize the Lead client
          
          Args:
              base_client: BaseClient instance for making API requests
          """
          self.base_client = base_client
          
      async def create_lead(self, title: str, ...):
          """Create a new lead in Pipedrive"""
          payload = {"title": title, ...}
          # Specify version="v1" for v1 endpoints
          return await self.base_client.request(
              "POST", 
              "/leads", 
              json_payload=payload,
              version="v1"  # Explicitly use v1 API
          )
          
      async def search_leads(self, term: str, ...):
          """Search for leads using v2 endpoint"""
          # This specific endpoint uses v2
          return await self.base_client.request(
              "GET", 
              "/leads/search", 
              query_params={"term": term, ...},
              version="v2"  # Explicitly use v2 API
          )
  ```

  ### UUID Handling
  Leads use UUID strings for IDs rather than integers. The existing id_conversion utility handles integer IDs, so we need to:

  1. Create a new utility function for validating UUID format in `shared/conversion/`
  2. Or modify the existing function to handle both integer and UUID formats

  ### Lead-Deal Custom Field Inheritance
  Leads use the same custom fields as deals, so we need to:

  1. Understand the custom field structure already implemented for deals
  2. Ensure the Lead model handles these custom fields correctly

  ## Validation Gates
  - Each model must have proper Pydantic v2 validation
  - Each client method must handle API errors gracefully 
  - Each tool must be validated by running the appropriate tests
  - All tools must handle error cases gracefully (e.g., invalid IDs, not found records)
  - Every tool must provide user-friendly error messages
  - Follow the existing patterns for error handling and response formatting
  - All tests must pass when running `uv run pytest`

  ## Implementation Checkpoints/Testing

  ### 1. Lead Models
  - Implement `Lead` model with relevant fields (title, value, currency, etc.)
  - Implement `LeadLabel` model
  - Add proper validation with Pydantic
  - Write tests for model validation

  ### 2. Lead Client
  - Implement `LeadClient` class using the API version abstraction
  - Add methods for all lead operations with appropriate version parameters
  - Add proper error handling and logging
  - Write tests for client functionality with both v1 and v2 endpoints

  ### 3. Basic Lead Tools
  - Implement `create_lead_in_pipedrive` tool
  - Implement `get_lead_from_pipedrive` tool
  - Implement `list_leads_from_pipedrive` tool
  - Implement `search_leads_in_pipedrive` tool
  - Implement `update_lead_in_pipedrive` tool
  - Implement `delete_lead_from_pipedrive` tool
  - Implement `get_lead_labels_from_pipedrive` tool
  - Implement `get_lead_sources_from_pipedrive` tool

  ### 4. Update Main Client & Testing
  - Update `PipedriveClient` to initialize and expose the lead client
  - Update `server.py` to import and register all tools
  - Write comprehensive tests for all tools
  - Test integration with both v1 and v2 endpoints

  ## Other Considerations

  ### UUID vs Integer IDs
  - Leads use UUID strings (e.g., "adf21080-0e10-11eb-879b-05d71fb426ec")
  - Need to create a validation utility specific to UUID format
  - Tools should accept these string IDs directly without conversion

  ### Lead-specific Data Types
  - Lead Labels and Lead Sources have specific formats and limitations
  - Implement proper validation and error handling for these types