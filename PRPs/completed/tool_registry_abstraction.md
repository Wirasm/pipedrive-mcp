name: "MCP Tool Registry Abstraction"
description: |

  ## Goal
  Create a modular, configurable system for registering MCP tools that eliminates the need to directly import each tool in server.py and allows for feature-based toggling and management.

  ## Why
  - The current approach requires manual imports of every tool function in server.py
  - Adding or removing features requires modifying the main server file
  - There's no easy way to enable/disable features without code changes
  - A more modular approach would improve maintainability and extensibility
  - Feature flags would allow for controlled rollouts and testing

  ## What
  This PRP proposes creating:
  1. A registry system for MCP tools organized by feature
  2. A configuration mechanism to enable/disable features
  3. Automatic tool discovery and registration
  4. Centralized tool metadata and documentation

  ## Current Implementation

  Currently, tools are registered by:
  1. Importing each tool function in server.py
  2. Using the @mcp.tool() decorator in each tool file
  3. The decorator automatically registers tools with the central MCP instance

  This approach works but has limitations:
  - Requires modifying server.py for every new tool
  - No control over which features are enabled
  - Difficult to maintain as the number of features grows
  - Hard to implement feature flags or conditional features

  ## Proposed Solution

  ### 1. Feature Registry Pattern

  Create a registry system that organizes tools by feature and handles registration:

  ```python
  # pipedrive/api/features/tool_registry.py
  from typing import Dict, List, Callable, Set, Optional
  from dataclasses import dataclass, field

  @dataclass
  class FeatureMetadata:
      """Metadata for a Pipedrive API feature"""
      name: str
      description: str
      version: str = "1.0.0"
      dependencies: List[str] = field(default_factory=list)
      
  class FeatureRegistry:
      """Registry for Pipedrive API features and their tools"""
      
      def __init__(self):
          self._features: Dict[str, FeatureMetadata] = {}
          self._tools: Dict[str, Set[Callable]] = {}
          self._enabled_features: Set[str] = set()
          
      def register_feature(self, feature_id: str, metadata: FeatureMetadata) -> None:
          """Register a feature with the registry"""
          self._features[feature_id] = metadata
          if feature_id not in self._tools:
              self._tools[feature_id] = set()
          
      def register_tool(self, feature_id: str, tool_func: Callable) -> None:
          """Register a tool function with a feature"""
          if feature_id not in self._features:
              raise ValueError(f"Feature {feature_id} is not registered")
              
          if feature_id not in self._tools:
              self._tools[feature_id] = set()
              
          self._tools[feature_id].add(tool_func)
          
      def enable_feature(self, feature_id: str) -> None:
          """Enable a feature"""
          if feature_id not in self._features:
              raise ValueError(f"Feature {feature_id} is not registered")
              
          self._enabled_features.add(feature_id)
          
      def disable_feature(self, feature_id: str) -> None:
          """Disable a feature"""
          self._enabled_features.discard(feature_id)
          
      def get_enabled_tools(self) -> List[Callable]:
          """Get all tools from enabled features"""
          tools = []
          for feature_id in self._enabled_features:
              tools.extend(self._tools.get(feature_id, []))
          return tools
          
      def is_feature_enabled(self, feature_id: str) -> bool:
          """Check if a feature is enabled"""
          return feature_id in self._enabled_features
          
      def get_feature_metadata(self, feature_id: str) -> Optional[FeatureMetadata]:
          """Get metadata for a feature"""
          return self._features.get(feature_id)
          
      def get_all_features(self) -> Dict[str, FeatureMetadata]:
          """Get all registered features"""
          return self._features.copy()
          
      def get_enabled_features(self) -> Dict[str, FeatureMetadata]:
          """Get all enabled features"""
          return {
              feature_id: metadata 
              for feature_id, metadata in self._features.items()
              if feature_id in self._enabled_features
          }
  
  # Create global registry instance
  registry = FeatureRegistry()
  ```

  ### 2. Feature-specific Tool Registration

  Each feature would define its tools in a feature-specific registry file:

  ```python
  # pipedrive/api/features/persons/persons_tool_registry.py
  from pipedrive.api.features.registry import registry, FeatureMetadata
  from pipedrive.api.features.persons.tools.person_create_tool import create_person_in_pipedrive
  from pipedrive.api.features.persons.tools.person_get_tool import get_person_from_pipedrive
  from pipedrive.api.features.persons.tools.person_update_tool import update_person_in_pipedrive
  from pipedrive.api.features.persons.tools.person_delete_tool import delete_person_from_pipedrive
  from pipedrive.api.features.persons.tools.person_search_tool import search_persons_in_pipedrive

  # Register the feature
  registry.register_feature(
      "persons",
      FeatureMetadata(
          name="Persons",
          description="Tools for managing person entities in Pipedrive",
          version="1.0.0",
      )
  )

  # Register all tools for this feature
  registry.register_tool("persons", create_person_in_pipedrive)
  registry.register_tool("persons", get_person_from_pipedrive)
  registry.register_tool("persons", update_person_in_pipedrive)
  registry.register_tool("persons", delete_person_from_pipedrive)
  registry.register_tool("persons", search_persons_in_pipedrive)
  ```

  ### 3. Tool Decorator Modification

  Update the tool decorator to register with the feature registry:

  ```python
  # Modified tool decorator
  def tool(feature_id: str):
      def decorator(func):
          # Register with MCP as before
          mcp_decorated = mcp.tool()(func)
          
          # Also register with our feature registry
          registry.register_tool(feature_id, mcp_decorated)
          
          return mcp_decorated
      return decorator
  ```

  ### 4. Feature Configuration

  Create a configuration system to enable/disable features:

  ```python
  # pipedrive/feature_config.py
  from typing import Dict, Any
  import os
  import json
  from pathlib import Path
  
  from pipedrive.api.features.registry import registry

  class FeatureConfig:
      """Configuration for Pipedrive API features"""
      
      def __init__(self, config_path: str = None):
          self.config_path = config_path or os.getenv(
              "FEATURE_CONFIG_PATH", 
              str(Path(__file__).parent / "feature_config.json")
          )
          self.load_config()
          
      def load_config(self) -> None:
          """Load feature configuration from file"""
          if not os.path.exists(self.config_path):
              self._create_default_config()
              
          try:
              with open(self.config_path, "r") as f:
                  config = json.load(f)
                  
              # Enable features based on config
              for feature_id, enabled in config.get("features", {}).items():
                  if enabled:
                      registry.enable_feature(feature_id)
                  else:
                      registry.disable_feature(feature_id)
                      
          except Exception as e:
              print(f"Error loading feature config: {e}")
              self._create_default_config()
              
      def _create_default_config(self) -> None:
          """Create default configuration enabling all features"""
          config = {
              "features": {
                  feature_id: True for feature_id in registry.get_all_features()
              }
          }
          
          os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
          
          with open(self.config_path, "w") as f:
              json.dump(config, f, indent=2)
              
          # Enable all features by default
          for feature_id in registry.get_all_features():
              registry.enable_feature(feature_id)
              
      def get_enabled_features(self) -> Dict[str, Any]:
          """Get all enabled features"""
          return registry.get_enabled_features()
  ```

  ### 5. Auto-Discovery of Features

  Implement automatic discovery of feature registry modules:

  ```python
  # pipedrive/api/features/__init__.py
  import importlib
  import pkgutil
  import os
  from pathlib import Path

  def discover_features():
      """Discover and load all feature registry modules"""
      features_dir = Path(__file__).parent
      
      for _, name, ispkg in pkgutil.iter_modules([str(features_dir)]):
          if ispkg:
              # Check if this package has a registry.py file
              registry_path = features_dir / name / f"{name}_tool_registry.py"
              if os.path.exists(registry_path):
                  # Import the registry module to register the feature
                  importlib.import_module(f"pipedrive.api.features.{name}.{name}_tool_registry")
  ```

  ### 6. Modified Server.py

  Simplify the server.py file to use the registry:

  ```python
  import asyncio
  import os

  from dotenv import load_dotenv
  from log_config import logger
  
  # Import feature registry and discovery
  from pipedrive.api.features.tool_registry import registry
  from pipedrive.api.features import discover_features
  from pipedrive.feature_config import FeatureConfig
  from pipedrive.api.pipedrive_context import pipedrive_lifespan
  from pipedrive.mcp_instance import mcp

  load_dotenv()

  # Discover and register all features
  discover_features()

  # Load feature configuration
  feature_config = FeatureConfig()

  async def main():
      transport = os.getenv("TRANSPORT", "sse")
      server_host = os.getenv("HOST", "0.0.0.0")
      server_port = int(os.getenv("PORT", "8152"))
      
      # Log enabled features
      enabled_features = feature_config.get_enabled_features()
      logger.info(f"Enabled features: {', '.join(enabled_features.keys())}")
      
      logger.info(
          f"Starting Pipedrive MCP server. Transport: {transport}, Host: {server_host}, Port: {server_port}"
      )
      
      if transport == "sse":
          await mcp.run_sse_async()
      else:
          logger.info(
              "Stdio transport selected. Ensure your FastMCP setup supports this or modify."
          )
          if hasattr(mcp, "run_stdio_async"):
              await mcp.run_stdio_async()
          else:
              logger.warning(
                  "run_stdio_async method not found on mcp object. Defaulting to SSE behavior..."
              )
              await mcp.run_sse_async()

  if __name__ == "__main__":
      asyncio.run(main())
  ```

  ## Feature Flag Configuration

  Using environment variables or a JSON configuration file:

  ```json
  // feature_config.json
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

  Or using environment variables:

  ```
  PIPEDRIVE_FEATURE_PERSONS=true
  PIPEDRIVE_FEATURE_DEALS=true
  PIPEDRIVE_FEATURE_LEADS=false
  ```

  ## Implementation Plan

  1. Create the feature registry system:
     - Implement FeatureRegistry class
     - Create registry instance

  2. Modify MCP tool decorator:
     - Update to register tools with feature registry
     - Maintain backward compatibility

  3. Create feature-specific registry files:
     - Add one registry file per feature
     - Register all tools for each feature

  4. Implement feature configuration:
     - Add JSON configuration support
     - Add environment variable override

  5. Add auto-discovery mechanism:
     - Discover feature packages
     - Load registry modules automatically

  6. Update server.py:
     - Remove manual imports
     - Use registry to discover and register tools
     - Enable features based on configuration

  7. Add tests:
     - Test feature registry functionality
     - Test tool discovery and registration
     - Test feature enabling/disabling

  ## Validation Gates

  - All existing tools must work as before
  - Feature flags must correctly enable/disable features
  - Auto-discovery must find all feature packages
  - Configuration changes must be reflected without code changes
  - New tools added to feature packages should be auto-registered
  - All tests must pass when running `uv run pytest`

  ## Files to Add/Modify

  1. `pipedrive/api/features/tool_registry.py` - New file for registry class
  2. `pipedrive/feature_config.py` - New file for feature configuration
  3. `pipedrive/api/features/__init__.py` - Add feature discovery
  4. `pipedrive/api/features/*/[feature]_tool_registry.py` - Add one per feature
  5. `server.py` - Simplify to use registry
  6. `pipedrive/mcp_instance.py` - Potentially update for integration

  ## Migration Strategy

  1. Implement the feature registry without changing existing code
  2. Add feature-specific registry files
  3. Update server.py to use both approaches (for backward compatibility)
  4. Gradually migrate tools to use the new registry
  5. Once all tools are migrated, simplify server.py

