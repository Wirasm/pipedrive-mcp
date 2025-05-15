import inspect
import re
from typing import Callable, Dict, List, Optional, Any, Set, Tuple
from functools import wraps

from log_config import logger
from pipedrive.api.features.tool_registry import registry
from pipedrive.mcp_instance import mcp


def validate_docstring(func: Callable, feature_id: str) -> List[str]:
    """
    Validate a tool function's docstring against the standardized format.
    
    Args:
        func: The function to validate
        feature_id: The feature this tool belongs to
        
    Returns:
        List of validation warnings, empty if docstring is valid
    """
    warnings = []
    docstring = inspect.getdoc(func)
    
    if not docstring:
        warnings.append(f"Tool '{func.__name__}' has no docstring")
        return warnings
        
    # Check for one-line summary (first line)
    lines = docstring.strip().split("\n")
    if not lines[0] or len(lines[0]) < 10:
        warnings.append(f"Tool '{func.__name__}' is missing a clear one-line summary")
        
    # Check for detailed description
    if len(lines) < 3:
        warnings.append(f"Tool '{func.__name__}' is missing a detailed description")
        
    # Check for format requirements section
    format_section = False
    example_section = False
    args_section = False
    returns_section = False
    
    for i, line in enumerate(lines):
        if line.strip().lower() == "format requirements:":
            format_section = True
        elif line.strip().lower() == "example:":
            example_section = True
        elif line.strip().lower() == "args:":
            args_section = True
        elif line.strip().lower() == "returns:":
            returns_section = True
    
    if not format_section:
        warnings.append(f"Tool '{func.__name__}' is missing 'Format requirements:' section")
    if not example_section:
        warnings.append(f"Tool '{func.__name__}' is missing 'Example:' section")
    if not args_section:
        warnings.append(f"Tool '{func.__name__}' is missing 'Args:' section")
    if not returns_section:
        warnings.append(f"Tool '{func.__name__}' is missing 'Returns:' section")
        
    # Check for examples in parameter descriptions
    # This is an approximation - a more robust parser would be needed for complex docstrings
    params = set(re.findall(r'\s+([a-zA-Z_][a-zA-Z0-9_]*):(?:\s|$)', docstring))
    signature_params = list(inspect.signature(func).parameters.keys())
    
    # Skip ctx parameter in the check
    if "ctx" in signature_params:
        signature_params.remove("ctx")
    
    # Check if all parameters from signature are documented
    for param in signature_params:
        if param not in params:
            warnings.append(f"Parameter '{param}' is not documented in the docstring")
    
    return warnings


def tool(feature_id: str, validate: bool = True):
    """
    Enhanced decorator for MCP tools that registers them with the feature registry.
    
    This decorator wraps the MCP tool decorator to also register tools with the
    feature registry for feature management. Tools will only be executed when their
    feature is enabled. It also validates docstrings against the standardized format.
    
    Args:
        feature_id: The ID of the feature this tool belongs to
        validate: Whether to validate the tool's docstring (defaults to True)
        
    Returns:
        Decorator function for tool
    """
    def decorator(func: Callable) -> Callable:
        # Validate docstring if requested
        if validate:
            warnings = validate_docstring(func, feature_id)
            if warnings:
                for warning in warnings:
                    logger.warning(warning)
        
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