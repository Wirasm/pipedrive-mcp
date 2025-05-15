import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

from pipedrive.api.features.deals.tools.deal_create_tool import create_deal_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class TestCreateDealTool:
    """Test suite for the create_deal_in_pipedrive tool"""

    @pytest.fixture
    def mock_context(self):
        """Fixture for mock MCP context"""
        context = MagicMock(spec=Context)
        pipedrive_client = MagicMock()
        pipedrive_client.deals = MagicMock()
        pipedrive_client.deals.create_deal = AsyncMock()

        # Set up the context to return our mock pipedrive client
        context.request_context.lifespan_context.pipedrive_client = pipedrive_client

        return context

    @pytest.mark.asyncio
    async def test_create_deal_success(self, mock_context):
        """Test successful deal creation"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "title": "Test Deal",
            "value": 1000,
            "currency": "USD",
            "status": "open",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.create_deal.return_value = mock_response

        # Call the tool
        result = await create_deal_in_pipedrive(
            mock_context, title="Test Deal", value="1000", currency="USD", status="open"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["id"] == 123
        assert response["data"]["title"] == "Test Deal"
        assert response["data"]["value"] == 1000
        assert response["data"]["currency"] == "USD"
        assert response["data"]["status"] == "open"

        # Verify that create_deal was called with correct arguments
        create_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.create_deal
        create_deal_mock.assert_called_once()
        call_args = create_deal_mock.call_args[1]
        assert call_args["title"] == "Test Deal"
        assert call_args["value"] == 1000.0
        assert call_args["currency"] == "USD"
        assert call_args["status"] == "open"

    @pytest.mark.asyncio
    async def test_create_deal_with_optional_params(self, mock_context):
        """Test creating a deal with optional parameters"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "title": "Test Deal",
            "value": 1000,
            "currency": "USD",
            "person_id": 456,
            "org_id": 789,
            "expected_close_date": "2023-12-31",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.create_deal.return_value = mock_response

        # Call the tool with optional parameters
        result = await create_deal_in_pipedrive(
            mock_context,
            title="Test Deal",
            value="1000",
            currency="USD",
            person_id_str="456",
            org_id_str="789",
            expected_close_date="2023-12-31",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["id"] == 123
        assert response["data"]["person_id"] == 456
        assert response["data"]["org_id"] == 789
        assert response["data"]["expected_close_date"] == "2023-12-31"

        # Verify that create_deal was called with correct arguments
        create_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.create_deal
        create_deal_mock.assert_called_once()
        call_args = create_deal_mock.call_args[1]
        assert call_args["title"] == "Test Deal"
        assert call_args["value"] == 1000.0
        assert call_args["currency"] == "USD"
        assert call_args["person_id"] == 456
        assert call_args["org_id"] == 789
        assert call_args["expected_close_date"] == "2023-12-31"

    @pytest.mark.asyncio
    async def test_create_deal_invalid_id(self, mock_context):
        """Test creating a deal with invalid ID format"""
        # Call the tool with invalid person_id
        result = await create_deal_in_pipedrive(
            mock_context, title="Test Deal", person_id_str="not_a_number"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "person_id must be a numeric string" in response["error"]

        # Verify that create_deal was not called
        create_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.create_deal
        create_deal_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_deal_api_error(self, mock_context):
        """Test handling of API errors"""
        # Setup validation error
        mock_context.request_context.lifespan_context.pipedrive_client.deals.create_deal.side_effect = ValueError("Deal title cannot be empty")

        # Call the tool
        result = await create_deal_in_pipedrive(mock_context, title="")

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Deal title cannot be empty" in response["error"]

    @pytest.mark.asyncio
    async def test_create_deal_invalid_value(self, mock_context):
        """Test creating a deal with invalid value format"""
        # Call the tool with invalid value
        result = await create_deal_in_pipedrive(
            mock_context, title="Test Deal", value="not_a_number"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid deal value format" in response["error"]

        # Verify that create_deal was not called
        create_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.create_deal
        create_deal_mock.assert_not_called()
