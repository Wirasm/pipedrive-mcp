import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp.server.fastmcp import Context
from pipedrive.api.features.persons.tools.person_get_tool import get_person_from_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient for testing"""
    # Create mock persons client
    persons_client = AsyncMock()

    # Set up mock response for get_person
    persons_client.get_person.return_value = {
        "id": 123,
        "name": "Test Person",
        "emails": [{"value": "test@example.com", "label": "work", "primary": True}],
        "phones": [{"value": "123456789", "label": "work", "primary": True}]
    }

    # Create main client with persons property
    client = MagicMock()
    client.persons = persons_client

    return client


class TestGetPersonTool:
    @pytest.mark.asyncio
    async def test_get_person_success(self, mock_pipedrive_client):
        """Test successful person retrieval"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function
        result = await get_person_from_pipedrive(
            ctx=mock_ctx,
            id_str="123"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success and data
        assert result_data["success"] is True
        assert "data" in result_data
        assert result_data["data"]["id"] == 123
        assert result_data["data"]["name"] == "Test Person"
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.persons.get_person.assert_called_once_with(
            person_id=123,
            include_fields=None,
            custom_fields_keys=None
        )
    
    @pytest.mark.asyncio
    async def test_get_person_with_fields(self, mock_pipedrive_client):
        """Test person retrieval with additional fields"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with include_fields
        result = await get_person_from_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            include_fields_str="open_deals_count,notes_count",
            custom_fields_str="custom_field1,custom_field2"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.persons.get_person.assert_called_once_with(
            person_id=123,
            include_fields=["open_deals_count", "notes_count"],
            custom_fields_keys=["custom_field1", "custom_field2"]
        )
    
    @pytest.mark.asyncio
    async def test_get_person_invalid_id(self, mock_pipedrive_client):
        """Test error handling with invalid ID input"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid ID
        result = await get_person_from_pipedrive(
            ctx=mock_ctx,
            id_str="not_a_number"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "person_id must be a numeric string" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.get_person.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_person_not_found(self, mock_pipedrive_client):
        """Test handling when person is not found"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Make the client return empty result (person not found)
        mock_pipedrive_client.persons.get_person.return_value = {}
        
        # Call the tool function
        result = await get_person_from_pipedrive(
            ctx=mock_ctx,
            id_str="999"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Person with ID 999 not found" in result_data["error"]
    
    @pytest.mark.asyncio
    async def test_get_person_api_error(self, mock_pipedrive_client):
        """Test handling of API errors"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client

        # Make the client raise an API error
        api_error = PipedriveAPIError(
            message="API Error",
            status_code=404,
            error_info="Person not found",
            response_data={"error": "The requested person does not exist"}
        )
        mock_pipedrive_client.persons.get_person.side_effect = api_error

        # Call the tool function
        result = await get_person_from_pipedrive(
            ctx=mock_ctx,
            id_str="123"
        )

        # Parse the JSON result
        result_data = json.loads(result)

        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "API Error" in result_data["error"]
        assert "data" in result_data
        assert result_data["data"]["error"] == "The requested person does not exist"