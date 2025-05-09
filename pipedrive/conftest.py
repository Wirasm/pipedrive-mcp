import pytest
from unittest.mock import AsyncMock

from pipedrive.api.pipedrive_client import PipedriveClient


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient for testing"""
    client = AsyncMock(spec=PipedriveClient)
    
    # Set up mock responses for common methods
    client.create_person.return_value = {
        "id": 123,
        "name": "Test Person",
        "emails": [{"value": "test@example.com", "label": "work", "primary": True}],
        "phones": [{"value": "123456789", "label": "work", "primary": True}]
    }
    
    client.get_person.return_value = {
        "id": 123,
        "name": "Test Person",
        "emails": [{"value": "test@example.com", "label": "work", "primary": True}],
        "phones": [{"value": "123456789", "label": "work", "primary": True}]
    }
    
    client.update_person.return_value = {
        "id": 123,
        "name": "Updated Person",
        "emails": [{"value": "updated@example.com", "label": "work", "primary": True}],
        "phones": [{"value": "987654321", "label": "work", "primary": True}]
    }
    
    client.delete_person.return_value = {
        "id": 123,
        "success": True
    }
    
    return client