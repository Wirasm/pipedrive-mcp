from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pipedrive.api.features.tool_decorator import tool, validate_docstring


# Helper functions for testing
def create_mock_func(docstring=None):
    """Create a mock function with the given docstring."""

    async def mock_func(ctx, param1, param2=None):
        return "result"

    if docstring:
        mock_func.__doc__ = docstring

    return mock_func


class TestValidateDocstring:
    def test_no_docstring(self):
        """Test validating a function with no docstring."""
        func = create_mock_func()
        warnings = validate_docstring(func, "test_feature")

        assert len(warnings) > 0
        assert "has no docstring" in warnings[0]

    def test_minimal_docstring(self):
        """Test validating a function with minimal docstring."""
        func = create_mock_func("Short description.")
        warnings = validate_docstring(func, "test_feature")

        assert len(warnings) > 0
        assert any("Format requirements" in warning for warning in warnings)
        assert any("Example" in warning for warning in warnings)
        assert any("Args" in warning for warning in warnings)
        assert any("Returns" in warning for warning in warnings)

    def test_complete_docstring(self):
        """Test validating a function with complete docstring."""
        complete_docstring = """One-line summary of what the tool does.

        Detailed description explaining the tool's purpose.

        Format requirements:
        - param1: Must be a string

        Example:
        ```
        test_func(param1="value")
        ```

        Args:
            ctx: Context object
            param1: First parameter
            param2: Second parameter

        Returns:
            JSON formatted response
        """

        func = create_mock_func(complete_docstring)
        warnings = validate_docstring(func, "test_feature")

        assert len(warnings) == 0

    def test_missing_param_documentation(self):
        """Test validating a function with missing parameter documentation."""
        docstring = """One-line summary of what the tool does.

        Detailed description explaining the tool's purpose.

        Format requirements:
        - param1: Must be a string

        Example:
        ```
        test_func(param1="value")
        ```

        Args:
            ctx: Context object
            param1: First parameter

        Returns:
            JSON formatted response
        """

        func = create_mock_func(docstring)
        warnings = validate_docstring(func, "test_feature")

        assert len(warnings) > 0
        assert any("param2" in warning for warning in warnings)


@pytest.mark.asyncio
@patch("pipedrive.api.features.tool_decorator.registry")
@patch("pipedrive.api.features.tool_decorator.mcp")
async def test_tool_decorator_enabled_feature(mock_mcp, mock_registry):
    """Test tool decorator with enabled feature."""
    # Setup mocks
    mock_registry.is_feature_enabled.return_value = True
    mock_mcp.tool.return_value = lambda func: func

    # Create a decorated function
    @tool("test_feature", validate=False)
    async def test_func(ctx):
        return "success"

    # Create a mock context
    ctx = MagicMock()

    # Call the function
    result = await test_func(ctx)

    # Verify the result
    assert result == "success"
    mock_registry.is_feature_enabled.assert_called_with("test_feature")


@pytest.mark.asyncio
@patch("pipedrive.api.features.tool_decorator.registry")
@patch("pipedrive.api.features.tool_decorator.mcp")
@patch("pipedrive.api.features.tool_decorator.logger")
async def test_tool_decorator_disabled_feature(mock_logger, mock_mcp, mock_registry):
    """Test tool decorator with disabled feature."""
    # Setup mocks
    mock_registry.is_feature_enabled.return_value = False
    mock_mcp.tool.return_value = lambda func: func

    # Create a decorated function
    @tool("test_feature", validate=False)
    async def test_func(ctx):
        return "success"

    # Create a mock context
    ctx = MagicMock()

    # Call the function
    result = await test_func(ctx)

    # Verify the result
    assert "feature is disabled" in result
    mock_registry.is_feature_enabled.assert_called_with("test_feature")
    mock_logger.warning.assert_called()


@pytest.mark.asyncio
@patch("pipedrive.api.features.tool_decorator.validate_docstring")
@patch("pipedrive.api.features.tool_decorator.registry")
@patch("pipedrive.api.features.tool_decorator.mcp")
@patch("pipedrive.api.features.tool_decorator.logger")
async def test_tool_decorator_with_validation(
    mock_logger, mock_mcp, mock_registry, mock_validate
):
    """Test tool decorator with docstring validation."""
    # Setup mocks
    mock_registry.is_feature_enabled.return_value = True
    mock_mcp.tool.return_value = lambda func: func
    mock_validate.return_value = ["Warning 1", "Warning 2"]

    # Create a decorated function
    @tool("test_feature", validate=True)
    async def test_func(ctx):
        return "success"

    # Create a mock context
    ctx = MagicMock()

    # Call the function
    result = await test_func(ctx)

    # Verify the result
    assert result == "success"
    assert mock_validate.called  # Just check if it was called, not with which exact function
    assert mock_logger.warning.call_count == 2
