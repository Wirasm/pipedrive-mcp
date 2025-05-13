name: "Item Search API MCP Tools"
description: |

  ## Goal
  Implement a generalized item search MCP tool for Pipedrive that allows searching across multiple entity types simultaneously. This will enable more powerful and flexible search capabilities compared to the entity-specific search tools already implemented.

  ## Why
  - Enable mcp clients to search across multiple entity types (deals, persons, organizations, products, etc.) in a single operation
  - Provide a more efficient way to find information when the entity type is unknown
  - Complement the existing entity-specific search tools with a more versatile search capability
  - Follow Pipedrive's API design which offers both entity-specific and general search endpoints

  ## What
  The item search feature will implement MCP tools that leverage Pipedrive's itemSearch endpoints:
  1. A general multi-entity search tool (`search_items_in_pipedrive`)
  2. A field-specific search tool (`search_item_field_in_pipedrive`)

  These tools will allow mcp clients to search across multiple Pipedrive entity types and retrieve results in a standardized format.

  ## Endpoints to Implement
  
  **Search Across Multiple Item Types**
  - GET /api/v2/itemSearch
  - Searches across specified entity types (deals, persons, organizations, products, etc.)
  - Supports searching by field, exact matching, and pagination
  
  **Search Using a Specific Field**
  - GET /api/v2/itemSearch/field
  - Performs field-specific searches with different matching options
  - Useful for searching specific field values (like autocomplete suggestions)

  ## Current Directory Structure
  ```
  ├── pipedrive
  │   ├── api
  │   │   ├── features
  │   │   │   ├── deals
  │   │   │   │   ├── client
  │   │   │   │   │   ├── deal_client.py          (has search_deals method)
  │   │   │   │   ├── tools
  │   │   │   │   │   ├── deal_search_tool.py     (has search_deals_in_pipedrive tool)
  │   │   │   ├── persons
  │   │   │   │   ├── client
  │   │   │   │   │   ├── person_client.py        (has search_persons method)
  │   │   │   │   ├── tools
  │   │   │   │   │   ├── person_search_tool.py   (has search_persons_in_pipedrive tool)
  │   │   │   ├── shared
  │   │   │       ├── conversion
  │   │   │       │   ├── id_conversion.py        (for ID validation)
  │   │   │       ├── utils.py                    (for response formatting)
  │   │   ├── base_client.py                     (Base HTTP client)
  │   │   ├── pipedrive_client.py                (Main client delegating to feature clients)
  │   │   ├── pipedrive_context.py               (Context for MCP integration)
  ```

  ## Proposed Directory Structure
  ```
  ├── pipedrive
  │   ├── api
  │   │   ├── features
  │   │   │   ├── deals/                         (existing feature)
  │   │   │   ├── persons/                       (existing feature)
  │   │   │   ├── item_search/                   (new feature)
  │   │   │   │   ├── __init__.py
  │   │   │   │   ├── client
  │   │   │   │   │   ├── __init__.py
  │   │   │   │   │   ├── item_search_client.py
  │   │   │   │   │   └── tests
  │   │   │   │   │       ├── __init__.py
  │   │   │   │   │       └── test_item_search_client.py
  │   │   │   │   ├── models
  │   │   │   │   │   ├── __init__.py
  │   │   │   │   │   ├── search_result.py
  │   │   │   │   │   └── tests
  │   │   │   │   │       ├── __init__.py
  │   │   │   │   │       └── test_search_result.py
  │   │   │   │   └── tools
  │   │   │   │       ├── __init__.py
  │   │   │   │       ├── item_search_tool.py
  │   │   │   │       ├── item_field_search_tool.py
  │   │   │   │       └── tests
  │   │   │   │           ├── __init__.py
  │   │   │   │           ├── test_item_search_tool.py
  │   │   │   │           └── test_item_field_search_tool.py
  │   │   │   └── shared/                        (existing shared utilities)
  ```

  ## Files to Reference
  - [pipedrive/api/features/persons/client/person_client.py](read_only) (reference for client implementation patterns)
    - Contains `search_persons` method which can be used as a template for `search_items` method
  - [pipedrive/api/features/persons/tools/person_search_tool.py](read_only) (reference for tool implementation patterns)
    - Contains `search_persons_in_pipedrive` tool which can be used as a template for `search_items_in_pipedrive` tool
  - [pipedrive/api/features/deals/client/deal_client.py](read_only) (reference for client implementation patterns)
    - Contains `search_deals` method which can be used as a template for `search_items` method
  - [pipedrive/api/features/deals/tools/deal_search_tool.py](read_only) (reference for tool implementation patterns)
    - Contains `search_deals_in_pipedrive` tool which can be used as a template for `search_items_in_pipedrive` tool
  - [pipedrive/api/features/shared/conversion/id_conversion.py](read_only) (for ID validation)
    - Contains `convert_id_string` utility for string-to-integer conversion
  - [pipedrive/api/features/shared/utils.py](read_only) (for response formatting)
    - Contains `format_tool_response` utility for standardized JSON responses
  - [pipedrive/api/pipedrive_client.py](read_only) (for integrating the new client)
    - Need to update this file to expose the new item search client
  - [server.py](read_only) (for registering the new tools)
    - Need to update this file to import and register the new item search tools
  - [ai_docs/pipedrive_item_search.md](read_only) (for API reference)
    - Contains the Pipedrive API documentation for item search endpoints

  ## Files to Implement (concept)
  
  ### Client
  
  1. `item_search_client.py`
  ```python
  # Client for item search operations
  from typing import Any, Dict, List, Optional, Tuple
  
  from pipedrive.api.base_client import BaseClient
  
  class ItemSearchClient:
      """Client for Pipedrive itemSearch API endpoints"""
      
      def __init__(self, base_client: BaseClient):
          self.base_client = base_client
      
      async def search_items(
          self,
          term: str,
          item_types: Optional[List[str]] = None,
          fields: Optional[List[str]] = None,
          search_for_related_items: bool = False,
          exact_match: bool = False,
          include_fields: Optional[List[str]] = None,
          limit: int = 100,
          cursor: Optional[str] = None,
      ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
          """Search for items across multiple types in Pipedrive"""
          # Implementation...
      
      async def search_field(
          self,
          term: str,
          entity_type: str,
          field: str,
          match: str = "exact",
          limit: int = 100,
          cursor: Optional[str] = None,
      ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
          """Search for items using a specific field"""
          # Implementation...
  ```
  
  ### Models
  
  2. `search_result.py`
  ```python
  # Pydantic models for search results
  from typing import Dict, List, Optional, Union
  from pydantic import BaseModel, Field
  
  class SearchResult(BaseModel):
      """Model representing an item search result"""
      
      id: int
      type: str
      result_score: float
      # Common fields across all item types
      name: Optional[str] = None
      title: Optional[str] = None
      
      # Additional type-specific fields
      # ...
  ```

  ### Tools
  
  3. `item_search_tool.py`
  ```python
  # MCP tool for general item search
  from typing import Optional
  
  from mcp.contrib.anthropic import Context
  
  from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
  from pipedrive.api.features.shared.utils import format_tool_response
  from pipedrive.api.pipedrive_context import get_pipedrive_client
  from pipedrive.mcp_instance import mcp
  
  @mcp.tool()
  async def search_items_in_pipedrive(
      ctx: Context,
      term: str,
      item_types_str: Optional[str] = None,
      fields_str: Optional[str] = None,
      search_for_related_items: bool = False,
      exact_match: bool = False,
      include_fields_str: Optional[str] = None,
      limit_str: Optional[str] = "100",
      cursor: Optional[str] = None,
  ) -> str:
      """
      Searches for items across multiple types in Pipedrive CRM.
      
      This tool searches across specified item types using the provided term.
      
      args:
      ctx: Context
      term: str - The search term to look for (min 2 chars, or 1 if exact_match=True)
      
      item_types_str: Optional[str] = None - Comma-separated list of item types to search (deal, person, organization, product, lead, file, mail_attachment)
      
      fields_str: Optional[str] = None - Comma-separated list of fields to search in (depends on item types)
      
      search_for_related_items: bool = False - When True, includes related items in the results
      
      exact_match: bool = False - When True, only exact matches are returned
      
      include_fields_str: Optional[str] = None - Comma-separated list of additional fields to include
      
      limit_str: Optional[str] = "100" - Maximum number of results to return (max 500)
      
      cursor: Optional[str] = None - Pagination cursor for the next page
      """
      # Implementation...
  ```
  
  4. `item_field_search_tool.py`
  ```python
  # MCP tool for field-specific search
  from typing import Optional
  
  from mcp.contrib.anthropic import Context
  
  from pipedrive.api.features.shared.utils import format_tool_response
  from pipedrive.api.pipedrive_context import get_pipedrive_client
  from pipedrive.mcp_instance import mcp
  
  @mcp.tool()
  async def search_item_field_in_pipedrive(
      ctx: Context,
      term: str,
      entity_type: str,
      field: str,
      match: str = "exact",
      limit_str: Optional[str] = "100",
      cursor: Optional[str] = None,
  ) -> str:
      """
      Searches for values of a specific field in Pipedrive.
      
      This tool is useful for finding autocomplete values for specific fields.
      
      args:
      ctx: Context
      term: str - The search term to look for (min 2 chars, or 1 if match is not 'exact')
      
      entity_type: str - The type of entity to search (deal, person, organization, product, lead, project)
      
      field: str - The field key to search in
      
      match: str = "exact" - Type of match: exact, beginning, or middle
      
      limit_str: Optional[str] = "100" - Maximum number of results to return (max 500)
      
      cursor: Optional[str] = None - Pagination cursor for the next page
      """
      # Implementation...
  ```

  ## Implementation Notes
  
  ### Client Implementation
  
  1. **Item Search Client:**
     - Create a new `ItemSearchClient` class in `item_search_client.py`
     - Implement methods for searching items and searching fields
     - Follow the same patterns used in `PersonClient` and `DealClient`
     - Make proper use of the base client for API requests
     - Handle response processing, especially pagination
     - Process the `result_score` field that appears in search results

  2. **Add to the Main Client:**
     - In `pipedrive_client.py`, initialize and expose the new item search client
     - Add convenience methods forwarding to the item search client
     - Ensure proper initialization during PipedriveClient creation

  ### Models Implementation
  
  1. **Search Result Model:**
     - Create a `SearchResult` model in `search_result.py`
     - Include common fields that appear across all search result types
     - Use optional fields for type-specific properties
     - Implement proper field validation with Pydantic
     - Add factory methods for creating from API responses

  ### Tools Implementation
  
  1. **Item Search Tool:**
     - Implement `search_items_in_pipedrive` in `item_search_tool.py`
     - Process comma-separated string parameters properly
     - Validate input parameters (term length, valid option values)
     - Handle numeric limit conversion
     - Format the response using `format_tool_response`
     - Include counts by item type in the response
     - Provide pagination support

  2. **Item Field Search Tool:**
     - Implement `search_item_field_in_pipedrive` in `item_field_search_tool.py`
     - Validate the entity_type parameter against allowed values
     - Validate the match parameter against allowed values
     - Handle numeric limit conversion
     - Format the response using `format_tool_response`

  3. **Register Tools:**
     - Update `server.py` to import and register the new tools
     - Follow the existing pattern for tool imports and declarations

  ### Quirks and Edge Cases
  
  1. **Result Typing:**
     - Search results contain different fields depending on the item type
     - Consider using a discriminated union type or type adapters
     - Include type information clearly in the response

  2. **Related Items:**
     - When `search_for_related_items` is enabled, results include related items
     - Need to handle the nested structure of related items in responses

  3. **Field Validation:**
     - Different item types support different fields to search in
     - Validate that the provided fields are applicable to the requested item types

  4. **Term Length:**
     - Search term must be at least 2 characters (or 1 if exact_match=True)
     - Properly validate and return friendly error messages

  ## Validation Gates
  - Each method must have unit tests with mocked responses
  - Tests should cover both success and error scenarios
  - Tests should verify pagination handling
  - Tests should verify parameter formatting and validation
  - Client and tool error handling should be tested
  - Response formatting should be verified
  - All tests must pass when running `uv run pytest`
  - Specific test command: `uv run pytest pipedrive/api/features/item_search/`

  ## Implementation Checkpoints/Testing
  
  1. **ItemSearchClient Implementation:**
     - Implement `search_items` method
     - Implement `search_field` method
     - Test URL construction, parameter handling, and response processing
     - Test pagination handling
     - Command: `uv run pytest pipedrive/api/features/item_search/client/tests/test_item_search_client.py -v`

  2. **SearchResult Model:**
     - Implement model with validation
     - Test model creation from various API response formats
     - Command: `uv run pytest pipedrive/api/features/item_search/models/tests/test_search_result.py -v`

  3. **Item Search Tool:**
     - Implement `search_items_in_pipedrive` tool
     - Test parameter validation, especially:
       - term length
       - item_types_str validation
       - fields_str validation
       - limit_str conversion
     - Test error handling and response formatting
     - Command: `uv run pytest pipedrive/api/features/item_search/tools/tests/test_item_search_tool.py -v`

  4. **Item Field Search Tool:**
     - Implement `search_item_field_in_pipedrive` tool
     - Test parameter validation, especially:
       - term length
       - entity_type validation
       - match validation
       - limit_str conversion
     - Test error handling and response formatting
     - Command: `uv run pytest pipedrive/api/features/item_search/tools/tests/test_item_field_search_tool.py -v`

  5. **Integration Testing:**
     - Verify all tools are registered correctly
     - Verify the tools can be called through MCP
     - Test with real API responses (mocked at the HTTP client level)
     - Command: `uv run pytest pipedrive/api/features/item_search/tools/tests/`

  ## Other Considerations

  1. **Documentation Format:**
     - Ensure consistent docstring formatting in tool implementations
     - Separate parameter descriptions with newlines for better readability
     - Follow the format shown in the MCP example in ai_docs/mcp_example.md

  2. **Performance:**
     - Item search can potentially return large result sets see ai_docs/pipedrive_basics.md for more information
     - Use pagination properly to manage result size
     - Consider caching frequently searched terms

  2. **Error Handling:**
     - Handle API rate limiting
     - Provide clear error messages for validation failures
     - Log unexpected errors with sufficient context for debugging

  3. **Extensibility:**
     - Design the search models to accommodate future item types
     - Make parameter handling flexible enough to support API changes

  4. **Documentation:**
     - Add clear docstrings to all public methods
     - Document the expected input/output formats for MCP tools
     - Include examples of usage in the docstrings