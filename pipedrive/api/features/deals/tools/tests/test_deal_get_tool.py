import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

from pipedrive.api.features.deals.tools.deal_get_tool import get_deal_from_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class TestGetDealTool:
    """Test suite for the get_deal_from_pipedrive tool"""

    @pytest.fixture
    def mock_context(self):
        """Fixture for mock MCP context"""
        context = MagicMock(spec=Context)
        pipedrive_client = MagicMock()
        pipedrive_client.deals = MagicMock()
        pipedrive_client.deals.get_deal = AsyncMock()

        # Set up the context to return our mock pipedrive client
        context.request_context.lifespan_context.pipedrive_client = pipedrive_client

        return context

    @pytest.mark.asyncio
    async def test_get_deal_success(self, mock_context):
        """Test successful deal retrieval"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "title": "Test Deal",
            "value": 1000,
            "currency": "USD",
            "status": "open",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.get_deal.return_value = mock_response

        # Call the tool
        result = await get_deal_from_pipedrive(mock_context, id_str="123")

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["id"] == 123
        assert response["data"]["title"] == "Test Deal"
        assert response["data"]["value"] == 1000
        assert response["data"]["currency"] == "USD"
        assert response["data"]["status"] == "open"

        # Verify that get_deal was called with correct arguments
        get_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.get_deal
        get_deal_mock.assert_called_once_with(
            deal_id=123, include_fields=None, custom_fields_keys=None
        )

    @pytest.mark.asyncio
    async def test_get_deal_with_include_fields(self, mock_context):
        """Test getting a deal with include_fields parameter"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "title": "Test Deal",
            "products_count": 2,
            "files_count": 5,
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.get_deal.return_value = mock_response

        # Call the tool with include_fields
        result = await get_deal_from_pipedrive(
            mock_context, id_str="123", include_fields_str="products_count,files_count"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["id"] == 123
        assert response["data"]["title"] == "Test Deal"
        assert response["data"]["products_count"] == 2
        assert response["data"]["files_count"] == 5

        # Verify that get_deal was called with correct arguments
        get_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.get_deal
        get_deal_mock.assert_called_once_with(
            deal_id=123,
            include_fields=["products_count", "files_count"],
            custom_fields_keys=None,
        )

    @pytest.mark.asyncio
    async def test_get_deal_with_custom_fields(self, mock_context):
        """Test getting a deal with custom_fields parameter"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "title": "Test Deal",
            "custom_field1": "value1",
            "custom_field2": "value2",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.get_deal.return_value = mock_response

        # Call the tool with custom_fields
        result = await get_deal_from_pipedrive(
            mock_context, id_str="123", custom_fields_str="custom_field1,custom_field2"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["id"] == 123
        assert response["data"]["title"] == "Test Deal"
        assert response["data"]["custom_field1"] == "value1"
        assert response["data"]["custom_field2"] == "value2"

        # Verify that get_deal was called with correct arguments
        get_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.get_deal
        get_deal_mock.assert_called_once_with(
            deal_id=123,
            include_fields=None,
            custom_fields_keys=["custom_field1", "custom_field2"],
        )

    @pytest.mark.asyncio
    async def test_get_deal_invalid_id(self, mock_context):
        """Test getting a deal with invalid ID format"""
        # Call the tool with invalid ID
        result = await get_deal_from_pipedrive(mock_context, id_str="not_a_number")

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid deal_id format" in response["error"]

        # Verify that get_deal was not called
        get_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.get_deal
        get_deal_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_deal_api_error(self, mock_context):
        """Test handling of API errors"""
        # Set up the mock to raise an API error
        error_data = {
            "success": False,
            "error": "API Error",
            "error_info": "Deal not found",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.get_deal.side_effect = PipedriveAPIError(
            message="API Error: Deal not found",
            status_code=404,
            error_info="Deal not found",
            response_data=error_data,
        )

        # Call the tool
        result = await get_deal_from_pipedrive(mock_context, id_str="999")

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "API Error: Deal not found" in response["error"]
        assert response["data"] == error_data
