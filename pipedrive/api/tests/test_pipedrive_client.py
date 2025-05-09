import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from pipedrive.api.pipedrive_client import PipedriveClient
from pipedrive.api.base_client import BaseClient
from pipedrive.api.features.persons.client.person_client import PersonClient


@pytest.fixture
def mock_http_client():
    """Create a mock httpx.AsyncClient"""
    return AsyncMock(spec=httpx.AsyncClient)


class TestPipedriveClient:
    """Tests for the PipedriveClient class"""
    
    def test_init(self, mock_http_client):
        """Test initializing PipedriveClient"""
        with patch("pipedrive.api.pipedrive_client.BaseClient") as mock_base_client_class:
            with patch("pipedrive.api.pipedrive_client.PersonClient") as mock_person_client_class:
                # Set up mock return values
                mock_base_client = MagicMock()
                mock_base_client_class.return_value = mock_base_client
                
                mock_person_client = MagicMock()
                mock_person_client_class.return_value = mock_person_client
                
                # Create client
                client = PipedriveClient(
                    api_token="test_token",
                    company_domain="test",
                    http_client=mock_http_client
                )
                
                # Check that base client was initialized correctly
                mock_base_client_class.assert_called_once_with(
                    "test_token", "test", mock_http_client
                )
                
                # Check that person client was initialized correctly
                mock_person_client_class.assert_called_once_with(mock_base_client)
                
                # Check client attributes
                assert client.base_client == mock_base_client
                assert client.persons == mock_person_client
    
    @pytest.mark.asyncio
    async def test_create_person_delegates_to_persons_client(self, mock_http_client):
        """Test that create_person delegates to persons client"""
        # Create client with mock persons client
        client = PipedriveClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        # Replace persons client with mock
        mock_persons_client = AsyncMock(spec=PersonClient)
        mock_persons_client.create_person.return_value = {"id": 123, "name": "Test Person"}
        client.persons = mock_persons_client
        
        # Call the method
        result = await client.create_person(
            name="Test Person",
            owner_id=456,
            emails=[{"value": "test@example.com"}]
        )
        
        # Check result
        assert result["id"] == 123
        assert result["name"] == "Test Person"
        
        # Check that persons client method was called with correct parameters
        mock_persons_client.create_person.assert_called_once_with(
            name="Test Person",
            owner_id=456,
            emails=[{"value": "test@example.com"}],
            org_id=None,
            phones=None,
            visible_to=None,
            add_time=None,
            custom_fields=None
        )
    
    @pytest.mark.asyncio
    async def test_get_person_delegates_to_persons_client(self, mock_http_client):
        """Test that get_person delegates to persons client"""
        # Create client with mock persons client
        client = PipedriveClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        # Replace persons client with mock
        mock_persons_client = AsyncMock(spec=PersonClient)
        mock_persons_client.get_person.return_value = {"id": 123, "name": "Test Person"}
        client.persons = mock_persons_client
        
        # Call the method
        result = await client.get_person(person_id=123)
        
        # Check result
        assert result["id"] == 123
        assert result["name"] == "Test Person"
        
        # Check that persons client method was called with correct parameters
        mock_persons_client.get_person.assert_called_once_with(
            person_id=123,
            include_fields=None,
            custom_fields_keys=None
        )
    
    @pytest.mark.asyncio
    async def test_update_person_delegates_to_persons_client(self, mock_http_client):
        """Test that update_person delegates to persons client"""
        # Create client with mock persons client
        client = PipedriveClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        # Replace persons client with mock
        mock_persons_client = AsyncMock(spec=PersonClient)
        mock_persons_client.update_person.return_value = {"id": 123, "name": "Updated Person"}
        client.persons = mock_persons_client
        
        # Call the method
        result = await client.update_person(
            person_id=123,
            name="Updated Person"
        )
        
        # Check result
        assert result["id"] == 123
        assert result["name"] == "Updated Person"
        
        # Check that persons client method was called with correct parameters
        mock_persons_client.update_person.assert_called_once_with(
            person_id=123,
            name="Updated Person",
            owner_id=None,
            org_id=None,
            emails=None,
            phones=None,
            visible_to=None,
            custom_fields=None
        )
    
    @pytest.mark.asyncio
    async def test_delete_person_delegates_to_persons_client(self, mock_http_client):
        """Test that delete_person delegates to persons client"""
        # Create client with mock persons client
        client = PipedriveClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        # Replace persons client with mock
        mock_persons_client = AsyncMock(spec=PersonClient)
        mock_persons_client.delete_person.return_value = {"id": 123}
        client.persons = mock_persons_client
        
        # Call the method
        result = await client.delete_person(person_id=123)
        
        # Check result
        assert result["id"] == 123
        
        # Check that persons client method was called with correct parameters
        mock_persons_client.delete_person.assert_called_once_with(person_id=123)
    
    @pytest.mark.asyncio
    async def test_list_persons_delegates_to_persons_client(self, mock_http_client):
        """Test that list_persons delegates to persons client"""
        # Create client with mock persons client
        client = PipedriveClient(
            api_token="test_token",
            company_domain="test",
            http_client=mock_http_client
        )
        
        # Replace persons client with mock
        mock_persons_client = AsyncMock(spec=PersonClient)
        mock_persons_client.list_persons.return_value = (
            [{"id": 123}, {"id": 456}],
            "next_cursor"
        )
        client.persons = mock_persons_client
        
        # Call the method
        persons, next_cursor = await client.list_persons(
            limit=2,
            owner_id=789
        )
        
        # Check result
        assert len(persons) == 2
        assert persons[0]["id"] == 123
        assert persons[1]["id"] == 456
        assert next_cursor == "next_cursor"
        
        # Check that persons client method was called with correct parameters
        mock_persons_client.list_persons.assert_called_once_with(
            limit=2,
            cursor=None,
            filter_id=None,
            owner_id=789,
            org_id=None,
            sort_by=None,
            sort_direction=None,
            include_fields=None,
            custom_fields_keys=None,
            updated_since=None,
            updated_until=None
        )