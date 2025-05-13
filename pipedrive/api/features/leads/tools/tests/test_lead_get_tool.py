import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from mcp.server.fastmcp import Context

from pipedrive.api.features.leads.tools.lead_get_tool import get_lead_from_pipedrive
from pipedrive.api.pipedrive_context import PipedriveMCPContext


@pytest.mark.asyncio
class TestLeadGetTool:
    """Tests for the get_lead_from_pipedrive MCP tool"""
    
    @pytest.fixture
    def mock_pipedrive_client(self):
        """Fixture for mocked PipedriveClient"""
        mock_client = MagicMock()
        mock_client.lead_client = MagicMock()
        mock_client.lead_client.get_lead = AsyncMock()
        return mock_client
    
    @pytest.fixture
    def mock_context(self, mock_pipedrive_client):
        """Fixture for mocked Context with pipedrive context"""
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context = MagicMock()
        mock_ctx.request_context.lifespan_context = MagicMock(spec=PipedriveMCPContext)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        return mock_ctx
    
    async def test_get_lead_from_pipedrive_success(self, mock_context, mock_pipedrive_client):
        """Test successful lead retrieval"""
        # Setup mock
        lead_id = "adf21080-0e10-11eb-879b-05d71fb426ec"
        mock_lead_data = {
            "id": lead_id,
            "title": "Test Lead",
            "person_id": 123,
            "amount": 1000,
            "currency": "USD"
        }
        mock_pipedrive_client.lead_client.get_lead.return_value = mock_lead_data
        
        # Call the tool
        result = await get_lead_from_pipedrive(
            ctx=mock_context,
            lead_id=lead_id
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is True
        assert "data" in result_dict
        assert result_dict["data"]["id"] == lead_id
        assert result_dict["data"]["title"] == "Test Lead"
        assert result_dict["data"]["person_id"] == 123
        assert result_dict["data"]["amount"] == 1000
        assert result_dict["data"]["currency"] == "USD"
        
        # Check that the client was called correctly
        mock_pipedrive_client.lead_client.get_lead.assert_called_once_with(lead_id=lead_id)
    
    async def test_get_lead_from_pipedrive_invalid_uuid(self, mock_context, mock_pipedrive_client):
        """Test that an invalid UUID returns an error response"""
        # Call with invalid UUID
        result = await get_lead_from_pipedrive(
            ctx=mock_context,
            lead_id="not-a-uuid"
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is False
        assert "error" in result_dict
        assert "Invalid" in result_dict["error"]
        assert "UUID" in result_dict["error"]
        
        # Client should not be called
        mock_pipedrive_client.lead_client.get_lead.assert_not_called()
    
    async def test_get_lead_from_pipedrive_not_found(self, mock_context, mock_pipedrive_client):
        """Test handling a lead that doesn't exist"""
        # Setup mock to return None (not found)
        lead_id = "adf21080-0e10-11eb-879b-05d71fb426ec"
        mock_pipedrive_client.lead_client.get_lead.return_value = None
        
        # Call the tool
        result = await get_lead_from_pipedrive(
            ctx=mock_context,
            lead_id=lead_id
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is False
        assert "error" in result_dict
        assert "not found" in result_dict["error"]
        
        # Client should be called
        mock_pipedrive_client.lead_client.get_lead.assert_called_once_with(lead_id=lead_id)
    
    async def test_get_lead_from_pipedrive_client_error(self, mock_context, mock_pipedrive_client):
        """Test that client errors are handled correctly"""
        # Setup mock to raise an exception
        lead_id = "adf21080-0e10-11eb-879b-05d71fb426ec"
        mock_pipedrive_client.lead_client.get_lead.side_effect = Exception("API Error")
        
        # Call the tool
        result = await get_lead_from_pipedrive(
            ctx=mock_context,
            lead_id=lead_id
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is False
        assert "error" in result_dict
        assert "API Error" in result_dict["error"]