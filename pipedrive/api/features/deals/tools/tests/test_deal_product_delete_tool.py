import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp.server.fastmcp import Context

from pipedrive.api.features.deals.tools.deal_product_delete_tool import (
    delete_product_from_deal_in_pipedrive,
)
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class TestDeleteProductFromDealTool:
    """Test suite for the delete_product_from_deal_in_pipedrive tool"""

    @pytest.fixture
    def mock_context(self):
        """Fixture for mock MCP context"""
        context = MagicMock(spec=Context)
        pipedrive_client = MagicMock()
        pipedrive_client.deals = MagicMock()
        pipedrive_client.deals.delete_product_from_deal = AsyncMock()

        # Set up the context to return our mock pipedrive client
        context.request_context.lifespan_context.pipedrive_client = pipedrive_client

        return context

    @pytest.mark.asyncio
    async def test_delete_product_from_deal_success(self, mock_context):
        """Test successful product deletion from deal"""
        # Set up the mock to return a successful response
        mock_response = {
            "success": True,
            "data": {"id": 123, "deal_id": 456}
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.delete_product_from_deal.return_value = mock_response

        # Call the tool
        result = await delete_product_from_deal_in_pipedrive(
            mock_context, id_str="456", product_attachment_id_str="123"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["success"] is True
        assert response["data"]["data"]["id"] == 123
        assert response["data"]["data"]["deal_id"] == 456

        # Verify that delete_product_from_deal was called with correct arguments
        delete_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.delete_product_from_deal
        delete_product_mock.assert_called_once()
        call_args = delete_product_mock.call_args[1]
        assert call_args["deal_id"] == 456
        assert call_args["product_attachment_id"] == 123

    @pytest.mark.asyncio
    async def test_delete_product_from_deal_invalid_deal_id(self, mock_context):
        """Test deleting a product with invalid deal ID format"""
        # Call the tool with invalid deal ID
        result = await delete_product_from_deal_in_pipedrive(
            mock_context, id_str="not_a_number", product_attachment_id_str="123"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "deal_id must be a numeric string" in response["error"]

        # Verify that delete_product_from_deal was not called
        delete_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.delete_product_from_deal
        delete_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_product_from_deal_invalid_attachment_id(self, mock_context):
        """Test deleting a product with invalid product attachment ID format"""
        # Call the tool with invalid product attachment ID
        result = await delete_product_from_deal_in_pipedrive(
            mock_context, id_str="456", product_attachment_id_str="not_a_number"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "product_attachment_id must be a numeric string" in response["error"]

        # Verify that delete_product_from_deal was not called
        delete_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.delete_product_from_deal
        delete_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_product_from_deal_api_error(self, mock_context):
        """Test handling of API errors"""
        # Set up the mock to raise an API error
        error_data = {
            "success": False,
            "error": "API Error",
            "error_info": "Product attachment not found"
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.delete_product_from_deal.side_effect = PipedriveAPIError(
            message="API Error: Product attachment not found",
            status_code=404,
            error_info="Product attachment not found",
            response_data=error_data,
        )

        # Call the tool
        result = await delete_product_from_deal_in_pipedrive(
            mock_context, id_str="456", product_attachment_id_str="999"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "API Error: Product attachment not found" in response["error"]
        assert response["data"] == error_data

    @pytest.mark.asyncio
    async def test_delete_product_from_deal_unexpected_error(self, mock_context):
        """Test handling of unexpected errors"""
        # Set up the mock to raise an unexpected error
        mock_context.request_context.lifespan_context.pipedrive_client.deals.delete_product_from_deal.side_effect = Exception(
            "Unexpected error occurred"
        )

        # Call the tool
        result = await delete_product_from_deal_in_pipedrive(
            mock_context, id_str="456", product_attachment_id_str="123"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "An unexpected error occurred" in response["error"]