# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

IMPORTANT: Before making changes, take time to understand the vertical slice architecture and existing patterns. When solving complex problems, use the phrase "think hard" to activate extended thinking mode for more thorough analysis.

IMPORTANT: NEVER add Claude attribution comment blocks like "Generated with Claude Code" or "Co-Authored-By: Claude" to commit messages or code files. These are unnecessary in this project and will be rejected.

## Project Overview

The mcp-concept project is a Model Control Protocol (MCP) server implementation for interacting with the Pipedrive CRM API. It provides a way for Claude to access and manipulate Pipedrive data through tool calls.

## Environment Setup

1. Create a `.env` file in the root directory with the following environment variables:
   ```
   PIPEDRIVE_API_TOKEN=your_api_token
   PIPEDRIVE_COMPANY_DOMAIN=your_company_domain
   HOST=0.0.0.0  # Optional, defaults to 0.0.0.0
   PORT=8152     # Optional, defaults to 8152
   TRANSPORT=sse  # or "stdio", defaults to "stdio"
   ```

## Dependencies

We always run script and the server with uv run.
`uv run <script>`

This project requires the following dependencies (defined in pyproject.toml):
- httpx >= 0.28.1 (for async HTTP requests)
- mcp[cli] >= 1.8.0 (for MCP server functionality)
- pydantic >= 2.11.4 (for data validation and serialization)
- pytest >= 8.3.5 (for testing)
- pytest-asyncio >= 0.26.0 (for async testing)
- python-dotenv >= 1.1.0 (for environment variable loading)

any additional dependencies should be added by running `uv add <dependency_name>`

## Commands

### Installation

To install the MCP server to Claude desktop:
```bash
cd mcp-concept
mcp install server.py
```

### Running

To run the server locally:
```bash
uv run server.py
```

### Testing

To run all tests:
```bash
uv run pytest
```

To run specific tests:
```bash
uv run pytest pipedrive/api/features/persons/tools/tests/test_person_create_tool.py -v
```

### Package Management

This project uses `uv` for package management:

```bash
uv pip install -e .  # Install package in development mode
```

## Project Structure

```
pipedrive/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── base_client.py                       (Core HTTP client functionality)
│   ├── pipedrive_api_error.py               (Custom error handling for API responses)
│   ├── pipedrive_client.py                  (Main client that delegates to feature-specific clients)
│   ├── pipedrive_context.py                 (Context manager for MCP integration)
│   ├── features/
│   │   ├── __init__.py
│   │   ├── persons/                         (Person feature module)
│   │   │   ├── __init__.py
│   │   │   ├── client/                      (Person-specific API client)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── person_client.py         (Client for person API endpoints)
│   │   │   │   └── tests/                   (Tests for person client)
│   │   │   ├── models/                      (Person data models)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── contact_info.py          (Email and Phone models)
│   │   │   │   ├── person.py                (Person model with validation)
│   │   │   │   └── tests/                   (Tests for person models)
│   │   │   └── tools/                       (Person MCP tools)
│   │   │       ├── __init__.py
│   │   │       ├── person_create_tool.py    (Tool for creating persons)
│   │   │       └── tests/                   (Tests for person tools)
│   │   └── shared/                          (Shared utilities across features)
│   │       ├── __init__.py
│   │       ├── conversion/                  (Type conversion utilities)
│   │       │   ├── __init__.py
│   │       │   ├── id_conversion.py         (String to integer ID conversion)
│   │       │   └── tests/                   (Tests for conversion utilities)
│   │       └── utils.py                     (Shared utility functions)
│   └── tests/                               (Tests for core API components)
└── mcp_instance.py                          (MCP server instance configuration)
```

## Project Architecture

### Core Components

1. **Base Client:** (`pipedrive/api/base_client.py`) Provides common HTTP request functionality used by all feature-specific clients.

2. **Pipedrive Client:** (`pipedrive/api/pipedrive_client.py`) Main client that delegates to resource-specific clients like the Person client.

3. **Feature-specific Clients:** (e.g., `pipedrive/api/features/persons/client/person_client.py`) Handle API requests for specific resource types.

4. **Data Models:** (e.g., `pipedrive/api/features/persons/models/`) Pydantic models that represent Pipedrive person entities with validation.

