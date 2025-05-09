import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from pipedrive.api.base_client import BaseClient
from pipedrive.api.features.persons.client.person_client import PersonClient


@pytest.fixture
def mock_base_client():
    """Create a mock BaseClient"""
    client = AsyncMock(spec=BaseClient)
    
    # Mock successful response for create_person
    client.request.return_value = {
        "success": True,
        "data": {
            "id": 123,
            "name": "Test Person",
            "emails": [{"value": "test@example.com", "label": "work", "primary": True}],
            "phones": [{"value": "123456789", "label": "work", "primary": True}]
        }
    }
    
    return client


class TestPersonClient:
    """Tests for the PersonClient class"""
    
    def test_init(self, mock_base_client):
        """Test initializing PersonClient"""
        client = PersonClient(mock_base_client)
        assert client.base_client == mock_base_client
    
    @pytest.mark.asyncio
    async def test_create_person(self, mock_base_client):
        """Test creating a person"""
        client = PersonClient(mock_base_client)
        
        # Call the method
        result = await client.create_person(
            name="Test Person",
            owner_id=456,
            emails=[{"value": "test@example.com", "label": "work", "primary": True}]
        )
        
        # Check result
        assert result["id"] == 123
        assert result["name"] == "Test Person"
        
        # Check that base_client.request was called with correct parameters
        mock_base_client.request.assert_called_once()
        call_args = mock_base_client.request.call_args
        assert call_args[0][0] == "POST"  # Method
        assert call_args[0][1] == "/persons"  # Endpoint
        
        # Check JSON payload
        payload = call_args[1]["json_payload"]
        assert payload["name"] == "Test Person"
        assert payload["owner_id"] == 456
        assert payload["emails"][0]["value"] == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_get_person(self, mock_base_client):
        """Test getting a person"""
        client = PersonClient(mock_base_client)
        
        # Set up mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "name": "Test Person"
            }
        }
        
        # Call the method
        result = await client.get_person(person_id=123)
        
        # Check result
        assert result["id"] == 123
        assert result["name"] == "Test Person"
        
        # Check that base_client.request was called with correct parameters
        mock_base_client.request.assert_called_once()
        call_args = mock_base_client.request.call_args
        assert call_args[0][0] == "GET"  # Method
        assert call_args[0][1] == "/persons/123"  # Endpoint
    
    @pytest.mark.asyncio
    async def test_update_person(self, mock_base_client):
        """Test updating a person"""
        client = PersonClient(mock_base_client)
        
        # Set up mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "name": "Updated Person"
            }
        }
        
        # Call the method
        result = await client.update_person(
            person_id=123,
            name="Updated Person"
        )
        
        # Check result
        assert result["id"] == 123
        assert result["name"] == "Updated Person"
        
        # Check that base_client.request was called with correct parameters
        mock_base_client.request.assert_called_once()
        call_args = mock_base_client.request.call_args
        assert call_args[0][0] == "PATCH"  # Method
        assert call_args[0][1] == "/persons/123"  # Endpoint
        assert call_args[1]["json_payload"]["name"] == "Updated Person"
    
    @pytest.mark.asyncio
    async def test_update_person_no_fields(self, mock_base_client):
        """Test updating a person with no fields"""
        client = PersonClient(mock_base_client)
        
        # Test that ValueError is raised when no update fields are provided
        with pytest.raises(ValueError, match="At least one field must be provided"):
            await client.update_person(person_id=123)
        
        # Check that base_client.request was not called
        mock_base_client.request.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_delete_person(self, mock_base_client):
        """Test deleting a person"""
        client = PersonClient(mock_base_client)
        
        # Set up mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123
            }
        }
        
        # Call the method
        result = await client.delete_person(person_id=123)
        
        # Check result
        assert result["id"] == 123
        
        # Check that base_client.request was called with correct parameters
        mock_base_client.request.assert_called_once()
        call_args = mock_base_client.request.call_args
        assert call_args[0][0] == "DELETE"  # Method
        assert call_args[0][1] == "/persons/123"  # Endpoint
    
    @pytest.mark.asyncio
    async def test_list_persons(self, mock_base_client):
        """Test listing persons"""
        client = PersonClient(mock_base_client)
        
        # Set up mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": [
                {"id": 123, "name": "Person 1"},
                {"id": 456, "name": "Person 2"}
            ],
            "additional_data": {
                "next_cursor": "next_page_cursor"
            }
        }
        
        # Call the method
        persons, next_cursor = await client.list_persons(
            limit=2,
            owner_id=789
        )
        
        # Check result
        assert len(persons) == 2
        assert persons[0]["id"] == 123
        assert persons[1]["name"] == "Person 2"
        assert next_cursor == "next_page_cursor"
        
        # Check that base_client.request was called with correct parameters
        mock_base_client.request.assert_called_once()
        call_args = mock_base_client.request.call_args
        assert call_args[0][0] == "GET"  # Method
        assert call_args[0][1] == "/persons"  # Endpoint
        
        # Check query parameters
        query_params = call_args[1]["query_params"]
        assert query_params["limit"] == 2
        assert query_params["owner_id"] == 789