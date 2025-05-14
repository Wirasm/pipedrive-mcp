import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp.server.fastmcp import Context
from pipedrive.api.features.organizations.tools.organization_create_tool import create_organization_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient for testing with the new structure"""
    # Create mock organizations client
    organizations_client = AsyncMock()

    # Set up mock response for create_organization
    organizations_client.create_organization.return_value = {
        "id": 123,
        "name": "Test Organization",
        "address": "123 Main St",
        "owner_id": 456,
        "visible_to": 3
    }

    # Create main client with organizations property
    client = MagicMock()
    client.organizations = organizations_client

    return client


class TestCreateOrganizationTool:
    @pytest.mark.asyncio
    async def test_create_organization_success(self, mock_pipedrive_client):
        """Test successful organization creation"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function
        result = await create_organization_in_pipedrive(
            ctx=mock_ctx,
            name="Test Organization",
            address="123 Main St",
            visible_to_str="3",
            industry="Technology"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success and data
        assert result_data["success"] is True
        assert "data" in result_data
        assert result_data["data"]["id"] == 123
        assert result_data["data"]["name"] == "Test Organization"
        assert result_data["data"]["address"] == "123 Main St"
        assert result_data["data"]["visible_to"] == 3
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.organizations.create_organization.assert_called_once()
        call_kwargs = mock_pipedrive_client.organizations.create_organization.call_args.kwargs
        assert call_kwargs["name"] == "Test Organization"
        assert call_kwargs["address"] == {"value": "123 Main St"}
        assert call_kwargs["visible_to"] == 3
        assert call_kwargs["industry"] == "Technology"
    
    @pytest.mark.asyncio
    async def test_create_organization_invalid_id(self, mock_pipedrive_client):
        """Test error handling with invalid ID input"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid owner_id
        result = await create_organization_in_pipedrive(
            ctx=mock_ctx,
            name="Test Organization",
            owner_id_str="not_a_number"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "owner_id must be a numeric string" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.organizations.create_organization.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_create_organization_with_custom_fields(self, mock_pipedrive_client):
        """Test organization creation with custom fields"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Custom fields dictionary
        custom_fields = {
            "cf_annual_revenue": 1000000,
            "cf_company_size": "101-250"
        }
        
        # Call the tool function
        result = await create_organization_in_pipedrive(
            ctx=mock_ctx,
            name="Test Organization with Custom Fields",
            custom_fields_dict=custom_fields
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success and data
        assert result_data["success"] is True
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.organizations.create_organization.assert_called_once()
        call_kwargs = mock_pipedrive_client.organizations.create_organization.call_args.kwargs
        assert call_kwargs["name"] == "Test Organization with Custom Fields"
        assert call_kwargs["cf_annual_revenue"] == 1000000
        assert call_kwargs["cf_company_size"] == "101-250"
        
    @pytest.mark.asyncio
    async def test_create_organization_api_error(self, mock_pipedrive_client):
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
        mock_pipedrive_client.organizations.create_organization.side_effect = api_error

        # Call the tool function
        result = await create_organization_in_pipedrive(
            ctx=mock_ctx,
            name="Test Organization"
        )

        # Parse the JSON result
        result_data = json.loads(result)

        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "API Error" in result_data["error"]
        assert "data" in result_data
        assert result_data["data"]["error"] == "Something went wrong"