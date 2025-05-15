import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock, ANY

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
            "due_time": "10:00"
        }
        mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.return_value = mock_activity
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                owner_id="1",
                due_date="2023-01-01",
                due_time="10:00"
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
                due_time="10:00"
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
            "due_time": "10:00",
            "duration": "01:00",
            "busy": True,
            "done": False,
            "note": "Test note",
            "location": {"value": "Test location"},
            "public_description": "Test description",
            "priority": 1
        }
        mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.return_value = mock_activity
        
        participants = [{"person_id": 123, "primary_flag": True}]
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                owner_id="1",
                deal_id="2",
                lead_id="46c3b0e1-db35-59ca-1828-4817378dff71",
                person_id="3",
                org_id="4",
                due_date="2023-01-01",
                due_time="10:00",
                duration="01:00",
                busy=True,
                done=False,
                note="Test note",
                location="Test location",
                public_description="Test description",
                priority="1",
                participants=participants
            )
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the result
            assert result_dict["success"] is True
            assert result_dict["data"] == mock_activity
            
            # Verify the client was called with the correct arguments
            # Using ANY for location since we're converting a string to a dict
            mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.assert_called_once_with(
                subject="Test Activity",
                type="call",
                owner_id=1,
                deal_id=2,
                lead_id="46c3b0e1-db35-59ca-1828-4817378dff71",
                person_id=3,
                org_id=4,
                due_date="2023-01-01",
                due_time="10:00",
                duration="01:00",
                busy=True,
                done=False,
                note="Test note",
                location=ANY,
                public_description="Test description",
                priority=1,
                participants=participants
            )
            
            # Verify that location was converted to a dict
            call_args = mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.call_args
            assert call_args is not None
            call_kwargs = call_args[1]
            assert isinstance(call_kwargs["location"], dict)
            assert call_kwargs["location"]["value"] == "Test location"
    
    @pytest.mark.asyncio
    async def test_time_format_conversions(self, mock_context, enable_feature):
        """Test the conversion of various time formats"""
        # Setup mock response
        mock_activity = {
            "id": 123,
            "subject": "Test Activity",
            "type": "call",
            "due_date": "2023-01-01",
            "due_time": "10:00",
            "duration": "01:30"
        }
        mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.return_value = mock_activity
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Test HH:MM:SS format conversion
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                due_date="2023-01-01",
                due_time="10:00:00",
                duration="01:30:00"
            )
            
            result_dict = json.loads(result)
            assert result_dict["success"] is True
            
            # Check that the API received HH:MM format
            mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.assert_called_with(
                subject="Test Activity",
                type="call",
                due_date="2023-01-01",
                due_time="10:00",   # Converted from 10:00:00
                duration="01:30"    # Converted from 01:30:00
            )
            
            # Reset mock for next test
            mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.reset_mock()
            
            # Test ISO datetime format conversion
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                due_date="2023-01-01",
                due_time="2023-01-01T10:00:00Z"
            )
            
            result_dict = json.loads(result)
            assert result_dict["success"] is True
            
            # Check that the API received HH:MM format
            mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.assert_called_with(
                subject="Test Activity",
                type="call",
                due_date="2023-01-01",
                due_time="10:00"   # Converted from ISO format
            )
            
            # Reset mock for next test
            mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.reset_mock()
            
            # Test duration as seconds
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                due_date="2023-01-01",
                due_time="10:00",
                duration="5400"  # 1 hour 30 minutes in seconds
            )
            
            result_dict = json.loads(result)
            assert result_dict["success"] is True
            
            # Check that the API received HH:MM format
            mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.assert_called_with(
                subject="Test Activity",
                type="call",
                due_date="2023-01-01",
                due_time="10:00",
                duration="01:30"  # Converted from seconds
            )
    
    @pytest.mark.asyncio
    async def test_location_format_handling(self, mock_context, enable_feature):
        """Test various location format handling"""
        # Setup mock response
        mock_activity = {
            "id": 123,
            "subject": "Test Activity",
            "type": "call",
            "location": {"value": "123 Main St, City"}
        }
        mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.return_value = mock_activity
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Test string location
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                location="123 Main St, City"
            )
            
            result_dict = json.loads(result)
            assert result_dict["success"] is True
            
            # Check that location was converted to object format
            call_args = mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.call_args
            assert call_args is not None
            call_kwargs = call_args[1]
            assert isinstance(call_kwargs["location"], dict)
            assert call_kwargs["location"]["value"] == "123 Main St, City"
            
            # Reset mock for next test
            mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.reset_mock()
            
            # Test dictionary location
            location_dict = {"value": "123 Main St, City"}
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                location=location_dict
            )
            
            result_dict = json.loads(result)
            assert result_dict["success"] is True
            
            # Check that the location dict was passed through
            call_args = mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.call_args
            assert call_args is not None
            call_kwargs = call_args[1]
            assert call_kwargs["location"] == location_dict
    
    @pytest.mark.asyncio
    async def test_participants_handling(self, mock_context, enable_feature):
        """Test participants parameter handling"""
        # Setup mock response
        mock_activity = {
            "id": 123,
            "subject": "Test Activity",
            "type": "call",
            "participants": [{"person_id": 123, "primary_flag": True}]
        }
        mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.return_value = mock_activity
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Test with participants array
            participants = [{"person_id": 123, "primary_flag": True}]
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                participants=participants
            )
            
            result_dict = json.loads(result)
            assert result_dict["success"] is True
            
            # Check that participants were passed through
            call_args = mock_context.request_context.lifespan_context.pipedrive_client.activities.create_activity.call_args
            assert call_args is not None
            call_kwargs = call_args[1]
            assert call_kwargs["participants"] == participants
    
    @pytest.mark.asyncio
    async def test_invalid_id_strings(self, mock_context, enable_feature):
        """Test error handling for invalid ID strings"""
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Test invalid owner_id
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                owner_id="not_an_id"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "owner_id must be a numeric string" in result_dict["error"]
            
            # Test invalid deal_id
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                deal_id="not_an_id"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "deal_id must be a numeric string" in result_dict["error"]
            
            # Test invalid lead_id (not a UUID)
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                lead_id="not_a_uuid"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "lead_id must be a valid UUID string" in result_dict["error"]
            
            # Test invalid priority
            result = await create_activity_in_pipedrive(
                ctx=mock_context,
                subject="Test Activity",
                type="call",
                priority="not_a_number"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "Priority must be a numeric string" in result_dict["error"]
    
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
            assert "'subject' field is required" in result_dict["error"]
    
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