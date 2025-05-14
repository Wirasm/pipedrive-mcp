import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp.server.fastmcp import Context
from pipedrive.api.features.persons.tools.person_create_tool import create_person_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient for testing with the new structure"""
    # Create mock persons client
    persons_client = AsyncMock()

    # Set up mock response for create_person
    persons_client.create_person.return_value = {
        "id": 123,
        "name": "Test Person",
        "emails": [{"value": "test@example.com", "label": "work", "primary": True}],
        "phones": [{"value": "123456789", "label": "work", "primary": True}]
    }

    # Create main client with persons property
    client = MagicMock()
    client.persons = persons_client

    return client


class TestCreatePersonTool:
    @pytest.mark.asyncio
    async def test_create_person_success(self, mock_pipedrive_client):
        """Test successful person creation"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function
        result = await create_person_in_pipedrive(
            ctx=mock_ctx,
            name="Test Person",
            email_address="test@example.com",
            phone_number="123456789"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success and data
        assert result_data["success"] is True
        assert "data" in result_data
        assert result_data["data"]["id"] == 123
        assert result_data["data"]["name"] == "Test Person"
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.persons.create_person.assert_called_once()
        call_kwargs = mock_pipedrive_client.persons.create_person.call_args.kwargs
        assert call_kwargs["name"] == "Test Person"
        assert isinstance(call_kwargs["emails"], list)
        assert call_kwargs["emails"][0]["value"] == "test@example.com"
        assert isinstance(call_kwargs["phones"], list)
        assert call_kwargs["phones"][0]["value"] == "123456789"
    
    @pytest.mark.asyncio
    async def test_create_person_with_custom_fields(self, mock_pipedrive_client):
        """Test creating a person with custom fields"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with custom fields
        custom_fields_str = '{"customer_type": "Premium", "lead_source": "Website"}'
        result = await create_person_in_pipedrive(
            ctx=mock_ctx,
            name="Test Person",
            email_address="test@example.com",
            custom_fields_str=custom_fields_str
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        
        # Verify the client was called with correct custom fields
        call_kwargs = mock_pipedrive_client.persons.create_person.call_args.kwargs
        assert call_kwargs["customer_type"] == "Premium"
        assert call_kwargs["lead_source"] == "Website"
    
    @pytest.mark.asyncio
    async def test_create_person_invalid_id(self, mock_pipedrive_client):
        """Test error handling with invalid ID input"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid owner_id
        result = await create_person_in_pipedrive(
            ctx=mock_ctx,
            name="Test Person",
            owner_id_str="not_a_number"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "owner_id must be a numeric string" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.create_person.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_create_person_invalid_email_format(self, mock_pipedrive_client):
        """Test error handling with invalid email format"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid email
        result = await create_person_in_pipedrive(
            ctx=mock_ctx,
            name="Test Person",
            email_address="invalid-email-format"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Invalid email format" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.create_person.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_create_person_invalid_visible_to(self, mock_pipedrive_client):
        """Test error handling with invalid visible_to value"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid visible_to
        result = await create_person_in_pipedrive(
            ctx=mock_ctx,
            name="Test Person",
            visible_to_str="5"  # Only 1, 2, 3 are valid
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Invalid visible_to value" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.create_person.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_create_person_invalid_custom_fields_json(self, mock_pipedrive_client):
        """Test error handling with invalid custom fields JSON"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid custom fields JSON
        result = await create_person_in_pipedrive(
            ctx=mock_ctx,
            name="Test Person",
            custom_fields_str="invalid json"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Invalid custom_fields_str format" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.create_person.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_create_person_api_error(self, mock_pipedrive_client):
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
        mock_pipedrive_client.persons.create_person.side_effect = api_error

        # Call the tool function
        result = await create_person_in_pipedrive(
            ctx=mock_ctx,
            name="Test Person"
        )

        # Parse the JSON result
        result_data = json.loads(result)

        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "API Error" in result_data["error"]
        assert "data" in result_data
        assert result_data["data"]["error"] == "Something went wrong"