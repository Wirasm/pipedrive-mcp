name: "Person API MCP Tools"
description: |

  ## Goal
  Implement a complete set of MCP tools for managing persons in Pipedrive. The project already has the create_person_in_pipedrive tool, and we need to add tools for:
  1. Getting person details
  2. Updating a person 
  3. Deleting a person
  4. Searching for persons

  ## Why
  - Provide a complete CRUD interface for Person entity management through MCP
  - Allow Claude to perform all standard operations on Pipedrive persons without needing additional development
  - Create a foundation pattern for implementing other Pipedrive entities (deals, organizations, etc.)

  ## Endpoints to Implement
  
  **Get Person Details**
  - GET /api/v2/persons/{id}
  - Returns the details of a specific person with optional fields
  
  **Update Person**
  - PATCH /api/v2/persons/{id}
  - Updates the properties of a person
  
  **Delete Person**
  - DELETE /api/v2/persons/{id}
  - Marks a person as deleted
  
  **Search Persons**
  - GET /api/v2/persons/search
  - Searches all persons by name, email, phone, notes, and custom fields

  ## Current Directory Structure
  ```
├── ai_docs
│   ├── example_server_readme.md
│   ├── full_mcp.txt
│   ├── mcp_example.md
│   ├── pipedrive_api_architecture.md
│   ├── pipedrive_basics.md
│   ├── pipedrive_item_search.md
│   ├── pipedrive_persons.md
│   └── pipedrive_v2_migrate.md
├── CLAUDE.md
├── log_config.py
├── pipedrive
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── base_client.py
│   │   ├── features
│   │   │   ├── __init__.py
│   │   │   ├── persons
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── person_client.py
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   ├── models
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── contact_info.py
│   │   │   │   │   ├── person.py
│   │   │   │   │   └── tests
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       └── test_person.py
│   │   │   │   └── tools
│   │   │   │       ├── __init__.py
│   │   │   │       ├── person_create_tool.py
│   │   │   │       └── tests
│   │   │   │           ├── __init__.py
│   │   │   │           └── test_person_create_tool.py
│   │   │   └── shared
│   │   │       ├── __init__.py
│   │   │       ├── conversion
│   │   │       │   ├── __init__.py
│   │   │       │   ├── id_conversion.py
│   │   │       │   └── tests
│   │   │       │       ├── __init__.py
│   │   │       │       └── test_id_conversion.py
│   │   │       └── utils.py
│   │   ├── pipedrive_api_error.py
│   │   ├── pipedrive_client.py
│   │   ├── pipedrive_context.py
│   │   └── tests
│   │       ├── __init__.py
│   │       ├── test_base_client.py
│   │       └── test_pipedrive_client.py
│   ├── conftest.py
│   └── mcp_instance.py
├── PRPs
│   ├── persons_init.md
│   └── test.yaml
├── pyproject.toml
├── pytest.ini
├── README.md
├── report.md
├── server.py
├── simple_claude_run.py
└── uv.lock
  ```

  ## Files to Reference
  - pipedrive/api/features/persons/client/person_client.py (has methods for get, update, delete, search)
  - pipedrive/api/features/persons/tools/person_create_tool.py (reference for tool implementation)
  - pipedrive/api/features/shared/conversion/id_conversion.py (for ID validation)
  - pipedrive/api/features/shared/utils.py (for response formatting)
  - ai_docs/pipedrive_basics.md (for more information about the Pipedrive API)
  - ai_docs/pipedrive_persons.md (for more information about the Pipedrive persons API)

  ## Editable Context
  - Create new files in pipedrive/api/features/persons/tools/:
    - person_get_tool.py
    - person_update_tool.py
    - person_delete_tool.py
    - person_search_tool.py
  - Update server.py to register the new tools

  ## Implementation Checklist
  1. Implement get_person_from_pipedrive tool
     - Required parameter: id_str
     - Optional parameters: include_fields_str (comma-separated list)
     - Return formatted person details

  2. Implement update_person_in_pipedrive tool
     - Required parameters: id_str, at least one field to update
     - Optional parameters: name, owner_id_str, org_id_str, email_address, etc.
     - Return updated person details

  3. Implement delete_person_from_pipedrive tool
     - Required parameter: id_str
     - Return success response

  4. Implement search_persons_in_pipedrive tool
     - Required parameter: term
     - Optional parameters: exact_match, fields_str, org_id_str
     - Return formatted search results

  5. Update server.py to import and register all tools

  6. Create tests for all new tools in pipedrive/api/features/persons/tools/tests/

  7. Ensure that you import existing shared utilities and models create new ones ONLY if you are absolutley sure that you need to
     - Use the existing shared utilities for string-to-integer ID conversion
     - Use the existing shared utilities for response formatting
     - Use the existing shared utilities for error handling
     - Use the existing shared utilities for logging

  ## Validation Gates
  - Each tool must be validated by running the appropriate tests
  - All tools must handle error cases gracefully (e.g., invalid IDs, not found records)
  - Every tool must provide user-friendly error messages
  - Follow the existing patterns for error handling and response formatting
  - run `uv run pytest` tests must pass

  ## Notes
  - Maintain consistent parameter naming across tools (e.g., id_str for string IDs)
  - Use the shared conversion utilities for string-to-integer ID conversion
  - Follow the format_tool_response pattern for uniform response structure
  - Add proper documentation to each tool function
  - Update any relevant documentation to reflect the new tools