import json
from unittest.mock import AsyncMock, Mock, patch

import pytest

from pipedrive.api.features.item_search.tools.item_field_search_tool import search_item_field_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.mark.asyncio
@patch("pipedrive.api.features.tool_decorator.registry.is_feature_enabled", return_value=True)
class TestSearchItemFieldInPipedrive:
    
    @pytest.fixture
    def mock_context(self):
        """Create a mock context with a lifespan_context containing a mock pipedrive_client"""
        mock_ctx = Mock()
        mock_ctx.request_context = Mock()
        mock_lifespan_ctx = Mock()
        mock_pipedrive_client = Mock()
        mock_pipedrive_client.search_field = AsyncMock()
        mock_lifespan_ctx.pipedrive_client = mock_pipedrive_client
        mock_ctx.request_context.lifespan_context = mock_lifespan_ctx
        return mock_ctx

    async def test_search_field_with_minimal_params(self, mock_registry, mock_context):
        """Test searching field with minimal parameters"""
        # Arrange
        term = "test"
        entity_type = "person"
        field = "name"
        
        mock_context.request_context.lifespan_context.pipedrive_client.search_field.return_value = (
            [
                {"id": 1, "name": "Test Person"}
            ],
            None
        )
        
        # Act
        result = await search_item_field_in_pipedrive(mock_context, term, entity_type, field)
        
        # Assert
        mock_context.request_context.lifespan_context.pipedrive_client.search_field.assert_called_once_with(
            term="test",
            entity_type="person",
            field="name",
            match="exact",
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
        assert result_dict["data"]["items"][0]["name"] == "Test Person"
    
    async def test_search_field_with_all_params(self, mock_registry, mock_context):
        """Test searching field with all parameters"""
        # Arrange
        term = "test"
        entity_type = "deal"
        field = "title"
        match = "beginning"
        limit_str = "50"
        cursor = "next_page_token"
        
        mock_context.request_context.lifespan_context.pipedrive_client.search_field.return_value = (
            [
                {"id": 1, "name": "Test Deal"},
                {"id": 2, "name": "Testing Contract"}
            ],
            "another_page_token"
        )
        
        # Act
        result = await search_item_field_in_pipedrive(
            mock_context, 
            term=term,
            entity_type=entity_type,
            field=field,
            match=match,
            limit_str=limit_str,
            cursor=cursor
        )
        
        # Assert
        mock_context.request_context.lifespan_context.pipedrive_client.search_field.assert_called_once_with(
            term="test",
            entity_type="deal",
            field="title",
            match="beginning",
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
    
    async def test_search_field_with_empty_results(self, mock_registry, mock_context):
        """Test searching field with empty results"""
        # Arrange
        term = "nonexistent"
        entity_type = "person"
        field = "name"
        
        mock_context.request_context.lifespan_context.pipedrive_client.search_field.return_value = (
            [],
            None
        )
        
        # Act
        result = await search_item_field_in_pipedrive(mock_context, term, entity_type, field)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is True
        assert "data" in result_dict
        assert "items" in result_dict["data"]
        assert len(result_dict["data"]["items"]) == 0
        assert "message" in result_dict["data"]
        assert "No values found" in result_dict["data"]["message"]
    
    async def test_search_field_with_invalid_term(self, mock_registry, mock_context):
        """Test searching field with invalid term"""
        # Arrange
        term = ""
        entity_type = "person"
        field = "name"
        
        # Act
        result = await search_item_field_in_pipedrive(mock_context, term, entity_type, field)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert result_dict["error"] == "Search term cannot be empty"
    
    async def test_search_field_with_empty_entity_type(self, mock_registry, mock_context):
        """Test searching field with empty entity_type"""
        # Arrange
        term = "test"
        entity_type = ""
        field = "name"
        
        # Act
        result = await search_item_field_in_pipedrive(mock_context, term, entity_type, field)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert result_dict["error"] == "Entity type cannot be empty"
    
    async def test_search_field_with_empty_field(self, mock_registry, mock_context):
        """Test searching field with empty field"""
        # Arrange
        term = "test"
        entity_type = "person"
        field = ""
        
        # Act
        result = await search_item_field_in_pipedrive(mock_context, term, entity_type, field)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert result_dict["error"] == "Field key cannot be empty"
    
    async def test_search_field_with_invalid_entity_type(self, mock_registry, mock_context):
        """Test searching field with invalid entity_type"""
        # Arrange
        term = "test"
        entity_type = "invalid"
        field = "name"
        
        # Act
        result = await search_item_field_in_pipedrive(mock_context, term, entity_type, field)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert "Invalid entity type" in result_dict["error"]
    
    async def test_search_field_with_invalid_match(self, mock_registry, mock_context):
        """Test searching field with invalid match"""
        # Arrange
        term = "test"
        entity_type = "person"
        field = "name"
        match = "invalid"
        
        # Act
        result = await search_item_field_in_pipedrive(mock_context, term, entity_type, field, match)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert "Invalid match type" in result_dict["error"]
    
    async def test_search_field_with_short_term_for_non_exact_match(self, mock_registry, mock_context):
        """Test searching field with short term for non-exact match"""
        # Arrange
        term = "a"
        entity_type = "person"
        field = "name"
        match = "beginning"
        
        # Act
        result = await search_item_field_in_pipedrive(mock_context, term, entity_type, field, match)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert "Search term must be at least 2 characters" in result_dict["error"]
    
    async def test_search_field_with_invalid_limit(self, mock_registry, mock_context):
        """Test searching field with invalid limit"""
        # Arrange
        term = "test"
        entity_type = "person"
        field = "name"
        limit_str = "invalid"
        
        mock_context.request_context.lifespan_context.pipedrive_client.search_field.return_value = (
            [{"id": 1, "name": "Test Person"}],
            None
        )
        
        # Act
        result = await search_item_field_in_pipedrive(
            mock_context, term, entity_type, field, limit_str=limit_str
        )
        
        # Assert - should not fail, but use default limit
        mock_context.request_context.lifespan_context.pipedrive_client.search_field.assert_called_once_with(
            term="test",
            entity_type="person",
            field="name",
            match="exact",
            limit=100,  # Default limit
            cursor=None
        )
    
    async def test_search_field_with_api_error(self, mock_registry, mock_context):
        """Test handling API errors"""
        # Arrange
        term = "test"
        entity_type = "person"
        field = "name"
        
        error_response = {"success": False, "error": "API error", "error_code": 400}
        mock_context.request_context.lifespan_context.pipedrive_client.search_field.side_effect = (
            PipedriveAPIError("API error", response_data=error_response)
        )
        
        # Act
        result = await search_item_field_in_pipedrive(mock_context, term, entity_type, field)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert "API error" in result_dict["error"]
        assert result_dict["data"] == error_response
    
    async def test_search_field_with_unexpected_error(self, mock_registry, mock_context):
        """Test handling unexpected errors"""
        # Arrange
        term = "test"
        entity_type = "person"
        field = "name"
        
        mock_context.request_context.lifespan_context.pipedrive_client.search_field.side_effect = (
            Exception("Unexpected error")
        )
        
        # Act
        result = await search_item_field_in_pipedrive(mock_context, term, entity_type, field)
        
        # Assert
        result_dict = json.loads(result)
        assert result_dict["success"] is False
        assert "An unexpected error occurred" in result_dict["error"]