5. **MCP Tools:** (e.g., `pipedrive/api/features/persons/tools/`) Person MCP tools that Claude can call through the MCP protocol.

6. **Shared Utilities:** (`pipedrive/api/features/shared/`) Common utilities used across different features:
   - `utils.py`: Contains `format_tool_response()` for standardized JSON responses
   - `conversion/id_conversion.py`: Contains `convert_id_string()` for string-to-integer conversion

7. **Pipedrive Context:** (`pipedrive/api/pipedrive_context.py`) Manages the lifecycle of the Pipedrive client.

### Data Flow

1. Claude calls an MCP tool function
2. The tool function accesses the Pipedrive client via context
3. The client delegates to the appropriate feature-specific client
4. The feature client makes an API request to Pipedrive
5. Results are processed and returned to Claude in a standardized format

### Key Features

- **Vertical Slice Architecture:** Code is organized by feature rather than by technical layer
- **Asynchronous API Client:** Uses `httpx` for async HTTP requests
- **Type Safety:** Uses Pydantic models for data validation
- **Testability:** Co-located tests with the code they test

## Workflows

### Explore, Plan, Code, Commit

Follow this workflow for complex tasks:

1. **Explore**: Use `Glob`, `Grep`, and `Read` to understand the codebase before making changes
2. **Plan**: Outline your approach and consider potential issues
3. **Code**: Implement your solution following established patterns
4. **Test**: Verify your changes work as expected
5. **Commit**: Create descriptive commit messages

### Test-Driven Development

For new features or bug fixes:

1. Write tests first
2. Verify tests fail
3. Implement code to make tests pass
4. Refactor while keeping tests passing

## Adding New Features

When creating new features (e.g., for deals, organizations):

1. **Use the custom command**: Run `/project:new-feature feature_name` to get started

2. **Create Feature Structure:**
   ```
   pipedrive/api/features/new_feature/
   ├── __init__.py
   ├── client/
   │   ├── __init__.py
   │   ├── new_feature_client.py
   │   └── tests/
   ├── models/
   │   ├── __init__.py
   │   ├── new_feature_model.py
   │   └── tests/
   └── tools/
       ├── __init__.py
       ├── new_feature_tool.py
       └── tests/
   ```

3. **Add Client to Main Client:**
   Update `pipedrive/api/pipedrive_client.py` to initialize and expose the new feature client.

4. **Create Tools:**
   Define new MCP tools in the feature's tools directory.

5. **Register Tools:**
   Import the tools in `server.py` to register them with the MCP server.

6. **Follow Templates:**
   Use the templates in `.claude/guides/templates.md` for consistent implementation.

## Shared Utilities

To avoid duplication, always use the existing shared utilities:

1. **Response Formatting:**
   ```python
   from pipedrive.api.features.shared.utils import format_tool_response
   
   # Use for consistent JSON response formatting
   return format_tool_response(success=True, data=result)
   ```

2. **ID Conversion:**
   ```python
   from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
   
   # Use for converting string IDs to integers with error handling
   id_value, error = convert_id_string(id_str, "field_name")
   if error:
       return format_tool_response(False, error_message=error)
   ```

## Testing

Tests are co-located with the code they test. When adding new functionality:

1. Create unit tests for models, clients, and utilities
2. Create integration tests for tools
3. Run tests with `uv run pytest`

### Fixing Tests

If you encounter test failures:

1. Use `/project:fix-test path/to/test_file.py` to get assistance
2. Ensure all async tests have `@pytest.mark.asyncio` decorator
3. Check for mocking issues with AsyncMock objects
4. Verify all coroutines are properly awaited

## Documentation and Resources

- **Templates**: See `.claude/guides/templates.md` for code templates
- **Edge Cases**: See `.claude/guides/edge-cases.md` for Pipedrive API quirks
- **Development Guide**: See `.claude/guides/dev-guide.md` for architecture details

## Using Subagents for Research

When tackling complex problems, use subagents to explore different aspects of the codebase simultaneously:

```python
# Example of using a subagent
subagent_result = await Task(
    description="Explore person models",
    prompt="Analyze the current person models structure and provide a summary of key fields and validation rules."
)
```

This allows you to gather information without consuming your main context window.