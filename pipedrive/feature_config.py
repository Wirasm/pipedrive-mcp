from typing import Dict, Any
import os
import json
from pathlib import Path
import logging

from log_config import logger
from pipedrive.api.features.tool_registry import registry

class FeatureConfig:
    """Configuration for Pipedrive API features"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize the feature configuration.
        
        Args:
            config_path: Path to the configuration file. If None, uses environment
                         variable FEATURE_CONFIG_PATH or a default path.
        """
        self.config_path = config_path or os.getenv(
            "FEATURE_CONFIG_PATH", 
            str(Path(__file__).parent / "feature_config.json")
        )
        self.load_config()
        
    def load_config(self) -> None:
        """
        Load feature configuration from file or environment variables.
        
        First checks for a configuration file. If not found or if there's an error,
        checks for environment variables in the format PIPEDRIVE_FEATURE_{FEATURE_ID}.
        If neither is found, creates a default configuration enabling all features.
        """
        # First try to load from file
        config_loaded = self._load_config_from_file()
        
        # If file loading failed or no features were enabled, try environment variables
        if not config_loaded:
            config_loaded = self._load_config_from_env()
            
        # If still no configuration, create default
        if not config_loaded:
            self._create_default_config()
    
    def _load_config_from_file(self) -> bool:
        """
        Load configuration from JSON file.
        
        Returns:
            bool: True if configuration was successfully loaded, False otherwise
        """
        if not os.path.exists(self.config_path):
            logger.debug(f"Feature config file not found at {self.config_path}")
            return False
            
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                
            # Enable features based on config
            features_enabled = False
            for feature_id, enabled in config.get("features", {}).items():
                if enabled:
                    try:
                        registry.enable_feature(feature_id)
                        features_enabled = True
                    except ValueError:
                        logger.warning(f"Feature {feature_id} from config is not registered")
                else:
                    registry.disable_feature(feature_id)
                    
            logger.info(f"Loaded feature configuration from {self.config_path}")
            return features_enabled
            
        except Exception as e:
            logger.error(f"Error loading feature config from file: {e}")
            return False
    
    def _load_config_from_env(self) -> bool:
        """
        Load configuration from environment variables.
        
        Environment variables are expected in the format PIPEDRIVE_FEATURE_{FEATURE_ID}=true|false
        
        Returns:
            bool: True if at least one feature was enabled, False otherwise
        """
        logger.debug("Checking environment variables for feature configuration")
        features_enabled = False
        
        # Get all registered features
        all_features = registry.get_all_features()
        
        # Check environment variables for each feature
        for feature_id in all_features:
            env_var = f"PIPEDRIVE_FEATURE_{feature_id.upper()}"
            env_value = os.getenv(env_var)
            
            if env_value is not None:
                # Convert string to boolean
                is_enabled = env_value.lower() in ("true", "1", "yes", "y", "on")
                
                if is_enabled:
                    try:
                        registry.enable_feature(feature_id)
                        features_enabled = True
                        logger.info(f"Enabled feature {feature_id} from environment variable {env_var}")
                    except ValueError:
                        logger.warning(f"Feature {feature_id} from environment is not registered")
                else:
                    registry.disable_feature(feature_id)
                    logger.info(f"Disabled feature {feature_id} from environment variable {env_var}")
                    
        return features_enabled
    
    def _create_default_config(self) -> None:
        """
        Create default configuration enabling all features.
        
        Writes the configuration to the config file and enables all features.
        """
        logger.info("Creating default feature configuration (all features enabled)")
        
        config = {
            "features": {
                feature_id: True for feature_id in registry.get_all_features()
            }
        }
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        try:
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logger.error(f"Error creating default feature config file: {e}")
            
        # Enable all features by default
        for feature_id in registry.get_all_features():
            try:
                registry.enable_feature(feature_id)
            except ValueError:
                pass  # Skip if already enabled
            
    def get_enabled_features(self) -> Dict[str, Any]:
        """Get all enabled features"""
        return registry.get_enabled_features()
    
    def to_json(self) -> str:
        """
        Convert current feature configuration to JSON string.
        
        Returns:
            JSON string representation of the configuration
        """
        all_features = registry.get_all_features()
        config = {
            "features": {
                feature_id: registry.is_feature_enabled(feature_id)
                for feature_id in all_features
            }
        }
        return json.dumps(config, indent=2)
    
    def save_config(self) -> bool:
        """
        Save current feature configuration to file.
        
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            config = {
                "features": {
                    feature_id: registry.is_feature_enabled(feature_id)
                    for feature_id in registry.get_all_features()
                }
            }
            
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
                
            logger.info(f"Saved feature configuration to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving feature configuration: {e}")
            return False