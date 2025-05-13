import pytest
from pydantic import ValidationError

from pipedrive.api.features.item_search.models.search_result import (
    SearchResult,
    ItemSearchResults,
    FieldSearchResult,
    FieldSearchResults
)


class TestSearchResult:
    def test_search_result_creation(self):
        """Test creating a SearchResult with valid data"""
        data = {
            "id": 123,
            "type": "deal",
            "result_score": 0.95,
            "title": "Sample Deal"
        }
        
        result = SearchResult(**data)
        
        assert result.id == 123
        assert result.type == "deal"
        assert result.result_score == 0.95
        assert result.title == "Sample Deal"
        
    def test_search_result_with_invalid_type(self):
        """Test that creating a SearchResult with invalid type raises error"""
        data = {
            "id": 123,
            "type": "invalid_type",
            "result_score": 0.95
        }
        
        with pytest.raises(ValidationError) as exc_info:
            SearchResult(**data)
            
        # Check that the error message contains info about invalid type
        assert "Invalid item type" in str(exc_info.value)
        
    def test_from_api_response_deal(self):
        """Test creating a SearchResult from a deal API response"""
        api_data = {
            "id": 42,
            "type": "deal",
            "result_score": 1.22724,
            "title": "Sample Deal",
            "value": 53883,
            "currency": "USD",
            "status": "open",
            "visible_to": 3,
            "person_id": 6,
            "person_name": "Sample Person",
            "org_id": 9,
            "org_name": "Sample Organization",
            "custom_fields": {"Sample text": "Sample value"}
        }
        
        result = SearchResult.from_api_response(api_data)
        
        assert result.id == 42
        assert result.type == "deal"
        assert result.result_score == 1.22724
        assert result.title == "Sample Deal"
        assert result.value == 53883
        assert result.currency == "USD"
        assert result.status == "open"
        assert result.visible_to == 3
        assert result.person == {"id": 6, "name": "Sample Person"}
        assert result.organization == {"id": 9, "name": "Sample Organization"}
        
    def test_from_api_response_person(self):
        """Test creating a SearchResult from a person API response"""
        api_data = {
            "id": 6,
            "type": "person",
            "result_score": 0.29955,
            "name": "Sample Person",
            "phone": [{"value": "555123123", "primary": "true"}],
            "email": [{"value": "primary@email.com", "primary": "true"}],
            "visible_to": 1,
            "org_id": 9,
            "org_name": "Sample Organization"
        }
        
        result = SearchResult.from_api_response(api_data)
        
        assert result.id == 6
        assert result.type == "person"
        assert result.result_score == 0.29955
        assert result.name == "Sample Person"
        assert result.phone[0]["value"] == "555123123"
        assert result.email[0]["value"] == "primary@email.com"
        assert result.visible_to == 1
        assert result.organization == {"id": 9, "name": "Sample Organization"}
        
    def test_from_api_response_organization(self):
        """Test creating a SearchResult from an organization API response"""
        api_data = {
            "id": 9,
            "type": "organization",
            "result_score": 0.31335002,
            "name": "Sample Organization",
            "address": "Dabas, Hungary",
            "visible_to": 3
        }
        
        result = SearchResult.from_api_response(api_data)
        
        assert result.id == 9
        assert result.type == "organization"
        assert result.result_score == 0.31335002
        assert result.name == "Sample Organization"
        assert result.address == "Dabas, Hungary"
        assert result.visible_to == 3
        
    def test_from_api_response_file(self):
        """Test creating a SearchResult from a file API response"""
        api_data = {
            "id": 3,
            "type": "file",
            "result_score": 0.0093,
            "name": "Sample file attachment.txt",
            "url": "/files/3/download"
        }
        
        result = SearchResult.from_api_response(api_data)
        
        assert result.id == 3
        assert result.type == "file"
        assert result.result_score == 0.0093
        assert result.name == "Sample file attachment.txt"
        assert result.url == "/files/3/download"


class TestItemSearchResults:
    def test_item_search_results_creation(self):
        """Test creating ItemSearchResults with valid data"""
        item1 = SearchResult(id=1, type="deal", result_score=0.9, title="Deal 1")
        item2 = SearchResult(id=2, type="person", result_score=0.8, name="Person 1")
        
        results = ItemSearchResults(items=[item1, item2], next_cursor="abc123")
        
        assert len(results.items) == 2
        assert results.next_cursor == "abc123"
        assert results.total_count is None  # Not set manually
        
    def test_from_api_response(self):
        """Test creating ItemSearchResults from API response"""
        api_data = {
            "items": [
                {
                    "id": 42,
                    "type": "deal",
                    "result_score": 1.22724,
                    "title": "Sample Deal"
                },
                {
                    "id": 6,
                    "type": "person",
                    "result_score": 0.29955,
                    "name": "Sample Person"
                },
                {
                    "id": 9,
                    "type": "organization",
                    "result_score": 0.31335002,
                    "name": "Sample Organization"
                }
            ],
            "next_cursor": "eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
        }
        
        results = ItemSearchResults.from_api_response(api_data)
        
        assert len(results.items) == 3
        assert results.total_count == 3
        assert results.next_cursor == "eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
        assert results.deal_count == 1
        assert results.person_count == 1
        assert results.organization_count == 1
        assert results.product_count == 0


class TestFieldSearchResult:
    def test_field_search_result_creation(self):
        """Test creating a FieldSearchResult with valid data"""
        data = {
            "id": 123,
            "name": "John Doe"
        }
        
        result = FieldSearchResult(**data)
        
        assert result.id == 123
        assert result.name == "John Doe"
        
    def test_from_api_response(self):
        """Test creating a FieldSearchResult from API response"""
        api_data = {
            "id": 1,
            "name": "Jane Doe"
        }
        
        result = FieldSearchResult.from_api_response(api_data)
        
        assert result.id == 1
        assert result.name == "Jane Doe"


class TestFieldSearchResults:
    def test_field_search_results_creation(self):
        """Test creating FieldSearchResults with valid data"""
        item1 = FieldSearchResult(id=1, name="Value 1")
        item2 = FieldSearchResult(id=2, name="Value 2")
        
        results = FieldSearchResults(items=[item1, item2], next_cursor="abc123")
        
        assert len(results.items) == 2
        assert results.next_cursor == "abc123"
        
    def test_from_api_response(self):
        """Test creating FieldSearchResults from API response"""
        api_data = {
            "items": [
                {
                    "id": 1,
                    "name": "Jane Doe"
                },
                {
                    "id": 2,
                    "name": "John Doe"
                }
            ],
            "next_cursor": "eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"
        }
        
        results = FieldSearchResults.from_api_response(api_data)
        
        assert len(results.items) == 2
        assert results.items[0].id == 1
        assert results.items[0].name == "Jane Doe"
        assert results.items[1].id == 2
        assert results.items[1].name == "John Doe"
        assert results.next_cursor == "eyJmaWVsZCI6ImlkIiwiZmllbGRWYWx1ZSI6Nywic29ydERpcmVjdGlvbiI6ImFzYyIsImlkIjo3fQ"