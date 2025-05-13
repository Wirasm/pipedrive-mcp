import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from pipedrive.api.features.leads.client.lead_client import LeadClient


@pytest.mark.asyncio
class TestLeadClient:
    """Tests for the LeadClient"""
    
    @pytest.fixture
    def mock_base_client(self):
        """Fixture for a mocked BaseClient"""
        base_client = AsyncMock()
        base_client.request = AsyncMock()
        return base_client
    
    @pytest.fixture
    def lead_client(self, mock_base_client):
        """Fixture for a LeadClient instance with a mocked BaseClient"""
        return LeadClient(mock_base_client)
    
    async def test_create_lead(self, lead_client, mock_base_client):
        """Test creating a lead"""
        # Mock response
        mock_response = {
            "success": True,
            "data": {
                "id": "adf21080-0e10-11eb-879b-05d71fb426ec",
                "title": "Test Lead",
                "person_id": 123,
                "amount": 1000,
                "currency": "USD"
            }
        }
        mock_base_client.request.return_value = mock_response
        
        # Call create_lead
        result = await lead_client.create_lead(
            title="Test Lead",
            amount=1000.0,
            currency="USD",
            person_id=123
        )
        
        # Assertions
        mock_base_client.request.assert_called_once()
        args, kwargs = mock_base_client.request.call_args
        
        assert args[0] == "POST"
        assert args[1] == "/leads"
        assert "json_payload" in kwargs
        assert kwargs["version"] == "v1"
        assert kwargs["json_payload"]["title"] == "Test Lead"
        assert "value" in kwargs["json_payload"]
        assert kwargs["json_payload"]["value"]["amount"] == 1000.0
        assert kwargs["json_payload"]["value"]["currency"] == "USD"
        assert kwargs["json_payload"]["person_id"] == 123
        
        assert result == mock_response["data"]
    
    async def test_get_lead(self, lead_client, mock_base_client):
        """Test getting a lead by ID"""
        lead_id = "adf21080-0e10-11eb-879b-05d71fb426ec"
        
        # Mock response
        mock_response = {
            "success": True,
            "data": {
                "id": lead_id,
                "title": "Test Lead",
                "person_id": 123
            }
        }
        mock_base_client.request.return_value = mock_response
        
        # Call get_lead
        result = await lead_client.get_lead(lead_id)
        
        # Assertions
        mock_base_client.request.assert_called_once()
        args, kwargs = mock_base_client.request.call_args
        
        assert args[0] == "GET"
        assert args[1] == f"/leads/{lead_id}"
        assert kwargs["version"] == "v1"
        
        assert result == mock_response["data"]
    
    async def test_update_lead(self, lead_client, mock_base_client):
        """Test updating a lead"""
        lead_id = "adf21080-0e10-11eb-879b-05d71fb426ec"
        
        # Mock response
        mock_response = {
            "success": True,
            "data": {
                "id": lead_id,
                "title": "Updated Lead",
                "person_id": 123
            }
        }
        mock_base_client.request.return_value = mock_response
        
        # Call update_lead
        result = await lead_client.update_lead(
            lead_id=lead_id,
            title="Updated Lead"
        )
        
        # Assertions
        mock_base_client.request.assert_called_once()
        args, kwargs = mock_base_client.request.call_args
        
        assert args[0] == "PATCH"
        assert args[1] == f"/leads/{lead_id}"
        assert "json_payload" in kwargs
        assert kwargs["version"] == "v1"
        assert kwargs["json_payload"]["title"] == "Updated Lead"
        
        assert result == mock_response["data"]
    
    async def test_update_lead_with_value(self, lead_client, mock_base_client):
        """Test updating a lead's value"""
        lead_id = "adf21080-0e10-11eb-879b-05d71fb426ec"
        
        # Mock responses
        mock_response = {
            "success": True,
            "data": {
                "id": lead_id,
                "title": "Updated Lead",
                "value": {
                    "amount": 2000.0,
                    "currency": "EUR"
                }
            }
        }
        mock_base_client.request.return_value = mock_response
        
        # Call update_lead
        result = await lead_client.update_lead(
            lead_id=lead_id,
            amount=2000.0,
            currency="EUR"
        )
        
        # Assertions
        mock_base_client.request.assert_called_once()
        args, kwargs = mock_base_client.request.call_args
        
        assert args[0] == "PATCH"
        assert args[1] == f"/leads/{lead_id}"
        assert "json_payload" in kwargs
        assert "value" in kwargs["json_payload"]
        assert kwargs["json_payload"]["value"]["amount"] == 2000.0
        assert kwargs["json_payload"]["value"]["currency"] == "EUR"
        
        assert result == mock_response["data"]
    
    async def test_delete_lead(self, lead_client, mock_base_client):
        """Test deleting a lead"""
        lead_id = "adf21080-0e10-11eb-879b-05d71fb426ec"
        
        # Mock response
        mock_response = {
            "success": True,
            "data": {
                "id": lead_id
            }
        }
        mock_base_client.request.return_value = mock_response
        
        # Call delete_lead
        result = await lead_client.delete_lead(lead_id)
        
        # Assertions
        mock_base_client.request.assert_called_once()
        args, kwargs = mock_base_client.request.call_args
        
        assert args[0] == "DELETE"
        assert args[1] == f"/leads/{lead_id}"
        assert kwargs["version"] == "v1"
        
        assert result == mock_response["data"]
    
    async def test_list_leads(self, lead_client, mock_base_client):
        """Test listing leads"""
        # Mock response
        mock_response = {
            "success": True,
            "data": [
                {"id": "id1", "title": "Lead 1"},
                {"id": "id2", "title": "Lead 2"}
            ],
            "additional_data": {
                "pagination": {
                    "total_count": 2,
                    "more_items_in_collection": False,
                    "next_start": None
                }
            }
        }
        mock_base_client.request.return_value = mock_response
        
        # Call list_leads
        leads, total_count, next_start = await lead_client.list_leads(
            limit=50,
            start=0,
            archived_status="not_archived",
            owner_id=123
        )
        
        # Assertions
        mock_base_client.request.assert_called_once()
        args, kwargs = mock_base_client.request.call_args
        
        assert args[0] == "GET"
        assert args[1] == "/leads"
        assert "query_params" in kwargs
        assert kwargs["version"] == "v1"
        assert kwargs["query_params"]["limit"] == 50
        assert kwargs["query_params"]["start"] == 0
        assert kwargs["query_params"]["archived_status"] == "not_archived"
        assert kwargs["query_params"]["owner_id"] == 123
        
        assert leads == mock_response["data"]
        assert total_count == 2
        assert next_start == 0
    
    async def test_search_leads(self, lead_client, mock_base_client):
        """Test searching leads"""
        # Mock response
        mock_response = {
            "success": True,
            "data": {
                "items": [
                    {
                        "result_score": 0.9,
                        "item": {"id": "id1", "title": "Lead 1"}
                    },
                    {
                        "result_score": 0.8,
                        "item": {"id": "id2", "title": "Lead 2"}
                    }
                ]
            },
            "additional_data": {
                "next_cursor": "next-cursor-value"
            }
        }
        mock_base_client.request.return_value = mock_response
        
        # Call search_leads
        results, next_cursor = await lead_client.search_leads(
            term="test",
            fields=["title", "notes"],
            exact_match=False,
            person_id=123,
            limit=10
        )
        
        # Assertions
        mock_base_client.request.assert_called_once()
        args, kwargs = mock_base_client.request.call_args
        
        assert args[0] == "GET"
        assert args[1] == "/leads/search"
        assert "query_params" in kwargs
        assert kwargs["version"] == "v2"  # Note: search uses v2
        assert kwargs["query_params"]["term"] == "test"
        assert kwargs["query_params"]["fields"] == "title,notes"
        assert kwargs["query_params"]["exact_match"] is False
        assert kwargs["query_params"]["person_id"] == 123
        assert kwargs["query_params"]["limit"] == 10
        
        assert results == mock_response["data"]["items"]
        assert next_cursor == "next-cursor-value"
    
    async def test_get_lead_labels(self, lead_client, mock_base_client):
        """Test getting lead labels"""
        # Mock response
        mock_response = {
            "success": True,
            "data": [
                {"id": "id1", "name": "Hot", "color": "red"},
                {"id": "id2", "name": "Cold", "color": "blue"}
            ]
        }
        mock_base_client.request.return_value = mock_response
        
        # Call get_lead_labels
        result = await lead_client.get_lead_labels()
        
        # Assertions
        mock_base_client.request.assert_called_once()
        args, kwargs = mock_base_client.request.call_args
        
        assert args[0] == "GET"
        assert args[1] == "/leadLabels"
        assert kwargs["version"] == "v1"
        
        assert result == mock_response["data"]
    
    async def test_get_lead_sources(self, lead_client, mock_base_client):
        """Test getting lead sources"""
        # Mock response
        mock_response = {
            "success": True,
            "data": [
                {"name": "API"},
                {"name": "Web forms"}
            ]
        }
        mock_base_client.request.return_value = mock_response
        
        # Call get_lead_sources
        result = await lead_client.get_lead_sources()
        
        # Assertions
        mock_base_client.request.assert_called_once()
        args, kwargs = mock_base_client.request.call_args
        
        assert args[0] == "GET"
        assert args[1] == "/leadSources"
        assert kwargs["version"] == "v1"
        
        assert result == mock_response["data"]