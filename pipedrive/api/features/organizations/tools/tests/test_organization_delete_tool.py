import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp.server.fastmcp import Context
from pipedrive.api.features.organizations.tools.organization_delete_tool import delete_organization_from_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient for testing"""
    # Create mock organizations client
    organizations_client = AsyncMock()

    # Set up mock response for delete_organization
    organizations_client.delete_organization.return_value = {
        "id": 123,
        "success": True
    }

    # Create main client with organizations property
    client = MagicMock()
    client.organizations = organizations_client

    return client


class TestDeleteOrganizationTool:
    @pytest.mark.asyncio
    async def test_delete_organization_success(self, mock_pipedrive_client):
        """Test successful organization deletion"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function
        result = await delete_organization_from_pipedrive(
            ctx=mock_ctx,
            id_str="123"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success and data
        assert result_data["success"] is True
        assert "data" in result_data
        assert result_data["data"]["id"] == 123
        assert result_data["data"]["success"] is True
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.organizations.delete_organization.assert_called_once_with(
            organization_id=123
        )
    
    @pytest.mark.asyncio
    async def test_delete_organization_invalid_id(self, mock_pipedrive_client):
        """Test error handling with invalid ID input"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid ID
        result = await delete_organization_from_pipedrive(
            ctx=mock_ctx,
            id_str="not_a_number"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "organization_id must be a numeric string" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.organizations.delete_organization.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_delete_organization_api_error(self, mock_pipedrive_client):
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
        mock_pipedrive_client.organizations.delete_organization.side_effect = api_error

        # Call the tool function
        result = await delete_organization_from_pipedrive(
            ctx=mock_ctx,
            id_str="999"
        )

        # Parse the JSON result
        result_data = json.loads(result)

        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "API Error" in result_data["error"]
        assert "data" in result_data
        assert result_data["data"]["error"] == "Organization not found"