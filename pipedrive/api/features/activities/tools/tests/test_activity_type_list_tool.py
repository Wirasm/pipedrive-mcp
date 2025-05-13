import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock

from mcp.server.fastmcp import Context

from pipedrive.api.features.activities.tools.activity_type_list_tool import get_activity_types_from_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_registry import registry


class TestActivityTypeListTool:
    @pytest.fixture
    def enable_feature(self):
        # Enable the activities feature for testing
        if "activities" in registry._features:
            registry._enabled_features.add("activities")
        else:
            # If not already registered, we'll mock is_feature_enabled
            with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
                yield
            return

        # Reset after the test
        yield
        registry._enabled_features.discard("activities")

    @pytest.fixture
    def mock_context(self):
        mock_ctx = MagicMock(spec=Context)
        mock_pipedrive_client = MagicMock()
        mock_pipedrive_client.activities = MagicMock()
        mock_pipedrive_client.activities.get_activity_types = AsyncMock()
        
        # Set up the context to provide the Pipedrive client
        mock_mcp_ctx = MagicMock(spec=PipedriveMCPContext)
        mock_mcp_ctx.pipedrive_client = mock_pipedrive_client
        mock_ctx.request_context.lifespan_context = mock_mcp_ctx
        
        return mock_ctx

    @pytest.mark.asyncio
    async def test_get_activity_types_success(self, mock_context, enable_feature):
        """Test successful retrieval of activity types"""
        # Setup mock response
        mock_activity_types = [
            {
                "id": 1,
                "name": "Call",
                "icon_key": "call",
                "key_string": "call",
                "color": "FFFFFF",
                "active_flag": True,
                "is_custom_flag": False
            },
            {
                "id": 2,
                "name": "Meeting",
                "icon_key": "meeting",
                "key_string": "meeting",
                "color": "CCCCCC",
                "active_flag": True,
                "is_custom_flag": False
            }
        ]
        mock_context.request_context.lifespan_context.pipedrive_client.activities.get_activity_types.return_value = mock_activity_types
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await get_activity_types_from_pipedrive(ctx=mock_context)
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the result
            assert result_dict["success"] is True
            assert result_dict["data"] == mock_activity_types
            assert result_dict["error"] is None
            
            # Verify the client was called
            mock_context.request_context.lifespan_context.pipedrive_client.activities.get_activity_types.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_empty_activity_types(self, mock_context, enable_feature):
        """Test handling of empty activity types list"""
        # Setup mock response
        mock_context.request_context.lifespan_context.pipedrive_client.activities.get_activity_types.return_value = []
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await get_activity_types_from_pipedrive(ctx=mock_context)
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the result (should be successful with empty data)
            assert result_dict["success"] is True
            assert result_dict["data"] == []
            assert result_dict["error"] is None
    
    @pytest.mark.asyncio
    async def test_api_error_handling(self, mock_context, enable_feature):
        """Test error handling for Pipedrive API errors"""
        # Setup mock to raise PipedriveAPIError
        error_message = "API Error"
        mock_context.request_context.lifespan_context.pipedrive_client.activities.get_activity_types.side_effect = PipedriveAPIError(message=error_message)
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await get_activity_types_from_pipedrive(ctx=mock_context)
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the error response
            assert result_dict["success"] is False
            assert "Pipedrive API error" in result_dict["error"]
            assert error_message in result_dict["error"]
    
    @pytest.mark.asyncio
    async def test_unexpected_error_handling(self, mock_context, enable_feature):
        """Test handling of unexpected errors"""
        # Setup mock to raise an unexpected error
        error_message = "Unexpected error"
        mock_context.request_context.lifespan_context.pipedrive_client.activities.get_activity_types.side_effect = Exception(error_message)
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await get_activity_types_from_pipedrive(ctx=mock_context)
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the error response
            assert result_dict["success"] is False
            assert "An unexpected error occurred" in result_dict["error"]
            assert error_message in result_dict["error"]