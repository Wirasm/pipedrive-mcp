import json
from unittest.mock import AsyncMock, MagicMock

import pytest
from mcp.server.fastmcp import Context

from pipedrive.api.features.deals.tools.deal_search_tool import (
    search_deals_in_pipedrive,
)
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class TestSearchDealsTool:
    """Test suite for the search_deals_in_pipedrive tool"""

    @pytest.fixture
    def mock_context(self):
        """Fixture for mock MCP context"""
        context = MagicMock(spec=Context)
        pipedrive_client = MagicMock()
        pipedrive_client.deals = MagicMock()
        pipedrive_client.deals.search_deals = AsyncMock()

        # Set up the context to return our mock pipedrive client
        context.request_context.lifespan_context.pipedrive_client = pipedrive_client

        return context

    @pytest.mark.asyncio
    async def test_search_deals_success(self, mock_context):
        """Test successful deals search"""
        # Set up the mock to return a successful response
        mock_items = [
            {"id": 123, "title": "Search Deal 1"},
            {"id": 456, "title": "Search Deal 2"},
        ]
        mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals.return_value = (
            mock_items,
            "next_page_token",
        )

        # Call the tool
        result = await search_deals_in_pipedrive(mock_context, term="Search")

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert len(response["data"]["items"]) == 2
        assert response["data"]["items"][0]["id"] == 123
        assert response["data"]["items"][0]["title"] == "Search Deal 1"
        assert response["data"]["items"][1]["id"] == 456
        assert response["data"]["items"][1]["title"] == "Search Deal 2"
        assert response["data"]["next_cursor"] == "next_page_token"

        # Verify that search_deals was called with correct arguments
        search_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals
        search_deals_mock.assert_called_once()
        call_args = search_deals_mock.call_args[1]
        assert call_args["term"] == "Search"
        assert call_args["exact_match"] is False

    @pytest.mark.asyncio
    async def test_search_deals_with_parameters(self, mock_context):
        """Test searching deals with all parameters"""
        # Set up the mock to return a successful response
        mock_items = [{"id": 123, "title": "Exact Match Deal"}]
        mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals.return_value = (
            mock_items,
            None,
        )

        # Call the tool with all parameters
        result = await search_deals_in_pipedrive(
            mock_context,
            term="Exact",
            fields_str="title,notes",
            exact_match=True,
            person_id_str="789",
            organization_id_str="101",
            status="open",
            include_fields_str="cc_email",
            limit_str="50",
            cursor="search_cursor",
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag and data
        assert response["success"] is True
        assert len(response["data"]["items"]) == 1
        assert response["data"]["items"][0]["id"] == 123
        assert response["data"]["items"][0]["title"] == "Exact Match Deal"
        assert response["data"]["next_cursor"] is None

        # Verify that search_deals was called with correct arguments
        search_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals
        search_deals_mock.assert_called_once()
        call_args = search_deals_mock.call_args[1]
        assert call_args["term"] == "Exact"
        assert call_args["fields"] == ["title", "notes"]
        assert call_args["exact_match"] is True
        assert call_args["person_id"] == 789
        assert call_args["organization_id"] == 101
        assert call_args["status"] == "open"
        assert call_args["include_fields"] == ["cc_email"]
        assert call_args["limit"] == 50
        assert call_args["cursor"] == "search_cursor"

    @pytest.mark.asyncio
    async def test_search_deals_empty_term(self, mock_context):
        """Test searching deals with empty term"""
        # Call the tool with empty term
        result = await search_deals_in_pipedrive(mock_context, term="")

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Search term cannot be empty" in response["error"]

        # Verify that search_deals was not called
        search_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals
        search_deals_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_search_deals_short_term(self, mock_context):
        """Test searching deals with term that's too short"""
        # Call the tool with short term (needs min 2 chars if not exact match)
        result = await search_deals_in_pipedrive(
            mock_context, term="A", exact_match=False
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Search term must be at least 2 characters long" in response["error"]

        # Verify that search_deals was not called
        search_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals
        search_deals_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_search_deals_short_term_exact_match(self, mock_context):
        """Test searching deals with short term but exact_match=True"""
        # Set up the mock to return a successful response
        mock_items = [{"id": 123, "title": "A"}]
        mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals.return_value = (
            mock_items,
            None,
        )

        # Call the tool with short term but exact_match=True (should work)
        result = await search_deals_in_pipedrive(
            mock_context, term="A", exact_match=True
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify success flag
        assert response["success"] is True

        # Verify that search_deals was called
        search_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals
        search_deals_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_deals_invalid_id(self, mock_context):
        """Test searching deals with invalid ID format"""
        # Call the tool with invalid person_id
        result = await search_deals_in_pipedrive(
            mock_context, term="Search", person_id_str="not_a_number"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid person_id format" in response["error"]

        # Verify that search_deals was not called
        search_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals
        search_deals_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_search_deals_invalid_status(self, mock_context):
        """Test searching deals with invalid status"""
        # Call the tool with invalid status
        result = await search_deals_in_pipedrive(
            mock_context, term="Search", status="invalid_status"
        )

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "Invalid status:" in response["error"]

        # Verify that search_deals was not called
        search_deals_mock = mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals
        search_deals_mock.assert_not_called()

    @pytest.mark.asyncio
    async def test_search_deals_api_error(self, mock_context):
        """Test handling of API errors"""
        # Set up the mock to raise an API error
        error_data = {
            "success": False,
            "error": "API Error",
            "error_info": "Invalid search term",
        }
        mock_context.request_context.lifespan_context.pipedrive_client.deals.search_deals.side_effect = PipedriveAPIError(
            message="API Error: Invalid search term",
            status_code=400,
            error_info="Invalid search term",
            response_data=error_data,
        )

        # Call the tool
        result = await search_deals_in_pipedrive(mock_context, term="Search")

        # Parse the JSON response
        response = json.loads(result)

        # Verify error response
        assert response["success"] is False
        assert "API Error: Invalid search term" in response["error"]
        assert response["data"] == error_data
