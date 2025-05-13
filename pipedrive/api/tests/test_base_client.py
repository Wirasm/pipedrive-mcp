import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
import json

from pipedrive.api.base_client import BaseClient
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_http_client():
    """Create a mock httpx.AsyncClient"""
    client = AsyncMock(spec=httpx.AsyncClient)
    
    # Set up mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"success":true,"data":{"id":123,"name":"Test"}}'
    mock_response.json.return_value = {"success": True, "data": {"id": 123, "name": "Test"}}
    client.request.return_value = mock_response
    
    return client


class TestBaseClient:
    """Tests for the BaseClient class"""
    
    def test_init_with_valid_params(self, mock_http_client):
        """Test initializing with valid parameters"""
        client = BaseClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        assert client.api_token == "test_token"
        assert client.domain == "https://test.pipedrive.com"
        assert client.api_version == "v2"  # Default version should be v2
        assert client.http_client == mock_http_client
    
    def test_init_with_invalid_params(self, mock_http_client):
        """Test initializing with invalid parameters"""
        # Test missing API token
        with pytest.raises(ValueError, match="Pipedrive API token is required"):
            BaseClient(
                api_token="",
                company_domain="test",
                http_client=mock_http_client
            )
        
        # Test missing company domain
        with pytest.raises(ValueError, match="Pipedrive company domain is required"):
            BaseClient(
                api_token="test_token",
                company_domain="",
                http_client=mock_http_client
            )
        
        # Test missing HTTP client
        with pytest.raises(ValueError, match="httpx.AsyncClient is required"):
            BaseClient(
                api_token="test_token",
                company_domain="test",
                http_client=None
            )
    
    def test_get_url(self, mock_http_client):
        """Test URL construction with different API versions"""
        client = BaseClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        # Test v2 URL construction (default)
        assert client.get_url("/deals") == "https://test.pipedrive.com/api/v2/deals"
        
        # Test v1 URL construction
        assert client.get_url("/leads", "v1") == "https://test.pipedrive.com/v1/leads"
        
        # Test explicitly specifying v2
        assert client.get_url("/persons", "v2") == "https://test.pipedrive.com/api/v2/persons"
        
        # Test invalid version
        with pytest.raises(ValueError, match="Unsupported API version"):
            client.get_url("/test", "v3")
    
    @pytest.mark.asyncio
    async def test_request_success_default_version(self, mock_http_client):
        """Test successful API request with default version (v2)"""
        client = BaseClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        result = await client.request(
            method="GET",
            endpoint="/test",
            query_params={"param1": "value1"},
            json_payload={"field1": "value1"}
        )
        
        # Check result
        assert result == {"success": True, "data": {"id": 123, "name": "Test"}}
        
        # Check that client.request was called with correct parameters
        mock_http_client.request.assert_called_once()
        call_args = mock_http_client.request.call_args
        assert call_args[0][0] == "GET"  # Method
        assert call_args[0][1] == "https://test.pipedrive.com/api/v2/test"  # URL with v2
        
        # Check query parameters
        assert call_args[1]["params"] == {"api_token": "test_token", "param1": "value1"}
        
        # Check JSON payload
        assert call_args[1]["json"] == {"field1": "value1"}
    
    @pytest.mark.asyncio
    async def test_request_success_v1_version(self, mock_http_client):
        """Test successful API request with v1 version"""
        client = BaseClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        result = await client.request(
            method="GET",
            endpoint="/leads",
            query_params={"param1": "value1"},
            json_payload={"field1": "value1"},
            version="v1"  # Explicitly use v1
        )
        
        # Check result
        assert result == {"success": True, "data": {"id": 123, "name": "Test"}}
        
        # Check that client.request was called with correct parameters
        mock_http_client.request.assert_called_once()
        call_args = mock_http_client.request.call_args
        assert call_args[0][0] == "GET"  # Method
        assert call_args[0][1] == "https://test.pipedrive.com/v1/leads"  # URL with v1
        
        # Check query parameters
        assert call_args[1]["params"] == {"api_token": "test_token", "param1": "value1"}
        
        # Check JSON payload
        assert call_args[1]["json"] == {"field1": "value1"}
    
    @pytest.mark.asyncio
    async def test_request_with_changed_default_version(self, mock_http_client):
        """Test request with a changed default API version"""
        client = BaseClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        # Change default API version to v1
        client.api_version = "v1"
        
        result = await client.request(
            method="GET",
            endpoint="/leads"
            # No version specified, should use default
        )
        
        # Check that URL used the correct version
        call_args = mock_http_client.request.call_args
        assert call_args[0][1] == "https://test.pipedrive.com/v1/leads"  # URL with v1
    
    @pytest.mark.asyncio
    async def test_request_api_error(self, mock_http_client):
        """Test handling API error response"""
        # Set up mock response with API error
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"success":false,"error":"API Error","error_info":"Additional info"}'
        mock_response.json.return_value = {
            "success": False,
            "error": "API Error",
            "error_info": "Additional info"
        }
        mock_http_client.request.return_value = mock_response

        client = BaseClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )

        # Test that API error is raised
        with pytest.raises(PipedriveAPIError) as exc_info:
            await client.request(method="GET", endpoint="/test")

        # Check exception details
        assert "API Error" in str(exc_info.value)
        # The inner error details are part of the message, not the exception attributes
        assert "Additional info" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_request_http_error(self, mock_http_client):
        """Test handling HTTP error response"""
        # Set up mock response with HTTP error
        error_response = MagicMock()
        error_response.text = '{"error":"Not Found"}'
        error_response.json.return_value = {"error": "Not Found"}
        error_response.status_code = 404
        
        http_error = httpx.HTTPStatusError(
            "404 Not Found",
            request=MagicMock(),
            response=error_response
        )
        mock_http_client.request.side_effect = http_error
        
        client = BaseClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        # Test that HTTP error is raised as PipedriveAPIError
        with pytest.raises(PipedriveAPIError) as exc_info:
            await client.request(method="GET", endpoint="/test")
        
        # Check exception details
        assert "404" in str(exc_info.value)
        assert exc_info.value.status_code == 404