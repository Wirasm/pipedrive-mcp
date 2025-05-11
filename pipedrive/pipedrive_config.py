"""
Pipedrive Configuration Module

This module provides centralized configuration management for Pipedrive API interactions.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class PipedriveSettings(BaseModel):
    """
    Pydantic model for Pipedrive API configuration settings.
    
    This class centralizes all configuration values for Pipedrive API access
    and provides validation and default values.
    """
    
    # Required settings
    api_token: str = Field(..., description="Pipedrive API token for authentication")
    company_domain: str = Field(..., description="Pipedrive company domain (e.g., 'mycompany')")
    
    # Optional settings with defaults
    base_url: str = Field("https://api.pipedrive.com/v2", description="Base URL for Pipedrive API")
    timeout: int = Field(30, description="Request timeout in seconds")
    retry_attempts: int = Field(3, description="Number of retry attempts for failed requests")
    retry_backoff: float = Field(0.5, description="Exponential backoff factor for retries")
    
    # Logging settings
    log_requests: bool = Field(False, description="Whether to log API requests")
    log_responses: bool = Field(False, description="Whether to log API responses")
    
    @field_validator('api_token')
    @classmethod
    def validate_api_token(cls, value):
        """Validate that API token is properly formatted."""
        if not value or len(value) < 10:
            raise ValueError("API token is missing or too short")
        return value

    @field_validator('company_domain')
    @classmethod
    def validate_company_domain(cls, value):
        """Validate company domain format."""
        if not value or "." in value:
            raise ValueError("Company domain should be provided without TLD (e.g., 'mycompany' not 'mycompany.pipedrive.com')")
        return value
    
    @classmethod
    def from_env(cls):
        """
        Create settings from environment variables.
        
        Uses the following environment variables:
        - PIPEDRIVE_API_TOKEN: Required
        - PIPEDRIVE_COMPANY_DOMAIN: Required
        - PIPEDRIVE_BASE_URL: Optional
        - PIPEDRIVE_TIMEOUT: Optional
        - PIPEDRIVE_RETRY_ATTEMPTS: Optional
        - PIPEDRIVE_RETRY_BACKOFF: Optional
        - PIPEDRIVE_LOG_REQUESTS: Optional
        - PIPEDRIVE_LOG_RESPONSES: Optional
        """
        return cls(
            api_token=os.getenv("PIPEDRIVE_API_TOKEN", ""),
            company_domain=os.getenv("PIPEDRIVE_COMPANY_DOMAIN", ""),
            base_url=os.getenv("PIPEDRIVE_BASE_URL", "https://api.pipedrive.com/v2"),
            timeout=int(os.getenv("PIPEDRIVE_TIMEOUT", "30")),
            retry_attempts=int(os.getenv("PIPEDRIVE_RETRY_ATTEMPTS", "3")),
            retry_backoff=float(os.getenv("PIPEDRIVE_RETRY_BACKOFF", "0.5")),
            log_requests=os.getenv("PIPEDRIVE_LOG_REQUESTS", "").lower() == "true",
            log_responses=os.getenv("PIPEDRIVE_LOG_RESPONSES", "").lower() == "true",
        )


# Default settings instance from environment variables
settings = PipedriveSettings.from_env()