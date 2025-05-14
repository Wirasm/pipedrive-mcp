import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from pipedrive.api.features.tool_registry import registry


@pytest.fixture(autouse=True)
def enable_leads_feature():
    """
    Fixture to enable the 'leads' feature for all tests in this module.
    
    This fixture is automatically used in all tests in this directory.
    It ensures the 'leads' feature is reported as enabled during tests.
    """
    with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled') as mock_is_enabled:
        # Return True for 'leads' feature, otherwise use the real implementation
        def side_effect(feature_id):
            if feature_id == "leads":
                return True
            return registry.is_feature_enabled(feature_id)
            
        mock_is_enabled.side_effect = side_effect
        yield


@pytest.fixture
def mock_context():
    """Create a mock context with a mock Pipedrive client"""
    mock_ctx = MagicMock()
    mock_ctx.request_context.lifespan_context.pipedrive_client = MagicMock()
    
    # Setup lead_client mock
    mock_ctx.request_context.lifespan_context.pipedrive_client.lead_client = AsyncMock()
    
    return mock_ctx


@pytest.fixture
def mock_pipedrive_client(mock_context):
    """Get the mock Pipedrive client from the mock context"""
    return mock_context.request_context.lifespan_context.pipedrive_client