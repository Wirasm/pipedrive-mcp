# Project Renovation Proposal: Configuration Consolidation

## Summary

This PRP proposes a consolidation of configuration management in the MCP Pipedrive project to improve maintainability, discoverability, and consistency of configuration options.

## Problem Statement

Currently, configuration is managed through multiple mechanisms:

1. Environment variables are loaded in several different files:
   - `server.py`
   - `pipedrive/mcp_instance.py`
   - `pipedrive/pipedrive_config.py`
   - `pipedrive/feature_config.py`

2. Configuration settings are not uniformly documented:
   - Some are only documented in code comments
   - Some are documented in the `.env.example` file
   - The README does not have a comprehensive list of configuration options

3. Different settings use different naming conventions and loading patterns:
   - Some settings use boolean string conversion with different approaches
   - Some use numeric conversion with different approaches
   - Feature flags follow a separate pattern from other settings

4. The `.env.example` file is incomplete and doesn't list all available options.

## Proposed Solution

### 1. Create a Unified Configuration System

Create a single `AppConfig` class that:
- Consolidates all configuration from all sources
- Provides a uniform interface for accessing config values
- Properly validates and documents all settings
- Follows consistent patterns for environment variable loading

### 2. Implementation Details

#### 2.1 Create a new `app_config.py` file

