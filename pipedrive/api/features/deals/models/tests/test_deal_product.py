import pytest
from pydantic import ValidationError

from pipedrive.api.features.deals.models.deal_product import DealProduct


class TestDealProductModel:
    """Test suite for the DealProduct model"""

    def test_valid_deal_product_creation(self):
        """Test that a valid deal product can be created with required fields"""
        deal_product = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=2
        )
        assert deal_product.product_id == 1
        assert deal_product.item_price == 100.0
        assert deal_product.quantity == 2
        assert deal_product.discount == 0
        assert deal_product.tax == 0
        assert deal_product.currency == "USD"
        assert deal_product.discount_type == "percentage"
        assert deal_product.tax_method == "inclusive"
        assert deal_product.is_enabled is True
        assert deal_product.billing_frequency == "one-time"
        assert deal_product.billing_frequency_cycles is None
        assert deal_product.billing_start_date is None
        
    def test_deal_product_to_api_dict(self):
        """Test the to_api_dict method converts model correctly"""
        deal_product = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=2,
            discount=10.0,
            tax=7.5,
            comments="Test comment",
            currency="EUR",
            discount_type="amount",
            tax_method="exclusive",
            is_enabled=True,
            product_variation_id=123,
            billing_frequency="monthly",
            billing_frequency_cycles=12,
            billing_start_date="2023-01-01",
            deal_id=456,  # This should be excluded in the API dict
            id=789  # This should be excluded in the API dict
        )
        
        api_dict = deal_product.to_api_dict()
        
        # Check that ID and deal_id are excluded
        assert "id" not in api_dict
        assert "deal_id" not in api_dict
        
        # Check that all other fields are included correctly
        assert api_dict["product_id"] == 1
        assert api_dict["item_price"] == 100.0
        assert api_dict["quantity"] == 2
        assert api_dict["discount"] == 10.0
        assert api_dict["tax"] == 7.5
        assert api_dict["comments"] == "Test comment"
        assert api_dict["currency"] == "EUR"
        assert api_dict["discount_type"] == "amount"
        assert api_dict["tax_method"] == "exclusive"
        assert api_dict["is_enabled"] is True
        assert api_dict["product_variation_id"] == 123
        assert api_dict["billing_frequency"] == "monthly"
        assert api_dict["billing_frequency_cycles"] == 12
        assert api_dict["billing_start_date"] == "2023-01-01"
        
    def test_deal_product_from_api_dict(self):
        """Test the from_api_dict method creates model correctly"""
        api_response = {
            "id": 123,
            "product_id": 456,
            "item_price": 200.0,
            "quantity": 3,
            "discount": 5.0,
            "tax": 15.0,
            "comments": "API comment",
            "currency": "GBP",
            "discount_type": "percentage",
            "tax_method": "inclusive",
            "is_enabled": True,
            "product_variation_id": 789,
            "billing_frequency": "quarterly",
            "billing_frequency_cycles": 4,
            "billing_start_date": "2023-06-15",
            "deal_id": 999
        }
        
        deal_product = DealProduct.from_api_dict(api_response)
        
        assert deal_product.id == 123
        assert deal_product.product_id == 456
        assert deal_product.item_price == 200.0
        assert deal_product.quantity == 3
        assert deal_product.discount == 5.0
        assert deal_product.tax == 15.0
        assert deal_product.comments == "API comment"
        assert deal_product.currency == "GBP"
        assert deal_product.discount_type == "percentage"
        assert deal_product.tax_method == "inclusive"
        assert deal_product.is_enabled is True
        assert deal_product.product_variation_id == 789
        assert deal_product.billing_frequency == "quarterly"
        assert deal_product.billing_frequency_cycles == 4
        assert deal_product.billing_start_date == "2023-06-15"
        assert deal_product.deal_id == 999
        
    def test_item_price_validation(self):
        """Test that item_price must be positive"""
        # Valid item price
        deal_product = DealProduct(
            product_id=1,
            item_price=0.01,
            quantity=1
        )
        assert deal_product.item_price == 0.01
        
        # Invalid item price
        with pytest.raises(ValidationError) as exc_info:
            DealProduct(
                product_id=1,
                item_price=0,
                quantity=1
            )
            
        # Check error message
        error_msg = str(exc_info.value)
        assert "Item price must be greater than zero" in error_msg
        
        with pytest.raises(ValidationError) as exc_info:
            DealProduct(
                product_id=1,
                item_price=-10.0,
                quantity=1
            )
            
        # Check error message
        error_msg = str(exc_info.value)
        assert "Item price must be greater than zero" in error_msg
        
    def test_quantity_validation(self):
        """Test that quantity must be positive"""
        # Valid quantity
        deal_product = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=1
        )
        assert deal_product.quantity == 1
        
        # Invalid quantity
        with pytest.raises(ValidationError) as exc_info:
            DealProduct(
                product_id=1,
                item_price=100.0,
                quantity=0
            )
            
        # Check error message
        error_msg = str(exc_info.value)
        assert "Quantity must be greater than zero" in error_msg
        
        with pytest.raises(ValidationError) as exc_info:
            DealProduct(
                product_id=1,
                item_price=100.0,
                quantity=-5
            )
            
        # Check error message
        error_msg = str(exc_info.value)
        assert "Quantity must be greater than zero" in error_msg
        
    def test_discount_type_validation(self):
        """Test discount_type must be one of valid options"""
        # Valid discount types
        deal_product1 = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=1,
            discount_type="percentage"
        )
        deal_product2 = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=1,
            discount_type="amount"
        )
        
        assert deal_product1.discount_type == "percentage"
        assert deal_product2.discount_type == "amount"
        
        # Invalid discount type
        with pytest.raises(ValidationError) as exc_info:
            DealProduct(
                product_id=1,
                item_price=100.0,
                quantity=1,
                discount_type="invalid"
            )
            
        # Check error message
        error_msg = str(exc_info.value)
        assert "Invalid discount_type" in error_msg
        assert "Must be one of: percentage, amount" in error_msg
        
    def test_tax_method_validation(self):
        """Test tax_method must be one of valid options"""
        # Valid tax methods
        deal_product1 = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=1,
            tax_method="inclusive"
        )
        deal_product2 = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=1,
            tax_method="exclusive"
        )
        deal_product3 = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=1,
            tax_method="none"
        )
        
        assert deal_product1.tax_method == "inclusive"
        assert deal_product2.tax_method == "exclusive"
        assert deal_product3.tax_method == "none"
        
        # Invalid tax method
        with pytest.raises(ValidationError) as exc_info:
            DealProduct(
                product_id=1,
                item_price=100.0,
                quantity=1,
                tax_method="invalid"
            )
            
        # Check error message
        error_msg = str(exc_info.value)
        assert "Invalid tax_method" in error_msg
        assert "Must be one of: inclusive, exclusive, none" in error_msg
        
    def test_billing_frequency_validation(self):
        """Test billing_frequency must be one of valid options"""
        # Valid billing frequencies
        valid_frequencies = [
            "one-time", "annually", "semi-annually",
            "quarterly", "monthly"
        ]

        for freq in valid_frequencies:
            deal_product = DealProduct(
                product_id=1,
                item_price=100.0,
                quantity=1,
                billing_frequency=freq
            )
            assert deal_product.billing_frequency == freq

        # Test weekly with cycles
        deal_product_weekly = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=1,
            billing_frequency="weekly",
            billing_frequency_cycles=12
        )
        assert deal_product_weekly.billing_frequency == "weekly"
        assert deal_product_weekly.billing_frequency_cycles == 12
        
        # Invalid billing frequency
        with pytest.raises(ValidationError) as exc_info:
            DealProduct(
                product_id=1,
                item_price=100.0,
                quantity=1,
                billing_frequency="invalid"
            )
            
        # Check error message
        error_msg = str(exc_info.value)
        assert "Invalid billing_frequency" in error_msg
        
    def test_billing_frequency_cycles_validation(self):
        """Test billing_frequency_cycles validation rules"""
        # Test one-time with None cycles (valid)
        deal_product1 = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=1,
            billing_frequency="one-time",
            billing_frequency_cycles=None
        )
        assert deal_product1.billing_frequency_cycles is None
        
        # Test one-time with cycles (invalid)
        with pytest.raises(ValidationError) as exc_info:
            DealProduct(
                product_id=1,
                item_price=100.0,
                quantity=1,
                billing_frequency="one-time",
                billing_frequency_cycles=12
            )
            
        # Check error message
        error_msg = str(exc_info.value)
        assert "When billing_frequency is 'one-time', billing_frequency_cycles must be null" in error_msg
        
        # Test weekly with None cycles (invalid)
        with pytest.raises(ValidationError) as exc_info:
            DealProduct(
                product_id=1,
                item_price=100.0,
                quantity=1,
                billing_frequency="weekly",
                billing_frequency_cycles=None
            )
            
        # Check error message
        error_msg = str(exc_info.value)
        assert "When billing_frequency is 'weekly', billing_frequency_cycles must be specified" in error_msg
        
        # Test valid cycles range
        deal_product2 = DealProduct(
            product_id=1,
            item_price=100.0,
            quantity=1,
            billing_frequency="monthly",
            billing_frequency_cycles=12
        )
        assert deal_product2.billing_frequency_cycles == 12
        
        # Test cycles too large
        with pytest.raises(ValidationError) as exc_info:
            DealProduct(
                product_id=1,
                item_price=100.0,
                quantity=1,
                billing_frequency="monthly",
                billing_frequency_cycles=209  # Max is 208
            )
            
        # Check error message
        error_msg = str(exc_info.value)
        assert "billing_frequency_cycles" in error_msg.lower()
        assert "208" in error_msg