import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp.server.fastmcp import Context
from pipedrive.api.features.persons.tools.person_search_tool import search_persons_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient for testing"""
    # Create mock persons client
    persons_client = AsyncMock()

    # Set up mock response for search_persons
    search_results = [
        {
            "id": 123,
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+123456789",
            "organization": {"id": 456, "name": "Example Org"}
        },
        {
            "id": 124,
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "+987654321",
            "organization": {"id": 456, "name": "Example Org"}
        }
    ]
    persons_client.search_persons.return_value = (search_results, "next_cursor_value")

    # Create main client with persons property
    client = MagicMock()
    client.persons = persons_client

    return client


class TestSearchPersonsTool:
    @pytest.mark.asyncio
    async def test_search_persons_success(self, mock_pipedrive_client):
        """Test successful person search"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function
        result = await search_persons_in_pipedrive(
            ctx=mock_ctx,
            term="Doe"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success and data
        assert result_data["success"] is True
        assert "data" in result_data
        assert "items" in result_data["data"]
        assert len(result_data["data"]["items"]) == 2
        assert result_data["data"]["count"] == 2
        assert result_data["data"]["next_cursor"] == "next_cursor_value"
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.persons.search_persons.assert_called_once_with(
            term="Doe",
            fields=None,
            exact_match=False,
            organization_id=None,
            include_fields=None,
            limit=100
        )
    
    @pytest.mark.asyncio
    async def test_search_persons_with_fields(self, mock_pipedrive_client):
        """Test person search with additional parameters"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with additional parameters
        result = await search_persons_in_pipedrive(
            ctx=mock_ctx,
            term="Doe",
            fields_str="name,email",
            exact_match=True,
            org_id_str="456",
            include_fields_str="person.picture",
            limit_str="50"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.persons.search_persons.assert_called_once_with(
            term="Doe",
            fields=["name", "email"],
            exact_match=True,
            organization_id=456,
            include_fields=["person.picture"],
            limit=50
        )
    
    @pytest.mark.asyncio
    async def test_search_persons_short_term(self, mock_pipedrive_client):
        """Test error handling with too short search term"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with short term
        result = await search_persons_in_pipedrive(
            ctx=mock_ctx,
            term="A"  # Too short when exact_match is False
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Search term must be at least 2 characters" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.search_persons.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_search_persons_empty_term(self, mock_pipedrive_client):
        """Test error handling with empty search term"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with empty term
        result = await search_persons_in_pipedrive(
            ctx=mock_ctx,
            term="   "  # Empty or whitespace
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Search term cannot be empty" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.search_persons.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_search_persons_no_results(self, mock_pipedrive_client):
        """Test handling when no search results are found"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Set up empty search results
        mock_pipedrive_client.persons.search_persons.return_value = ([], None)
        
        # Call the tool function
        result = await search_persons_in_pipedrive(
            ctx=mock_ctx,
            term="NonExistentPerson"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success but empty results
        assert result_data["success"] is True
        assert "data" in result_data
        assert "items" in result_data["data"]
        assert len(result_data["data"]["items"]) == 0
        assert "message" in result_data["data"]
        assert "No persons found matching" in result_data["data"]["message"]
    
    @pytest.mark.asyncio
    async def test_search_persons_invalid_org_id(self, mock_pipedrive_client):
        """Test error handling with invalid organization ID"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid org_id
        result = await search_persons_in_pipedrive(
            ctx=mock_ctx,
            term="Doe",
            org_id_str="not_a_number"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Invalid organization_id format" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.search_persons.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_search_persons_invalid_limit(self, mock_pipedrive_client):
        """Test handling of invalid limit value"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid limit
        result = await search_persons_in_pipedrive(
            ctx=mock_ctx,
            term="Doe",
            limit_str="not_a_number"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success (should default to 100)
        assert result_data["success"] is True
        
        # Verify the client was called with default limit
        mock_pipedrive_client.persons.search_persons.assert_called_once()
        call_kwargs = mock_pipedrive_client.persons.search_persons.call_args.kwargs
        assert call_kwargs["limit"] == 100
    
    @pytest.mark.asyncio
    async def test_search_persons_api_error(self, mock_pipedrive_client):
        """Test handling of API errors"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client

        # Make the client raise an API error
        api_error = PipedriveAPIError(
            message="API Error",
            status_code=400,
            error_info="Bad Request",
            response_data={"error": "Search failed"}
        )
        mock_pipedrive_client.persons.search_persons.side_effect = api_error

        # Call the tool function
        result = await search_persons_in_pipedrive(
            ctx=mock_ctx,
            term="Doe"
        )

        # Parse the JSON result
        result_data = json.loads(result)

        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "API Error" in result_data["error"]
        assert "data" in result_data
        assert result_data["data"]["error"] == "Search failed"