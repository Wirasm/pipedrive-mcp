import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock

from pipedrive.api.base_client import BaseClient
from pipedrive.api.features.activities.client.activity_client import ActivityClient
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_base_client():
    base_client = AsyncMock(spec=BaseClient)
    base_client.request = AsyncMock()
    return base_client


@pytest.fixture
def activity_client(mock_base_client):
    return ActivityClient(mock_base_client)


class TestActivityClient:
    @pytest.mark.asyncio
    async def test_create_activity(self, activity_client, mock_base_client):
        """Test creating a new activity"""
        # Setup expected response
        mock_response = {
            "success": True,
            "data": {
                "id": 123,
                "subject": "Test Activity",
                "type": "call",
                "due_date": "2023-01-01",
                "due_time": "10:00:00",
                "owner_id": 1
            }
        }
        mock_base_client.request.return_value = mock_response

        # Call the method
        result = await activity_client.create_activity(
            subject="Test Activity",
            type="call",
            due_date="2023-01-01",
            due_time="10:00:00",
            owner_id=1
        )

        # Verify request was made correctly
        mock_base_client.request.assert_called_once_with(
            "POST",
            "/activities",
            json_payload={
                "subject": "Test Activity",
                "type": "call",
                "due_date": "2023-01-01",
                "due_time": "10:00:00",
                "owner_id": 1
            },
            version="v2"
        )

        # Verify result
        assert result == mock_response.get("data")

    @pytest.mark.asyncio
    async def test_get_activity(self, activity_client, mock_base_client):
        """Test getting an activity by ID"""
        # Setup expected response
        mock_response = {
            "success": True,
            "data": {
                "id": 123,
                "subject": "Test Activity",
                "type": "call",
                "due_date": "2023-01-01",
                "due_time": "10:00:00",
                "owner_id": 1
            }
        }
        mock_base_client.request.return_value = mock_response

        # Call the method
        result = await activity_client.get_activity(activity_id=123)

        # Verify request was made correctly
        mock_base_client.request.assert_called_once_with(
            "GET",
            "/activities/123",
            query_params=None,
            version="v2"
        )

        # Verify result
        assert result == mock_response.get("data")

    @pytest.mark.asyncio
    async def test_get_activity_with_include_fields(self, activity_client, mock_base_client):
        """Test getting an activity with include_fields"""
        # Setup expected response
        mock_response = {
            "success": True,
            "data": {
                "id": 123,
                "subject": "Test Activity",
                "type": "call",
                "due_date": "2023-01-01",
                "due_time": "10:00:00",
                "owner_id": 1,
                "attendees": []
            }
        }
        mock_base_client.request.return_value = mock_response

        # Call the method
        result = await activity_client.get_activity(
            activity_id=123,
            include_fields=["attendees"]
        )

        # Verify request was made correctly
        mock_base_client.request.assert_called_once_with(
            "GET",
            "/activities/123",
            query_params={"include_fields": "attendees"},
            version="v2"
        )

        # Verify result
        assert result == mock_response.get("data")

    @pytest.mark.asyncio
    async def test_list_activities(self, activity_client, mock_base_client):
        """Test listing activities"""
        # Setup expected response
        mock_response = {
            "success": True,
            "data": [
                {
                    "id": 123,
                    "subject": "Test Activity 1",
                    "type": "call"
                },
                {
                    "id": 124,
                    "subject": "Test Activity 2",
                    "type": "meeting"
                }
            ],
            "additional_data": {
                "next_cursor": "next_cursor_value"
            }
        }
        mock_base_client.request.return_value = mock_response

        # Call the method
        result, next_cursor = await activity_client.list_activities(
            limit=2,
            owner_id=1
        )

        # Verify request was made correctly
        mock_base_client.request.assert_called_once_with(
            "GET",
            "/activities",
            query_params={"limit": 2, "owner_id": 1},
            version="v2"
        )

        # Verify result
        assert result == mock_response.get("data")
        assert next_cursor == "next_cursor_value"

    @pytest.mark.asyncio
    async def test_update_activity(self, activity_client, mock_base_client):
        """Test updating an activity"""
        # Setup expected response
        mock_response = {
            "success": True,
            "data": {
                "id": 123,
                "subject": "Updated Activity",
                "type": "call",
                "due_date": "2023-01-01",
                "due_time": "10:00:00",
                "owner_id": 1
            }
        }
        mock_base_client.request.return_value = mock_response

        # Call the method
        result = await activity_client.update_activity(
            activity_id=123,
            subject="Updated Activity"
        )

        # Verify request was made correctly
        mock_base_client.request.assert_called_once_with(
            "PATCH",
            "/activities/123",
            json_payload={"subject": "Updated Activity"},
            version="v2"
        )

        # Verify result
        assert result == mock_response.get("data")

    @pytest.mark.asyncio
    async def test_delete_activity(self, activity_client, mock_base_client):
        """Test deleting an activity"""
        # Setup expected response
        mock_response = {
            "success": True,
            "data": {
                "id": 123
            }
        }
        mock_base_client.request.return_value = mock_response

        # Call the method
        result = await activity_client.delete_activity(activity_id=123)

        # Verify request was made correctly
        mock_base_client.request.assert_called_once_with(
            "DELETE",
            "/activities/123",
            version="v2"
        )

        # Verify result
        assert result == mock_response.get("data")

    @pytest.mark.asyncio
    async def test_get_activity_types(self, activity_client, mock_base_client):
        """Test getting activity types"""
        # Setup expected response
        mock_response = {
            "success": True,
            "data": [
                {
                    "id": 1,
                    "name": "Call",
                    "icon_key": "call",
                    "color": "FFFFFF"
                },
                {
                    "id": 2,
                    "name": "Meeting",
                    "icon_key": "meeting",
                    "color": "CCCCCC"
                }
            ]
        }
        mock_base_client.request.return_value = mock_response

        # Call the method
        result = await activity_client.get_activity_types()

        # Verify request was made correctly
        mock_base_client.request.assert_called_once_with(
            "GET",
            "/activityTypes",
            version="v1"  # Activity Types use v1 API
        )

        # Verify result
        assert result == mock_response.get("data")

    @pytest.mark.asyncio
    async def test_create_activity_type(self, activity_client, mock_base_client):
        """Test creating an activity type"""
        # Setup expected response
        mock_response = {
            "success": True,
            "data": {
                "id": 123,
                "name": "Test Activity Type",
                "icon_key": "call",
                "color": "FFFFFF"
            }
        }
        mock_base_client.request.return_value = mock_response

        # Call the method
        result = await activity_client.create_activity_type(
            name="Test Activity Type",
            icon_key="call",
            color="FFFFFF"
        )

        # Verify request was made correctly
        mock_base_client.request.assert_called_once_with(
            "POST",
            "/activityTypes",
            json_payload={
                "name": "Test Activity Type",
                "icon_key": "call",
                "color": "FFFFFF"
            },
            version="v1"  # Activity Types use v1 API
        )

        # Verify result
        assert result == mock_response.get("data")

    @pytest.mark.asyncio
    async def test_validation_error_handling(self, activity_client, mock_base_client):
        """Test that validation errors are properly handled"""
        # Test invalid activity ID
        with pytest.raises(ValueError, match="Invalid activity ID"):
            await activity_client.get_activity(activity_id=-1)

        # Test invalid limit
        with pytest.raises(ValueError, match="Invalid limit"):
            await activity_client.list_activities(limit=-1)

        # Test update with no fields
        with pytest.raises(ValueError, match="At least one field must be provided"):
            await activity_client.update_activity(activity_id=123)

    @pytest.mark.asyncio
    async def test_api_error_handling(self, activity_client, mock_base_client):
        """Test that API errors are properly propagated"""
        # Setup mock to raise PipedriveAPIError
        error_message = "API Error"
        mock_base_client.request.side_effect = PipedriveAPIError(message=error_message)

        # Test API error is propagated
        with pytest.raises(PipedriveAPIError, match=error_message):
            await activity_client.get_activity(activity_id=123)