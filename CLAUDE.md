# CLAUDE.md

KISS (Keep It Simple, Stupid): Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. Simple solutions are easier to understand, maintain, and debug.

YAGNI (You Aren't Gonna Need It): Avoid building functionality on speculation. Implement features only when they are needed, not when you anticipate they might be useful in the future.

Dependency Inversion: High-level modules should not depend on low-level modules. Both should depend on abstractions. This principle enables flexibility and testability.

Open/Closed Principle: Software entities should be open for extension but closed for modification. Design your systems so that new functionality can be added with minimal changes to existing code.

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
   
   # Feature flags (optional)
   PIPEDRIVE_FEATURE_PERSONS=true
   PIPEDRIVE_FEATURE_DEALS=true
   PIPEDRIVE_FEATURE_ORGANIZATIONS=true
   PIPEDRIVE_FEATURE_LEADS=true
   PIPEDRIVE_FEATURE_ITEM_SEARCH=true
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
│   │   ├── __init__.py                      (Feature discovery mechanism)
│   │   ├── tool_registry.py                 (Feature registry system)
│   │   ├── tool_decorator.py                (Feature-aware tool decorator)
│   │   ├── persons/                         (Person feature module)
│   │   │   ├── __init__.py
│   │   │   ├── persons_tool_registry.py     (Person feature registry)
│   │   │   ├── client/                      (Person-specific API client)
│   │   │   ├── models/                      (Person data models)
│   │   │   └── tools/                       (Person MCP tools)
│   │   ├── organizations/                   (Organization feature module)
│   │   ├── deals/                           (Deal feature module)
│   │   ├── leads/                           (Leads feature module)
│   │   ├── item_search/                     (Item search feature module)
│   │   └── shared/                          (Shared utilities across features)
│   └── tests/                               (Tests for core API components)
├── mcp_instance.py                          (MCP server instance configuration)
└── feature_config.py                        (Feature configuration management)
```

## Project Architecture

### Core Components

1. **Base Client:** (`pipedrive/api/base_client.py`) Provides common HTTP request functionality used by all feature-specific clients.

2. **Pipedrive Client:** (`pipedrive/api/pipedrive_client.py`) Main client that delegates to resource-specific clients like the Person client.

3. **Feature-specific Clients:** (e.g., `pipedrive/api/features/persons/client/person_client.py`) Handle API requests for specific resource types.

4. **Data Models:** (e.g., `pipedrive/api/features/persons/models/`) Pydantic models that represent Pipedrive entities with validation.

5. **MCP Tools:** (e.g., `pipedrive/api/features/persons/tools/`) MCP tools that Claude can call through the MCP protocol.

6. **Feature Registry:** (`pipedrive/api/features/tool_registry.py`) System for registering and managing features and their tools.

7. **Feature Configuration:** (`pipedrive/feature_config.py`) System for enabling/disabling features at runtime.

8. **Tool Decorator:** (`pipedrive/api/features/tool_decorator.py`) Feature-aware decorator for MCP tools.

9. **Shared Utilities:** (`pipedrive/api/features/shared/`) Common utilities used across different features:
   - `utils.py`: Contains `format_tool_response()` for standardized JSON responses
   - `conversion/id_conversion.py`: Contains `convert_id_string()` for string-to-integer conversion

10. **Pipedrive Context:** (`pipedrive/api/pipedrive_context.py`) Manages the lifecycle of the Pipedrive client.

### Data Flow

1. Claude calls an MCP tool function
2. The tool decorator checks if the feature is enabled
3. The tool function accesses the Pipedrive client via context
4. The client delegates to the appropriate feature-specific client
5. The feature client makes an API request to Pipedrive
6. Results are processed and returned to Claude in a standardized format

### Key Features

- **Vertical Slice Architecture:** Code is organized by feature rather than by technical layer
- **Feature Registry:** Modular, configurable system for registering MCP tools
- **Feature Flags:** Runtime enabling/disabling of features
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
   ├── new_feature_tool_registry.py
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

3. **Register the Feature:**
   Create a feature registry file (`new_feature_tool_registry.py`):
   ```python
   from pipedrive.api.features.tool_registry import registry, FeatureMetadata
   
   # Register the feature
   registry.register_feature(
       "new_feature",
       FeatureMetadata(
           name="New Feature",
           description="Description of the new feature",
           version="1.0.0",
       )
   )
   
   # Import and register tools
   from .tools.new_feature_tool import new_feature_tool
   registry.register_tool("new_feature", new_feature_tool)
   ```

4. **Add Client to Main Client:**
   Update `pipedrive/api/pipedrive_client.py` to initialize and expose the new feature client.

5. **Create Tools:**
   Define new MCP tools in the feature's tools directory using the feature-aware decorator:
   ```python
   from pipedrive.api.features.tool_decorator import tool
   
   @tool("new_feature")
   async def new_feature_tool(ctx, param1, param2):
       """Documentation for the tool"""
       # Tool implementation
   ```

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

## Feature Configuration

Features can be enabled/disabled through:

1. **Environment Variables:**
   ```
   PIPEDRIVE_FEATURE_PERSONS=true
   PIPEDRIVE_FEATURE_DEALS=false
   ```

2. **JSON Configuration File:**
   ```json
   {
     "features": {
       "persons": true,
       "deals": true,
       "organizations": true,
       "leads": false,
       "item_search": true
     }
   }
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

## API Quirks and Model Requirements

- **Organization Address Format**: The Pipedrive API expects organization addresses in a dictionary format like `{"value": "123 Main St, City, Country"}` rather than a simple string. Always use the dictionary format for organization addresses in both create and update operations.

- **Label Arrays**: Some fields like `label_ids` must be sent as arrays even when only one item is present.

- **Visible To**: The `visible_to` parameter must be an integer between 1-4 representing the visibility level.

## Documentation and Resources

- **Templates**: See `.claude/guides/templates.md` for code templates
- **Edge Cases**: See `.claude/guides/edge-cases.md` for Pipedrive API quirks
- **Development Guide**: See `.claude/guides/dev-guide.md` for architecture details
- **MCP Tools**: Format docstrings with newlines between parameters for better readability, following the pattern in `ai_docs/mcp_example.md`
- **Migration Guide**: See `MIGRATION_GUIDE.md` for details on the new feature registry system

## MCP Tool Documentation Standards

IMPORTANT: Follow these standards for all MCP tool implementations, as docstrings and type hints are used by the MCP protocol to generate tool schemas for clients:

1. **Docstring Format**: 
   - Begin with a one-line summary of what the tool does
   - Follow with a detailed description of the tool's purpose
   - Include a "Format requirements" section for parameters with specific formats
   - Provide a complete usage example
   - Document each parameter with clear descriptions and format requirements
   - End with information about what the tool returns

2. **Type Hints**:
   - Use accurate type hints that reflect the expected parameter types
   - Use Optional[type] for optional parameters
   - Use appropriate return type annotations

3. **Parameter Naming**:
   - For numeric IDs: Use consistent naming conventions (e.g., `entity_id`)
   - Document format requirements in the parameter description
   - Always specify format examples for complex types

4. **Error Handling**:
   - Validate inputs early and provide clear error messages
   - Include expected format and examples in error messages
   - Return consistent error responses with the format_tool_response utility

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