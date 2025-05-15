import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock, ANY

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from pipedrive.api.features.activities.tools.activity_list_tool import list_activities_from_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_registry import registry


class TestActivityListTool:
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
        mock_pipedrive_client.activities.list_activities = AsyncMock()
        
        # Set up the context to provide the Pipedrive client
        mock_mcp_ctx = MagicMock(spec=PipedriveMCPContext)
        mock_mcp_ctx.pipedrive_client = mock_pipedrive_client
        mock_ctx.request_context.lifespan_context = mock_mcp_ctx
        
        return mock_ctx

    @pytest.mark.asyncio
    async def test_list_activities_success(self, mock_context, enable_feature):
        """Test successful activities listing with default parameters"""
        # Setup mock response
        mock_activities = [
            {
                "id": 123,
                "subject": "Test Activity 1",
                "type": "call",
                "due_date": "2023-01-01",
                "due_time": "10:00"
            },
            {
                "id": 124,
                "subject": "Test Activity 2",
                "type": "meeting",
                "due_date": "2023-01-02",
                "due_time": "14:00"
            }
        ]
        next_cursor = "next_page_token"
        mock_context.request_context.lifespan_context.pipedrive_client.activities.list_activities.return_value = (mock_activities, next_cursor)
        
        # Call the tool with default parameters
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            result = await list_activities_from_pipedrive(
                ctx=mock_context
            )
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the result
            assert result_dict["success"] is True
            assert result_dict["data"]["items"] == mock_activities
            assert result_dict["data"]["additional_data"]["next_cursor"] == next_cursor
            assert result_dict["error"] is None
            
            # Verify the client was called with the correct arguments
            mock_context.request_context.lifespan_context.pipedrive_client.activities.list_activities.assert_called_once_with(
                limit=100,  # Default
                cursor=None,
                filter_id=None,
                owner_id=None,
                deal_id=None,
                lead_id=None,
                person_id=None,
                org_id=None,
                updated_since=None,
                updated_until=None,
                sort_by=None,
                sort_direction=None,
                include_fields=None
            )

    @pytest.mark.asyncio
    async def test_list_activities_with_filters(self, mock_context, enable_feature):
        """Test activities listing with various filter parameters"""
        # Setup mock response
        mock_activities = [
            {
                "id": 123,
                "subject": "Test Activity 1",
                "type": "call",
                "due_date": "2023-01-01",
                "due_time": "10:00",
                "owner_id": 1
            }
        ]
        next_cursor = "next_page_token"
        mock_context.request_context.lifespan_context.pipedrive_client.activities.list_activities.return_value = (mock_activities, next_cursor)
        
        # Call the tool with filters
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            result = await list_activities_from_pipedrive(
                ctx=mock_context,
                limit_str="50",
                owner_id_str="1",
                deal_id_str="2",
                lead_id_str="46c3b0e1-db35-59ca-1828-4817378dff71",
                person_id_str="3",
                org_id_str="4",
                updated_since="2023-01-01T00:00:00Z",
                updated_until="2023-01-02T00:00:00Z",
                sort_by="update_time",
                sort_direction="desc",
                include_fields_str="subject,note"
            )
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the result
            assert result_dict["success"] is True
            assert result_dict["data"]["items"] == mock_activities
            
            # Verify the client was called with the correct arguments
            mock_context.request_context.lifespan_context.pipedrive_client.activities.list_activities.assert_called_once_with(
                limit=50,
                cursor=None,
                filter_id=None,
                owner_id=1,
                deal_id=2,
                lead_id="46c3b0e1-db35-59ca-1828-4817378dff71",
                person_id=3,
                org_id=4,
                updated_since="2023-01-01T00:00:00Z",
                updated_until="2023-01-02T00:00:00Z",
                sort_by="update_time",
                sort_direction="desc",
                include_fields=["subject", "note"]
            )

    @pytest.mark.asyncio
    async def test_pagination(self, mock_context, enable_feature):
        """Test activities listing with pagination"""
        # Setup mock response for first page
        mock_activities_page1 = [
            {"id": 123, "subject": "Test Activity 1"}
        ]
        next_cursor = "next_page_token"
        mock_context.request_context.lifespan_context.pipedrive_client.activities.list_activities.return_value = (mock_activities_page1, next_cursor)
        
        # Call the tool for first page
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            result = await list_activities_from_pipedrive(
                ctx=mock_context,
                limit_str="10"
            )
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the result has next_cursor
            assert result_dict["success"] is True
            assert result_dict["data"]["additional_data"]["next_cursor"] == next_cursor
            
            # Reset mock for second page
            mock_context.request_context.lifespan_context.pipedrive_client.activities.list_activities.reset_mock()
            
            # Setup mock response for second page
            mock_activities_page2 = [
                {"id": 124, "subject": "Test Activity 2"}
            ]
            mock_context.request_context.lifespan_context.pipedrive_client.activities.list_activities.return_value = (mock_activities_page2, None)
            
            # Call the tool for second page using the cursor
            result = await list_activities_from_pipedrive(
                ctx=mock_context,
                limit_str="10",
                cursor=next_cursor
            )
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the result for second page (no more pages)
            assert result_dict["success"] is True
            assert result_dict["data"]["items"] == mock_activities_page2
            assert "next_cursor" not in result_dict["data"]["additional_data"]
            
            # Verify cursor was passed correctly
            mock_context.request_context.lifespan_context.pipedrive_client.activities.list_activities.assert_called_once_with(
                limit=10,
                cursor=next_cursor,
                filter_id=None,
                owner_id=None,
                deal_id=None,
                lead_id=None,
                person_id=None,
                org_id=None,
                updated_since=None,
                updated_until=None,
                sort_by=None,
                sort_direction=None,
                include_fields=None
            )

    @pytest.mark.asyncio
    async def test_invalid_parameters(self, mock_context, enable_feature):
        """Test error handling for invalid parameters"""
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Test invalid limit
            result = await list_activities_from_pipedrive(
                ctx=mock_context,
                limit_str="not_a_number"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "Invalid limit value" in result_dict["error"]
            
            # Test invalid owner_id
            result = await list_activities_from_pipedrive(
                ctx=mock_context,
                owner_id_str="not_a_number"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "owner_id must be a numeric string" in result_dict["error"]
            
            # Test invalid lead_id (not a UUID)
            result = await list_activities_from_pipedrive(
                ctx=mock_context,
                lead_id_str="not_a_uuid"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "lead_id must be a valid UUID string" in result_dict["error"]
            
            # Test invalid sort_by
            result = await list_activities_from_pipedrive(
                ctx=mock_context,
                sort_by="invalid_field"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "Invalid sort_by value" in result_dict["error"]
            
            # Test invalid sort_direction
            result = await list_activities_from_pipedrive(
                ctx=mock_context,
                sort_direction="invalid_direction"
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "Invalid sort_direction value" in result_dict["error"]
            
            # Test invalid RFC3339 date format
            result = await list_activities_from_pipedrive(
                ctx=mock_context,
                updated_since="2023-01-01" # Missing time component
            )
            result_dict = json.loads(result)
            assert result_dict["success"] is False
            assert "Invalid updated_since format" in result_dict["error"]

    @pytest.mark.asyncio
    async def test_api_error_handling(self, mock_context, enable_feature):
        """Test error handling for Pipedrive API errors"""
        # Setup mock to raise PipedriveAPIError
        error_message = "API Error"
        mock_context.request_context.lifespan_context.pipedrive_client.activities.list_activities.side_effect = PipedriveAPIError(message=error_message)
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await list_activities_from_pipedrive(
                ctx=mock_context
            )
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the error response
            assert result_dict["success"] is False
            assert "Pipedrive API error" in result_dict["error"]
            assert error_message in result_dict["error"]

    @pytest.mark.asyncio
    async def test_unexpected_error_handling(self, mock_context, enable_feature):
        """Test error handling for unexpected exceptions"""
        # Setup mock to raise an unexpected exception
        error_message = "Unexpected error"
        mock_context.request_context.lifespan_context.pipedrive_client.activities.list_activities.side_effect = Exception(error_message)
        
        # Mock the registry's is_feature_enabled method
        with patch('pipedrive.api.features.tool_registry.registry.is_feature_enabled', return_value=True):
            # Call the tool
            result = await list_activities_from_pipedrive(
                ctx=mock_context
            )
            
            # Parse the JSON result
            result_dict = json.loads(result)
            
            # Verify the error response
            assert result_dict["success"] is False
            assert "An unexpected error occurred" in result_dict["error"]
            assert error_message in result_dict["error"]