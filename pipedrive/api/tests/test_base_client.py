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
        assert client.base_url == "https://test.pipedrive.com/api/v2"
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
    
    @pytest.mark.asyncio
    async def test_request_success(self, mock_http_client):
        """Test successful API request"""
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
        assert call_args[0][1] == "https://test.pipedrive.com/api/v2/test"  # URL
        
        # Check query parameters
        assert call_args[1]["params"] == {"api_token": "test_token", "param1": "value1"}
        
        # Check JSON payload
        assert call_args[1]["json"] == {"field1": "value1"}
    
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