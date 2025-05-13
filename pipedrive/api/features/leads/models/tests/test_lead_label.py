import pytest
from datetime import datetime
from pydantic import ValidationError

from pipedrive.api.features.leads.models.lead_label import LeadLabel


class TestLeadLabelModel:
    """Tests for the LeadLabel Pydantic model"""
    
    def test_valid_lead_label_creation(self):
        """Test creating a valid LeadLabel model"""
        # Test with minimum required fields
        label = LeadLabel(
            name="Hot",
            color="red"
        )
        assert label.name == "Hot"
        assert label.color == "red"
        assert label.id is None
        assert label.add_time is None
        assert label.update_time is None
        
        # Test with all fields
        now = datetime.now()
        label = LeadLabel(
            name="Hot",
            color="red",
            id="f08b42a0-4e75-11ea-9643-03698ef1cfd6",
            add_time=now,
            update_time=now
        )
        assert label.name == "Hot"
        assert label.color == "red"
        assert label.id == "f08b42a0-4e75-11ea-9643-03698ef1cfd6"
        assert label.add_time == now
        assert label.update_time == now
    
    def test_lead_label_missing_name(self):
        """Test that a LeadLabel without a name raises ValidationError"""
        with pytest.raises(ValidationError):
            LeadLabel(color="red")
        
        with pytest.raises(ValidationError):
            LeadLabel(name="", color="red")
        
        with pytest.raises(ValidationError):
            LeadLabel(name="   ", color="red")
    
    def test_lead_label_missing_color(self):
        """Test that a LeadLabel without a color raises ValidationError"""
        with pytest.raises(ValidationError):
            LeadLabel(name="Hot")
        
        with pytest.raises(ValidationError):
            LeadLabel(name="Hot", color="")
        
        with pytest.raises(ValidationError):
            LeadLabel(name="Hot", color="   ")
    
    def test_lead_label_invalid_color(self):
        """Test that an invalid color raises ValidationError"""
        with pytest.raises(ValidationError):
            LeadLabel(
                name="Hot",
                color="invalid-color"
            )
        
        # Test that case doesn't matter (should not raise)
        label = LeadLabel(
            name="Hot",
            color="RED"
        )
        assert label.color == "red"
    
    def test_lead_label_invalid_id(self):
        """Test that an invalid UUID for id raises ValidationError"""
        with pytest.raises(ValidationError):
            LeadLabel(
                name="Hot",
                color="red",
                id="not-a-uuid"
            )
    
    def test_lead_label_from_api_dict(self):
        """Test converting API response to LeadLabel model"""
        api_data = {
            "id": "f08b42a0-4e75-11ea-9643-03698ef1cfd6",
            "name": "Hot",
            "color": "red",
            "add_time": "2020-02-13T15:31:44.000Z",
            "update_time": "2020-02-13T15:31:44.000Z"
        }
        
        label = LeadLabel.from_api_dict(api_data)
        
        assert label.id == "f08b42a0-4e75-11ea-9643-03698ef1cfd6"
        assert label.name == "Hot"
        assert label.color == "red"
        assert isinstance(label.add_time, datetime)
        assert isinstance(label.update_time, datetime)
        assert label.add_time.year == 2020
        assert label.add_time.month == 2
        assert label.add_time.day == 13
    
    def test_lead_label_to_api_dict(self):
        """Test converting LeadLabel model to API-compatible dictionary"""
        now = datetime.now()
        label = LeadLabel(
            name="Hot",
            color="red",
            id="f08b42a0-4e75-11ea-9643-03698ef1cfd6",
            add_time=now,
            update_time=now
        )
        
        api_dict = label.to_api_dict()
        
        assert api_dict["name"] == "Hot"
        assert api_dict["color"] == "red"
        assert "id" not in api_dict
        assert "add_time" not in api_dict
        assert "update_time" not in api_dict