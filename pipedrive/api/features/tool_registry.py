from typing import Dict, List, Callable, Set, Optional, Any
from dataclasses import dataclass, field
from log_config import logger

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
        logger.debug(f"Registering feature: {feature_id} ({metadata.name})")
        self._features[feature_id] = metadata
        if feature_id not in self._tools:
            self._tools[feature_id] = set()
        
    def register_tool(self, feature_id: str, tool_func: Callable) -> None:
        """Register a tool function with a feature"""
        if feature_id not in self._features:
            raise ValueError(f"Feature {feature_id} is not registered")
            
        if feature_id not in self._tools:
            self._tools[feature_id] = set()
            
        logger.debug(f"Registering tool: {tool_func.__name__} with feature: {feature_id}")
        self._tools[feature_id].add(tool_func)
        
    def enable_feature(self, feature_id: str) -> None:
        """Enable a feature"""
        if feature_id not in self._features:
            raise ValueError(f"Feature {feature_id} is not registered")
            
        logger.info(f"Enabling feature: {feature_id}")
        self._enabled_features.add(feature_id)
        
        # Also enable all dependencies
        for dependency in self._features[feature_id].dependencies:
            if dependency not in self._enabled_features and dependency in self._features:
                logger.info(f"Enabling dependency: {dependency} for feature: {feature_id}")
                self._enabled_features.add(dependency)
        
    def disable_feature(self, feature_id: str) -> None:
        """Disable a feature"""
        logger.info(f"Disabling feature: {feature_id}")
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
    
    def register_tool_for_feature(self, feature_id: str, tool_func: Callable) -> Callable:
        """
        Decorator for registering a tool with a feature.
        
        Args:
            feature_id: Feature ID to register the tool with
            tool_func: Tool function to register
            
        Returns:
            The original tool function
        """
        self.register_tool(feature_id, tool_func)
        return tool_func

    def get_tool_count(self, feature_id: Optional[str] = None) -> int:
        """
        Get the number of tools registered, either for a specific feature or total.
        
        Args:
            feature_id: Optional feature ID to count tools for
            
        Returns:
            Number of tools
        """
        if feature_id:
            if feature_id not in self._tools:
                return 0
            return len(self._tools[feature_id])
        else:
            total = 0
            for tools in self._tools.values():
                total += len(tools)
            return total

    def __str__(self) -> str:
        """String representation of the registry"""
        enabled_count = len(self._enabled_features)
        total_count = len(self._features)
        tool_count = self.get_tool_count()
        
        return f"FeatureRegistry: {enabled_count}/{total_count} features enabled, {tool_count} tools registered"

# Create global registry instance
registry = FeatureRegistry()