import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp.server.fastmcp import Context

from pipedrive.api.features.deals.tools.deal_list_tool import list_deals_from_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class TestListDealsTool:
    """Test suite for the list_deals_from_pipedrive tool"""

    @pytest.fixture
    def mock_context(self):
        """Fixture for mock MCP context"""
        context = MagicMock(spec=Context)
        pipedrive_client = MagicMock()
        pipedrive_client.deals = MagicMock()
        pipedrive_client.deals.list_deals = AsyncMock()

        # Set up the context to return our mock pipedrive client
        context.request_context.lifespan_context.pipedrive_client = pipedrive_client

        return context

    @pytest.mark.asyncio
    async def test_list_deals_success(self, mock_context):
        """Test successful deals listing"""
        # Set up the mock to return a successful response
        mock_deals = [{"id": 123, "title": "Deal 1"}, {"id": 456, "title": "Deal 2"}]
        mock_context.request_context.lifespan_context.pipedrive_client.deals.list_deals.return_value = (
            mock_deals,
            "next_page_token",
        )

        # Call the tool
        result = await list_deals_from_pipedrive(mock_context, limit_str="2")

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert len(response["data"]["items"]) == 2
        assert response["data"]["items"][0]["id"] == 123
        assert response["data"]["items"][0]["title"] == "Deal 1"
        assert response["data"]["items"][1]["id"] == 456
        assert response["data"]["items"][1]["title"] == "Deal 2"
        assert response["data"]["next_cursor"] == "next_page_token"

        # Verify that list_deals was called with correct arguments
        list_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.list_deals
        list_deals_mock.assert_called_once()
        call_args = list_deals_mock.call_args[1]
        assert call_args["limit"] == 2

    @pytest.mark.asyncio
    async def test_list_deals_with_filters(self, mock_context):
        """Test listing deals with filter parameters"""
        # Set up the mock to return a successful response
        mock_deals = [{"id": 123, "title": "Deal 1", "person_id": 789, "org_id": 101}]
        mock_context.request_context.lifespan_context.pipedrive_client.deals.list_deals.return_value = (
            mock_deals,
            None,
        )

        # Call the tool with filter parameters
        result = await list_deals_from_pipedrive(
            mock_context,
            limit_str="10",
            cursor="some_cursor",
            filter_id_str="202",
            owner_id_str="303",
            person_id_str="789",
            org_id_str="101",
            pipeline_id_str="404",
            stage_id_str="505",
            status="open",
            sort_by="update_time",
            sort_direction="desc",
            include_fields_str="products_count,notes_count",
            custom_fields_str="custom1,custom2",
            updated_since="2023-01-01T00:00:00Z",
            updated_until="2023-12-31T23:59:59Z",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert len(response["data"]["items"]) == 1
        assert response["data"]["items"][0]["id"] == 123
        assert response["data"]["items"][0]["title"] == "Deal 1"
        assert response["data"]["next_cursor"] is None

        # Verify that list_deals was called with correct arguments
        list_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.list_deals
        list_deals_mock.assert_called_once()
        call_args = list_deals_mock.call_args[1]
        assert call_args["limit"] == 10
        assert call_args["cursor"] == "some_cursor"
        assert call_args["filter_id"] == 202
        assert call_args["owner_id"] == 303
        assert call_args["person_id"] == 789
        assert call_args["org_id"] == 101
        assert call_args["pipeline_id"] == 404
        assert call_args["stage_id"] == 505
        assert call_args["status"] == "open"
        assert call_args["sort_by"] == "update_time"
        assert call_args["sort_direction"] == "desc"
        assert call_args["include_fields"] == ["products_count", "notes_count"]
        assert call_args["custom_fields_keys"] == ["custom1", "custom2"]
        assert call_args["updated_since"] == "2023-01-01T00:00:00Z"
        assert call_args["updated_until"] == "2023-12-31T23:59:59Z"

    @pytest.mark.asyncio
    async def test_list_deals_invalid_id(self, mock_context):
        """Test listing deals with invalid ID format"""
        # Call the tool with invalid filter_id
        result = await list_deals_from_pipedrive(
            mock_context, filter_id_str="not_a_number"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "filter_id must be a numeric string" in response["error"]

        # Verify that list_deals was not called
        list_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.list_deals
        list_deals_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_list_deals_invalid_limit(self, mock_context):
        """Test listing deals with invalid limit format"""
        # Call the tool with invalid limit
        result = await list_deals_from_pipedrive(mock_context, limit_str="not_a_number")

        # Parse the JSON response
        response = json.loads(result)

        # Check that the tool handles invalid limit by returning an error
        assert response["success"] is False
        assert "An unexpected error occurred" in response["error"]

        # Verify that list_deals was called with the default limit
        list_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.list_deals
        list_deals_mock.assert_called_once()
        call_args = list_deals_mock.call_args[1]
        assert call_args["limit"] == 100

    @pytest.mark.asyncio
    async def test_list_deals_api_error(self, mock_context):
        """Test handling of API errors"""
        # Set up the mock to raise an API error
        error_data = {
            "success": False,
            "error": "API Error",
            "error_info": "Invalid filter ID",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.list_deals.side_effect = PipedriveAPIError(
            message="API Error: Invalid filter ID",
            status_code=400,
            error_info="Invalid filter ID",
            response_data=error_data,
        )

        # Call the tool
        result = await list_deals_from_pipedrive(mock_context, filter_id_str="999")

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "API Error: Invalid filter ID" in response["error"]
        assert response["data"] == error_data
