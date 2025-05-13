# Project Templates

This document provides templates for common components in the Pipedrive MCP project.

## Model Template

Use this template when creating new Pydantic models:

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator

class FeatureModel(BaseModel):
    """
    Model representing a [feature description].
    
    This model handles validation and conversion between API and domain representations.
    """
    id: Optional[int] = None
    name: str
    # Add other fields here
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API-compatible dictionary"""
        # Start with the model dict excluding None values
        result = {k: v for k, v in self.model_dump().items() 
                  if v is not None and k != "id"}
        
        # Handle nested objects if needed
        # if self.nested_objects:
        #     result["nested_objects"] = [obj.to_dict() for obj in self.nested_objects]
        
        return result
    
    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> 'FeatureModel':
        """Create model from API response dictionary"""
        # Extract basic fields
        model_data = {
            "id": data.get("id"),
            "name": data.get("name", ""),
            # Map other fields here
        }
        
        # Process nested objects if needed
        # nested_objects = []
        # if "nested_objects" in data and data["nested_objects"]:
        #     for nested_data in data["nested_objects"]:
        #         nested_objects.append(NestedModel(
        #             id=nested_data.get("id"),
        #             # Add other nested fields
        #         ))
        # model_data["nested_objects"] = nested_objects
        
        return cls(**model_data)
    
    @model_validator(mode='after')
    def validate_model(self) -> 'FeatureModel':
        """Validate model fields"""
        # Add custom validation logic here
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        return self
```

## Client Template

Use this template when creating new feature clients:

```python
import json
from typing import Any, Dict, List, Optional, Tuple

from log_config import logger
from pipedrive.api.base_client import BaseClient

class FeatureClient:
    """Client for [Feature] API endpoints"""
    
    def __init__(self, base_client: BaseClient):
        """
        Initialize the Feature client
        
        Args:
            base_client: BaseClient instance for making API requests
        """
        self.base_client = base_client
    
    async def create_feature(
        self,
        feature_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create a new feature in Pipedrive
        
        Args:
            feature_data: Data for the new feature
            
        Returns:
            Created feature data
        """
        logger.info(f"FeatureClient: Attempting to create feature")
        
        response_data = await self.base_client.request(
            "POST", 
            "/features", 
            json_payload=feature_data
        )
        return response_data.get("data", {})
    
    async def get_feature(
        self,
        feature_id: int,
        include_fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Get a feature by ID
        
        Args:
            feature_id: ID of the feature to retrieve
            include_fields: Additional fields to include
            
        Returns:
            Feature data
        """
        logger.info(f"FeatureClient: Attempting to get feature with ID {feature_id}")
        
        query_params: Dict[str, Any] = {}
        if include_fields:
            query_params["include_fields"] = ",".join(include_fields)

        response_data = await self.base_client.request(
            "GET",
            f"/features/{feature_id}",
            query_params=query_params if query_params else None,
        )
        return response_data.get("data", {})
    
    async def update_feature(
        self,
        feature_id: int,
        update_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Update an existing feature
        
        Args:
            feature_id: ID of the feature to update
            update_data: Data to update
            
        Returns:
            Updated feature data
        """
        logger.info(f"FeatureClient: Attempting to update feature with ID {feature_id}")
        
        if not update_data:
            raise ValueError("At least one field must be provided for updating a feature")

        response_data = await self.base_client.request(
            "PATCH", 
            f"/features/{feature_id}", 
            json_payload=update_data
        )
        return response_data.get("data", {})
    
    async def delete_feature(self, feature_id: int) -> Dict[str, Any]:
        """
        Delete a feature
        
        Args:
            feature_id: ID of the feature to delete
            
        Returns:
            Deletion result
        """
        logger.info(f"FeatureClient: Attempting to delete feature with ID {feature_id}")
        
        response_data = await self.base_client.request(
            "DELETE", 
            f"/features/{feature_id}"
        )
        
        return (
            response_data.get("data", {})
            if response_data.get("success")
            else {"id": feature_id, "error_details": response_data}
        )
    
    async def list_features(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        # Add other filter parameters
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """
        List features with pagination
        
        Args:
            limit: Maximum number of results
            cursor: Pagination cursor
            
        Returns:
            Tuple of (list of features, next cursor)
        """
        logger.info(f"FeatureClient: Attempting to list features")
        
        query_params: Dict[str, Any] = {
            "limit": limit,
            "cursor": cursor,
            # Add other parameters
        }

        # Filter out None values
        final_query_params = {k: v for k, v in query_params.items() if v is not None}

        response_data = await self.base_client.request(
            "GET",
            "/features",
            query_params=final_query_params if final_query_params else None,
        )

        features_list = response_data.get("data", [])
        additional_data = response_data.get("additional_data", {})
        next_cursor = (
            additional_data.get("next_cursor")
            if isinstance(additional_data, dict)
            else None
        )
        
        return features_list, next_cursor
```

## Tool Template

Use this template when creating new MCP tools:

```python
from typing import Optional

from mcp.server.fastmcp import Context
from pydantic import ValidationError

from log_config import logger
from pipedrive.api.features.shared.utils import format_tool_response
from pipedrive.api.features.shared.conversion.id_conversion import convert_id_string
from pipedrive.api.features.feature.models.feature_model import FeatureModel
from pipedrive.api.pipedrive_api_error import PipedriveAPIError
from pipedrive.api.pipedrive_context import PipedriveMCPContext
from pipedrive.api.features.tool_decorator import tool


@tool("feature_name")
async def create_feature_in_pipedrive(
    ctx: Context,
    name: str,
    id_str: Optional[str] = None,
    # Add other parameters
) -> str:
    """
    Creates a new feature entity within the Pipedrive CRM.
    
    This tool requires the feature's name and can optionally take other details.
    It returns the details of the created feature upon success.
    
    args:
    ctx: Context
    name: str - Name of the feature
    id_str: Optional[str] - ID as a string (will be converted to int)
    """
    logger.debug(f"Tool 'create_feature_in_pipedrive' ENTERED with name='{name}'")

    pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context

    # Convert string IDs to integers
    id_value, error = convert_id_string(id_str, "id")
    if error:
        logger.error(error)
        return format_tool_response(False, error_message=error)
    
    try:
        # Create model instance with validation
        feature = FeatureModel(
            name=name,
            id=id_value,
            # Add other fields
        )
        
        # Convert model to API-compatible dict
        payload = feature.to_api_dict()
        
        logger.debug(f"Prepared payload for feature creation: {payload}")
        
        # Call the Pipedrive API
        created_feature = await pd_mcp_ctx.pipedrive_client.features.create_feature(payload)
        
        logger.info(f"Successfully created feature '{name}' with ID: {created_feature.get('id')}")
        
        # Return the API response
        return format_tool_response(True, data=created_feature)
        
    except ValidationError as e:
        logger.error(f"Validation error creating feature '{name}': {str(e)}")
        return format_tool_response(False, error_message=f"Validation error: {str(e)}")
    except PipedriveAPIError as e:
        logger.error(f"PipedriveAPIError in tool 'create_feature_in_pipedrive': {str(e)}")
        return format_tool_response(False, error_message=str(e), data=e.response_data)
    except Exception as e:
        logger.exception(f"Unexpected error in tool 'create_feature_in_pipedrive': {str(e)}")
        return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")
```

## Feature Registry Template

Use this template when creating feature registry files:

```python
from pipedrive.api.features.tool_registry import registry, FeatureMetadata

# Register the feature
registry.register_feature(
    "feature_name",
    FeatureMetadata(
        name="Feature Name",
        description="Description of the feature",
        version="1.0.0",
        dependencies=[],  # Optional dependencies on other features
    )
)

# Import and register tools
from .tools.feature_tool1 import feature_tool1
from .tools.feature_tool2 import feature_tool2
from .tools.feature_tool3 import feature_tool3

# Register all tools for this feature
registry.register_tool("feature_name", feature_tool1)
registry.register_tool("feature_name", feature_tool2)
registry.register_tool("feature_name", feature_tool3)
```

## Test Templates

### Model Test Template

```python
import pytest
from pydantic import ValidationError

from pipedrive.api.features.feature.models.feature_model import FeatureModel


class TestFeatureModel:
    def test_create_valid_model(self):
        """Test creating a valid model"""
        model = FeatureModel(name="Test Feature")
        assert model.name == "Test Feature"
        # Assert other fields
    
    def test_validation_error(self):
        """Test validation errors"""
        with pytest.raises(ValidationError):
            FeatureModel(name="")  # Empty name should fail validation
    
    def test_to_api_dict(self):
        """Test conversion to API dictionary"""
        model = FeatureModel(
            name="Test Feature",
            # Add other fields
        )
        
        api_dict = model.to_api_dict()
        
        assert api_dict["name"] == "Test Feature"
        # Assert other fields
        assert "id" not in api_dict  # id should not be included
    
    def test_from_api_dict(self):
        """Test creating model from API response"""
        api_data = {
            "id": 123,
            "name": "API Feature",
            # Add other fields
        }
        
        model = FeatureModel.from_api_dict(api_data)
        
        assert model.id == 123
        assert model.name == "API Feature"
        # Assert other fields
```

### Client Test Template

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

from pipedrive.api.base_client import BaseClient
from pipedrive.api.features.feature.client.feature_client import FeatureClient


@pytest.fixture
def mock_base_client():
    """Create a mock BaseClient"""
    client = AsyncMock(spec=BaseClient)
    
    # Mock successful response
    client.request.return_value = {
        "success": True,
        "data": {
            "id": 123,
            "name": "Test Feature"
        }
    }
    
    return client


class TestFeatureClient:
    def test_init(self, mock_base_client):
        """Test initializing client"""
        client = FeatureClient(mock_base_client)
        assert client.base_client == mock_base_client
    
    @pytest.mark.asyncio
    async def test_create_feature(self, mock_base_client):
        """Test creating a feature"""
        client = FeatureClient(mock_base_client)
        
        # Call the method
        result = await client.create_feature({"name": "Test Feature"})
        
        # Check result
        assert result["id"] == 123
        assert result["name"] == "Test Feature"
        
        # Check that base_client.request was called with correct parameters
        mock_base_client.request.assert_called_once()
        call_args = mock_base_client.request.call_args
        assert call_args[0][0] == "POST"  # Method
        assert call_args[0][1] == "/features"  # Endpoint
        assert call_args[1]["json_payload"]["name"] == "Test Feature"
    
    # Add tests for other methods
```

### Tool Test Template

```python
import json
import pytest
from unittest.mock import AsyncMock, MagicMock

from mcp.server.fastmcp import Context
from pipedrive.api.features.feature.tools.feature_tool import create_feature_in_pipedrive
from pipedrive.api.pipedrive_api_error import PipedriveAPIError


@pytest.fixture
def mock_pipedrive_client():
    """Create a mock PipedriveClient"""
    # Create mock feature client
    feature_client = AsyncMock()
    feature_client.create_feature.return_value = {
        "id": 123,
        "name": "Test Feature"
    }
    
    # Create main client with feature property
    client = MagicMock()
    client.features = feature_client
    
    return client


class TestCreateFeatureTool:
    @pytest.mark.asyncio
    async def test_create_feature_success(self, mock_pipedrive_client):
        """Test successful feature creation"""
        # Mock the context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool
        result = await create_feature_in_pipedrive(
            ctx=mock_ctx,
            name="Test Feature"
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify success
        assert result_data["success"] is True
        assert "data" in result_data
        assert result_data["data"]["id"] == 123
        assert result_data["data"]["name"] == "Test Feature"
        
        # Verify the client was called correctly
        mock_pipedrive_client.features.create_feature.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_feature_validation_error(self, mock_pipedrive_client):
        """Test handling of validation errors"""
        # Mock the context
        mock_ctx = MagicMock(spec=Context)
        mock_ctx.request_context.lifespan_context.pipedrive_client = mock_pipedrive_client
        
        # Call the tool with invalid data
        result = await create_feature_in_pipedrive(
            ctx=mock_ctx,
            name=""  # Empty name should fail validation
        )
        
        # Parse the JSON result
        result_data = json.loads(result)
        
        # Verify error response
        assert result_data["success"] is False
        assert "error" in result_data
        assert "Validation error" in result_data["error"]
        
        # Verify the client was not called
        mock_pipedrive_client.features.create_feature.assert_not_called()
    
    # Add more test cases
```