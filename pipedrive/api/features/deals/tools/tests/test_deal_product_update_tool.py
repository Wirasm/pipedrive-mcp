import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp.server.fastmcp import Context

from pipedrive.api.features.deals.tools.deal_product_update_tool import (
    update_product_in_deal_in_pipedrive,
)
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class TestUpdateProductInDealTool:
    """Test suite for the update_product_in_deal_in_pipedrive tool"""

    @pytest.fixture
    def mock_context(self):
        """Fixture for mock MCP context"""
        context = MagicMock(spec=Context)
        pipedrive_client = MagicMock()
        pipedrive_client.deals = MagicMock()
        pipedrive_client.deals.update_product_in_deal = AsyncMock()

        # Set up the context to return our mock pipedrive client
        context.request_context.lifespan_context.pipedrive_client = pipedrive_client

        return context

    @pytest.mark.asyncio
    async def test_update_product_in_deal_success(self, mock_context):
        """Test successful product update in deal"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "deal_id": 456,
            "product_id": 789,
            "item_price": 150,
            "quantity": 3,
            "discount": 0,
            "tax": 0,
            "comments": "Updated product",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal.return_value = mock_response

        # Call the tool
        result = await update_product_in_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_attachment_id_str="123",
            item_price="150",
            quantity="3",
            comments="Updated product",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["id"] == 123
        assert response["data"]["deal_id"] == 456
        assert response["data"]["item_price"] == 150
        assert response["data"]["quantity"] == 3
        assert response["data"]["comments"] == "Updated product"

        # Verify that update_product_in_deal was called with correct arguments
        update_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal
        update_product_mock.assert_called_once()
        call_args = update_product_mock.call_args[1]
        assert call_args["deal_id"] == 456
        assert call_args["product_attachment_id"] == 123
        assert call_args["item_price"] == 150.0
        assert call_args["quantity"] == 3
        assert call_args["comments"] == "Updated product"

    @pytest.mark.asyncio
    async def test_update_product_in_deal_with_all_parameters(self, mock_context):
        """Test updating a product in a deal with all parameters"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "deal_id": 456,
            "product_id": 789,
            "item_price": 150,
            "quantity": 3,
            "discount": 15,
            "tax": 7.5,
            "comments": "Updated product",
            "discount_type": "amount",
            "tax_method": "exclusive",
            "is_enabled": True,
            "product_variation_id": 101,
            "billing_frequency": "monthly",
            "billing_frequency_cycles": 12,
            "billing_start_date": "2023-12-31",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal.return_value = mock_response

        # Call the tool with all parameters
        result = await update_product_in_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_attachment_id_str="123",
            item_price="150",
            quantity="3",
            tax="7.5",
            comments="Updated product",
            discount="15",
            discount_type="amount",
            tax_method="exclusive",
            is_enabled=True,
            product_variation_id_str="101",
            billing_frequency="monthly",
            billing_frequency_cycles="12",
            billing_start_date="2023-12-31",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True

        # Verify that update_product_in_deal was called with correct arguments
        update_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal
        update_product_mock.assert_called_once()
        call_args = update_product_mock.call_args[1]
        assert call_args["deal_id"] == 456
        assert call_args["product_attachment_id"] == 123
        assert call_args["item_price"] == 150.0
        assert call_args["quantity"] == 3
        assert call_args["tax"] == 7.5
        assert call_args["comments"] == "Updated product"
        assert call_args["discount"] == 15.0
        assert call_args["discount_type"] == "amount"
        assert call_args["tax_method"] == "exclusive"
        assert call_args["is_enabled"] is True
        assert call_args["product_variation_id"] == 101
        assert call_args["billing_frequency"] == "monthly"
        assert call_args["billing_frequency_cycles"] == 12
        assert call_args["billing_start_date"] == "2023-12-31"

    @pytest.mark.asyncio
    async def test_update_product_in_deal_no_fields(self, mock_context):
        """Test updating a product in a deal with no fields provided"""
        # Call the tool with no fields to update
        result = await update_product_in_deal_in_pipedrive(
            mock_context, id_str="456", product_attachment_id_str="123"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert (
            "At least one field must be provided for updating a product in a deal"
            in response["error"]
        )

        # Verify that update_product_in_deal was not called
        update_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal
        update_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_product_in_deal_invalid_deal_id(self, mock_context):
        """Test updating a product with invalid deal ID format"""
        # Call the tool with invalid deal ID
        result = await update_product_in_deal_in_pipedrive(
            mock_context,
            id_str="not_a_number",
            product_attachment_id_str="123",
            item_price="150",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "deal_id must be a numeric string" in response["error"]

        # Verify that update_product_in_deal was not called
        update_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal
        update_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_product_in_deal_invalid_attachment_id(self, mock_context):
        """Test updating a product with invalid product attachment ID format"""
        # Call the tool with invalid product attachment ID
        result = await update_product_in_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_attachment_id_str="not_a_number",
            item_price="150",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "product_attachment_id must be a numeric string" in response["error"]

        # Verify that update_product_in_deal was not called
        update_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal
        update_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_product_in_deal_invalid_price(self, mock_context):
        """Test updating a product with invalid price format"""
        # Call the tool with invalid price
        result = await update_product_in_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_attachment_id_str="123",
            item_price="not_a_number",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid item price format" in response["error"]

        # Verify that update_product_in_deal was not called
        update_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal
        update_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_product_in_deal_invalid_quantity(self, mock_context):
        """Test updating a product with invalid quantity format"""
        # Call the tool with invalid quantity
        result = await update_product_in_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_attachment_id_str="123",
            quantity="not_a_number",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid quantity format" in response["error"]

        # Verify that update_product_in_deal was not called
        update_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal
        update_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_product_in_deal_invalid_discount_type(self, mock_context):
        """Test updating a product with invalid discount type"""
        # Call the tool with invalid discount type
        result = await update_product_in_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_attachment_id_str="123",
            discount_type="invalid_type",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid discount_type format" in response["error"]

        # Verify that update_product_in_deal was not called
        update_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal
        update_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_product_in_deal_invalid_tax_method(self, mock_context):
        """Test updating a product with invalid tax method"""
        # Call the tool with invalid tax method
        result = await update_product_in_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_attachment_id_str="123",
            tax_method="invalid_method",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid tax_method format" in response["error"]

        # Verify that update_product_in_deal was not called
        update_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal
        update_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_product_in_deal_api_error(self, mock_context):
        """Test handling of API errors"""
        # Set up the mock to raise an API error
        error_data = {
            "success": False,
            "error": "API Error",
            "error_info": "Product attachment not found",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.update_product_in_deal.side_effect = PipedriveAPIError(
            message="API Error: Product attachment not found",
            status_code=404,
            error_info="Product attachment not found",
            response_data=error_data,
        )

        # Call the tool
        result = await update_product_in_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_attachment_id_str="999",
            item_price="150",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "API Error: Product attachment not found" in response["error"]
        assert response["data"] == error_data
