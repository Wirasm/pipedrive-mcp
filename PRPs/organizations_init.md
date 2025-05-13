name: "Organization API MCP Tools"
description: |

  ## Goal
  Implement a complete set of MCP tools for managing organizations in Pipedrive. This project will create tools for:
  1. Getting all organizations (with filtering options)
  2. Getting organization details
  3. Searching for organizations
  4. Creating an organization
  5. Updating an organization
  6. Deleting an organization
  7. Managing organization followers (add, delete)

  ## Why
  - Provide a complete CRUD interface for Organization entity management through MCP
  - Allow MCP clients to perform all standard operations on Pipedrive organizations without needing additional development
  - Continue the pattern established with Person and Deal entity implementations
  - Enable integration with organization-related workflows in CRM operations

  ## What
  The Organization feature will follow the same vertical slice architecture used for the Person and Deal features, implementing:
  - Pydantic models for organizations
  - API client for interacting with the Pipedrive Organizations endpoints
  - MCP tools that expose organization management functionality
  - Comprehensive tests for all components

  ## Endpoints to Implement
  
  **Get All Organizations**
  - GET /api/v2/organizations
  - Returns all organizations with optional filtering and pagination
  
  **Get Organization Details**
  - GET /api/v2/organizations/{id}
  - Returns the details of a specific organization with optional fields
  
  **Search Organizations**
  - GET /api/v2/organizations/search
  - Searches all organizations by name, address, notes, and/or custom fields
  
  **Create Organization**
  - POST /api/v2/organizations
  - Creates a new organization with the provided details
  
  **Update Organization**
  - PATCH /api/v2/organizations/{id}
  - Updates the properties of an organization
  
  **Delete Organization**
  - DELETE /api/v2/organizations/{id}
  - Marks an organization as deleted
  
  **Add Follower to Organization**
  - POST /api/v2/organizations/{id}/followers
  - Adds a user as a follower to the organization
  
  **Delete Follower from Organization**
  - DELETE /api/v2/organizations/{id}/followers/{follower_id}
  - Deletes a user follower from the organization

  ## Current Directory Structure
  ```
  ├── pipedrive
  │   ├── api
  │   │   ├── features
  │   │   │   ├── deals                      (existing feature)
  │   │   │   │   ├── client
  │   │   │   │   ├── models
  │   │   │   │   └── tools
  │   │   │   ├── item_search                (existing feature)
  │   │   │   │   ├── client
  │   │   │   │   ├── models
  │   │   │   │   └── tools
  │   │   │   ├── persons                    (existing feature)
  │   │   │   │   ├── client
  │   │   │   │   ├── models
  │   │   │   │   └── tools
  │   │   │   └── shared                     (shared utilities)
  │   │   │       ├── conversion
  │   │   │       │   └── id_conversion.py
  │   │   │       └── utils.py
  │   │   ├── base_client.py
  │   │   ├── pipedrive_api_error.py
  │   │   ├── pipedrive_client.py
  │   │   └── pipedrive_context.py
  ```

  ## Proposed Directory Structure
  ```
  ├── pipedrive
  │   ├── api
  │   │   ├── features
  │   │   │   ├── organizations              (new feature)
  │   │   │   │   ├── __init__.py
  │   │   │   │   ├── client
  │   │   │   │   │   ├── __init__.py
  │   │   │   │   │   ├── organization_client.py
  │   │   │   │   │   └── tests
  │   │   │   │   │       ├── __init__.py
  │   │   │   │   │       └── test_organization_client.py
  │   │   │   │   ├── models
  │   │   │   │   │   ├── __init__.py
  │   │   │   │   │   ├── organization.py
  │   │   │   │   │   ├── organization_follower.py
  │   │   │   │   │   └── tests
  │   │   │   │   │       ├── __init__.py
  │   │   │   │   │       ├── test_organization.py
  │   │   │   │   │       └── test_organization_follower.py
  │   │   │   │   └── tools
  │   │   │   │       ├── __init__.py
  │   │   │   │       ├── organization_create_tool.py
  │   │   │   │       ├── organization_get_tool.py
  │   │   │   │       ├── organization_list_tool.py
  │   │   │   │       ├── organization_search_tool.py
  │   │   │   │       ├── organization_update_tool.py
  │   │   │   │       ├── organization_delete_tool.py
  │   │   │   │       ├── organization_follower_add_tool.py
  │   │   │   │       ├── organization_follower_delete_tool.py
  │   │   │   │       └── tests
  │   │   │   │           ├── __init__.py
  │   │   │   │           ├── test_organization_create_tool.py
  │   │   │   │           ├── test_organization_get_tool.py
  │   │   │   │           ├── test_organization_list_tool.py
  │   │   │   │           ├── test_organization_search_tool.py
  │   │   │   │           ├── test_organization_update_tool.py
  │   │   │   │           ├── test_organization_delete_tool.py
  │   │   │   │           ├── test_organization_follower_add_tool.py
  │   │   │   │           └── test_organization_follower_delete_tool.py
  ```

  ## Files to Reference
  - [ai_docs/pipedrive_organizations.md](read_only) MUST READ (detailed API reference for Organizations endpoints)
  - [pipedrive/api/features/persons/](read_only) (directory to MIRROR for organizations implementation)
  - [pipedrive/api/features/persons/client/person_client.py](read_only) (reference for client implementation)
  - [pipedrive/api/features/persons/models/person.py](read_only) (reference for model implementation)
  - [pipedrive/api/features/persons/tools/person_create_tool.py](read_only) (reference for tool implementation)
  - [pipedrive/api/features/shared/conversion/id_conversion.py](read_only) (for ID validation)
  - [pipedrive/api/features/shared/utils.py](read_only) (for response formatting)

  ## Files to Implement (concept)
  
  ### Models
  1. `organization.py` - Pydantic model representing an organization with validation rules
  ```python
  from typing import Any, Dict, List, Optional
  from pydantic import BaseModel, Field, field_validator

  class Organization(BaseModel):
      """Model representing an organization in Pipedrive with validation"""
      
      name: str
      owner_id: Optional[int] = None
      visible_to: Optional[int] = None  # Visibility setting (1-4)
      address: Optional[str] = None
      
      @field_validator('visible_to')
      def validate_visible_to(cls, v):
          """Validate visibility setting"""
          if v is not None and v not in [1, 2, 3, 4]:
              raise ValueError(f"Invalid visibility value: {v}. Must be one of: 1, 2, 3, 4")
          return v
          
      def to_api_dict(self) -> Dict[str, Any]:
          """Convert model to API-compatible dict format"""
          # Implementation following the pattern from person.py
  ```

  2. `organization_follower.py` - Pydantic model for managing organization followers
  ```python
  from typing import Optional
  from pydantic import BaseModel

  class OrganizationFollower(BaseModel):
      """Model representing a follower of an organization in Pipedrive"""
      
      user_id: int
      add_time: Optional[str] = None
  ```

  ### Client
  1. `organization_client.py` - API client with methods for all organization operations
  ```python
  import json
  from typing import Any, Dict, List, Optional, Tuple, Union

  from log_config import logger
  from pipedrive.api.base_client import BaseClient

  class OrganizationClient:
      """Client for Pipedrive Organization API endpoints"""
      
      def __init__(self, base_client: BaseClient):
          self.base_client = base_client
        
      async def create_organization(
          self,
          name: str,
          owner_id: Optional[int] = None,
          visible_to: Optional[int] = None,
          address: Optional[str] = None,
          # Implementation following the pattern from person_client.py
      ) -> Dict[str, Any]:
          """Create a new organization in Pipedrive"""
          # Implementation similar to create_person
      
      async def get_organization(
          self,
          organization_id: int,
          include_fields: Optional[List[str]] = None,
          custom_fields_keys: Optional[List[str]] = None,
      ) -> Dict[str, Any]:
          """Get organization details by ID"""
          # Implementation similar to get_person
      
      async def list_organizations(
          self,
          limit: int = 100,
          cursor: Optional[str] = None,
          filter_id: Optional[int] = None,
          # Other filtering parameters
      ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
          """List organizations with filtering and pagination"""
          # Implementation similar to list_persons
      
      async def search_organizations(
          self,
          term: str,
          fields: Optional[List[str]] = None,
          exact_match: bool = False,
          # Other search parameters
      ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
          """Search for organizations"""
          # Implementation similar to search_persons
      
      async def update_organization(
          self,
          organization_id: int,
          name: Optional[str] = None,
          owner_id: Optional[int] = None,
          # Other update parameters
      ) -> Dict[str, Any]:
          """Update an existing organization"""
          # Implementation similar to update_person
      
      async def delete_organization(
          self,
          organization_id: int
      ) -> Dict[str, Any]:
          """Delete an organization"""
          # Implementation similar to delete_person
          
      async def add_follower(
          self,
          organization_id: int,
          user_id: int
      ) -> Dict[str, Any]:
          """Add a follower to an organization"""
          # Implementation following API docs
          
      async def delete_follower(
          self,
          organization_id: int,
          follower_id: int
      ) -> Dict[str, Any]:
          """Delete a follower from an organization"""
          # Implementation following API docs
  ```

  ### Tools
  1. `organization_create_tool.py` - Tool to create a new organization
  ```python
  from typing import Optional
  
  from mcp.server.fastmcp import Context
  from pydantic import ValidationError
  
  from log_config import logger
  from pipedrive.api.features.organizations.models.organization import Organization
  from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
  from pipedrive.api.features.shared.utils import format_tool_response
  from pipedrive.api.pipedrive_api_error import PipedriveAPIError
  from pipedrive.api.pipedrive_context import PipedriveMCPContext
  from pipedrive.mcp_instance import mcp
  
  @mcp.tool()
  async def create_organization_in_pipedrive(
      ctx: Context,
      name: str,
      owner_id_str: Optional[str] = None,
      address: Optional[str] = None,
      visible_to_str: Optional[str] = None,
  ) -> str:
      """
      Creates a new organization entity within the Pipedrive CRM.
      
      This tool requires the organization's name and can optionally take details
      like owner ID, address, and visibility settings.
      
      args:
      ctx: Context
      name: str - The name of the organization
      
      owner_id_str: Optional[str] = None - The ID of the user who owns the organization
      
      address: Optional[str] = None - The address of the organization
      
      visible_to_str: Optional[str] = None - Visibility setting of the organization (1-4)
      """
      # Implementation following the pattern from person_create_tool.py
  ```

  2. `organization_get_tool.py` - Tool to get organization details
  ```python
  from typing import Optional
  
  from mcp.server.fastmcp import Context
  
  from log_config import logger
  from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
  from pipedrive.api.features.shared.utils import format_tool_response, safe_split_to_list
  from pipedrive.api.pipedrive_api_error import PipedriveAPIError
  from pipedrive.api.pipedrive_context import PipedriveMCPContext
  from pipedrive.mcp_instance import mcp
  
  @mcp.tool()
  async def get_organization_from_pipedrive(
      ctx: Context,
      id_str: str,
      include_fields_str: Optional[str] = None,
      custom_fields_str: Optional[str] = None,
  ) -> str:
      """
      Gets the details of a specific organization from Pipedrive CRM.
      
      This tool retrieves complete information about an organization by its ID, with
      options to include additional fields and custom fields in the response.
      
      args:
      ctx: Context
      id_str: str - The ID of the organization to retrieve
      
      include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
      
      custom_fields_str: Optional[str] = None - Comma-separated list of custom fields to include
      """
      # Implementation similar to person_get_tool.py
  ```

  3. Other tools following the same patterns as the Persons and Deals features

  ## Implementation Checkpoints

  ### 1. Organization Models
  - Implement `Organization` model with relevant fields (name, owner_id, address, etc.)
  - Implement `OrganizationFollower` model for managing followers
  - Add proper validation with Pydantic
  - Write tests for model validation

  ### 2. Organization Client
  - Implement `OrganizationClient` class with methods for CRUD operations
  - Add methods for follower management
  - Add proper error handling and logging
  - Write tests for client functionality

  ### 3. Basic Organization Tools
  - Implement `create_organization_in_pipedrive` tool
    - Required parameters: name
    - Optional parameters: owner_id_str, address, visible_to_str, etc.
    - Return created organization details

  - Implement `get_organization_from_pipedrive` tool
    - Required parameter: id_str
    - Optional parameters: include_fields_str, custom_fields_str
    - Return organization details

  - Implement `list_organizations_from_pipedrive` tool
    - Optional parameters: filter_id_str, owner_id_str, etc.
    - Return list of organizations

  - Implement `search_organizations_in_pipedrive` tool
    - Required parameter: term
    - Optional parameters: fields_str, exact_match, etc.
    - Return search results

  - Implement `update_organization_in_pipedrive` tool
    - Required parameters: id_str, at least one field to update
    - Optional parameters: name, owner_id_str, etc.
    - Return updated organization details

  - Implement `delete_organization_from_pipedrive` tool
    - Required parameter: id_str
    - Return success response

  ### 4. Organization Follower Tools
  - Implement `add_follower_to_organization_in_pipedrive` tool
    - Required parameters: id_str, user_id_str
    - Return follower details

  - Implement `delete_follower_from_organization_in_pipedrive` tool
    - Required parameters: id_str, follower_id_str
    - Return success response

  ### 5. Update Server & Testing
  - Update `server.py` to import and register all tools
  - Write comprehensive tests for all tools
  - Test integration with the Pipedrive API
  - Update pipedrive_client.py to expose the organization client

  ## Validation Gates
  - Each model must have proper Pydanticv2 validation
  - Each client method must handle API errors gracefully
  - Each tool must be validated by running the appropriate tests
  - All tools must handle error cases gracefully (e.g., invalid IDs, not found records)
  - Every tool must provide user-friendly error messages
  - Follow the existing patterns for error handling and response formatting
  - All tests must pass when running `uv run pytest`
  - Specific test commands:
    ```bash
    uv run pytest pipedrive/api/features/organizations/models/tests/
    uv run pytest pipedrive/api/features/organizations/client/tests/
    uv run pytest pipedrive/api/features/organizations/tools/tests/
    ```

  ## Implementation Notes
  - **MIRROR the pipedrive/api/features/persons directory structure and adapt it for organizations**
  - Maintain consistent parameter naming across tools (e.g., id_str for string IDs)
  - Use the shared conversion utilities for string-to-integer ID conversion
  - Follow the format_tool_response pattern for uniform response structure
  - Add proper documentation to each function and class
  - Update any relevant documentation to reflect the new tools
  - Use existing shared utilities and models before creating new ones
  - All string IDs from MCP should be converted to integers using the shared conversion utilities
  - Ensure proper handling of optional parameters
  - Follow existing patterns for error handling and response formatting
  - API tokens and authentication should be handled through the existing base client

  ## Testing Strategy
  - Unit tests for models
  - Unit tests for client methods with mocked API responses
  - Integration tests for tools with mocked client responses
  - Testing both successful and error scenarios
  - Testing edge cases (invalid IDs, missing required parameters, etc.)
  - MIRROR the test structure from the persons feature

  ## Other Considerations
  - Address handling may require special consideration for formatting and validation
  - Organization fields like visible_to have specific allowed values that must be validated
  - Organization visibility settings impact access control in Pipedrive
  - The follower functionality allows tracking users interested in specific organizations
  - Carefully handle organization search which can search across multiple field types
  - Pagination is important for listing organizations in larger Pipedrive instances
  - Custom fields support is critical for organizations with extended data models
  - Handle label_ids feature for categorization of organizations
  - See ai_docs/pipedrive_basics.md for more information on rate limiting and API best practices