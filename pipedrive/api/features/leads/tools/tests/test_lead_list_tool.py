import json
import pytest
from unittest.mock import AsyncMock, MagicMock

from pipedrive.api.features.leads.tools.lead_list_tool import list_leads_from_pipedrive


@pytest.mark.asyncio
class TestLeadListTool:
    """Tests for the list_leads_from_pipedrive MCP tool"""
    
    async def test_list_leads_from_pipedrive_success(self, mock_context, mock_pipedrive_client):
        """Test successful leads listing"""
        # Setup mock
        mock_leads_data = [
            {
                "id": "adf21080-0e10-11eb-879b-05d71fb426ec",
                "title": "Lead 1",
                "person_id": 123,
                "amount": 1000,
                "currency": "USD"
            },
            {
                "id": "bdf21080-0e10-11eb-879b-05d71fb426ed",
                "title": "Lead 2",
                "organization_id": 456,
                "amount": 2000,
                "currency": "EUR"
            }
        ]
        
        # Set up mock_pipedrive_client.lead_client.list_leads to return leads, total count, and next_start
        mock_pipedrive_client.lead_client.list_leads = AsyncMock(
            return_value=(mock_leads_data, 2, 0)
        )
        
        # Call the tool
        result = await list_leads_from_pipedrive(
            ctx=mock_context,
            limit="10",
            archived_status="not_archived"
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is True
        assert "data" in result_dict
        assert "leads" in result_dict["data"]
        assert len(result_dict["data"]["leads"]) == 2
        assert result_dict["data"]["leads"][0]["title"] == "Lead 1"
        assert result_dict["data"]["leads"][1]["title"] == "Lead 2"
        assert "pagination" in result_dict["data"]
        assert result_dict["data"]["pagination"]["total_count"] == 2
        
        # Check that the client was called correctly
        mock_pipedrive_client.lead_client.list_leads.assert_called_once_with(
            limit=10,
            start=None,
            archived_status="not_archived",
            owner_id=None,
            person_id=None,
            organization_id=None,
            filter_id=None,
            sort=None
        )
    
    async def test_list_leads_from_pipedrive_invalid_parameters(self, mock_context, mock_pipedrive_client):
        """Test validation of parameters"""
        # Call with invalid limit
        result = await list_leads_from_pipedrive(
            ctx=mock_context,
            limit="invalid"
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is False
        assert "error" in result_dict
        assert "Invalid" in result_dict["error"]
        
        # Call with invalid archived_status
        result = await list_leads_from_pipedrive(
            ctx=mock_context,
            archived_status="invalid_status"
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is False
        assert "error" in result_dict
        assert "archived_status" in result_dict["error"]
        
        # Client should not be called
        mock_pipedrive_client.lead_client.list_leads.assert_not_called()
    
    async def test_list_leads_from_pipedrive_client_error(self, mock_context, mock_pipedrive_client):
        """Test that client errors are handled correctly"""
        # Setup mock to raise an exception
        mock_pipedrive_client.lead_client.list_leads.side_effect = Exception("API Error")
        
        # Call the tool
        result = await list_leads_from_pipedrive(
            ctx=mock_context
        )
        
        # Parse JSON result
        result_dict = json.loads(result)
        
        # Assertions
        assert result_dict["success"] is False
        assert "error" in result_dict
        assert "API Error" in result_dict["error"]