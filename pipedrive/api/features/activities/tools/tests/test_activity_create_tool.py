import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from pipedrive.api.features.activities.tools.activity_create_tool import create_activity_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_registry import registry


class TestCreateActivityTool:
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
        mock_pipedrive_client.activities.create_activity = AsyncMock()
        
        # Set up the context to provide the Pipedrive client
        mock_mcp_ctx = MagicMock(spec=PipedriveMCPContext)
        mock_mcp_ctx.pipedrive_client = mock_pipedrive_client
        mock_ctx.request_context.lifespan_context = mock_mcp_ctx
        
        return mock_ctx

    @pytest.mark.asyncio
    async def test_create_activity_success(self, mock_context, enable_feature):
        """Test successful activity creation with basic fields"""
        # Setup mock response
        mock_activity = {
            "id": 123,
            "subject": "Test Activity",
            "type": "call",
            "owner_id": 1,
            "due_date": "2023-01-01",
            "due_time": "10:00:00"
        }
        mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.return_value = mock_activity
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                owner_id_str="1",
                due_date="2023-01-01",
                due_time="10:00:00"
            )
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the result
            assert result_dict["success"] is True
            assert result_dict["data"] == mock_activity
            assert result_dict["error"] is None
            
            # Verify the client was called with the correct arguments
            mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.assert_called_once_with(
                subject="Test Activity",
                type="call",
                owner_id=1,
                due_date="2023-01-01",
                due_time="10:00:00"
            )
    
    @pytest.mark.asyncio
    async def test_create_activity_with_all_fields(self, mock_context, enable_feature):
        """Test activity creation with all possible fields"""
        # Setup mock response
        mock_activity = {
            "id": 123,
            "subject": "Test Activity",
            "type": "call",
            "owner_id": 1,
            "deal_id": 2,
            "lead_id": "46c3b0e1-db35-59ca-1828-4817378dff71",
            "person_id": 3,
            "org_id": 4,
            "due_date": "2023-01-01",
            "due_time": "10:00:00",
            "duration": "01:00:00",
            "busy": True,
            "done": False,
            "note": "Test note",
            "location": "Test location",
            "public_description": "Test description",
            "priority": 1
        }
        mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.return_value = mock_activity
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                owner_id_str="1",
                deal_id_str="2",
                lead_id_str="46c3b0e1-db35-59ca-1828-4817378dff71",
                person_id_str="3",
                org_id_str="4",
                due_date="2023-01-01",
                due_time="10:00:00",
                duration="01:00:00",
                busy=True,
                done=False,
                note="Test note",
                location="Test location",
                public_description="Test description",
                priority_str="1"
            )
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the result
            assert result_dict["success"] is True
            assert result_dict["data"] == mock_activity
            
            # Verify the client was called with the correct arguments
            mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.assert_called_once_with(
                subject="Test Activity",
                type="call",
                owner_id=1,
                deal_id=2,
                lead_id="46c3b0e1-db35-59ca-1828-4817378dff71",
                person_id=3,
                org_id=4,
                due_date="2023-01-01",
                due_time="10:00:00",
                duration="01:00:00",
                busy=True,
                done=False,
                note="Test note",
                location="Test location",
                public_description="Test description",
                priority=1
            )
    
    @pytest.mark.asyncio
    async def test_invalid_id_strings(self, mock_context, enable_feature):
        """Test error handling for invalid ID strings"""
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Test invalid owner_id_str
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                owner_id_str="not_an_id"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "Invalid owner_id format" in result_dict["error"]
            
            # Test invalid deal_id_str
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                deal_id_str="not_an_id"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "Invalid deal_id format" in result_dict["error"]
            
            # Test invalid lead_id_str (not a UUID)
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                lead_id_str="not_a_uuid"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "Invalid lead_id format" in result_dict["error"]
            
            # Test invalid priority_str
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                priority_str="not_a_number"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "Invalid priority format" in result_dict["error"]
    
    @pytest.mark.asyncio
    async def test_validation_error_handling(self, mock_context, enable_feature):
        """Test error handling for validation errors"""
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call with empty subject (required field) - this will raise validation error
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="",
                type="call"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "Validation error" in result_dict["error"]
    
    @pytest.mark.asyncio
    async def test_api_error_handling(self, mock_context, enable_feature):
        """Test error handling for Pipedrive API errors"""
        # Setup mock to raise PipedriveAPIError
        error_message = "API Error"
        mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.side_effect = PipedriveAPIError(message=error_message)
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call"
            )
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the error response
            assert result_dict["success"] is False
            assert "Pipedrive API error" in result_dict["error"]
            assert error_message in result_dict["error"]