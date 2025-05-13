import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp.server.fastmcp import Context
from pipedrive.api.features.organizations.tools.organization_update_tool import update_organization_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient for testing"""
    # Create mock organizations client
    organizations_client = AsyncMock()

    # Set up mock response for update_organization
    organizations_client.update_organization.return_value = {
        "id": 123,
        "name": "Updated Organization",
        "address": "456 New Street",
        "owner_id": 789,
        "visible_to": 3
    }

    # Create main client with organizations property
    client = MagicMock()
    client.organizations = organizations_client

    return client


class TestUpdateOrganizationTool:
    @pytest.mark.asyncio
    async def test_update_organization_success(self, mock_pipedrive_client):
        """Test successful organization update"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function
        result = await update_organization_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            name="Updated Organization",
            address="456 New Street",
            owner_id_str="789",
            visible_to_str="3"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success and data
        assert result_data["success"] is True
        assert "data" in result_data
        assert result_data["data"]["id"] == 123
        assert result_data["data"]["name"] == "Updated Organization"
        assert result_data["data"]["address"] == "456 New Street"
        assert result_data["data"]["owner_id"] == 789
        assert result_data["data"]["visible_to"] == 3
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.organizations.update_organization.assert_called_once_with(
            organization_id=123,
            name="Updated Organization",
            address={"value": "456 New Street"},
            owner_id=789,
            visible_to=3
        )
    
    @pytest.mark.asyncio
    async def test_update_organization_partial(self, mock_pipedrive_client):
        """Test partial organization update"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with only one field
        result = await update_organization_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            name="Updated Organization"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.organizations.update_organization.assert_called_once_with(
            organization_id=123,
            name="Updated Organization"
        )
    
    @pytest.mark.asyncio
    async def test_update_organization_no_fields(self, mock_pipedrive_client):
        """Test error handling when no update fields are provided"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with no update fields
        result = await update_organization_in_pipedrive(
            ctx=mock_ctx,
            id_str="123"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "At least one field must be provided" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.organizations.update_organization.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_organization_invalid_id(self, mock_pipedrive_client):
        """Test error handling with invalid ID input"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid ID
        result = await update_organization_in_pipedrive(
            ctx=mock_ctx,
            id_str="not_a_number",
            name="Updated Organization"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Invalid organization_id format" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.organizations.update_organization.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_organization_invalid_visible_to(self, mock_pipedrive_client):
        """Test error handling with invalid visible_to value"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid visible_to
        result = await update_organization_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            visible_to_str="5"  # Invalid visibility value, should be 1-4
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Invalid visibility value" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.organizations.update_organization.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_organization_api_error(self, mock_pipedrive_client):
        """Test handling of API errors"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client

        # Make the client raise an API error
        api_error = PipedriveAPIError(
            message="API Error",
            status_code=404,
            error_info="Not Found",
            response_data={"error": "Organization not found"}
        )
        mock_pipedrive_client.organizations.update_organization.side_effect = api_error

        # Call the tool function
        result = await update_organization_in_pipedrive(
            ctx=mock_ctx,
            id_str="999",
            name="Updated Organization"
        )

        # Parse the JSON result
        result_data = json.loads(result)

        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "API Error" in result_data["error"]
        assert "data" in result_data
        assert result_data["data"]["error"] == "Organization not found"