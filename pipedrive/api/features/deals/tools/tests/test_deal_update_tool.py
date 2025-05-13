import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp.server.fastmcp import Context

from pipedrive.api.features.deals.tools.deal_update_tool import update_deal_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class TestUpdateDealTool:
    """Test suite for the update_deal_in_pipedrive tool"""

    @pytest.fixture
    def mock_context(self):
        """Fixture for mock MCP context"""
        context = MagicMock(spec=Context)
        pipedrive_client = MagicMock()
        pipedrive_client.deals = MagicMock()
        pipedrive_client.deals.update_deal = AsyncMock()

        # Set up the context to return our mock pipedrive client
        context.request_context.lifespan_context.pipedrive_client = pipedrive_client

        return context

    @pytest.mark.asyncio
    async def test_update_deal_success(self, mock_context):
        """Test successful deal update"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "title": "Updated Deal",
            "value": 2000,
            "currency": "EUR",
            "status": "open",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal.return_value = mock_response

        # Call the tool
        result = await update_deal_in_pipedrive(
            mock_context,
            id_str="123",
            title="Updated Deal",
            value="2000",
            currency="EUR",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["id"] == 123
        assert response["data"]["title"] == "Updated Deal"
        assert response["data"]["value"] == 2000
        assert response["data"]["currency"] == "EUR"
        assert response["data"]["status"] == "open"

        # Verify that update_deal was called with correct arguments
        update_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal
        update_deal_mock.assert_called_once()
        call_args = update_deal_mock.call_args[1]
        assert call_args["deal_id"] == 123
        assert call_args["title"] == "Updated Deal"
        assert call_args["value"] == 2000.0
        assert call_args["currency"] == "EUR"

    @pytest.mark.asyncio
    async def test_update_deal_with_all_fields(self, mock_context):
        """Test updating a deal with all fields"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "title": "Updated Deal",
            "value": 2000,
            "currency": "EUR",
            "person_id": 456,
            "org_id": 789,
            "status": "won",
            "owner_id": 101,
            "stage_id": 202,
            "pipeline_id": 303,
            "expected_close_date": "2023-12-31",
            "visible_to": 1,
            "probability": 90,
            "lost_reason": None,
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal.return_value = mock_response

        # Call the tool with all fields
        result = await update_deal_in_pipedrive(
            mock_context,
            id_str="123",
            title="Updated Deal",
            value="2000",
            currency="EUR",
            person_id_str="456",
            org_id_str="789",
            status="won",
            owner_id_str="101",
            stage_id_str="202",
            pipeline_id_str="303",
            expected_close_date="2023-12-31",
            visible_to_str="1",
            probability="90",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["id"] == 123

        # Verify that update_deal was called with correct arguments
        update_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal
        update_deal_mock.assert_called_once()
        call_args = update_deal_mock.call_args[1]
        assert call_args["deal_id"] == 123
        assert call_args["title"] == "Updated Deal"
        assert call_args["value"] == 2000.0
        assert call_args["currency"] == "EUR"
        assert call_args["person_id"] == 456
        assert call_args["org_id"] == 789
        assert call_args["status"] == "won"
        assert call_args["owner_id"] == 101
        assert call_args["stage_id"] == 202
        assert call_args["pipeline_id"] == 303
        assert call_args["expected_close_date"] == "2023-12-31"
        assert call_args["visible_to"] == 1
        assert call_args["probability"] == 90

    @pytest.mark.asyncio
    async def test_update_deal_no_fields(self, mock_context):
        """Test updating a deal with no fields provided"""
        # Call the tool with no fields to update
        result = await update_deal_in_pipedrive(mock_context, id_str="123")

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert (
            "At least one field must be provided for updating a deal"
            in response["error"]
        )

        # Verify that update_deal was not called
        update_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal
        update_deal_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_deal_invalid_id(self, mock_context):
        """Test updating a deal with invalid ID format"""
        # Call the tool with invalid ID
        result = await update_deal_in_pipedrive(
            mock_context, id_str="not_a_number", title="Updated Deal"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "deal_id must be a numeric string" in response["error"]

        # Verify that update_deal was not called
        update_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal
        update_deal_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_deal_invalid_value(self, mock_context):
        """Test updating a deal with invalid value format"""
        # Call the tool with invalid value
        result = await update_deal_in_pipedrive(
            mock_context, id_str="123", value="not_a_number"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid deal value format" in response["error"]

        # Verify that update_deal was not called
        update_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal
        update_deal_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_deal_invalid_probability(self, mock_context):
        """Test updating a deal with invalid probability format"""
        # Call the tool with invalid probability
        result = await update_deal_in_pipedrive(
            mock_context, id_str="123", probability="not_a_number"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid probability format" in response["error"]

        # Verify that update_deal was not called
        update_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal
        update_deal_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_deal_invalid_probability_range(self, mock_context):
        """Test updating a deal with probability outside valid range"""
        # Call the tool with probability outside range
        result = await update_deal_in_pipedrive(
            mock_context, id_str="123", probability="101"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid probability format" in response["error"]
        assert "Must be an integer between 0 and 100" in response["error"]

        # Verify that update_deal was not called
        update_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal
        update_deal_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_deal_invalid_status(self, mock_context):
        """Test updating a deal with invalid status"""
        # Call the tool with invalid status
        result = await update_deal_in_pipedrive(
            mock_context, id_str="123", status="invalid_status"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid status" in response["error"]

        # Verify that update_deal was not called
        update_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal
        update_deal_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_deal_lost_reason_without_lost_status(self, mock_context):
        """Test providing lost_reason without setting status to lost"""
        # Call the tool with lost_reason but non-lost status
        result = await update_deal_in_pipedrive(
            mock_context, id_str="123", lost_reason="Price too high", status="open"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert (
            "Lost reason can only be provided when status is 'lost'"
            in response["error"]
        )

        # Verify that update_deal was not called
        update_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal
        update_deal_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_deal_lost_reason_with_lost_status(self, mock_context):
        """Test providing lost_reason with lost status"""
        # Set up the mock to return a successful response
        mock_response = {
            "id": 123,
            "title": "Lost Deal",
            "status": "lost",
            "lost_reason": "Price too high",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal.return_value = mock_response

        # Call the tool with lost_reason and lost status
        result = await update_deal_in_pipedrive(
            mock_context, id_str="123", lost_reason="Price too high", status="lost"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert response["data"]["lost_reason"] == "Price too high"

        # Verify that update_deal was called with correct arguments
        update_deal_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal
        update_deal_mock.assert_called_once()
        call_args = update_deal_mock.call_args[1]
        assert call_args["lost_reason"] == "Price too high"
        assert call_args["status"] == "lost"

    @pytest.mark.asyncio
    async def test_update_deal_api_error(self, mock_context):
        """Test handling of API errors"""
        # Set up the mock to raise an API error
        error_data = {
            "success": False,
            "error": "API Error",
            "error_info": "Deal not found",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.update_deal.side_effect = PipedriveAPIError(
            message="API Error: Deal not found",
            status_code=404,
            error_info="Deal not found",
            response_data=error_data,
        )

        # Call the tool
        result = await update_deal_in_pipedrive(
            mock_context, id_str="999", title="Updated Deal"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "API Error: Deal not found" in response["error"]
        assert response["data"] == error_data
