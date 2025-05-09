import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp.server.fastmcp import Context
from pipedrive.api.features.persons.tools.person_delete_tool import delete_person_from_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient for testing"""
    # Create mock persons client
    persons_client = AsyncMock()

    # Set up mock response for delete_person
    persons_client.delete_person.return_value = {
        "id": 123
    }

    # Create main client with persons property
    client = MagicMock()
    client.persons = persons_client

    return client


class TestDeletePersonTool:
    @pytest.mark.asyncio
    async def test_delete_person_success(self, mock_pipedrive_client):
        """Test successful person deletion"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function
        result = await delete_person_from_pipedrive(
            ctx=mock_ctx,
            id_str="123"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success and data
        assert result_data["success"] is True
        assert "data" in result_data
        assert result_data["data"]["id"] == 123
        assert "message" in result_data["data"]
        assert "Person with ID 123 was successfully deleted" in result_data["data"]["message"]
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.persons.delete_person.assert_called_once_with(
            person_id=123
        )
    
    @pytest.mark.asyncio
    async def test_delete_person_invalid_id(self, mock_pipedrive_client):
        """Test error handling with invalid ID input"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid ID
        result = await delete_person_from_pipedrive(
            ctx=mock_ctx,
            id_str="not_a_number"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Invalid person_id format" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.delete_person.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_delete_person_failed_delete(self, mock_pipedrive_client):
        """Test handling when deletion fails"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Setup mock to return error details
        mock_pipedrive_client.persons.delete_person.return_value = {
            "id": 123,
            "error_details": {
                "success": False,
                "error": "Could not delete person"
            }
        }
        
        # Call the tool function
        result = await delete_person_from_pipedrive(
            ctx=mock_ctx,
            id_str="123"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Failed to delete person with ID 123" in result_data["error"]
    
    @pytest.mark.asyncio
    async def test_delete_person_api_error(self, mock_pipedrive_client):
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
        mock_pipedrive_client.persons.delete_person.side_effect = api_error

        # Call the tool function
        result = await delete_person_from_pipedrive(
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