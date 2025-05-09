I need you to fix a failing test in the Pipedrive MCP project.

Test file: $ARGUMENTS

Please:
1. Run the test and analyze what's failing
2. Check for common issues:
   - AsyncMock configuration issues
   - Missing pytest.mark.asyncio decorators
   - Unawaited coroutines
   - JSON serialization problems with mock objects
3. Fix the test without changing the intent of what's being tested
4. Verify the fix by running the test again

IMPORTANT: All tests must be run with `uv run pytest` to ensure correct environment setup.
IMPORTANT: Remember that asyncio_mode is set to "strict" in pytest.ini.