```python
"""
Application Configuration Module

This module provides a centralized configuration system for the entire application.
It consolidates all settings from environment variables and configuration files.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, Set
from pydantic import BaseModel, Field, field_validator, model_validator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ServerConfig(BaseModel):
    """Server configuration settings"""
    host: str = Field("127.0.0.1", description="Host address to bind the server to")
    port: int = Field(8152, description="Port number to run the server on")
    transport: str = Field("sse", description="Transport protocol (sse or stdio)")
    container_mode: bool = Field(False, description="Whether running in container mode")
    
    @field_validator('transport')
    @classmethod
    def validate_transport(cls, v):
        if v not in ["sse", "stdio"]:
            raise ValueError("Transport must be either 'sse' or 'stdio'")
        return v

class PipedriveConfig(BaseModel):
    """Pipedrive API configuration settings"""
    api_token: str = Field(..., description="Pipedrive API token for authentication")
    company_domain: str = Field(..., description="Pipedrive company domain (e.g., 'mycompany')")
    base_url: str = Field("https://api.pipedrive.com/v2", description="Base URL for Pipedrive API")
    timeout: int = Field(30, description="Request timeout in seconds")
    retry_attempts: int = Field(3, description="Number of retry attempts for failed requests")
    retry_backoff: float = Field(0.5, description="Exponential backoff factor for retries")
    verify_ssl: bool = Field(True, description="Whether to verify SSL certificates")
    log_requests: bool = Field(False, description="Whether to log API requests")
    log_responses: bool = Field(False, description="Whether to log API responses")
    
    @property
    def api_url(self) -> str:
        """
        Construct the full API URL with the company domain.
        Returns:
            str: The complete API URL including company domain
        """
        return f"https://{self.company_domain}.pipedrive.com/api/v2"
    
    @field_validator('api_token')
    @classmethod
    def validate_api_token(cls, v):
        if not v or len(v) < 10:
            raise ValueError("API token is missing or too short")
        return v
    
    @field_validator('company_domain')
    @classmethod
    def validate_company_domain(cls, v):
        if not v or "." in v:
            raise ValueError("Company domain should be provided without TLD")
        return v
    
    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError("Base URL must begin with http:// or https://")
        return v

class FeatureConfig(BaseModel):
    """Feature flag configuration"""
    persons: bool = Field(True, description="Enable Persons feature")
    organizations: bool = Field(True, description="Enable Organizations feature")
    deals: bool = Field(True, description="Enable Deals feature")
    leads: bool = Field(True, description="Enable Leads feature")
    item_search: bool = Field(True, description="Enable Item Search feature")
    activities: bool = Field(True, description="Enable Activities feature")
    
    config_path: Optional[str] = Field(None, description="Path to feature configuration file")
    
    def get_enabled_features(self) -> Set[str]:
        """Get a set of enabled feature IDs"""
        return {feature for feature, enabled in self.model_dump().items() 
                if enabled and feature != "config_path"}

class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = Field("INFO", description="Logging level")
    format: str = Field("%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s", 
                        description="Log message format")
    date_format: str = Field("%Y-%m-%d %H:%M:%S", description="Date format for log messages")
    
    @field_validator('level')
    @classmethod
    def validate_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {', '.join(valid_levels)}")
        return v.upper()

class AppConfig(BaseModel):
    """
    Application-wide configuration that consolidates all settings.
    This is the main configuration class that should be used throughout the application.
    """
    server: ServerConfig = Field(default_factory=ServerConfig)
    pipedrive: PipedriveConfig
    features: FeatureConfig = Field(default_factory=FeatureConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    @classmethod
    def from_env(cls):
        """
        Create configuration from environment variables.
        Returns an instance of AppConfig with all settings loaded from environment variables.
        """
        # Helper functions to safely convert environment variables
        def get_bool(name, default=False):
            value = os.getenv(name, "").lower()
            if value in ("true", "1", "yes", "y", "on"):
                return True
            if value in ("false", "0", "no", "n", "off"):
                return False
            return default
            
        def get_int(name, default):
            try:
                return int(os.getenv(name, default))
            except ValueError:
                return default
                
        def get_float(name, default):
            try:
                return float(os.getenv(name, default))
            except ValueError:
                return default
                
        # Load server configuration
        server_config = ServerConfig(
            host=os.getenv("HOST", "127.0.0.1"),
            port=get_int("PORT", 8152),
            transport=os.getenv("TRANSPORT", "sse"),
            container_mode=get_bool("CONTAINER_MODE")
        )
        
        # Determine host based on container mode
        if server_config.container_mode:
            server_config.host = "0.0.0.0"
        
        # Load Pipedrive configuration
        try:
            pipedrive_config = PipedriveConfig(
                api_token=os.getenv("PIPEDRIVE_API_TOKEN", ""),
                company_domain=os.getenv("PIPEDRIVE_COMPANY_DOMAIN", ""),
                base_url=os.getenv("PIPEDRIVE_BASE_URL", "https://api.pipedrive.com/v2"),
                timeout=get_int("PIPEDRIVE_TIMEOUT", 30),
                retry_attempts=get_int("PIPEDRIVE_RETRY_ATTEMPTS", 3),
                retry_backoff=get_float("PIPEDRIVE_RETRY_BACKOFF", 0.5),
                verify_ssl=get_bool("VERIFY_SSL", True),
                log_requests=get_bool("PIPEDRIVE_LOG_REQUESTS", False),
                log_responses=get_bool("PIPEDRIVE_LOG_RESPONSES", False)
            )
        except ValueError as e:
            # Handle required fields error more gracefully
            raise ValueError(f"Pipedrive configuration error: {str(e)}")
        
        # Load feature configuration
        feature_config = FeatureConfig(
            persons=get_bool("PIPEDRIVE_FEATURE_PERSONS", True),
            organizations=get_bool("PIPEDRIVE_FEATURE_ORGANIZATIONS", True),
            deals=get_bool("PIPEDRIVE_FEATURE_DEALS", True),
            leads=get_bool("PIPEDRIVE_FEATURE_LEADS", True),
            item_search=get_bool("PIPEDRIVE_FEATURE_ITEM_SEARCH", True),
            activities=get_bool("PIPEDRIVE_FEATURE_ACTIVITIES", True),
            config_path=os.getenv("FEATURE_CONFIG_PATH")
        )
        
        # Load logging configuration
        logging_config = LoggingConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            format=os.getenv("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s"),
            date_format=os.getenv("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
        )
        
        return cls(
            server=server_config,
            pipedrive=pipedrive_config,
            features=feature_config,
            logging=logging_config
        )
    
    def save_to_file(self, file_path: str) -> bool:
        """
        Save current configuration to a JSON file.
        Args:
            file_path: Path to the JSON file to save
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            data = self.model_dump()
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
            
    @classmethod
    def load_from_file(cls, file_path: str) -> Optional['AppConfig']:
        """
        Load configuration from a JSON file.
        Args:
            file_path: Path to the JSON file to load
        Returns:
            Optional[AppConfig]: Configuration instance or None if loading fails
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            return cls(**data)
        except Exception:
            return None

# Create a global instance of the configuration
config = AppConfig.from_env()
```

