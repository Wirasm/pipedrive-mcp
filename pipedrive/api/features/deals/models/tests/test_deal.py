from datetime import date

import pytest
from pydantic import ValidationError

from pipedrive.api.features.deals.models.deal import Deal


class TestDealModel:
    """Test suite for the Deal model"""

    def test_valid_deal_creation(self):
        """Test that a valid deal can be created with required fields"""
        deal = Deal(title="Test Deal", value=1000.0, currency="USD", status="open")
        assert deal.title == "Test Deal"
        assert deal.value == 1000.0
        assert deal.currency == "USD"
        assert deal.status == "open"

    def test_deal_to_api_dict(self):
        """Test the to_api_dict method converts model correctly"""
        deal = Deal(
            title="Test Deal",
            value=1000.0,
            currency="USD",
            person_id=123,
            org_id=456,
            status="open",
            owner_id=789,
            stage_id=10,
            pipeline_id=20,
            expected_close_date=date(2023, 12, 31),
            visible_to=3,
            probability=75,
            id=999,  # This should be excluded in the API dict
        )

        api_dict = deal.to_api_dict()

        # Check that ID is excluded
        assert "id" not in api_dict

        # Check that all other fields are included correctly
        assert api_dict["title"] == "Test Deal"
        assert api_dict["value"] == 1000.0
        assert api_dict["currency"] == "USD"
        assert api_dict["person_id"] == 123
        assert api_dict["org_id"] == 456
        assert api_dict["status"] == "open"
        assert api_dict["owner_id"] == 789
        assert api_dict["stage_id"] == 10
        assert api_dict["pipeline_id"] == 20
        assert api_dict["expected_close_date"] == "2023-12-31"
        assert api_dict["visible_to"] == 3
        assert api_dict["probability"] == 75

    def test_deal_from_api_dict(self):
        """Test the from_api_dict method creates model correctly"""
        api_response = {
            "id": 123,
            "title": "API Deal",
            "value": 5000.0,
            "currency": "EUR",
            "person_id": 456,
            "org_id": 789,
            "status": "won",
            "owner_id": 101,
            "stage_id": 202,
            "pipeline_id": 303,
            "expected_close_date": "2023-10-15",
            "visible_to": 1,
            "probability": 90,
            "lost_reason": None,
        }

        deal = Deal.from_api_dict(api_response)

        assert deal.id == 123
        assert deal.title == "API Deal"
        assert deal.value == 5000.0
        assert deal.currency == "EUR"
        assert deal.person_id == 456
        assert deal.org_id == 789
        assert deal.status == "won"
        assert deal.owner_id == 101
        assert deal.stage_id == 202
        assert deal.pipeline_id == 303
        assert deal.expected_close_date == date(2023, 10, 15)
        assert deal.visible_to == 1
        assert deal.probability == 90
        assert deal.lost_reason is None

    def test_deal_empty_title_validation(self):
        """Test that empty title raises validation error"""
        with pytest.raises(ValidationError) as exc_info:
            Deal(title="", status="open")

        # Check error message
        error_msg = str(exc_info.value)
        assert "Deal title cannot be empty" in error_msg

    def test_deal_invalid_status_validation(self):
        """Test that invalid status raises validation error"""
        with pytest.raises(ValidationError) as exc_info:
            Deal(title="Test Deal", status="invalid_status")

        # Check error message
        error_msg = str(exc_info.value)
        assert "Deal status must be one of: open, won, lost" in error_msg

    def test_deal_lost_reason_validation(self):
        """Test that lost_reason can only be set with status='lost'"""
        # Should be valid - lost status with reason
        deal = Deal(title="Lost Deal", status="lost", lost_reason="Price too high")
        assert deal.lost_reason == "Price too high"

        # Should raise error - not lost but has reason
        with pytest.raises(ValidationError) as exc_info:
            Deal(title="Open Deal", status="open", lost_reason="No reason needed")

        # Check error message
        error_msg = str(exc_info.value)
        assert "Lost reason can only be set if deal status is 'lost'" in error_msg

    def test_deal_probability_validation(self):
        """Test probability must be between 0 and 100"""
        # Valid probabilities
        deal1 = Deal(title="Deal 1", status="open", probability=0)
        deal2 = Deal(title="Deal 2", status="open", probability=50)
        deal3 = Deal(title="Deal 3", status="open", probability=100)

        assert deal1.probability == 0
        assert deal2.probability == 50
        assert deal3.probability == 100

        # Invalid probabilities
        with pytest.raises(ValidationError) as exc_info:
            Deal(title="Invalid Deal", status="open", probability=-10)

        # Check error message
        error_msg = str(exc_info.value)
        assert "Deal probability must be between 0 and 100" in error_msg

        with pytest.raises(ValidationError) as exc_info:
            Deal(title="Invalid Deal", status="open", probability=101)

        # Check error message
        error_msg = str(exc_info.value)
        assert "Deal probability must be between 0 and 100" in error_msg
