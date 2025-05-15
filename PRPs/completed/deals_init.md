name: "Deal API MCP Tools"
description: |

  ## Goal
  Implement a complete set of MCP tools for managing deals in Pipedrive. This project will create tools for:
  1. Getting all deals (with filtering options)
  2. Getting deal details
  3. Searching for deals
  4. Creating a deal
  5. Updating a deal
  6. Deleting a deal
  7. Managing deal products (update, delete)

  ## Why
  - Provide a complete CRUD interface for Deal entity management through MCP
  - Allow Claude to perform all standard operations on Pipedrive deals without needing additional development
  - Continue the pattern established with Person entity implementation
  - Enable advanced CRM operations like product management within deals

  ## Endpoints to Implement
  
  **Get All Deals**
  - GET /api/v2/deals
  - Returns all deals with optional filtering and pagination
  
  **Get Deal Details**
  - GET /api/v2/deals/{id}
  - Returns the details of a specific deal with optional fields
  
  **Search Deals**
  - GET /api/v2/deals/search
  - Searches all deals by title, notes, and/or custom fields
  
  **Create Deal**
  - POST /api/v2/deals
  - Creates a new deal with the provided details
  
  **Update Deal**
  - PATCH /api/v2/deals/{id}
  - Updates the properties of a deal
  
  **Delete Deal**
  - DELETE /api/v2/deals/{id}
  - Marks a deal as deleted
  
  ~~**Add Product to Deal**~~
  ~~- POST /api/v2/deals/{id}/products~~
  ~~- Adds a product to a deal, creating a new deal-product~~
  (This endpoint has been removed)
  
  **Update Deal Product**
  - PATCH /api/v2/deals/{id}/products/{product_attachment_id}
  - Updates the details of a product attached to a deal
  
  **Delete Deal Product**
  - DELETE /api/v2/deals/{id}/products/{product_attachment_id}
  - Deletes a product attachment from a deal

  ## Proposed Directory Structure
  ```
  ├── pipedrive
  │   ├── api
  │   │   ├── features
  │   │   │   ├── deals
  │   │   │   │   ├── __init__.py
  │   │   │   │   ├── client
  │   │   │   │   │   ├── __init__.py
  │   │   │   │   │   ├── deal_client.py
  │   │   │   │   │   └── tests
  │   │   │   │   │       ├── __init__.py
  │   │   │   │   │       └── test_deal_client.py
  │   │   │   │   ├── models
  │   │   │   │   │   ├── __init__.py
  │   │   │   │   │   ├── deal.py
  │   │   │   │   │   ├── deal_product.py
  │   │   │   │   │   └── tests
  │   │   │   │   │       ├── __init__.py
  │   │   │   │   │       ├── test_deal.py
  │   │   │   │   │       └── test_deal_product.py
  │   │   │   │   └── tools
  │   │   │   │       ├── __init__.py
  │   │   │   │       ├── deal_create_tool.py
  │   │   │   │       ├── deal_get_tool.py
  │   │   │   │       ├── deal_list_tool.py
  │   │   │   │       ├── deal_search_tool.py
  │   │   │   │       ├── deal_update_tool.py
  │   │   │   │       ├── deal_delete_tool.py
  │   │   │   │       ├── deal_product_update_tool.py
  │   │   │   │       ├── deal_product_delete_tool.py
  │   │   │   │       └── tests
  │   │   │   │           ├── __init__.py
  │   │   │   │           ├── test_deal_create_tool.py
  │   │   │   │           ├── test_deal_get_tool.py
  │   │   │   │           ├── test_deal_list_tool.py
  │   │   │   │           ├── test_deal_search_tool.py
  │   │   │   │           ├── test_deal_update_tool.py
  │   │   │   │           ├── test_deal_delete_tool.py
  │   │   │   │           ├── test_deal_product_update_tool.py
  │   │   │   │           └── test_deal_product_delete_tool.py
  ```

  ## Files to Reference
  - ai_docs/pipedrive_deals.md (detailed API reference for Deals endpoints)
  - pipedrive/api/features/persons/ (directory to MIRROR for deals implementation)
  - pipedrive/api/features/persons/client/person_client.py (reference for client implementation)
  - pipedrive/api/features/persons/models/person.py (reference for model implementation)
  - pipedrive/api/features/persons/tools/person_*_tool.py (reference for tool implementations)
  - pipedrive/api/features/shared/conversion/id_conversion.py (for ID validation)
  - pipedrive/api/features/shared/utils.py (for response formatting)

  ## Files to Implement
  
  ### Models
  1. `deal.py` - Pydantic model representing a deal
  2. `deal_product.py` - Pydantic model for deal products

  ### Client
  1. `deal_client.py` - API client with methods for all deal operations and deal product management

  ### Tools
  1. `deal_create_tool.py` - Create a new deal
  2. `deal_get_tool.py` - Get deal details
  3. `deal_list_tool.py` - List/get all deals with filtering
  4. `deal_search_tool.py` - Search for deals
  5. `deal_update_tool.py` - Update a deal
  6. `deal_delete_tool.py` - Delete a deal
  7. `deal_product_add_tool.py` - Add a product to a deal
  8. `deal_product_update_tool.py` - Update a product in a deal
  9. `deal_product_delete_tool.py` - Remove a product from a deal

  ## Implementation Checkpoints

  ### 1. Deal Models
  - Implement `Deal` model with relevant fields (title, value, currency, status, etc.)
  - Implement `DealProduct` model for products attached to deals (quantity, price, etc.)
  - Add proper validation with Pydantic
  - Write tests for model validation

  ### 2. Deal Client
  - Implement `DealClient` class with methods for CRUD operations on deals
  - Add methods for product management within deals
  - Add proper error handling and logging
  - Write tests for client functionality

  ### 3. Basic Deal Tools
  - Implement `create_deal_in_pipedrive` tool
    - Required parameters: title
    - Optional parameters: value, currency, person_id_str, org_id_str, etc.
    - Return created deal details

  - Implement `get_deal_from_pipedrive` tool
    - Required parameter: id_str
    - Optional parameters: include_fields_str
    - Return deal details

  - Implement `list_deals_from_pipedrive` tool
    - Optional parameters: filter_id_str, owner_id_str, etc.
    - Return list of deals

  - Implement `search_deals_in_pipedrive` tool
    - Required parameter: term
    - Optional parameters: fields_str, exact_match, etc.
    - Return search results

  - Implement `update_deal_in_pipedrive` tool
    - Required parameters: id_str, at least one field to update
    - Optional parameters: title, value, currency, etc.
    - Return updated deal details

  - Implement `delete_deal_from_pipedrive` tool
    - Required parameter: id_str
    - Return success response

  ### 4. Deal Product Tools

  - Implement `update_product_in_deal_in_pipedrive` tool
    - Required parameters: id_str, product_attachment_id_str
    - Optional parameters: item_price, quantity, etc.
    - Return updated product attachment details

  - Implement `delete_product_from_deal_in_pipedrive` tool
    - Required parameters: id_str, product_attachment_id_str
    - Return success response

  ### 5. Update Server & Testing
  - Update `server.py` to import and register all tools
  - Write comprehensive tests for all tools
  - Test integration with the Pipedrive API

  ## Validation Gates
  - Each model must have proper Pydanticv2 validation
  - Each client method must handle API errors gracefully
  - Each tool must be validated by running the appropriate tests
  - All tools must handle error cases gracefully (e.g., invalid IDs, not found records)
  - Every tool must provide user-friendly error messages
  - Follow the existing patterns for error handling and response formatting
  - All tests must pass when running `uv run pytest`

  ## Implementation Notes
  - **MIRROR the pipedrive/api/features/persons directory structure and adapt it for deals**
  - Thoroughly read and ingest the ai_docs/pipedrive_deals.md document for API reference
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
  - Payload construction should sanitize inputs by removing None values
  - HTTP request error handling should provide meaningful error messages
  - Proper logging should be implemented throughout
  - Ensure compatibility with API v2 endpoints
  - Maintain backward compatibility with the existing API client architecture