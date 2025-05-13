import pytest
from pydantic import ValidationError

from pipedrive.api.features.activities.models.activity_type import ActivityType


class TestActivityType:
    def test_valid_activity_type(self):
        """Test creating a valid ActivityType model"""
        activity_type = ActivityType(
            name="Test Activity",
            icon_key="call",
            color="FFFFFF",
            order_nr=1
        )
        
        assert activity_type.name == "Test Activity"
        assert activity_type.icon_key == "call"
        assert activity_type.color == "FFFFFF"
        assert activity_type.order_nr == 1
        assert activity_type.id is None
        assert activity_type.key_string is None
        assert activity_type.active_flag is True
        assert activity_type.is_custom_flag is None
    
    def test_required_fields(self):
        """Test that required fields are enforced"""
        # Missing name
        with pytest.raises(ValidationError):
            ActivityType(icon_key="call")
            
        # Missing icon_key
        with pytest.raises(ValidationError):
            ActivityType(name="Test Activity")
    
    def test_name_validation(self):
        """Test name field validation"""
        # Empty name
        with pytest.raises(ValidationError):
            ActivityType(name="", icon_key="call")
            
        # Whitespace-only name
        with pytest.raises(ValidationError):
            ActivityType(name="   ", icon_key="call")
            
        # Valid name with whitespace is trimmed
        activity_type = ActivityType(name=" Test Activity ", icon_key="call")
        assert activity_type.name == "Test Activity"
    
    def test_icon_key_validation(self):
        """Test icon_key field validation"""
        # Empty icon_key
        with pytest.raises(ValidationError):
            ActivityType(name="Test Activity", icon_key="")
            
        # Whitespace-only icon_key
        with pytest.raises(ValidationError):
            ActivityType(name="Test Activity", icon_key="   ")
            
        # Invalid icon_key
        with pytest.raises(ValidationError):
            ActivityType(name="Test Activity", icon_key="invalid_icon")
            
        # Valid icon_key with whitespace is trimmed
        activity_type = ActivityType(name="Test Activity", icon_key=" call ")
        assert activity_type.icon_key == "call"
    
    def test_color_validation(self):
        """Test color field validation"""
        # Valid color
        activity_type = ActivityType(name="Test Activity", icon_key="call", color="FFFFFF")
        assert activity_type.color == "FFFFFF"
        
        # Lowercase color is converted to uppercase
        activity_type = ActivityType(name="Test Activity", icon_key="call", color="ffffff")
        assert activity_type.color == "FFFFFF"
        
        # Invalid color (not 6 characters)
        with pytest.raises(ValidationError):
            ActivityType(name="Test Activity", icon_key="call", color="FFF")
            
        # Invalid color (contains non-hex characters)
            with pytest.raises(ValidationError):
                ActivityType(name="Test Activity", icon_key="call", color="FGHJKL")
                
        # Empty color is converted to None
        activity_type = ActivityType(name="Test Activity", icon_key="call", color="")
        assert activity_type.color is None
        
        # Whitespace-only color is converted to None
        activity_type = ActivityType(name="Test Activity", icon_key="call", color="   ")
        assert activity_type.color is None
    
    def test_order_nr_validation(self):
        """Test order_nr field validation"""
        # Valid order_nr
        activity_type = ActivityType(name="Test Activity", icon_key="call", order_nr=1)
        assert activity_type.order_nr == 1
        
        # Negative order_nr is invalid
        with pytest.raises(ValidationError):
            ActivityType(name="Test Activity", icon_key="call", order_nr=-1)
    
    def test_to_api_dict(self):
        """Test conversion to API-compatible dictionary"""
        activity_type = ActivityType(
            name="Test Activity",
            icon_key="call",
            color="FFFFFF",
            order_nr=1,
            id=123,
            key_string="test_activity",
            active_flag=True,
            is_custom_flag=True
        )
        
        api_dict = activity_type.to_api_dict()
        
        # Check that the API dict contains the expected fields
        assert api_dict["name"] == "Test Activity"
        assert api_dict["icon_key"] == "call"
        assert api_dict["color"] == "FFFFFF"
        assert api_dict["order_nr"] == 1
        
        # Check that the API dict excludes the specified fields
        assert "id" not in api_dict
        assert "key_string" not in api_dict
        assert "is_custom_flag" not in api_dict
        
        # Check that active_flag is included
        assert api_dict["active_flag"] is True
    
    def test_from_api_dict(self):
        """Test creation from API response dictionary"""
        api_response = {
            "id": 123,
            "name": "Test Activity",
            "icon_key": "call",
            "color": "FFFFFF",
            "order_nr": 1,
            "key_string": "test_activity",
            "active_flag": True,
            "is_custom_flag": True
        }
        
        activity_type = ActivityType.from_api_dict(api_response)
        
        # Check that all fields are set correctly
        assert activity_type.id == 123
        assert activity_type.name == "Test Activity"
        assert activity_type.icon_key == "call"
        assert activity_type.color == "FFFFFF"
        assert activity_type.order_nr == 1
        assert activity_type.key_string == "test_activity"
        assert activity_type.active_flag is True
        assert activity_type.is_custom_flag is True