#### 2.2 Update the .env.example file

```
# Server configuration
HOST=127.0.0.1                 # Host address to bind the server to (127.0.0.1 for local, 0.0.0.0 for containers)
PORT=8152                      # Port number to run the server on
TRANSPORT=sse                  # Transport protocol (sse or stdio)
CONTAINER_MODE=false           # Whether running in container mode (true/false)

# Pipedrive API credentials
PIPEDRIVE_API_TOKEN=your_api_token_here           # Your Pipedrive API token
PIPEDRIVE_COMPANY_DOMAIN=your_company_subdomain   # Only the subdomain part (e.g., "mycompany" from mycompany.pipedrive.com)

# Pipedrive API settings
PIPEDRIVE_BASE_URL=https://api.pipedrive.com/v2   # Base URL for Pipedrive API
PIPEDRIVE_TIMEOUT=30                              # Request timeout in seconds
PIPEDRIVE_RETRY_ATTEMPTS=3                        # Number of retry attempts for failed requests
PIPEDRIVE_RETRY_BACKOFF=0.5                       # Exponential backoff factor for retries
VERIFY_SSL=true                                   # Whether to verify SSL certificates (true/false)
PIPEDRIVE_LOG_REQUESTS=false                      # Whether to log API requests (true/false)
PIPEDRIVE_LOG_RESPONSES=false                     # Whether to log API responses (true/false)

# Feature flags - control which features are enabled
PIPEDRIVE_FEATURE_PERSONS=true                    # Enable/disable Persons feature
PIPEDRIVE_FEATURE_ORGANIZATIONS=true              # Enable/disable Organizations feature
PIPEDRIVE_FEATURE_DEALS=true                      # Enable/disable Deals feature
PIPEDRIVE_FEATURE_LEADS=true                      # Enable/disable Leads feature
PIPEDRIVE_FEATURE_ITEM_SEARCH=true                # Enable/disable Item Search feature
PIPEDRIVE_FEATURE_ACTIVITIES=true                 # Enable/disable Activities feature
FEATURE_CONFIG_PATH=                              # Path to feature configuration file (optional)

# Logging settings
LOG_LEVEL=INFO                                    # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_FORMAT="%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s"  # Log message format
LOG_DATE_FORMAT="%Y-%m-%d %H:%M:%S"               # Date format for log messages
```

#### 2.3 Modify Server Initialization

Update `server.py` to use the new unified configuration:

