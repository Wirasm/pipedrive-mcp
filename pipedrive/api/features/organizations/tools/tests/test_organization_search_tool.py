import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp.server.fastmcp import Context
from pipedrive.api.features.organizations.tools.organization_search_tool import search_organizations_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient for testing"""
    # Create mock organizations client
    organizations_client = AsyncMock()

    # Set up mock response for search_organizations with sample data and next cursor
    sample_search_results = [
        {
            "id": 123,
            "name": "Acme Inc",
            "address": "123 Main St",
            "owner_id": 456,
        },
        {
            "id": 126,
            "name": "Acme Widgets",
            "address": "500 Tech Dr",
            "owner_id": 789,
        }
    ]
    organizations_client.search_organizations.return_value = (sample_search_results, "next_cursor_token")

    # Create main client with organizations property
    client = MagicMock()
    client.organizations = organizations_client

    return client


class TestSearchOrganizationsTool:
    @pytest.mark.asyncio
    async def test_search_organizations_success(self, mock_pipedrive_client):
        """Test successful organizations search"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with search term
        result = await search_organizations_in_pipedrive(
            ctx=mock_ctx,
            term="Acme"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success and data
        assert result_data["success"] is True
        assert "data" in result_data
        assert "items" in result_data["data"]
        assert len(result_data["data"]["items"]) == 2
        assert result_data["data"]["next_cursor"] == "next_cursor_token"
        assert result_data["data"]["count"] == 2
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.organizations.search_organizations.assert_called_once_with(
            term="Acme",
            fields=None,
            exact_match=False,
            include_fields=None,
            limit=100,
            cursor=None
        )
    
    @pytest.mark.asyncio
    async def test_search_organizations_with_fields(self, mock_pipedrive_client):
        """Test organizations search with specific fields"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with fields
        result = await search_organizations_in_pipedrive(
            ctx=mock_ctx,
            term="Tech",
            fields_str="name,address",
            exact_match=True,
            include_fields_str="deals,activities",
            limit_str="50"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.organizations.search_organizations.assert_called_once_with(
            term="Tech",
            fields=["name", "address"],
            exact_match=True,
            include_fields=["deals", "activities"],
            limit=50,
            cursor=None
        )
    
    @pytest.mark.asyncio
    async def test_search_organizations_with_pagination(self, mock_pipedrive_client):
        """Test organizations search with pagination"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with cursor
        result = await search_organizations_in_pipedrive(
            ctx=mock_ctx,
            term="Acme",
            cursor="previous_cursor_token"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.organizations.search_organizations.assert_called_once_with(
            term="Acme",
            fields=None,
            exact_match=False,
            include_fields=None,
            limit=100,
            cursor="previous_cursor_token"
        )
    
    @pytest.mark.asyncio
    async def test_search_organizations_empty_term(self, mock_pipedrive_client):
        """Test error handling with empty search term"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with empty term
        result = await search_organizations_in_pipedrive(
            ctx=mock_ctx,
            term=""
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Search term cannot be empty" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.organizations.search_organizations.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_search_organizations_short_term(self, mock_pipedrive_client):
        """Test error handling with short search term when exact_match is False"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with short term
        result = await search_organizations_in_pipedrive(
            ctx=mock_ctx,
            term="A",
            exact_match=False
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Search term must be at least 2 characters long" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.organizations.search_organizations.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_search_organizations_short_term_exact_match(self, mock_pipedrive_client):
        """Test success with short search term when exact_match is True"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with short term but exact_match=True
        result = await search_organizations_in_pipedrive(
            ctx=mock_ctx,
            term="A",
            exact_match=True
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.organizations.search_organizations.assert_called_once_with(
            term="A",
            fields=None,
            exact_match=True,
            include_fields=None,
            limit=100,
            cursor=None
        )
    
    @pytest.mark.asyncio
    async def test_search_organizations_api_error(self, mock_pipedrive_client):
        """Test handling of API errors"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client

        # Make the client raise an API error
        api_error = PipedriveAPIError(
            message="API Error",
            status_code=400,
            error_info="Bad Request",
            response_data={"error": "Something went wrong"}
        )
        mock_pipedrive_client.organizations.search_organizations.side_effect = api_error

        # Call the tool function
        result = await search_organizations_in_pipedrive(
            ctx=mock_ctx,
            term="Acme"
        )

        # Parse the JSON result
        result_data = json.loads(result)

        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "API Error" in result_data["error"]
        assert "data" in result_data
        assert result_data["data"]["error"] == "Something went wrong"