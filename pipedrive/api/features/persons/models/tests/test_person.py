import pytest
from pydantic import ValidationError

from pipedrive.api.features.persons.models.person import Person
from pipedrive.api.features.persons.models.contact_info import Email, Phone


class TestPerson:
    def test_create_valid_person(self):
        """Test creating a valid Person model"""
        person = Person(name="Test Person")
        assert person.name == "Test Person"
        assert person.emails == []
        assert person.phones == []
        assert person.owner_id is None
        assert person.org_id is None
        assert person.visible_to is None
        assert person.id is None
    
    def test_empty_name_validation(self):
        """Test validation of empty name"""
        with pytest.raises(ValidationError):
            Person(name="")
    
    def test_to_api_dict(self):
        """Test conversion to API dictionary"""
        person = Person(
            name="Test Person",
            owner_id=123,
            emails=[Email(value="test@example.com")],
            phones=[Phone(value="1234567890")]
        )
        
        api_dict = person.to_api_dict()
        
        assert api_dict["name"] == "Test Person"
        assert api_dict["owner_id"] == 123
        assert len(api_dict["emails"]) == 1
        assert api_dict["emails"][0]["value"] == "test@example.com"
        assert api_dict["emails"][0]["primary"] is True
        assert len(api_dict["phones"]) == 1
        assert api_dict["phones"][0]["value"] == "1234567890"
        assert "id" not in api_dict  # id should not be included in API dict
    
    def test_from_api_dict(self):
        """Test creating Person from API response"""
        api_data = {
            "id": 123,
            "name": "API Person",
            "owner_id": 456,
            "emails": [
                {"value": "api@example.com", "label": "work", "primary": True}
            ],
            "phones": [
                {"value": "9876543210", "label": "mobile", "primary": True}
            ]
        }
        
        person = Person.from_api_dict(api_data)
        
        assert person.id == 123
        assert person.name == "API Person"
        assert person.owner_id == 456
        assert len(person.emails) == 1
        assert person.emails[0].value == "api@example.com"
        assert len(person.phones) == 1
        assert person.phones[0].value == "9876543210"
        assert person.phones[0].label == "mobile"
    
    def test_empty_api_response(self):
        """Test handling of empty API response"""
        api_data = {}
        
        with pytest.raises(ValidationError):
            Person.from_api_dict(api_data)  # Should fail because name is required