import json
from unittest.mock import AsyncMock, Mock, patch

import pytest

from pipedrive.api.features.item_search.client.item_search_client import ItemSearchClient


@pytest.mark.asyncio
class TestItemSearchClient:
    @pytest.fixture
    def base_client_mock(self):
        mock = AsyncMock()
        mock.request = AsyncMock()
        return mock
    
    @pytest.fixture
    def client(self, base_client_mock):
        return ItemSearchClient(base_client_mock)
    
    async def test_search_items_with_minimal_params(self, client, base_client_mock):
        """Test searching items with minimal parameters"""
        # Arrange
        term = "test"
        base_client_mock.request.return_value = {
            "success": True,
            "data": [
                {"id": 1, "type": "deal", "result_score": 0.9, "title": "Test Deal"}
            ],
            "additional_data": {"next_cursor": None}
        }
        
        # Act
        items, next_cursor = await client.search_items(term)
        
        # Assert
        base_client_mock.request.assert_called_once()
        args, kwargs = base_client_mock.request.call_args
        assert args[0] == "GET"
        assert args[1] == "/itemSearch"
        assert kwargs["query_params"] == {
            "term": "test",
            "exact_match": "false",
            "search_for_related_items": "false",
            "limit": 100
        }
        
        assert len(items) == 1
        assert items[0]["id"] == 1
        assert items[0]["type"] == "deal"
        assert next_cursor is None
    
    async def test_search_items_with_all_params(self, client, base_client_mock):
        """Test searching items with all parameters"""
        # Arrange
        term = "test"
        item_types = ["deal", "person"]
        fields = ["title", "name"]
        include_fields = ["deal.cc_email", "person.picture"]
        cursor = "next_page_token"
        
        base_client_mock.request.return_value = {
            "success": True,
            "data": [
                {"id": 1, "type": "deal", "result_score": 0.9, "title": "Test Deal"},
                {"id": 2, "type": "person", "result_score": 0.8, "name": "Test Person"}
            ],
            "additional_data": {"next_cursor": "another_page_token"}
        }
        
        # Act
        items, next_cursor = await client.search_items(
            term=term,
            item_types=item_types,
            fields=fields,
            search_for_related_items=True,
            exact_match=True,
            include_fields=include_fields,
            limit=50,
            cursor=cursor
        )
        
        # Assert
        base_client_mock.request.assert_called_once()
        args, kwargs = base_client_mock.request.call_args
        assert args[0] == "GET"
        assert args[1] == "/itemSearch"
        assert kwargs["query_params"] == {
            "term": "test",
            "item_types": "deal,person",
            "fields": "title,name",
            "search_for_related_items": "true",
            "exact_match": "true",
            "include_fields": "deal.cc_email,person.picture",
            "limit": 50,
            "cursor": "next_page_token"
        }
        
        assert len(items) == 2
        assert items[0]["id"] == 1
        assert items[0]["type"] == "deal"
        assert items[1]["id"] == 2
        assert items[1]["type"] == "person"
        assert next_cursor == "another_page_token"
    
    async def test_search_items_validation_empty_term(self, client):
        """Test that searching with an empty term raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            await client.search_items("")
        
        assert "Search term cannot be empty" in str(exc_info.value)
    
    async def test_search_items_validation_short_term(self, client):
        """Test that searching with a short term raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            await client.search_items("a", exact_match=False)
        
        assert "Search term must be at least 2 characters" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_search_field_with_minimal_params(self, client, base_client_mock):
        """Test searching field with minimal parameters"""
        # Arrange
        term = "test"
        entity_type = "person"
        field = "name"
        
        base_client_mock.request.return_value = {
            "success": True,
            "data": [
                {"id": 1, "name": "Test Person"}
            ],
            "additional_data": {"next_cursor": None}
        }
        
        # Act
        items, next_cursor = await client.search_field(term, entity_type, field)
        
        # Assert
        base_client_mock.request.assert_called_once()
        args, kwargs = base_client_mock.request.call_args
        assert args[0] == "GET"
        assert args[1] == "/itemSearch/field"
        assert kwargs["query_params"] == {
            "term": "test",
            "entity_type": "person",
            "field": "name",
            "match": "exact",
            "limit": 100
        }
        
        assert len(items) == 1
        assert items[0]["id"] == 1
        assert items[0]["name"] == "Test Person"
        assert next_cursor is None
    
    async def test_search_field_with_all_params(self, client, base_client_mock):
        """Test searching field with all parameters"""
        # Arrange
        term = "test"
        entity_type = "deal"
        field = "title"
        match = "beginning"
        cursor = "next_page_token"
        
        base_client_mock.request.return_value = {
            "success": True,
            "data": [
                {"id": 1, "name": "Test Deal"},
                {"id": 2, "name": "Testing Contract"}
            ],
            "additional_data": {"next_cursor": "another_page_token"}
        }
        
        # Act
        items, next_cursor = await client.search_field(
            term=term,
            entity_type=entity_type,
            field=field,
            match=match,
            limit=50,
            cursor=cursor
        )
        
        # Assert
        base_client_mock.request.assert_called_once()
        args, kwargs = base_client_mock.request.call_args
        assert args[0] == "GET"
        assert args[1] == "/itemSearch/field"
        assert kwargs["query_params"] == {
            "term": "test",
            "entity_type": "deal",
            "field": "title",
            "match": "beginning",
            "limit": 50,
            "cursor": "next_page_token"
        }
        
        assert len(items) == 2
        assert items[0]["id"] == 1
        assert items[0]["name"] == "Test Deal"
        assert items[1]["id"] == 2
        assert items[1]["name"] == "Testing Contract"
        assert next_cursor == "another_page_token"
    
    async def test_search_field_validation_empty_term(self, client):
        """Test that searching field with an empty term raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            await client.search_field("", "person", "name")
        
        assert "Search term cannot be empty" in str(exc_info.value)
    
    async def test_search_field_validation_invalid_entity_type(self, client):
        """Test that searching field with an invalid entity type raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            await client.search_field("test", "invalid_type", "name")
        
        assert "Invalid entity type" in str(exc_info.value)
    
    async def test_search_field_validation_empty_field(self, client):
        """Test that searching field with an empty field raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            await client.search_field("test", "person", "")
        
        assert "Field key cannot be empty" in str(exc_info.value)
    
    async def test_search_field_validation_invalid_match(self, client):
        """Test that searching field with an invalid match type raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            await client.search_field("test", "person", "name", match="invalid")
        
        assert "Invalid match type" in str(exc_info.value)