# MCP Tool Documentation Templates

This file contains standardized documentation templates for different types of MCP tools. Use these templates
when creating or updating tool implementations to ensure consistency across the codebase.

## Common Structure

All tool docstrings should follow this common structure:

```python
"""One-line summary of what the tool does.

Detailed multi-line description explaining the purpose and key functionality.
Highlight important information or constraints.

Format requirements:
- id_params: Must be numeric strings (e.g., "123")
- uuid_params: Must be valid UUID strings (e.g., "123e4567-e89b-12d3-a456-426614174000")
- time_params: Must use HH:MM:SS format (e.g., "14:30:00")
- date_params: Must use YYYY-MM-DD format (e.g., "2025-01-15")
- boolean_params: Use lowercase true/false

Example:
```
tool_name(
    required_param="Example value",
    id_param="123",
    boolean_param=true
)
```

Args:
    ctx: Context object provided by the MCP server
    required_param: Clear description with format requirements
    id_param: Numeric ID of the entity. Must be a positive integer as a string (e.g., "123")
    boolean_param: Whether to enable a feature. Use lowercase true/false

Returns:
    JSON formatted response with success/failure status and data or error message
"""
```

## Create Tool Template

```python
@tool("feature_name")
async def create_entity_in_pipedrive(
    ctx: Context,
    required_field: str,
    optional_field: Optional[str] = None,
    entity_id: Optional[str] = None,
    visible_to: Optional[str] = None,
) -> str:
    """Creates a new entity in Pipedrive CRM.

    This tool creates a new entity with the specified attributes in the Pipedrive CRM.
    The required_field is mandatory, while other parameters are optional.

    Format requirements:
    - entity_id: Must be a numeric string (e.g., "123")
    - visible_to: Must be a numeric string between "1" and "4" (e.g., "3")
    - date_fields: Must be in YYYY-MM-DD format (e.g., "2025-01-15")
    - time_fields: Must be in HH:MM:SS format (e.g., "14:30:00")
    - boolean_fields: Use lowercase true/false

    Example:
    ```
    create_entity_in_pipedrive(
        required_field="Example value",
        entity_id="123",
        visible_to="3"
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        required_field: Description of the required field
        optional_field: Description of the optional field
        entity_id: Numeric ID of the entity. Must be a positive integer as a string (e.g., "123")
        visible_to: Visibility level from 1-4. Use "1" for private, "3" for shared (e.g., "3")

    Returns:
        JSON formatted response with the created entity data or error message
    """
```

## Get Tool Template

```python
@tool("feature_name")
async def get_entity_from_pipedrive(
    ctx: Context,
    entity_id: str,
) -> str:
    """Retrieves a specific entity from Pipedrive CRM.

    This tool fetches a single entity by its ID from the Pipedrive CRM.
    The entity_id parameter is required and must be a valid ID.

    Format requirements:
    - entity_id: Must be a numeric string (e.g., "123")

    Example:
    ```
    get_entity_from_pipedrive(
        entity_id="123"
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        entity_id: Numeric ID of the entity to retrieve. Must be a positive integer as a string (e.g., "123")

    Returns:
        JSON formatted response with the entity data or error message
    """
```

## Update Tool Template

```python
@tool("feature_name")
async def update_entity_in_pipedrive(
    ctx: Context,
    entity_id: str,
    field_to_update: Optional[str] = None,
    another_field: Optional[str] = None,
    boolean_field: Optional[bool] = None,
) -> str:
    """Updates an existing entity in Pipedrive CRM.

    This tool updates the attributes of an existing entity in the Pipedrive CRM.
    The entity_id parameter is required, and at least one field to update must be provided.

    Format requirements:
    - entity_id: Must be a numeric string (e.g., "123")
    - date_fields: Must be in YYYY-MM-DD format (e.g., "2025-01-15")
    - time_fields: Must be in HH:MM:SS format (e.g., "14:30:00")
    - boolean_fields: Use lowercase true/false

    Example:
    ```
    update_entity_in_pipedrive(
        entity_id="123",
        field_to_update="New value",
        boolean_field=true
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        entity_id: Numeric ID of the entity to update. Must be a positive integer as a string (e.g., "123")
        field_to_update: New value for the field
        another_field: New value for another field
        boolean_field: New value for the boolean field. Use lowercase true/false

    Returns:
        JSON formatted response with the updated entity data or error message
    """
```

## Delete Tool Template

```python
@tool("feature_name")
async def delete_entity_from_pipedrive(
    ctx: Context,
    entity_id: str,
) -> str:
    """Deletes a specific entity from Pipedrive CRM.

    This tool permanently removes an entity from the Pipedrive CRM.
    The entity_id parameter is required and must be a valid ID.
    This action cannot be undone.

    Format requirements:
    - entity_id: Must be a numeric string (e.g., "123")

    Example:
    ```
    delete_entity_from_pipedrive(
        entity_id="123"
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        entity_id: Numeric ID of the entity to delete. Must be a positive integer as a string (e.g., "123")

    Returns:
        JSON formatted response with the success status or error message
    """
```

## List Tool Template

```python
@tool("feature_name")
async def list_entities_from_pipedrive(
    ctx: Context,
    limit: Optional[str] = "100",
    start: Optional[str] = "0",
    sort_field: Optional[str] = None,
    sort_order: Optional[str] = "asc",
    filter_field: Optional[str] = None,
) -> str:
    """Retrieves a list of entities from Pipedrive CRM.

    This tool fetches multiple entities from the Pipedrive CRM.
    Results can be paginated, sorted, and filtered based on the provided parameters.

    Format requirements:
    - limit: Must be a numeric string (e.g., "100")
    - start: Must be a numeric string (e.g., "0")
    - sort_order: Must be either "asc" or "desc"

    Example:
    ```
    list_entities_from_pipedrive(
        limit="50",
        start="0",
        sort_field="name",
        sort_order="asc"
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        limit: Maximum number of entities to retrieve. Must be a positive integer as a string (e.g., "100")
        start: Offset for pagination. Must be a positive integer as a string (e.g., "0")
        sort_field: Field to sort by (e.g., "name", "created_time")
        sort_order: Direction to sort in. Must be "asc" or "desc" (default: "asc")
        filter_field: Field to filter results by

    Returns:
        JSON formatted response with the list of entities or error message
    """
```

## Search Tool Template

```python
@tool("feature_name")
async def search_entities_in_pipedrive(
    ctx: Context,
    term: str,
    field: Optional[str] = None,
    exact_match: Optional[bool] = False,
    limit: Optional[str] = "100",
) -> str:
    """Searches for entities in Pipedrive CRM.

    This tool searches for entities matching the specified term in the Pipedrive CRM.
    The search term is required and can be restricted to a specific field.

    Format requirements:
    - limit: Must be a numeric string (e.g., "100")
    - exact_match: Use lowercase true/false

    Example:
    ```
    search_entities_in_pipedrive(
        term="John Doe",
        field="name",
        exact_match=false,
        limit="50"
    )
    ```

    Args:
        ctx: Context object provided by the MCP server
        term: Search term to look for
        field: Field to restrict the search to (e.g., "name", "email")
        exact_match: Whether to require an exact match. Use lowercase true/false
        limit: Maximum number of results to return. Must be a positive integer as a string (e.g., "100")

    Returns:
        JSON formatted response with the search results or error message
    """
```