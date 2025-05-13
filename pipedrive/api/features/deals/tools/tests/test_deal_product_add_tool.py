import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp.server.fastmcp import Context

from pipedrive.api.features.deals.tools.deal_product_add_tool import (
    add_product_to_deal_in_pipedrive,
)
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class TestAddProductToDealTool:
    """Test suite for the add_product_to_deal_in_pipedrive tool"""

    @pytest.fixture
    def mock_context(self):
        """Fixture for mock MCP context"""
        context = MagicMock(spec=Context)
        pipedrive_client = MagicMock()
        pipedrive_client.deals = MagicMock()
        pipedrive_client.deals.add_product_to_deal = AsyncMock()

        # Set up the context to return our mock pipedrive client
        context.request_context.lifespan_context.pipedrive_client = pipedrive_client

        return context

    @pytest.mark.asyncio
    async def test_add_product_to_deal_success(self, mock_context):
        """Test successful product addition to deal"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "deal_id": 456,
            "product_id": 789,
            "item_price": 100,
            "quantity": 2,
            "discount": 0,
            "tax": 0,
            "comments": "",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.add_product_to_deal.return_value = mock_response

        # Call the tool
        result = await add_product_to_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_id_str="789",
            item_price="100",
            quantity="2",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["id"] == 123
        assert response["data"]["deal_id"] == 456
        assert response["data"]["product_id"] == 789
        assert response["data"]["item_price"] == 100
        assert response["data"]["quantity"] == 2

        # Verify that add_product_to_deal was called with correct arguments
        add_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.add_product_to_deal
        add_product_mock.assert_called_once()
        call_args = add_product_mock.call_args[1]
        assert call_args["deal_id"] == 456
        assert call_args["product_id"] == 789
        assert call_args["item_price"] == 100.0
        assert call_args["quantity"] == 2

    @pytest.mark.asyncio
    async def test_add_product_to_deal_with_all_parameters(self, mock_context):
        """Test adding a product to a deal with all parameters"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "deal_id": 456,
            "product_id": 789,
            "item_price": 100,
            "quantity": 2,
            "discount": 10,
            "tax": 5,
            "comments": "Test product",
            "discount_type": "amount",
            "tax_method": "exclusive",
            "product_variation_id": 101,
            "billing_frequency": "monthly",
            "billing_frequency_cycles": 12,
            "billing_start_date": "2023-12-31",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.add_product_to_deal.return_value = mock_response

        # Call the tool with all parameters
        result = await add_product_to_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_id_str="789",
            item_price="100",
            quantity="2",
            tax="5",
            comments="Test product",
            discount="10",
            discount_type="amount",
            tax_method="exclusive",
            product_variation_id_str="101",
            billing_frequency="monthly",
            billing_frequency_cycles="12",
            billing_start_date="2023-12-31",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True

        # Verify that add_product_to_deal was called with correct arguments
        add_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.add_product_to_deal
        add_product_mock.assert_called_once()
        call_args = add_product_mock.call_args[1]
        assert call_args["deal_id"] == 456
        assert call_args["product_id"] == 789
        assert call_args["item_price"] == 100.0
        assert call_args["quantity"] == 2
        assert call_args["tax"] == 5.0
        assert call_args["comments"] == "Test product"
        assert call_args["discount"] == 10.0
        assert call_args["discount_type"] == "amount"
        assert call_args["tax_method"] == "exclusive"
        assert call_args["product_variation_id"] == 101
        assert call_args["billing_frequency"] == "monthly"
        assert call_args["billing_frequency_cycles"] == 12
        assert call_args["billing_start_date"] == "2023-12-31"

    @pytest.mark.asyncio
    async def test_add_product_to_deal_invalid_deal_id(self, mock_context):
        """Test adding a product with invalid deal ID format"""
        # Call the tool with invalid deal ID
        result = await add_product_to_deal_in_pipedrive(
            mock_context,
            id_str="not_a_number",
            product_id_str="789",
            item_price="100",
            quantity="2",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "deal_id must be a numeric string" in response["error"]

        # Verify that add_product_to_deal was not called
        add_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.add_product_to_deal
        add_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_product_to_deal_invalid_product_id(self, mock_context):
        """Test adding a product with invalid product ID format"""
        # Call the tool with invalid product ID
        result = await add_product_to_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_id_str="not_a_number",
            item_price="100",
            quantity="2",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "product_id must be a numeric string" in response["error"]

        # Verify that add_product_to_deal was not called
        add_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.add_product_to_deal
        add_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_product_to_deal_invalid_price(self, mock_context):
        """Test adding a product with invalid price format"""
        # Call the tool with invalid price
        result = await add_product_to_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_id_str="789",
            item_price="not_a_number",
            quantity="2",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid item price format" in response["error"]

        # Verify that add_product_to_deal was not called
        add_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.add_product_to_deal
        add_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_product_to_deal_invalid_quantity(self, mock_context):
        """Test adding a product with invalid quantity format"""
        # Call the tool with invalid quantity
        result = await add_product_to_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_id_str="789",
            item_price="100",
            quantity="not_a_number",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid quantity format" in response["error"]

        # Verify that add_product_to_deal was not called
        add_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.add_product_to_deal
        add_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_product_to_deal_zero_quantity(self, mock_context):
        """Test adding a product with zero quantity"""
        # Call the tool with zero quantity
        result = await add_product_to_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_id_str="789",
            item_price="100",
            quantity="0",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Quantity must be greater than zero" in response["error"]

        # Verify that add_product_to_deal was not called
        add_product_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.add_product_to_deal
        add_product_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_product_to_deal_api_error(self, mock_context):
        """Test handling of API errors"""
        # Set up the mock to raise an API error
        error_data = {
            "success": False,
            "error": "API Error",
            "error_info": "Product not found",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.add_product_to_deal.side_effect = PipedriveAPIError(
            message="API Error: Product not found",
            status_code=404,
            error_info="Product not found",
            response_data=error_data,
        )

        # Call the tool
        result = await add_product_to_deal_in_pipedrive(
            mock_context,
            id_str="456",
            product_id_str="999",
            item_price="100",
            quantity="2",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "API Error: Product not found" in response["error"]
        assert response["data"] == error_data
