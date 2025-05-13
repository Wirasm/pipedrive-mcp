import pytest
from datetime import date
from pydantic import ValidationError

from pipedrive.api.features.leads.models.lead import Lead


class TestLeadModel:
    """Tests for the Lead Pydantic model"""
    
    def test_valid_lead_creation(self):
        """Test creating a valid Lead model"""
        # Test with minimum required fields
        lead = Lead(
            title="Test Lead",
            person_id=123
        )
        assert lead.title == "Test Lead"
        assert lead.person_id == 123
        assert lead.organization_id is None
        
        # Test with organization instead of person
        lead = Lead(
            title="Test Lead",
            organization_id=456
        )
        assert lead.title == "Test Lead"
        assert lead.organization_id == 456
        assert lead.person_id is None
        
        # Test with all fields
        lead = Lead(
            title="Complete Lead",
            amount=1000.0,
            currency="EUR",
            person_id=123,
            organization_id=456,
            owner_id=789,
            expected_close_date=date(2023, 12, 31),
            visible_to=3,
            id="adf21080-0e10-11eb-879b-05d71fb426ec",
            label_ids=["f08b42a0-4e75-11ea-9643-03698ef1cfd6"],
            source_name="API",
            is_archived=False,
            was_seen=True,
            channel=52,
            channel_id="Marketing Campaign"
        )
        assert lead.title == "Complete Lead"
        assert lead.amount == 1000.0
        assert lead.currency == "EUR"
        assert lead.person_id == 123
        assert lead.organization_id == 456
        assert lead.owner_id == 789
        assert lead.expected_close_date == date(2023, 12, 31)
        assert lead.visible_to == 3
        assert lead.id == "adf21080-0e10-11eb-879b-05d71fb426ec"
        assert lead.label_ids == ["f08b42a0-4e75-11ea-9643-03698ef1cfd6"]
        assert lead.source_name == "API"
        assert lead.is_archived is False
        assert lead.was_seen is True
        assert lead.channel == 52
        assert lead.channel_id == "Marketing Campaign"
    
    def test_lead_missing_title(self):
        """Test that a Lead without a title raises ValidationError"""
        with pytest.raises(ValidationError):
            Lead(person_id=123)
        
        with pytest.raises(ValidationError):
            Lead(title="", person_id=123)
        
        with pytest.raises(ValidationError):
            Lead(title="   ", person_id=123)
    
    def test_lead_missing_person_and_organization(self):
        """Test that a Lead without person_id or organization_id raises ValidationError"""
        with pytest.raises(ValidationError):
            Lead(title="Test Lead")
    
    def test_lead_invalid_id(self):
        """Test that an invalid UUID for id raises ValidationError"""
        with pytest.raises(ValidationError):
            Lead(
                title="Test Lead",
                person_id=123,
                id="not-a-uuid"
            )
    
    def test_lead_invalid_currency(self):
        """Test that an invalid currency code raises ValidationError"""
        with pytest.raises(ValidationError):
            Lead(
                title="Test Lead",
                person_id=123,
                currency="INVALID"  # Not a 3-letter code
            )
        
        with pytest.raises(ValidationError):
            Lead(
                title="Test Lead",
                person_id=123,
                currency="123"  # Not alphabetic
            )
    
    def test_lead_negative_amount(self):
        """Test that a negative amount raises ValidationError"""
        with pytest.raises(ValidationError):
            Lead(
                title="Test Lead",
                person_id=123,
                amount=-100.0
            )
    
    def test_lead_invalid_visible_to(self):
        """Test that an invalid visible_to value raises ValidationError"""
        with pytest.raises(ValidationError):
            Lead(
                title="Test Lead",
                person_id=123,
                visible_to=2  # Not one of the valid values (1, 3, 5, 7)
            )
    
    def test_lead_from_api_dict(self):
        """Test converting API response to Lead model"""
        api_data = {
            "id": "adf21080-0e10-11eb-879b-05d71fb426ec",
            "title": "API Lead",
            "owner_id": 1,
            "creator_id": 1,
            "person_id": 1092,
            "organization_id": None,
            "source_name": "API",
            "origin": "API",
            "is_archived": False,
            "was_seen": False,
            "amount": 999,
            "currency": "USD",
            "expected_close_date": "2023-12-31",
            "visible_to": "3",
            "label_ids": ["f08b42a0-4e75-11ea-9643-03698ef1cfd6"]
        }
        
        lead = Lead.from_api_dict(api_data)
        
        assert lead.id == "adf21080-0e10-11eb-879b-05d71fb426ec"
        assert lead.title == "API Lead"
        assert lead.owner_id == 1
        assert lead.person_id == 1092
        assert lead.organization_id is None
        assert lead.amount == 999
        assert lead.currency == "USD"
        assert lead.expected_close_date == date(2023, 12, 31)
        assert lead.visible_to == 3
        assert lead.label_ids == ["f08b42a0-4e75-11ea-9643-03698ef1cfd6"]
    
    def test_lead_from_api_dict_with_value_object(self):
        """Test converting API response with value object to Lead model"""
        api_data = {
            "id": "adf21080-0e10-11eb-879b-05d71fb426ec",
            "title": "API Lead",
            "person_id": 1092,
            "value": {
                "amount": 999,
                "currency": "EUR"
            }
        }
        
        lead = Lead.from_api_dict(api_data)
        
        assert lead.amount == 999
        assert lead.currency == "EUR"
    
    def test_lead_to_api_dict(self):
        """Test converting Lead model to API-compatible dictionary"""
        lead = Lead(
            title="Test Lead",
            amount=1000.0,
            currency="EUR",
            person_id=123,
            expected_close_date=date(2023, 12, 31),
            visible_to=3,
            label_ids=["f08b42a0-4e75-11ea-9643-03698ef1cfd6"],
        )
        
        api_dict = lead.to_api_dict()
        
        assert api_dict["title"] == "Test Lead"
        assert api_dict["person_id"] == 123
        assert "value" in api_dict
        assert api_dict["value"]["amount"] == 1000.0
        assert api_dict["value"]["currency"] == "EUR"
        assert "amount" not in api_dict
        assert "currency" not in api_dict
        assert api_dict["expected_close_date"] == "2023-12-31"
        assert api_dict["visible_to"] == 3
        assert api_dict["label_ids"] == ["f08b42a0-4e75-11ea-9643-03698ef1cfd6"]