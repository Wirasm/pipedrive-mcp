import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp.server.fastmcp import Context
from pipedrive.api.features.persons.tools.person_update_tool import update_person_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient for testing"""
    # Create mock persons client
    persons_client = AsyncMock()

    # Set up mock response for update_person
    persons_client.update_person.return_value = {
        "id": 123,
        "name": "Updated Person",
        "emails": [{"value": "updated@example.com", "label": "work", "primary": True}],
        "phones": [{"value": "987654321", "label": "mobile", "primary": True}]
    }

    # Create main client with persons property
    client = MagicMock()
    client.persons = persons_client

    return client


class TestUpdatePersonTool:
    @pytest.mark.asyncio
    async def test_update_person_success(self, mock_pipedrive_client):
        """Test successful person update"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function
        result = await update_person_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            name="Updated Person",
            email_address="updated@example.com",
            phone_number="987654321",
            phone_label="mobile"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success and data
        assert result_data["success"] is True
        assert "data" in result_data
        assert result_data["data"]["id"] == 123
        assert result_data["data"]["name"] == "Updated Person"
        assert result_data["data"]["emails"][0]["value"] == "updated@example.com"
        
        # Verify the client was called with correct parameters
        mock_pipedrive_client.persons.update_person.assert_called_once()
        call_kwargs = mock_pipedrive_client.persons.update_person.call_args.kwargs
        assert call_kwargs["person_id"] == 123
        assert call_kwargs["name"] == "Updated Person"
        assert isinstance(call_kwargs["emails"], list)
        assert call_kwargs["emails"][0]["value"] == "updated@example.com"
        assert isinstance(call_kwargs["phones"], list)
        assert call_kwargs["phones"][0]["value"] == "987654321"
        assert call_kwargs["phones"][0]["label"] == "mobile"
    
    @pytest.mark.asyncio
    async def test_update_person_with_custom_fields(self, mock_pipedrive_client):
        """Test updating a person with custom fields"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with custom fields
        custom_fields_str = '{"customer_type": "Premium", "lead_source": "Website"}'
        result = await update_person_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            name="Updated Person",
            custom_fields_str=custom_fields_str
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        
        # Verify the client was called with correct custom fields
        call_kwargs = mock_pipedrive_client.persons.update_person.call_args.kwargs
        assert call_kwargs["customer_type"] == "Premium"
        assert call_kwargs["lead_source"] == "Website"
    
    @pytest.mark.asyncio
    async def test_update_person_remove_organization(self, mock_pipedrive_client):
        """Test removing organization association"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with null org_id
        result = await update_person_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            org_id_str="null"  # Special value to remove org association
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        
        # Verify the client was called with null org_id
        call_kwargs = mock_pipedrive_client.persons.update_person.call_args.kwargs
        assert call_kwargs["org_id"] is None
    
    @pytest.mark.asyncio
    async def test_update_person_clear_emails(self, mock_pipedrive_client):
        """Test clearing all emails"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with empty email
        result = await update_person_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            email_address=""  # Empty string clears all emails
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        
        # Verify the client was called with empty emails list
        call_kwargs = mock_pipedrive_client.persons.update_person.call_args.kwargs
        assert call_kwargs["emails"] == []
    
    @pytest.mark.asyncio
    async def test_update_person_no_fields(self, mock_pipedrive_client):
        """Test error handling when no update fields are provided"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with no update fields
        result = await update_person_in_pipedrive(
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
        mock_pipedrive_client.persons.update_person.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_person_invalid_id(self, mock_pipedrive_client):
        """Test error handling with invalid ID input"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid ID
        result = await update_person_in_pipedrive(
            ctx=mock_ctx,
            id_str="not_a_number",
            name="Updated Person"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "person_id must be a numeric string" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.update_person.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_person_invalid_email_format(self, mock_pipedrive_client):
        """Test error handling with invalid email format"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid email
        result = await update_person_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            email_address="invalid-email-format"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Invalid email format" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.update_person.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_person_invalid_visible_to(self, mock_pipedrive_client):
        """Test error handling with invalid visible_to value"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool function with invalid visible_to
        result = await update_person_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            visible_to_str="5"  # Only 1, 2, 3 are valid
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Invalid visible_to value" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.persons.update_person.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_person_api_error(self, mock_pipedrive_client):
        """Test handling of API errors"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client

        # Make the client raise an API error
        api_error = PipedriveAPIError(
            message="API Error",
            status_code=400,
            error_info="Bad Request",
            response_data={"error": "Failed to update person"}
        )
        mock_pipedrive_client.persons.update_person.side_effect = api_error

        # Call the tool function
        result = await update_person_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            name="Updated Person"
        )

        # Parse the JSON result
        result_data = json.loads(result)

        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "API Error" in result_data["error"]
        assert "data" in result_data
        assert result_data["data"]["error"] == "Failed to update person"
    
    @pytest.mark.asyncio
    async def test_update_person_value_error(self, mock_pipedrive_client):
        """Test handling of value errors from the update_person method"""
        # Mock the context and lifespan context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client

        # Make the client raise a ValueError
        mock_pipedrive_client.persons.update_person.side_effect = ValueError("No fields to update")

        # Call the tool function
        result = await update_person_in_pipedrive(
            ctx=mock_ctx,
            id_str="123",
            name="Updated Person"
        )

        # Parse the JSON result
        result_data = json.loads(result)

        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "No fields to update" in result_data["error"]