# MCP Tool Registry Migration Guide

This guide explains how to use the new MCP Tool Registry system, which provides a more modular, configurable approach to managing MCP tools.

## Overview

The new Tool Registry system allows:

1. Organization of tools by feature
2. Runtime enabling/disabling of features
3. Automatic tool discovery and registration
4. Centralized tool metadata and documentation

## Key Components

### 1. Feature Registry (`pipedrive/api/features/tool_registry.py`)

The core of the new system is the `FeatureRegistry` class which manages features and their tools. Features must be registered before their tools.

```python
from pipedrive.api.features.tool_registry import registry, FeatureMetadata

# Register a feature
registry.register_feature(
    "my_feature",
    FeatureMetadata(
        name="My Feature",
        description="Tools for my awesome feature",
        version="1.0.0",
        dependencies=[]  # Optional dependencies
    )
)
```

### 2. Tool Decorator (`pipedrive/api/features/tool_decorator.py`)

A new tool decorator replaces `@mcp.tool()` for feature-aware tools:

```python
from pipedrive.api.features.tool_decorator import tool

@tool("my_feature")
async def my_awesome_tool(ctx, param1, param2):
    """Tool documentation"""
    # Tool implementation
```

The decorator:
- Registers the tool with MCP (same as before)
- Also registers with the feature registry
- Adds runtime feature-enabled checks

### 3. Feature Registry Files

Each feature should have its own registry file (e.g., `persons_tool_registry.py`) that:
- Registers the feature with metadata
- Registers all tools for that feature

```python
# persons_tool_registry.py
from pipedrive.api.features.tool_registry import registry, FeatureMetadata
from pipedrive.api.features.persons.tools.person_create_tool import create_person_in_pipedrive
# Import other person tools...

# Register the feature
registry.register_feature(
    "persons",
    FeatureMetadata(
        name="Persons",
        description="Tools for managing person entities in Pipedrive",
        version="1.0.0",
    )
)

# Register all tools
registry.register_tool("persons", create_person_in_pipedrive)
# Register other tools...
```

### 4. Feature Configuration (`pipedrive/feature_config.py`)

The `FeatureConfig` class enables/disables features at runtime:

- Loads config from a JSON file
- Supports environment variable overrides
- Creates defaults if no config exists

## Migration Steps

### 1. For Existing Tools

1. Change the decorator from `@mcp.tool()` to `@tool("feature_id")`
2. Create a feature registry file if it doesn't exist
3. Register the feature and its tools in that file

### 2. For New Features

1. Create a feature folder with the standard structure (client, models, tools)
2. Add a `feature_tool_registry.py` file in the feature folder
3. Register the feature and its tools in that file
4. Use the `@tool("feature_id")` decorator in all tool functions

### 3. Feature Configuration

Set feature flags through:

1. Environment variables:
   ```
   PIPEDRIVE_FEATURE_PERSONS=true
   PIPEDRIVE_FEATURE_DEALS=false
   ```

2. JSON configuration file:
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

## Examples

### Creating a New Feature

1. Create the feature structure:
   ```
   pipedrive/api/features/new_feature/
   ├── __init__.py
   ├── client/
   ├── models/
   ├── tools/
   └── new_feature_tool_registry.py
   ```

2. Register the feature in `new_feature_tool_registry.py`:
   ```python
   from pipedrive.api.features.tool_registry import registry, FeatureMetadata
   
   registry.register_feature(
       "new_feature",
       FeatureMetadata(
           name="New Feature",
           description="Tools for the new feature",
           version="1.0.0",
       )
   )
   ```

3. Create tool implementations with the new decorator:
   ```python
   @tool("new_feature")
   async def my_new_tool(ctx, param1, param2):
       """Tool documentation"""
       # Tool implementation
   ```

4. Register tools in the registry file:
   ```python
   from .tools.my_tool import my_new_tool
   
   registry.register_tool("new_feature", my_new_tool)
   ```

## Best Practices

1. **Feature Organization**: Keep related tools in the same feature
2. **Feature Granularity**: Create features at the right level of granularity (not too big, not too small)
3. **Dependencies**: Specify feature dependencies if one feature relies on another
4. **Documentation**: Add clear descriptions to FeatureMetadata
5. **Configuration**: Set reasonable defaults for feature flags

## Troubleshooting

1. **Tool not registered**: Ensure the feature is registered before registering tools
2. **Feature not enabled**: Check configuration file or environment variables
3. **Discovery issues**: Verify the feature registry file has the correct name format
4. **Import errors**: Check for circular imports in registry files

## Contact

For questions or issues with the new system, please contact the project maintainers.