from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pipedrive.api.features.deals.client.deal_client import DealClient
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


class TestDealClient:
    """Test suite for the DealClient class"""

    @pytest.fixture
    def mock_base_client(self):
        """Fixture for mocked BaseClient"""
        mock_client = AsyncMock()
        mock_client.request = AsyncMock()
        return mock_client

    @pytest.fixture
    def deal_client(self, mock_base_client):
        """Fixture for DealClient instance with mocked base client"""
        return DealClient(mock_base_client)

    @pytest.mark.asyncio
    async def test_create_deal_success(self, deal_client, mock_base_client):
        """Test create_deal with successful API response"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "title": "Test Deal",
                "value": 1000,
                "currency": "USD",
                "status": "open",
            },
        }

        # Call the method
        result = await deal_client.create_deal(
            title="Test Deal", value=1000, currency="USD", status="open"
        )

        # Verify the result
        assert result["id"] == 123
        assert result["title"] == "Test Deal"
        assert result["value"] == 1000
        assert result["currency"] == "USD"
        assert result["status"] == "open"

        # Verify the API call
        mock_base_client.request.assert_called_once_with(
            "POST",
            "/deals",
            json_payload={
                "title": "Test Deal",
                "value": 1000,
                "currency": "USD",
                "status": "open",
            },
        )

    @pytest.mark.asyncio
    async def test_create_deal_with_all_parameters(self, deal_client, mock_base_client):
        """Test create_deal with all parameters"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "title": "Test Deal",
                "value": 1000,
                "currency": "USD",
                "person_id": 456,
                "org_id": 789,
                "status": "open",
                "expected_close_date": "2023-12-31",
                "owner_id": 101,
                "stage_id": 202,
                "pipeline_id": 303,
                "visible_to": 3,
                "probability": 75,
            },
        }

        # Call the method with all parameters
        result = await deal_client.create_deal(
            title="Test Deal",
            value=1000,
            currency="USD",
            person_id=456,
            org_id=789,
            status="open",
            expected_close_date="2023-12-31",
            owner_id=101,
            stage_id=202,
            pipeline_id=303,
            visible_to=3,
            probability=75,
            custom_fields={"custom_field_key": "custom_value"},
        )

        # Verify the result
        assert result["id"] == 123
        assert result["title"] == "Test Deal"

        # Verify the API call - check that all parameters were included
        called_with = mock_base_client.request.call_args[1]["json_payload"]
        assert called_with["title"] == "Test Deal"
        assert called_with["value"] == 1000
        assert called_with["currency"] == "USD"
        assert called_with["person_id"] == 456
        assert called_with["org_id"] == 789
        assert called_with["status"] == "open"
        assert called_with["expected_close_date"] == "2023-12-31"
        assert called_with["owner_id"] == 101
        assert called_with["stage_id"] == 202
        assert called_with["pipeline_id"] == 303
        assert called_with["visible_to"] == 3
        assert called_with["probability"] == 75
        assert called_with["custom_field_key"] == "custom_value"

    @pytest.mark.asyncio
    async def test_create_deal_api_error(self, deal_client, mock_base_client):
        """Test create_deal with API error"""
        # Setup mock to raise error
        error_response = {
            "success": False,
            "error": "Invalid data",
            "error_info": "Title is required",
        }
        mock_base_client.request.side_effect = PipedriveAPIError(
            message="API Error: Invalid data",
            status_code=400,
            error_info="Title is required",
            response_data=error_response,
        )

        # Call the method and expect exception
        with pytest.raises(PipedriveAPIError) as exc_info:
            await deal_client.create_deal(title="Test Deal")  # Use valid title to pass validation

        # Verify the exception
        assert "API Error: Invalid data" in str(exc_info.value)
        assert exc_info.value.status_code == 400
        assert exc_info.value.error_info == "Title is required"
        assert exc_info.value.response_data == error_response

    @pytest.mark.asyncio
    async def test_get_deal_success(self, deal_client, mock_base_client):
        """Test get_deal with successful API response"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "title": "Test Deal",
                "value": 1000,
                "currency": "USD",
                "status": "open",
            },
        }

        # Call the method
        result = await deal_client.get_deal(deal_id=123)

        # Verify the result
        assert result["id"] == 123
        assert result["title"] == "Test Deal"

        # Verify the API call
        mock_base_client.request.assert_called_once_with(
            "GET", "/deals/123", query_params=None
        )

    @pytest.mark.asyncio
    async def test_get_deal_with_include_fields(self, deal_client, mock_base_client):
        """Test get_deal with include_fields parameter"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "title": "Test Deal",
                "products_count": 2,
                "files_count": 5,
            },
        }

        # Call the method with include_fields
        result = await deal_client.get_deal(
            deal_id=123, include_fields=["products_count", "files_count"]
        )

        # Verify the result
        assert result["id"] == 123
        assert result["title"] == "Test Deal"
        assert result["products_count"] == 2
        assert result["files_count"] == 5

        # Verify the API call with query parameters
        mock_base_client.request.assert_called_once_with(
            "GET",
            "/deals/123",
            query_params={"include_fields": "products_count,files_count"},
        )

    @pytest.mark.asyncio
    async def test_update_deal_success(self, deal_client, mock_base_client):
        """Test update_deal with successful API response"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "title": "Updated Deal",
                "value": 2000,
                "currency": "EUR",
                "status": "open",
            },
        }

        # Call the method
        result = await deal_client.update_deal(
            deal_id=123, title="Updated Deal", value=2000, currency="EUR"
        )

        # Verify the result
        assert result["id"] == 123
        assert result["title"] == "Updated Deal"
        assert result["value"] == 2000
        assert result["currency"] == "EUR"

        # Verify the API call
        mock_base_client.request.assert_called_once_with(
            "PATCH",
            "/deals/123",
            json_payload={"title": "Updated Deal", "value": 2000, "currency": "EUR"},
        )

    @pytest.mark.asyncio
    async def test_update_deal_empty_payload(self, deal_client):
        """Test update_deal with empty payload raises error"""
        # Call the method with no fields to update and expect exception
        with pytest.raises(ValueError) as exc_info:
            await deal_client.update_deal(deal_id=123)

        # Verify the exception
        assert "At least one field must be provided for updating a deal" in str(
            exc_info.value
        )

    @pytest.mark.asyncio
    async def test_delete_deal_success(self, deal_client, mock_base_client):
        """Test delete_deal with successful API response"""
        # Setup mock response
        mock_base_client.request.return_value = {"success": True, "data": {"id": 123}}

        # Call the method
        result = await deal_client.delete_deal(deal_id=123)

        # Verify the result
        assert result["id"] == 123

        # Verify the API call
        mock_base_client.request.assert_called_once_with("DELETE", "/deals/123")

    @pytest.mark.asyncio
    async def test_delete_deal_error_handling(self, deal_client, mock_base_client):
        """Test delete_deal handles unsuccessful response correctly"""
        # Setup mock response with success=False
        mock_base_client.request.return_value = {
            "success": False,
            "error": "Deal not found",
        }

        # Call the method
        result = await deal_client.delete_deal(deal_id=123)

        # Verify the result includes error details
        assert result["id"] == 123
        assert "error_details" in result
        assert result["error_details"]["error"] == "Deal not found"

    @pytest.mark.asyncio
    async def test_list_deals_success(self, deal_client, mock_base_client):
        """Test list_deals with successful API response"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": [{"id": 123, "title": "Deal 1"}, {"id": 456, "title": "Deal 2"}],
            "additional_data": {"next_cursor": "next_page_token"},
        }

        # Call the method
        deals, next_cursor = await deal_client.list_deals(limit=2)

        # Verify the results
        assert len(deals) == 2
        assert deals[0]["id"] == 123
        assert deals[0]["title"] == "Deal 1"
        assert deals[1]["id"] == 456
        assert deals[1]["title"] == "Deal 2"
        assert next_cursor == "next_page_token"

        # Verify the API call
        mock_base_client.request.assert_called_once_with(
            "GET", "/deals", query_params={"limit": 2}
        )

    @pytest.mark.asyncio
    async def test_list_deals_with_filters(self, deal_client, mock_base_client):
        """Test list_deals with various filter parameters"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": [{"id": 123, "title": "Deal 1", "person_id": 789, "org_id": 101}],
            "additional_data": {"next_cursor": None},
        }

        # Call the method with filters
        deals, next_cursor = await deal_client.list_deals(
            limit=10,
            cursor="some_cursor",
            filter_id=202,
            owner_id=303,
            person_id=789,
            org_id=101,
            pipeline_id=404,
            stage_id=505,
            status="open",
            sort_by="update_time",
            sort_direction="desc",
            include_fields=["products_count", "notes_count"],
            custom_fields_keys=["custom1", "custom2"],
            updated_since="2023-01-01T00:00:00Z",
            updated_until="2023-12-31T23:59:59Z",
        )

        # Verify the results
        assert len(deals) == 1
        assert deals[0]["id"] == 123
        assert deals[0]["title"] == "Deal 1"
        assert next_cursor is None

        # Verify the API call with all filters
        called_with = mock_base_client.request.call_args[1]["query_params"]
        assert called_with["limit"] == 10
        assert called_with["cursor"] == "some_cursor"
        assert called_with["filter_id"] == 202
        assert called_with["owner_id"] == 303
        assert called_with["person_id"] == 789
        assert called_with["org_id"] == 101
        assert called_with["pipeline_id"] == 404
        assert called_with["stage_id"] == 505
        assert called_with["status"] == "open"
        assert called_with["sort_by"] == "update_time"
        assert called_with["sort_direction"] == "desc"
        assert called_with["include_fields"] == "products_count,notes_count"
        assert called_with["custom_fields"] == "custom1,custom2"
        assert called_with["updated_since"] == "2023-01-01T00:00:00Z"
        assert called_with["updated_until"] == "2023-12-31T23:59:59Z"

    @pytest.mark.asyncio
    async def test_search_deals_success(self, deal_client, mock_base_client):
        """Test search_deals with successful API response"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "items": [
                    {"id": 123, "title": "Search Deal 1"},
                    {"id": 456, "title": "Search Deal 2"},
                ]
            },
            "additional_data": {"next_cursor": "search_next_page"},
        }

        # Call the method
        items, next_cursor = await deal_client.search_deals(term="Search")

        # Verify the results
        assert len(items) == 2
        assert items[0]["id"] == 123
        assert items[0]["title"] == "Search Deal 1"
        assert items[1]["id"] == 456
        assert items[1]["title"] == "Search Deal 2"
        assert next_cursor == "search_next_page"

        # Verify the API call
        mock_base_client.request.assert_called_once_with(
            "GET",
            "/deals/search",
            query_params={"term": "Search", "exact_match": "false", "limit": 100},
        )

    @pytest.mark.asyncio
    async def test_search_deals_with_parameters(self, deal_client, mock_base_client):
        """Test search_deals with all parameters"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {"items": [{"id": 123, "title": "Exact Match Deal"}]},
            "additional_data": {"next_cursor": None},
        }

        # Call the method with parameters
        items, next_cursor = await deal_client.search_deals(
            term="Exact",
            fields=["title", "notes"],
            exact_match=True,
            person_id=789,
            organization_id=101,
            status="open",
            include_fields=["cc_email"],
            limit=50,
            cursor="search_cursor",
        )

        # Verify the results
        assert len(items) == 1
        assert items[0]["id"] == 123
        assert items[0]["title"] == "Exact Match Deal"
        assert next_cursor is None

        # Verify the API call with all parameters
        called_with = mock_base_client.request.call_args[1]["query_params"]
        assert called_with["term"] == "Exact"
        assert called_with["fields"] == "title,notes"
        assert called_with["exact_match"] == "true"
        assert called_with["person_id"] == 789
        assert called_with["organization_id"] == 101
        assert called_with["status"] == "open"
        assert called_with["include_fields"] == "cc_email"
        assert called_with["limit"] == 50
        assert called_with["cursor"] == "search_cursor"

    @pytest.mark.asyncio
    async def test_add_product_to_deal_success(self, deal_client, mock_base_client):
        """Test add_product_to_deal with successful API response"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "deal_id": 456,
                "product_id": 789,
                "item_price": 100,
                "quantity": 2,
                "discount": 10,
                "tax": 5,
                "comments": "Test product",
            }
        }

        # Call the method
        result = await deal_client.add_product_to_deal(
            deal_id=456,
            product_id=789,
            item_price=100,
            quantity=2,
            tax=5,
            comments="Test product",
            discount=10,
        )

        # Verify the result
        assert result["id"] == 123
        assert result["deal_id"] == 456
        assert result["product_id"] == 789
        assert result["item_price"] == 100
        assert result["quantity"] == 2

        # Verify the API call was made with the correct parameters
        mock_base_client.request.assert_called_once()
        call_args = mock_base_client.request.call_args
        assert call_args[0][0] == "POST"
        assert call_args[0][1] == "/deals/456/products"
        payload = call_args[1]["json_payload"]
        assert payload["product_id"] == 789
        assert payload["item_price"] == 100
        assert payload["quantity"] == 2
        assert payload["tax"] == 5
        assert payload["comments"] == "Test product"
        assert payload["discount"] == 10

    @pytest.mark.asyncio
    async def test_update_product_in_deal_success(self, deal_client, mock_base_client):
        """Test update_product_in_deal with successful API response"""
        # Setup mock response
        mock_base_client.request.return_value = {
            "success": True,
            "data": {
                "id": 123,
                "deal_id": 456,
                "product_id": 789,
                "item_price": 150,
                "quantity": 3,
                "discount": 15,
                "tax": 7.5,
                "comments": "Updated product",
            },
        }

        # Call the method
        result = await deal_client.update_product_in_deal(
            deal_id=456,
            product_attachment_id=123,
            item_price=150,
            quantity=3,
            tax=7.5,
            comments="Updated product",
            discount=15,
        )

        # Verify the result
        assert result["id"] == 123
        assert result["deal_id"] == 456
        assert result["item_price"] == 150
        assert result["quantity"] == 3

        # Verify the API call
        mock_base_client.request.assert_called_once_with(
            "PATCH",
            "/deals/456/products/123",
            json_payload={
                "item_price": 150,
                "quantity": 3,
                "tax": 7.5,
                "comments": "Updated product",
                "discount": 15,
            },
        )

    @pytest.mark.asyncio
    async def test_update_product_in_deal_empty_payload(self, deal_client):
        """Test update_product_in_deal with empty payload raises error"""
        # Call the method with no fields to update and expect exception
        with pytest.raises(ValueError) as exc_info:
            await deal_client.update_product_in_deal(
                deal_id=456, product_attachment_id=123
            )

        # Verify the exception
        assert (
            "At least one field must be provided for updating a product in a deal"
            in str(exc_info.value)
        )

    @pytest.mark.asyncio
    async def test_delete_product_from_deal_success(
        self, deal_client, mock_base_client
    ):
        """Test delete_product_from_deal with successful API response"""
        # Setup mock response
        mock_base_client.request.return_value = {"success": True, "data": {"id": 123}}

        # Call the method
        result = await deal_client.delete_product_from_deal(
            deal_id=456, product_attachment_id=123
        )

        # Verify the result
        assert result["id"] == 123

        # Verify the API call
        mock_base_client.request.assert_called_once_with(
            "DELETE", "/deals/456/products/123"
        )
