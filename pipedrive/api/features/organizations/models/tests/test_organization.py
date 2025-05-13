import pytest
from pydantic import ValidationError

from pipedrive.api.features.organizations.models.organization import Organization


class TestOrganization:
    """Tests for the Organization model"""

    def test_organization_validation_success(self):
        """Test organization creation with valid fields"""
        org = Organization(
            name="Test Organization",
            owner_id=123,
            address={"value": "123 Test St, Test City"},
            visible_to=1
        )
        assert org.name == "Test Organization"
        assert org.owner_id == 123
        assert org.address == {"value": "123 Test St, Test City"}
        assert org.visible_to == 1

    def test_organization_empty_name_validation_error(self):
        """Test organization with empty name fails validation"""
        with pytest.raises(ValidationError):
            Organization(name="")

    def test_organization_invalid_visible_to_validation_error(self):
        """Test organization with invalid visible_to value fails validation"""
        with pytest.raises(ValidationError):
            Organization(name="Test Organization", visible_to=5)

    def test_organization_to_api_dict(self):
        """Test conversion to API dictionary"""
        org = Organization(
            name="Test Organization",
            owner_id=123,
            address={"value": "123 Test St, Test City"},
            visible_to=1,
            id=456
        )
        api_dict = org.to_api_dict()
        
        assert "name" in api_dict
        assert api_dict["name"] == "Test Organization"
        assert api_dict["owner_id"] == 123
        assert api_dict["address"] == {"value": "123 Test St, Test City"}
        assert api_dict["visible_to"] == 1
        # id should be excluded
        assert "id" not in api_dict

    def test_organization_from_api_dict(self):
        """Test creation from API dictionary"""
        api_data = {
            "id": 789,
            "name": "API Organization",
            "owner_id": 456,
            "address": "456 API St, API City",
            "visible_to": 2,
            "label_ids": [1, 2, 3]
        }
        
        org = Organization.from_api_dict(api_data)
        
        assert org.id == 789
        assert org.name == "API Organization"
        assert org.owner_id == 456
        assert org.address == {"value": "456 API St, API City"}
        assert org.visible_to == 2
        assert org.label_ids == [1, 2, 3]