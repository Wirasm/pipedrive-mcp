import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from pipedrive.api.features.organizations.client.organization_client import OrganizationClient


@pytest.mark.asyncio
class TestOrganizationClient:
    """Tests for the OrganizationClient"""

    def setup_method(self):
        """Set up test fixtures"""
        self.base_client = AsyncMock()
        self.org_client = OrganizationClient(self.base_client)

    async def test_create_organization(self):
        """Test creating an organization"""
        # Arrange
        self.base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "name": "Test Organization",
                "owner_id": 456,
                "address": "123 Test St",
                "visible_to": 1
            }
        }

        # Act
        result = await self.org_client.create_organization(
            name="Test Organization",
            owner_id=456,
            address="123 Test St",
            visible_to=1
        )

        # Assert
        self.base_client.request.assert_called_once_with(
            "POST",
            "/organizations",
            json_payload={
                "name": "Test Organization",
                "owner_id": 456,
                "address": "123 Test St",
                "visible_to": 1
            }
        )
        assert result["id"] == 123
        assert result["name"] == "Test Organization"

    async def test_get_organization(self):
        """Test getting an organization by ID"""
        # Arrange
        self.base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "name": "Test Organization",
                "owner_id": 456,
                "address": "123 Test St",
                "visible_to": 1
            }
        }

        # Act
        result = await self.org_client.get_organization(
            organization_id=123,
            include_fields=["notes_count", "followers_count"],
            custom_fields_keys=["custom_field1", "custom_field2"]
        )

        # Assert
        self.base_client.request.assert_called_once_with(
            "GET",
            "/organizations/123",
            query_params={
                "include_fields": "notes_count,followers_count",
                "custom_fields": "custom_field1,custom_field2"
            }
        )
        assert result["id"] == 123
        assert result["name"] == "Test Organization"

    async def test_update_organization(self):
        """Test updating an organization"""
        # Arrange
        self.base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "name": "Updated Organization",
                "owner_id": 456,
                "address": "123 Test St",
                "visible_to": 1
            }
        }

        # Act
        result = await self.org_client.update_organization(
            organization_id=123,
            name="Updated Organization"
        )

        # Assert
        self.base_client.request.assert_called_once_with(
            "PATCH",
            "/organizations/123",
            json_payload={"name": "Updated Organization"}
        )
        assert result["id"] == 123
        assert result["name"] == "Updated Organization"

    async def test_update_organization_no_fields_raises_error(self):
        """Test updating an organization with no fields raises ValueError"""
        # Act & Assert
        with pytest.raises(ValueError):
            await self.org_client.update_organization(organization_id=123)

    async def test_delete_organization(self):
        """Test deleting an organization"""
        # Arrange
        self.base_client.request.return_value = {
            "success": True,
            "data": {"id": 123}
        }

        # Act
        result = await self.org_client.delete_organization(organization_id=123)

        # Assert
        self.base_client.request.assert_called_once_with("DELETE", "/organizations/123")
        assert result["id"] == 123

    async def test_list_organizations(self):
        """Test listing organizations"""
        # Arrange
        self.base_client.request.return_value = {
            "success": True,
            "data": [
                {"id": 123, "name": "Organization 1"},
                {"id": 456, "name": "Organization 2"}
            ],
            "additional_data": {
                "next_cursor": "next_page_token"
            }
        }

        # Act
        orgs, next_cursor = await self.org_client.list_organizations(
            limit=2,
            owner_id=789,
            sort_by="name",
            sort_direction="asc"
        )

        # Assert
        self.base_client.request.assert_called_once_with(
            "GET",
            "/organizations",
            query_params={
                "limit": 2,
                "owner_id": 789,
                "sort_by": "name",
                "sort_direction": "asc"
            }
        )
        assert len(orgs) == 2
        assert orgs[0]["name"] == "Organization 1"
        assert orgs[1]["name"] == "Organization 2"
        assert next_cursor == "next_page_token"

    async def test_search_organizations(self):
        """Test searching for organizations"""
        # Arrange
        self.base_client.request.return_value = {
            "success": True,
            "data": {
                "items": [
                    {"id": 123, "name": "Test Organization", "result_score": 0.9},
                    {"id": 456, "name": "Another Test Organization", "result_score": 0.7}
                ]
            },
            "additional_data": {
                "next_cursor": "search_next_page"
            }
        }

        # Act
        results, next_cursor = await self.org_client.search_organizations(
            term="Test",
            fields=["name", "address"],
            exact_match=False,
            limit=10
        )

        # Assert
        self.base_client.request.assert_called_once_with(
            "GET",
            "/organizations/search",
            query_params={
                "term": "Test",
                "fields": "name,address",
                "exact_match": "false",
                "limit": 10
            }
        )
        assert len(results) == 2
        assert results[0]["name"] == "Test Organization"
        assert next_cursor == "search_next_page"

    async def test_add_follower(self):
        """Test adding a follower to an organization"""
        # Arrange
        self.base_client.request.return_value = {
            "success": True,
            "data": {
                "user_id": 456,
                "add_time": "2021-01-01T00:00:00Z"
            }
        }

        # Act
        result = await self.org_client.add_follower(
            organization_id=123,
            user_id=456
        )

        # Assert
        self.base_client.request.assert_called_once_with(
            "POST",
            "/organizations/123/followers",
            json_payload={"user_id": 456}
        )
        assert result["user_id"] == 456

    async def test_delete_follower(self):
        """Test deleting a follower from an organization"""
        # Arrange
        self.base_client.request.return_value = {
            "success": True,
            "data": {"user_id": 456}
        }

        # Act
        result = await self.org_client.delete_follower(
            organization_id=123,
            follower_id=456
        )

        # Assert
        self.base_client.request.assert_called_once_with(
            "DELETE",
            "/organizations/123/followers/456"
        )
        assert result["user_id"] == 456