```python
import asyncio
from dotenv import load_dotenv

from log_config import logger
from app_config import config
from pipedrive.api.features.tool_registry import registry
from pipedrive.api.features import discover_features
from pipedrive.api.pipedrive_context import pipedrive_lifespan
from pipedrive.mcp_instance import mcp

load_dotenv()

# Discover and register all features
discover_features()

# Enable features based on configuration
for feature_name in config.features.get_enabled_features():
    try:
        registry.enable_feature(feature_name)
    except ValueError:
        logger.warning(f"Feature {feature_name} is enabled in config but not registered")

async def main():
    # Log enabled features
    enabled_features = registry.get_enabled_features()
    logger.info(f"Enabled features: {', '.join(enabled_features.keys())}")
    
    # Log registered tools
    tool_count = registry.get_tool_count()
    logger.info(f"Registered tools: {tool_count}")
    
    logger.info(
        f"Starting Pipedrive MCP server. Transport: {config.server.transport}, "
        f"Host: {config.server.host}, Port: {config.server.port}"
    )
    
    if config.server.transport == "sse":
        await mcp.run_sse_async()
    else:
        logger.info(
            "Stdio transport selected. Ensure your FastMCP setup supports this or modify."
        )
        if hasattr(mcp, "run_stdio_async"):
            await mcp.run_stdio_async()
        else:
            logger.warning(
                "run_stdio_async method not found on mcp object. Defaulting to SSE behavior."
            )
            await mcp.run_sse_async()


if __name__ == "__main__":
    asyncio.run(main())
```

#### 2.4 Update MCP Instance

Update `pipedrive/mcp_instance.py` to use the new configuration:

```python
from mcp.server.fastmcp import FastMCP
from app_config import config
from .api.pipedrive_context import pipedrive_lifespan  # Relative import

# Create the FastMCP instance
mcp = FastMCP(
    "mcp-pipedrive",
    description="MCP server for Pipedrive API v2",
    lifespan=pipedrive_lifespan,
    host=config.server.host,
    port=config.server.port,
)
```

#### 2.5 Update Logging Configuration

Update `log_config.py` to use the new configuration:

```python
import logging
from app_config import config

# --- Configure Logging ---
logging.basicConfig(
    level=getattr(logging, config.logging.level),
    format=config.logging.format,
    datefmt=config.logging.date_format,
)
logger = logging.getLogger(__name__)
```

#### 2.6 Update Pipedrive Context

Update `pipedrive/api/pipedrive_context.py` to use the new configuration:

```python
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator

import httpx
from mcp.server.fastmcp import FastMCP

from log_config import logger
from app_config import config
from pipedrive.api.pipedrive_client import PipedriveClient


@dataclass
class PipedriveMCPContext:
    pipedrive_client: PipedriveClient


@asynccontextmanager
async def pipedrive_lifespan(server: FastMCP) -> AsyncIterator[PipedriveMCPContext]:
    logger.info("Attempting to initialize Pipedrive MCP Context...")

    # Use the config singleton to get configuration
    if not config.pipedrive.verify_ssl:
        logger.warning("SSL verification is disabled. This should only be used in development environments.")

    async with httpx.AsyncClient(timeout=config.pipedrive.timeout, verify=config.pipedrive.verify_ssl) as client:
        pd_client = PipedriveClient(
            api_token=config.pipedrive.api_token,
            company_domain=config.pipedrive.company_domain,
            http_client=client,
        )
        mcp_context = PipedriveMCPContext(pipedrive_client=pd_client)
        try:
            logger.info("Pipedrive MCP Context initialized successfully.")
            yield mcp_context
        finally:
            logger.info("Pipedrive MCP Context cleaned up.")
```

### 3. Benefits

1. **Centralized Configuration**: All configuration is managed in one place
2. **Consistent API**: All parts of the application use the same pattern to access config
3. **Strong Validation**: All configuration options are validated with proper error messages
4. **Self-Documentation**: The configuration itself documents what options are available
5. **Type Safety**: The use of Pydantic ensures type safety for configuration values
6. **Improved Maintainability**: Changes to configuration are made in one place
7. **Better Developer Experience**: New developers can easily understand available options
8. **Feature Flag System**: The feature flag system is integrated with the main config

### 4. Implementation Plan

1. Create the `app_config.py` file
2. Update the `.env.example` file with all configuration options
3. Modify `server.py` to use the new configuration
4. Update `mcp_instance.py` to use the new configuration
5. Update `log_config.py` to use the new configuration
6. Update `pipedrive_context.py` to use the new configuration
7. Phase out the old configuration files
8. Update the README to document the new configuration system

