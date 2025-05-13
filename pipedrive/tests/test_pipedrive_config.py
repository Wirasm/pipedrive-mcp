import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from pipedrive.pipedrive_config import PipedriveSettings


class TestPipedriveSettings:
    """Tests for the PipedriveSettings Pydantic model."""

    def test_default_values(self):
        """Test default values are correctly set."""
        # Mandatory fields provided
        settings = PipedriveSettings(
            api_token="test_token_12345678901234567890", company_domain="testcompany"
        )

        # Check default values
        assert settings.base_url == "https://api.pipedrive.com/v2"
        assert settings.timeout == 30
        assert settings.retry_attempts == 3
        assert settings.retry_backoff == 0.5
        assert settings.verify_ssl is True
        assert settings.log_requests is False
        assert settings.log_responses is False

    def test_api_url_property(self):
        """Test that api_url property constructs URL correctly."""
        settings = PipedriveSettings(
            api_token="test_token_12345678901234567890", company_domain="testcompany"
        )

        expected_url = "https://testcompany.pipedrive.com/api/v2"
        assert settings.api_url == expected_url

    def test_api_token_validation(self):
        """Test validation for api_token field."""
        # Short token
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(api_token="short", company_domain="testcompany")

        assert "API token is missing or too short" in str(excinfo.value)

        # Empty token
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(api_token="", company_domain="testcompany")

        assert "API token is missing or too short" in str(excinfo.value)

    def test_company_domain_validation(self):
        """Test validation for company_domain field."""
        # Invalid domain with TLD
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(
                api_token="test_token_12345678901234567890",
                company_domain="testcompany.pipedrive.com",
            )

        assert "Company domain should be provided without TLD" in str(excinfo.value)

        # Empty domain
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(
                api_token="test_token_12345678901234567890", company_domain=""
            )

        assert "Company domain should be provided without TLD" in str(excinfo.value)

    def test_base_url_validation(self):
        """Test validation for base_url field."""
        # Invalid URL without protocol
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(
                api_token="test_token_12345678901234567890",
                company_domain="testcompany",
                base_url="api.example.com",
            )

        assert "Base URL must begin with http:// or https://" in str(excinfo.value)

    def test_timeout_validation(self):
        """Test validation for timeout field."""
        # Negative timeout
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(
                api_token="test_token_12345678901234567890",
                company_domain="testcompany",
                timeout=-1,
            )

        assert "Timeout must be positive" in str(excinfo.value)

        # Zero timeout
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(
                api_token="test_token_12345678901234567890",
                company_domain="testcompany",
                timeout=0,
            )

        assert "Timeout must be positive" in str(excinfo.value)

    def test_retry_attempts_validation(self):
        """Test validation for retry_attempts field."""
        # Negative retry attempts
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(
                api_token="test_token_12345678901234567890",
                company_domain="testcompany",
                retry_attempts=-1,
            )

        assert "Retry attempts cannot be negative" in str(excinfo.value)

        # Excessive retry attempts
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(
                api_token="test_token_12345678901234567890",
                company_domain="testcompany",
                retry_attempts=11,
            )

        assert "Retry attempts should not exceed 10" in str(excinfo.value)

    def test_retry_backoff_validation(self):
        """Test validation for retry_backoff field."""
        # Negative backoff factor
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(
                api_token="test_token_12345678901234567890",
                company_domain="testcompany",
                retry_backoff=-0.1,
            )

        assert "Retry backoff factor cannot be negative" in str(excinfo.value)

        # Excessive backoff factor
        with pytest.raises(ValidationError) as excinfo:
            PipedriveSettings(
                api_token="test_token_12345678901234567890",
                company_domain="testcompany",
                retry_backoff=5.1,
            )

        assert "Retry backoff factor should not exceed 5" in str(excinfo.value)

    @patch.dict(
        os.environ,
        {
            "PIPEDRIVE_API_TOKEN": "test_token_12345678901234567890",
            "PIPEDRIVE_COMPANY_DOMAIN": "envtestcompany",
            "PIPEDRIVE_BASE_URL": "https://custom.api.com",
            "PIPEDRIVE_TIMEOUT": "60",
            "PIPEDRIVE_RETRY_ATTEMPTS": "5",
            "PIPEDRIVE_RETRY_BACKOFF": "2.0",
            "VERIFY_SSL": "false",
            "PIPEDRIVE_LOG_REQUESTS": "true",
            "PIPEDRIVE_LOG_RESPONSES": "true",
        },
    )
    def test_from_env_with_all_env_vars(self):
        """Test from_env method with all environment variables set."""
        settings = PipedriveSettings.from_env()

        assert settings.api_token == "test_token_12345678901234567890"
        assert settings.company_domain == "envtestcompany"
        assert settings.base_url == "https://custom.api.com"
        assert settings.timeout == 60
        assert settings.retry_attempts == 5
        assert settings.retry_backoff == 2.0
        assert settings.verify_ssl is False
        assert settings.log_requests is True
        assert settings.log_responses is True

    @patch.dict(
        os.environ,
        {
            "PIPEDRIVE_API_TOKEN": "test_token_12345678901234567890",
            "PIPEDRIVE_COMPANY_DOMAIN": "envtestcompany",
            "PIPEDRIVE_TIMEOUT": "invalid",
            "PIPEDRIVE_RETRY_ATTEMPTS": "not_a_number",
            "PIPEDRIVE_RETRY_BACKOFF": "bad_float",
        },
    )
    def test_from_env_with_invalid_numeric_values(self):
        """Test from_env handles invalid numeric environment variables."""
        settings = PipedriveSettings.from_env()

        # Should use default values when conversion fails
        assert settings.timeout == 30
        assert settings.retry_attempts == 3
        assert settings.retry_backoff == 0.5

    @patch.dict(
        os.environ,
        {
            "PIPEDRIVE_API_TOKEN": "test_token_12345678901234567890",
            "PIPEDRIVE_COMPANY_DOMAIN": "envtestcompany",
        },
    )
    def test_from_env_with_minimal_env_vars(self):
        """Test from_env method with only required environment variables set."""
        settings = PipedriveSettings.from_env()

        # Explicit values from environment
        assert settings.api_token == "test_token_12345678901234567890"
        assert settings.company_domain == "envtestcompany"

        # Default values for missing environment variables
        assert settings.base_url == "https://api.pipedrive.com/v2"
        assert settings.timeout == 30
        assert settings.retry_attempts == 3
        assert settings.retry_backoff == 0.5
        assert settings.verify_ssl is True
        assert settings.log_requests is False
        assert settings.log_responses is False
