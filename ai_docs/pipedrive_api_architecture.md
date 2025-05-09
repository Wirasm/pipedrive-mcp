# Pipedrive API Architecture

This document describes the new architecture for Pipedrive API clients in the `pipe-mcp` project.

## Overview

The project now uses a modular, object-oriented approach for Pipedrive API interactions. This new architecture provides several advantages:

1. **Clean Separation of Concerns**
2. **Improved Code Reuse**
3. **Better Type Safety**
4. **Enhanced Error Handling**
5. **Model-based Data Validation**
6. **Consistent Client Management**

## Directory Structure

```
src/pipedrive/
├── api/
│   ├── base.py             # Base client implementation
│   ├── client_manager.py   # Client lifecycle management
│   ├── exceptions.py       # Custom exceptions
│   ├── models.py           # Pydantic models for API entities
│   ├── tools/              # MCP tools using the new architecture
│   │   └── ...
│   ├── v1.py               # V1 API client implementation
│   └── v2.py               # V2 API client implementation
├── pipedrive_client_v1.py  # Legacy client (will be deprecated)
└── pipedrive_client_v2.py  # Legacy client (will be deprecated)
```

## Components

### Base Client

The `BasePipedriveClient` class provides common functionality for all Pipedrive API clients:

- HTTP request handling
- Authentication
- Error processing
- Retry logic
- Resource utilities

```python
from pipedrive.api.base import BasePipedriveClient

class MyPipedriveClient(BasePipedriveClient):
    BASE_URL = "https://api.pipedrive.com/v3"  # For example
    
    async def get_custom_data(self):
        return await self._request("GET", "custom_endpoint")
```

### Entity Models

Pydantic models provide type safety and validation for Pipedrive entities:

```python
from pipedrive.api.models import Person, Deal, Organization

# Create a person with validation
person = Person(
    id=1,
    name="John Doe",
    emails=[{"value": "john@example.com", "primary": True}]
)

# Access properties with auto-completion and type hints
print(person.name)
print(person.emails[0].value)
```

### Client Management

The client manager provides singleton instances for efficient resource usage:

```python
from pipedrive.api.client_manager import get_pipedrive_v2_client

async def my_function():
    # Get the shared V2 client
    client = await get_pipedrive_v2_client()
    
    # Use the client
    persons = await client.get_persons(limit=5)
    
    # No need to close the client as it's managed globally
```

### Exception Handling

Custom exceptions make error handling more precise:

```python
from pipedrive.api.exceptions import PipedriveAPIError, PipedriveAuthError, PipedriveRateLimitError

async def fetch_data():
    try:
        result = await client.get_person(123)
        return result
    except PipedriveRateLimitError as e:
        # Handle rate limiting
        print(f"Rate limited, retry after: {e.retry_after} seconds")
    except PipedriveAuthError:
        # Handle authentication issues
        print("Authentication failed, please check your API token")
    except PipedriveAPIError as e:
        # Handle other API errors
        print(f"API error: {e}, code: {e.error_code}")
```

## Usage Examples

### Basic Client Usage

```python
import asyncio
from pipedrive.api import PipedriveClientV2, Person

async def main():
    # Using a client directly (automatically closed with context manager)
    async with PipedriveClientV2() as client:
        # Get persons with optional filtering
        persons = await client.get_persons(
            params={"limit": 5},
            include_fields=["open_deals_count", "email_messages_count"]
        )
        
        for person in persons:
            print(f"Person: {person.name}")
            
            # Work with typed data
            if person.emails:
                print(f"Email: {person.emails[0].value}")
            
        # Create a new person
        new_person = await client.create_person({
            "name": "Jane Smith",
            "email": [{"value": "jane@example.com", "primary": True}]
        })
        
        print(f"Created person with ID: {new_person.id}")

# Run the example
asyncio.run(main())
```

### MCP Tool Usage

```python
from mcp.server.fastmcp import Context, FastMCP

from pipedrive.api.tools import get_persons_v2_tool

# Register the tool with MCP
@mcp.tool()
async def pipedrive_v2_get_persons(
    ctx: Context,
    limit: int = 10,
    cursor: Optional[str] = None,
    include_fields: Optional[str] = None,
) -> str:
    """Get a list of persons from Pipedrive using V2 API."""
    return await get_persons_v2_tool(ctx, limit, cursor, include_fields=include_fields)
```

## Migration Guide

To migrate from the legacy clients to the new architecture:

1. Update imports to use the new API package:

```python
# Old import
from pipedrive import PipedriveV2Client

# New import
from pipedrive.api import PipedriveClientV2
```

2. Use the client manager for efficient resource usage:

```python
# Old approach
client = PipedriveV2Client()
try:
    # Use client
finally:
    await client.close()

# New approach
from pipedrive.api import get_pipedrive_v2_client

client = await get_pipedrive_v2_client()
# Use client (no need to close)
```

3. Work with typed entity models:

```python
# Old approach (untyped dictionaries)
person_dict = await client.get_person(123)
name = person_dict.get("name")

# New approach (typed models)
person = await client.get_person(123)
name = person.name  # Type safe with auto-completion
```

## Backwards Compatibility

The legacy clients (`PipedriveClient` and `PipedriveV2Client`) are still available for backwards compatibility but will be deprecated in future versions. All existing MCP tools continue to work as before.