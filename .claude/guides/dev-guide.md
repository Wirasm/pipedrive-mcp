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

## Feature Registry System

The project uses a feature registry system that allows:

1. **Runtime Feature Management**: Features can be enabled/disabled dynamically
2. **Tool Organization**: Tools are grouped by feature
3. **Feature Discovery**: New features are automatically discovered and registered

### Using the Feature Registry

```python
# Register a feature
from pipedrive.api.features.tool_registry import registry, FeatureMetadata

registry.register_feature(
    "feature_name",
    FeatureMetadata(
        name="Feature Name",
        description="Description of what this feature does",
        version="1.0.0"
    )
)

# Register a tool
from .tools.my_tool import my_tool_function
registry.register_tool("feature_name", my_tool_function)
```

## API Client Structure

The API client is structured into multiple layers:

### Base Client

The `BaseClient` handles basic HTTP functionality:

```python
# pipedrive/api/base_client.py
class BaseClient:
    """Base client for making API requests."""
    
    async def request(
        self, method: str, endpoint: str, 
        query_params: Optional[Dict[str, Any]] = None,
        json_payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Pipedrive API."""
        # Implementation...
```

### Pipedrive Client

The `PipedriveClient` combines all feature-specific clients:

```python
# pipedrive/api/pipedrive_client.py
class PipedriveClient:
    """Client for the Pipedrive API."""
    
    def __init__(self, api_token: str, company_domain: str):
        self.base_client = BaseClient(api_token, company_domain)
        
        # Initialize feature clients
        self.person = PersonClient(self.base_client)
        self.organization = OrganizationClient(self.base_client)
        self.deal = DealClient(self.base_client)
        self.lead = LeadClient(self.base_client)
        self.activities = ActivityClient(self.base_client)
        self.item_search = ItemSearchClient(self.base_client)
```

### Feature-Specific Clients

Each feature has its own client implementation:

```python
# pipedrive/api/features/persons/client/person_client.py
class PersonClient:
    """Client for the Persons API."""
    
    def __init__(self, base_client: BaseClient):
        self.base_client = base_client
    
    async def create_person(self, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new person in Pipedrive."""
        return await self.base_client.request(
            "POST", "/persons", json_payload=person_data
        )
```

## API Versioning Support

The Pipedrive API has different versions (v1 and v2) with different behavior:

- **v1 API**: Uses start/more_items_in_collection-based pagination
- **v2 API**: Uses cursor-based pagination (preferred when available)

The base client automatically handles the different API versions:

```python
# Example of making a v2 API request
response_data = await self.base_client.request(
    "GET", 
    "/v2/leads",  # Note the v2 prefix
    query_params={"cursor": cursor, "limit": limit}
)

# The base client detects the API version and handles pagination appropriately
```

## Tools Implementation

Each tool follows a consistent pattern using the feature-aware decorator:

```python
from pipedrive.api.features.tool_decorator import tool

@tool("feature_name")
async def create_entity_in_pipedrive(
    ctx: Context,
    required_param: str,
    optional_param: Optional[str] = None,
) -> str:
    """Creates a new entity in Pipedrive.
    
    This tool creates an entity with the specified details.
    
    Format requirements:
    - required_param: Description with format requirements
    - optional_param: Description with format requirements
    
    Example:
    ```
    create_entity_in_pipedrive(
        required_param="value",
        optional_param="optional"
    )
    ```
    
    Args:
        ctx: Context object containing the Pipedrive client
        required_param: Description
        optional_param: Description
    
    Returns:
        JSON string containing success status and created entity data or error message.
    """
    # Implementation...
```

## Common Utilities

### Response Formatting

```python
from pipedrive.api.features.shared.utils import format_tool_response

# Success response
return format_tool_response(True, data=response_data)

# Error response
return format_tool_response(False, error_message="Descriptive error message")
```

### ID Conversion

```python
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string

# Convert and validate ID
id_value, error = convert_id_string(id_str, "field_name")
if error:
    return format_tool_response(False, error_message=error)
```

## Testing

- Use `pytest` and `pytest-asyncio` for all tests
- Co-locate tests with the code they test
- Create fixture factories for common test data
- Use `AsyncMock` for mocking async functions

### Testing Tools

```python
@pytest.mark.asyncio
async def test_create_entity_success(mock_context):
    """Test successful entity creation."""
    # Mock the client response
    mock_context.request_context.lifespan_context.pipedrive_client.feature.create_entity.return_value = {
        "id": 123,
        "name": "Test Entity"
    }
    
    # Call the tool
    result = await create_entity_in_pipedrive(
        ctx=mock_context,
        required_param="Test Entity"
    )
    
    # Parse and verify result
    result_data = json.loads(result)
    assert result_data["success"] is True
    assert result_data["data"]["id"] == 123
```