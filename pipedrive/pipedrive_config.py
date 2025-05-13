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
    verify_ssl: bool = Field(True, description="Whether to verify SSL certificates")

    # Logging settings
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
    def validate_api_token(cls, value):
        """
        Validate that API token is properly formatted.

        Requirements:
        - Must not be empty
        - Must be at least 10 characters long

        Raises:
            ValueError: If the API token is missing or too short
        """
        if not value or len(value) < 10:
            raise ValueError("API token is missing or too short")
        return value

    @field_validator('company_domain')
    @classmethod
    def validate_company_domain(cls, value):
        """
        Validate company domain format.

        Requirements:
        - Must not be empty
        - Must not contain a dot (.) to ensure domain is provided without TLD

        Raises:
            ValueError: If the company domain is invalid
        """
        if not value or "." in value:
            raise ValueError("Company domain should be provided without TLD (e.g., 'mycompany' not 'mycompany.pipedrive.com')")
        return value

    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, value):
        """
        Validate that base_url is a properly formatted URL.

        Requirements:
        - Must start with 'http://' or 'https://'

        Raises:
            ValueError: If the URL doesn't start with a proper protocol
        """
        if not value.startswith(('http://', 'https://')):
            raise ValueError("Base URL must begin with http:// or https://")
        return value

    @field_validator('timeout')
    @classmethod
    def validate_timeout(cls, value):
        """
        Validate timeout is positive.

        Requirements:
        - Must be greater than 0

        Raises:
            ValueError: If timeout is not positive
        """
        if value <= 0:
            raise ValueError("Timeout must be positive")
        return value

    @field_validator('retry_attempts')
    @classmethod
    def validate_retry_attempts(cls, value):
        """
        Validate retry attempts is reasonable.

        Requirements:
        - Must be non-negative
        - Must not exceed 10 (to prevent excessive retries)

        Raises:
            ValueError: If retry attempts is negative or exceeds maximum
        """
        if value < 0:
            raise ValueError("Retry attempts cannot be negative")
        if value > 10:
            raise ValueError("Retry attempts should not exceed 10")
        return value

    @field_validator('retry_backoff')
    @classmethod
    def validate_retry_backoff(cls, value):
        """
        Validate retry backoff factor is reasonable.

        Requirements:
        - Must be non-negative
        - Must not exceed 5 (to prevent excessive delays)

        Raises:
            ValueError: If backoff factor is negative or exceeds maximum
        """
        if value < 0:
            raise ValueError("Retry backoff factor cannot be negative")
        if value > 5:
            raise ValueError("Retry backoff factor should not exceed 5")
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
        - VERIFY_SSL: Optional (defaults to True)
        """
        # Safe conversion of numeric values with defaults
        try:
            timeout = int(os.getenv("PIPEDRIVE_TIMEOUT", "30"))
        except ValueError:
            timeout = 30

        try:
            retry_attempts = int(os.getenv("PIPEDRIVE_RETRY_ATTEMPTS", "3"))
        except ValueError:
            retry_attempts = 3

        try:
            retry_backoff = float(os.getenv("PIPEDRIVE_RETRY_BACKOFF", "0.5"))
        except ValueError:
            retry_backoff = 0.5

        return cls(
            api_token=os.getenv("PIPEDRIVE_API_TOKEN", ""),
            company_domain=os.getenv("PIPEDRIVE_COMPANY_DOMAIN", ""),
            base_url=os.getenv("PIPEDRIVE_BASE_URL", "https://api.pipedrive.com/v2"),
            timeout=timeout,
            retry_attempts=retry_attempts,
            retry_backoff=retry_backoff,
            verify_ssl=os.getenv("VERIFY_SSL", "true").lower() != "false",
            log_requests=os.getenv("PIPEDRIVE_LOG_REQUESTS", "").lower() == "true",
            log_responses=os.getenv("PIPEDRIVE_LOG_RESPONSES", "").lower() == "true",
        )


# Default settings instance from environment variables
settings = PipedriveSettings.from_env()