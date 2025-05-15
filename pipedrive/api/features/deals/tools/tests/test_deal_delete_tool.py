import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp.server.fastmcp import Context

from pipedrive.api.features.deals.tools.deal_delete_tool import (
    delete_deal_from_pipedrive,
)
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class TestDeleteDealTool:
    """Test suite for the delete_deal_from_pipedrive tool"""

    @pytest.fixture
    def mock_context(self):
        """Fixture for mock MCP context"""
        context = MagicMock(spec=Context)
        pipedrive_client = MagicMock()
        pipedrive_client.deals = MagicMock()
        pipedrive_client.deals.delete_deal = AsyncMock()

        # Set up the context to return our mock pipedrive client
        context.request_context.lifespan_context.pipedrive_client = pipedrive_client

        return context

    @pytest.mark.asyncio
    async def test_delete_deal_success(self, mock_context):
        """Test successful deal deletion"""
        # Set up the mock to return a successful response
        mock_response = {"id": 123}
        mock_context.request_context.lifespan_context.pipedrive_client.deals.delete_deal.return_value = mock_response

        # Call the tool
        result = await delete_deal_from_pipedrive(mock_context, id_str="123")

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["id"] == 123

        # Verify that delete_deal was called with correct arguments
        delete_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.delete_deal
        delete_deal_mock.assert_called_once_with(deal_id=123)

    @pytest.mark.asyncio
    async def test_delete_deal_invalid_id(self, mock_context):
        """Test deleting a deal with invalid ID format"""
        # Call the tool with invalid ID
        result = await delete_deal_from_pipedrive(mock_context, id_str="not_a_number")

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "deal_id must be a numeric string" in response["error"]

        # Verify that delete_deal was not called
        delete_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.delete_deal
        delete_deal_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_deal_api_error(self, mock_context):
        """Test handling of API errors"""
        # Set up the mock to raise an API error
        error_data = {
            "success": False,
            "error": "API Error",
            "error_info": "Deal not found",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.delete_deal.side_effect = PipedriveAPIError(
            message="API Error: Deal not found",
            status_code=404,
            error_info="Deal not found",
            response_data=error_data,
        )

        # Call the tool
        result = await delete_deal_from_pipedrive(mock_context, id_str="999")

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "API Error: Deal not found" in response["error"]
        assert response["data"] == error_data
