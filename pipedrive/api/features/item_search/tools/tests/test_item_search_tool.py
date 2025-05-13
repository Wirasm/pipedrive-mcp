import json
from unittest.mock import AsyncMock, Mock, patch

import pytest

from pipedrive.api.features.item_search.tools.item_search_tool import search_items_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.mark.asyncio
class TestSearchItemsInPipedrive:
    @pytest.fixture
    def mock_context(self):
        """Create a mock context with a lifespan_context containing a mock pipedrive_client"""
        mock_ctx = Mock()
        mock_ctx.request_context = Mock()
        mock_lifespan_ctx = Mock()
        mock_pipedrive_client = Mock()
        mock_pipedrive_client.search_items = AsyncMock()
        mock_lifespan_ctx.pipedrive_client = mock_pipedrive_client
        mock_ctx.request_context.lifespan_context = mock_lifespan_ctx
        return mock_ctx

    async def test_search_items_with_minimal_params(self, mock_context):
        """Test searching items with minimal parameters"""
        # Arrange
        term = "test"
        mock_context.request_context.lifespan_context.pipedrive_client.search_items.return_value = (
            [
                {"id": 1, "type": "deal", "result_score": 0.9, "title": "Test Deal"}
            ],
            None
        )
        
        # Act
        result = await search_items_in_pipedrive(mock_context, term)
        
        # Assert
        mock_context.request_context.lifespan_context.pipedrive_client.search_items.assert_called_once_with(
            term="test",
            item_types=None,
            fields=None,
            search_for_related_items=False,
            exact_match=False,
            include_fields=None,
            limit=100,
            cursor=None
        )
        
        # Validate the response format and content
        result_dict = json.loads(result)
        assert result_dict["success"] is True
        assert "data" in result_dict
        assert "items" in result_dict["data"]
        assert len(result_dict["data"]["items"]) == 1
        assert result_dict["data"]["items"][0]["id"] == 1
        assert result_dict["data"]["items"][0]["type"] == "deal"
        assert result_dict["data"]["deal_count"] == 1
        assert result_dict["data"]["person_count"] == 0
    
    async def test_search_items_with_all_params(self, mock_context):
        """Test searching items with all parameters"""
        # Arrange
        term = "test"
        item_types_str = "deal,person"
        fields_str = "title,name"
        search_for_related_items = True
        exact_match = True
        include_fields_str = "deal.cc_email,person.picture"
        limit_str = "50"
        cursor = "next_page_token"
        
        mock_context.request_context.lifespan_context.pipedrive_client.search_items.return_value = (
            [
                {"id": 1, "type": "deal", "result_score": 0.9, "title": "Test Deal"},
                {"id": 2, "type": "person", "result_score": 0.8, "name": "Test Person"}
            ],
            "another_page_token"
        )
        
        # Act
        result = await search_items_in_pipedrive(
            mock_context, 
            term=term,
            item_types_str=item_types_str,
            fields_str=fields_str,
            search_for_related_items=search_for_related_items,
            exact_match=exact_match,
            include_fields_str=include_fields_str,
            limit_str=limit_str,
            cursor=cursor
        )
        
        # Assert
        mock_context.request_context.lifespan_context.pipedrive_client.search_items.assert_called_once_with(
            term="test",
            item_types=["deal", "person"],
            fields=["title", "name"],
            search_for_related_items=True,
            exact_match=True,
            include_fields=["deal.cc_email", "person.picture"],
            limit=50,
            cursor="next_page_token"
        )
        
        # Validate the response format and content
        result_dict = json.loads(result)
        assert result_dict["success"] is True
        assert "data" in result_dict
        assert "items" in result_dict["data"]
        assert len(result_dict["data"]["items"]) == 2
        assert result_dict["data"]["next_cursor"] == "another_page_token"
        assert result_dict["data"]["deal_count"] == 1
        assert result_dict["data"]["person_count"] == 1
        assert result_dict["data"]["total_count"] == 2
    
    async def test_search_items_with_empty_results(self, mock_context):
        """Test searching items with empty results"""
        # Arrange
        term = "nonexistent"
        mock_context.request_context.lifespan_context.pipedrive_client.search_items.return_value = (
            [],
            None
        )
        
        # Act
        result = await search_items_in_pipedrive(mock_context, term)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is True
        assert "data" in result_dict
        assert "items" in result_dict["data"]
        assert len(result_dict["data"]["items"]) == 0
        assert "message" in result_dict["data"]
        assert "No items found" in result_dict["data"]["message"]
    
    async def test_search_items_with_invalid_term(self, mock_context):
        """Test searching items with invalid term"""
        # Arrange
        term = ""
        
        # Act
        result = await search_items_in_pipedrive(mock_context, term)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert result_dict["error"] == "Search term cannot be empty"
    
    async def test_search_items_with_short_term(self, mock_context):
        """Test searching items with short term"""
        # Arrange
        term = "a"
        
        # Act
        result = await search_items_in_pipedrive(mock_context, term, exact_match=False)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert "Search term must be at least 2 characters" in result_dict["error"]
    
    async def test_search_items_with_invalid_item_type(self, mock_context):
        """Test searching items with invalid item type"""
        # Arrange
        term = "test"
        item_types_str = "deal,invalid"
        
        # Act
        result = await search_items_in_pipedrive(mock_context, term, item_types_str=item_types_str)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert "Invalid item type" in result_dict["error"]
    
    async def test_search_items_with_invalid_field(self, mock_context):
        """Test searching items with invalid field"""
        # Arrange
        term = "test"
        fields_str = "title,invalid"
        
        # Act
        result = await search_items_in_pipedrive(mock_context, term, fields_str=fields_str)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert "Invalid field" in result_dict["error"]
    
    async def test_search_items_with_invalid_limit(self, mock_context):
        """Test searching items with invalid limit"""
        # Arrange
        term = "test"
        limit_str = "invalid"
        mock_context.request_context.lifespan_context.pipedrive_client.search_items.return_value = (
            [{"id": 1, "type": "deal", "result_score": 0.9, "title": "Test Deal"}],
            None
        )
        
        # Act
        result = await search_items_in_pipedrive(mock_context, term, limit_str=limit_str)
        
        # Assert - should not fail, but use default limit
        mock_context.request_context.lifespan_context.pipedrive_client.search_items.assert_called_once_with(
            term="test",
            item_types=None,
            fields=None,
            search_for_related_items=False,
            exact_match=False,
            include_fields=None,
            limit=100,  # Default limit
            cursor=None
        )
    
    async def test_search_items_with_api_error(self, mock_context):
        """Test handling API errors"""
        # Arrange
        term = "test"
        error_response = {"success": False, "error": "API error", "error_code": 400}
        mock_context.request_context.lifespan_context.pipedrive_client.search_items.side_effect = (
            PipedriveAPIError("API error", response_data=error_response)
        )
        
        # Act
        result = await search_items_in_pipedrive(mock_context, term)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert "API error" in result_dict["error"]
        assert result_dict["data"] == error_response
    
    async def test_search_items_with_unexpected_error(self, mock_context):
        """Test handling unexpected errors"""
        # Arrange
        term = "test"
        mock_context.request_context.lifespan_context.pipedrive_client.search_items.side_effect = (
            Exception("Unexpected error")
        )
        
        # Act
        result = await search_items_in_pipedrive(mock_context, term)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert "An unexpected error occurred" in result_dict["error"]