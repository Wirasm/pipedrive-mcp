# Pipedrive MCP Development Guide

This guide explains the architecture and development practices for the Pipedrive MCP server.

## Vertical Slice Architecture

The project follows a vertical slice architecture, which organizes code by feature rather than by technical layer. This approach offers several benefits:

- **Feature Cohesion**: All code related to a single feature is located together
- **Independent Development**: Features can be developed and tested independently
- **Clear Boundaries**: Features have well-defined interfaces and dependencies
- **Scalability**: New features can be added without affecting existing ones

### Core Principles

1. **Feature-First Organization**: Code is organized by feature (e.g., persons, deals, organizations)
2. **Self-Contained Slices**: Each feature contains all necessary components (models, clients, tools)
3. **Minimal Cross-Feature Dependencies**: Features should be independent where possible
4. **Shared Utilities**: Common functionality is extracted to shared utilities

### Directory Structure

```
pipedrive/api/features/
├── feature1/                # A specific feature (e.g., persons)
│   ├── client/              # API client for this feature
│   │   ├── feature1_client.py
│   │   └── tests/
│   ├── models/              # Domain models for this feature
│   │   ├── model1.py
│   │   └── tests/
│   └── tools/               # MCP tools for this feature
│       ├── tool1.py
│       └── tests/
├── feature2/                # Another feature
│   └── ...
└── shared/                  # Shared utilities used across features
    ├── conversion/
    ├── validation/
    └── ...
```

## Implementation Guidelines

### Models

- Use Pydantic v2 for all models
- Include validation in models where appropriate
- Provide methods for converting between API and domain representations
- Always include to_api_dict() and from_api_dict() methods

Example:
```python
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    id: Optional[int] = None
    name: str
    active: bool = True
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary"""
        return {k: v for k, v in self.model_dump().items() if v is not None}
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'MyModel':
        """Create from API response dictionary"""
        return cls(**data)
```

### Clients

- Create feature-specific clients that focus on one resource type
- Use the base_client for HTTP communication
- Keep methods focused on single responsibilities
- Document parameters and return types

Example:
```python
class FeatureClient:
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client
    
    async def create_resource(self, resource: Resource) -> Dict[str, Any]:
        """Create a new resource."""
        return await self.base_client.request(
            method="POST",
            endpoint="/resources",
            json_payload=resource.to_api_dict()
        )
```

### Tools

- Create MCP tools that wrap client methods
- Use shared utilities for common operations
- Implement proper error handling
- Return standardized responses

Example:
```python
@mcp.tool()
async def create_resource_tool(ctx: Context, name: str, ...) -> str:
    """Creates a new resource."""
    # Get context
    pd_mcp_ctx = ctx.request_context.lifespan_context
    
    # Convert IDs
    id_value, error = convert_id_string(id_str, "field_name")
    if error:
        return format_tool_response(False, error_message=error)
    
    # Create resource
    try:
        resource = Resource(name=name, ...)
        result = await pd_mcp_ctx.pipedrive_client.feature.create_resource(resource)
        return format_tool_response(True, data=result)
    except Exception as e:
        return format_tool_response(False, error_message=str(e))
```

## Testing

- Co-locate tests with the code they test
- Test each component independently
- Use fixture factories for common test data
- Mock external dependencies

For more details, see the project's testing guidelines.

## Common Development Tasks

- **Adding a new feature**: Use the `/project:new-feature` command
- **Fixing tests**: Use the `/project:fix-test` command
- **Refactoring utilities**: Use the `/project:refactor-utility` command