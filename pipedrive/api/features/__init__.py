import importlib
import pkgutil
import os
from pathlib import Path
from log_config import logger

def discover_features():
    """
    Discover and load all feature registry modules.
    
    Looks for {feature_name}_tool_registry.py files in each feature subdirectory
    and imports them to register the feature and its tools.
    """
    logger.info("Discovering feature registry modules...")
    features_dir = Path(__file__).parent
    
    feature_count = 0
    
    for _, name, ispkg in pkgutil.iter_modules([str(features_dir)]):
        if ispkg:
            # Check if this package has a registry file
            registry_path = features_dir / name / f"{name}_tool_registry.py"
            if os.path.exists(registry_path):
                # Import the registry module to register the feature
                try:
                    logger.debug(f"Loading feature registry module: {name}_tool_registry.py")
                    importlib.import_module(f"pipedrive.api.features.{name}.{name}_tool_registry")
                    feature_count += 1
                except Exception as e:
                    logger.error(f"Error loading feature registry module for {name}: {e}")
    
    logger.info(f"Feature discovery complete. Found {feature_count} feature registry modules.")
    return feature_count