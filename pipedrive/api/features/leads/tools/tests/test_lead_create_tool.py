import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from mcp.server.fastmcp import Context

from pipedrive.api.features.leads.tools.lead_create_tool import create_lead_in_pipedrive
from pipedrive.api.pipedrive_context import PipedriveMCPContext


@pytest.mark.asyncio
class TestLeadCreateTool:
    """Tests for the create_lead_in_pipedrive MCP tool"""
    
    @pytest.fixture
    def mock_pipedrive_client(self):
        """Fixture for mocked PipedriveClient"""
        mock_client = MagicMock()
        mock_client.lead_client = MagicMock()
        mock_client.lead_client.create_lead = AsyncMock()
        return mock_client
    
    @pytest.fixture
    def mock_context(self, mock_pipedrive_client):
        """Fixture for mocked Context with pipedrive context"""
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context = MagicMock()
        mock_ctx.request_context.lifespan_context = MagicMock(spec=PipedriveMCPContext)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        return mock_ctx
    
    async def test_create_lead_in_pipedrive_success(self, mock_context, mock_pipedrive_client):
        """Test successful lead creation"""
        # Setup mock
        mock_lead_data = {
            "id": "adf21080-0e10-11eb-879b-05d71fb426ec",
            "title": "Test Lead",
            "person_id": 123,
            "amount": 1000,
            "currency": "USD"
        }
        mock_pipedrive_client.lead_client.create_lead.return_value = mock_lead_data
        
        # Call the tool
        result = await create_lead_in_pipedrive(
            ctx=mock_context,
            title="Test Lead",
            value="1000",
            currency="USD",
            person_id="123"
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is True
        assert "data" in result_dict
        assert result_dict["data"]["title"] == "Test Lead"
        assert result_dict["data"]["person_id"] == 123
        assert result_dict["data"]["amount"] == 1000
        assert result_dict["data"]["currency"] == "USD"
        
        # Check that the client was called correctly
        mock_pipedrive_client.lead_client.create_lead.assert_called_once()
        args, kwargs = mock_pipedrive_client.lead_client.create_lead.call_args
        assert kwargs["title"] == "Test Lead"
        assert kwargs["amount"] == 1000.0
        assert kwargs["currency"] == "USD"
        assert kwargs["person_id"] == 123
    
    async def test_create_lead_in_pipedrive_missing_required_fields(self, mock_context, mock_pipedrive_client):
        """Test that missing required fields returns an error response"""
        # Call without person_id or organization_id
        result = await create_lead_in_pipedrive(
            ctx=mock_context,
            title="Test Lead"
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is False
        assert "error" in result_dict
        assert "person_id or organization_id" in result_dict["error"]
        
        # Client should not be called
        mock_pipedrive_client.lead_client.create_lead.assert_not_called()
    
    async def test_create_lead_in_pipedrive_validation_error(self, mock_context, mock_pipedrive_client):
        """Test that validation errors are handled correctly"""
        # Call with invalid value
        result = await create_lead_in_pipedrive(
            ctx=mock_context,
            title="Test Lead",
            person_id="123",
            value="not-a-number"
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is False
        assert "error" in result_dict
        assert "Invalid value format" in result_dict["error"]
        
        # Client should not be called
        mock_pipedrive_client.lead_client.create_lead.assert_not_called()
    
    @patch("pipedrive.api.features.leads.tools.lead_create_tool.Lead")
    async def test_create_lead_in_pipedrive_client_error(self, mock_lead_class, mock_context, mock_pipedrive_client):
        """Test that client errors are handled correctly"""
        # Set up mock Lead class
        mock_lead_instance = MagicMock()
        mock_lead_instance.title = "Test Lead"
        mock_lead_instance.amount = 1000.0
        mock_lead_instance.currency = "USD"
        mock_lead_instance.person_id = 123
        mock_lead_instance.organization_id = None
        mock_lead_instance.owner_id = None
        mock_lead_instance.label_ids = None
        mock_lead_instance.expected_close_date = None
        mock_lead_instance.visible_to = None
        mock_lead_class.return_value = mock_lead_instance
        
        # Setup mock to raise an exception
        mock_pipedrive_client.lead_client.create_lead.side_effect = Exception("API Error")
        
        # Call the tool
        result = await create_lead_in_pipedrive(
            ctx=mock_context,
            title="Test Lead",
            value="1000",
            currency="USD",
            person_id="123"
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is False
        assert "error" in result_dict
        assert "API Error" in result_dict["error"]