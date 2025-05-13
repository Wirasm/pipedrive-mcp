import pytest
from pydantic import ValidationError

from pipedrive.api.features.organizations.models.organization_follower import OrganizationFollower


class TestOrganizationFollower:
    """Tests for the OrganizationFollower model"""

    def test_organization_follower_validation_success(self):
        """Test organization follower creation with valid fields"""
        follower = OrganizationFollower(
            user_id=123,
            add_time="2021-01-01T00:00:00Z"
        )
        assert follower.user_id == 123
        assert follower.add_time == "2021-01-01T00:00:00Z"

    def test_organization_follower_missing_user_id(self):
        """Test organization follower with missing user_id fails validation"""
        with pytest.raises(ValidationError):
            OrganizationFollower()

    def test_organization_follower_to_dict(self):
        """Test conversion to dictionary"""
        follower = OrganizationFollower(
            user_id=123,
            add_time="2021-01-01T00:00:00Z"
        )
        follower_dict = follower.to_dict()
        
        assert "user_id" in follower_dict
        assert follower_dict["user_id"] == 123
        assert follower_dict["add_time"] == "2021-01-01T00:00:00Z"

    def test_organization_follower_from_api_dict(self):
        """Test creation from API dictionary"""
        api_data = {
            "user_id": 456,
            "add_time": "2022-01-01T00:00:00Z"
        }
        
        follower = OrganizationFollower.from_api_dict(api_data)
        
        assert follower.user_id == 456
        assert follower.add_time == "2022-01-01T00:00:00Z"

    def test_organization_follower_optional_fields(self):
        """Test organization follower creation with optional fields omitted"""
        follower = OrganizationFollower(
            user_id=123
        )
        assert follower.user_id == 123
        assert follower.add_time is None