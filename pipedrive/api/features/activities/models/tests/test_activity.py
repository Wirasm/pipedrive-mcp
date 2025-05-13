import pytest
from pydantic import ValidationError

from pipedrive.api.features.activities.models.activity import Activity


class TestActivity:
    def test_valid_activity(self):
        """Test creating a valid Activity model"""
        activity = Activity(
            subject="Test Activity",
            type="call",
            due_date="2023-01-01",
            due_time="10:00:00",
            duration="01:00:00",
            owner_id=1,
            deal_id=2,
            lead_id="46c3b0e1-db35-59ca-1828-4817378dff71",
            person_id=3,
            org_id=4,
            busy=True,
            done=False,
            note="Test note",
            location="Test location",
            public_description="Test description",
            priority=1
        )
        
        assert activity.subject == "Test Activity"
        assert activity.type == "call"
        assert activity.due_date == "2023-01-01"
        assert activity.due_time == "10:00:00"
        assert activity.duration == "01:00:00"
        assert activity.owner_id == 1
        assert activity.deal_id == 2
        assert activity.lead_id == "46c3b0e1-db35-59ca-1828-4817378dff71"
        assert activity.person_id == 3
        assert activity.org_id == 4
        assert activity.busy is True
        assert activity.done is False
        assert activity.note == "Test note"
        assert activity.location == "Test location"
        assert activity.public_description == "Test description"
        assert activity.priority == 1
        assert activity.id is None
    
    def test_required_fields(self):
        """Test that required fields are enforced"""
        # Missing subject
        with pytest.raises(ValidationError):
            Activity(type="call")
            
        # Missing type
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity")
            
        # Valid with only required fields
        activity = Activity(subject="Test Activity", type="call")
        assert activity.subject == "Test Activity"
        assert activity.type == "call"
    
    def test_subject_validation(self):
        """Test subject field validation"""
        # Empty subject
        with pytest.raises(ValidationError):
            Activity(subject="", type="call")
            
        # Whitespace-only subject
        with pytest.raises(ValidationError):
            Activity(subject="   ", type="call")
            
        # Valid subject with whitespace is trimmed
        activity = Activity(subject=" Test Activity ", type="call")
        assert activity.subject == "Test Activity"
    
    def test_type_validation(self):
        """Test type field validation"""
        # Empty type
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="")
            
        # Whitespace-only type
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="   ")
            
        # Valid type with whitespace is trimmed
        activity = Activity(subject="Test Activity", type=" call ")
        assert activity.type == "call"
    
    def test_due_date_validation(self):
        """Test due_date field validation"""
        # Valid due_date
        activity = Activity(subject="Test Activity", type="call", due_date="2023-01-01")
        assert activity.due_date == "2023-01-01"
        
        # Invalid due_date format
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", due_date="01/01/2023")
            
        # Empty due_date is converted to None
        activity = Activity(subject="Test Activity", type="call", due_date="")
        assert activity.due_date is None
        
        # Whitespace-only due_date is converted to None
        activity = Activity(subject="Test Activity", type="call", due_date="   ")
        assert activity.due_date is None
    
    def test_due_time_validation(self):
        """Test due_time field validation"""
        # Valid due_time
        activity = Activity(subject="Test Activity", type="call", due_time="10:00:00")
        assert activity.due_time == "10:00:00"
        
        # Invalid due_time format
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", due_time="10:00")
            
        # Empty due_time is converted to None
        activity = Activity(subject="Test Activity", type="call", due_time="")
        assert activity.due_time is None
        
        # Whitespace-only due_time is converted to None
        activity = Activity(subject="Test Activity", type="call", due_time="   ")
        assert activity.due_time is None
    
    def test_duration_validation(self):
        """Test duration field validation"""
        # Valid duration
        activity = Activity(subject="Test Activity", type="call", duration="01:00:00")
        assert activity.duration == "01:00:00"
        
        # HH:MM format is auto-completed to HH:MM:00
        activity = Activity(subject="Test Activity", type="call", duration="01:00")
        assert activity.duration == "01:00:00"
        
        # Single-digit hour with no leading zero is fixed
        activity = Activity(subject="Test Activity", type="call", duration="1:00")
        assert activity.duration == "01:00:00"
        
        # Single-digit hour with seconds but no leading zero is fixed
        activity = Activity(subject="Test Activity", type="call", duration="1:00:00")
        assert activity.duration == "01:00:00"
        
        # Actually invalid duration format
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", duration="invalid")
            
        # Empty duration is converted to None
        activity = Activity(subject="Test Activity", type="call", duration="")
        assert activity.duration is None
        
        # Whitespace-only duration is converted to None
        activity = Activity(subject="Test Activity", type="call", duration="   ")
        assert activity.duration is None
    
    def test_id_validation(self):
        """Test ID fields validation"""
        # Valid IDs
        activity = Activity(
            subject="Test Activity", 
            type="call",
            owner_id=1,
            deal_id=2,
            person_id=3,
            org_id=4,
            project_id=5,
            id=6
        )
        assert activity.owner_id == 1
        assert activity.deal_id == 2
        assert activity.person_id == 3
        assert activity.org_id == 4
        assert activity.project_id == 5
        assert activity.id == 6
        
        # Negative IDs are invalid
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", owner_id=-1)
            
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", deal_id=-1)
            
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", person_id=-1)
            
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", org_id=-1)
            
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", project_id=-1)
            
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", id=-1)
    
    def test_lead_id_validation(self):
        """Test lead_id field validation"""
        # Valid UUID
        activity = Activity(
            subject="Test Activity", 
            type="call",
            lead_id="46c3b0e1-db35-59ca-1828-4817378dff71"
        )
        assert activity.lead_id == "46c3b0e1-db35-59ca-1828-4817378dff71"
        
        # Invalid UUID format
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", lead_id="not-a-uuid")
            
        # Empty lead_id is converted to None
        activity = Activity(subject="Test Activity", type="call", lead_id="")
        assert activity.lead_id is None
        
        # Whitespace-only lead_id is converted to None
        activity = Activity(subject="Test Activity", type="call", lead_id="   ")
        assert activity.lead_id is None
    
    def test_priority_validation(self):
        """Test priority field validation"""
        # Valid priority
        activity = Activity(subject="Test Activity", type="call", priority=100)
        assert activity.priority == 100
        
        # Negative priority is invalid
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", priority=-1)
            
        # Priority > 999 is invalid
        with pytest.raises(ValidationError):
            Activity(subject="Test Activity", type="call", priority=1000)
    
    def test_to_api_dict(self):
        """Test conversion to API-compatible dictionary"""
        activity = Activity(
            subject="Test Activity",
            type="call",
            due_date="2023-01-01",
            due_time="10:00:00",
            duration="01:00:00",
            owner_id=1,
            deal_id=2,
            lead_id="46c3b0e1-db35-59ca-1828-4817378dff71",
            person_id=3,
            org_id=4,
            project_id=5,
            busy=True,
            done=False,
            note="Test note",
            location="Test location",
            public_description="Test description",
            priority=1,
            id=123
        )
        
        api_dict = activity.to_api_dict()
        
        # Check that the API dict contains the expected fields
        assert api_dict["subject"] == "Test Activity"
        assert api_dict["type"] == "call"
        assert api_dict["due_date"] == "2023-01-01"
        assert api_dict["due_time"] == "10:00:00"
        assert api_dict["duration"] == "01:00:00"
        assert api_dict["owner_id"] == 1
        assert api_dict["deal_id"] == 2
        assert api_dict["lead_id"] == "46c3b0e1-db35-59ca-1828-4817378dff71"
        assert api_dict["person_id"] == 3
        assert api_dict["org_id"] == 4
        assert api_dict["project_id"] == 5
        assert api_dict["busy"] is True
        assert api_dict["done"] is False
        assert api_dict["note"] == "Test note"
        assert api_dict["location"] == "Test location"
        assert api_dict["public_description"] == "Test description"
        assert api_dict["priority"] == 1
        
        # Check that the API dict excludes ID
        assert "id" not in api_dict
    
    def test_from_api_dict(self):
        """Test creation from API response dictionary"""
        api_response = {
            "id": 123,
            "subject": "Test Activity",
            "type": "call",
            "due_date": "2023-01-01",
            "due_time": "10:00:00",
            "duration": "01:00:00",
            "owner_id": 1,
            "deal_id": 2,
            "lead_id": "46c3b0e1-db35-59ca-1828-4817378dff71",
            "person_id": 3,
            "org_id": 4,
            "project_id": 5,
            "busy": True,
            "done": False,
            "note": "Test note",
            "location": "Test location",
            "public_description": "Test description",
            "priority": 1
        }
        
        activity = Activity.from_api_dict(api_response)
        
        # Check that all fields are set correctly
        assert activity.id == 123
        assert activity.subject == "Test Activity"
        assert activity.type == "call"
        assert activity.due_date == "2023-01-01"
        assert activity.due_time == "10:00:00"
        assert activity.duration == "01:00:00"
        assert activity.owner_id == 1
        assert activity.deal_id == 2
        assert activity.lead_id == "46c3b0e1-db35-59ca-1828-4817378dff71"
        assert activity.person_id == 3
        assert activity.org_id == 4
        assert activity.project_id == 5
        assert activity.busy is True
        assert activity.done is False
        assert activity.note == "Test note"
        assert activity.location == "Test location"
        assert activity.public_description == "Test description"
        assert activity.priority == 1