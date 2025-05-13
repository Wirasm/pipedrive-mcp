from typing import Callable, Optional, Any
from functools import wraps

from log_config import logger
from pipedrive.api.features.tool_registry import registry
from pipedrive.mcp_instance import mcp

def tool(feature_id: str):
    """
    Decorator for MCP tools that also registers them with the feature registry.
    
    This decorator wraps the MCP tool decorator to also register tools with the
    feature registry for feature management. Tools will only be executed when their
    feature is enabled.
    
    Args:
        feature_id: The ID of the feature this tool belongs to
        
    Returns:
        Decorator function for tool
    """
    def decorator(func: Callable) -> Callable:
        # First register with MCP as before
        mcp_decorated = mcp.tool()(func)
        
        # Get the original function name for better logging
        original_name = func.__name__
        
        @wraps(mcp_decorated)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check if the feature is enabled
            if not registry.is_feature_enabled(feature_id):
                logger.warning(f"Tool '{original_name}' called but feature '{feature_id}' is not enabled")
                return (
                    f"This tool is not available because the '{feature_id}' "
                    f"feature is disabled. Please contact your administrator."
                )
                
            # Feature is enabled, execute the tool
            return await mcp_decorated(*args, **kwargs)
        
        # Register with our feature registry
        try:
            registry.register_tool(feature_id, wrapper)
        except ValueError:
            logger.warning(
                f"Tool '{original_name}' attempted to register with unknown feature '{feature_id}'. "
                f"Make sure to register the feature before registering tools."
            )
            
        return wrapper
        
    return decorator