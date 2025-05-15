Please remove the Pipedrive MCP tool $ARGUMENTS.

Follow these exact steps, making sure no trace of the tool remains in the codebase:

1. First, identify the tool file location:
   - Extract feature name and tool name from the input
   - Normalize the tool name to match the file naming convention
   - Verify the tool file exists

2. Remove import and registration from feature tool registry:
   - Locate the feature registry file at `pipedrive/api/features/<feature_name>/<feature_name>_tool_registry.py`
   - Remove the import line for the tool
   - Remove the `registry.register_tool("<feature_name>", <tool_function_name>)` line

3. Check for any imports or uses in __init__.py files:
   - Check for references in `pipedrive/api/features/<feature_name>/tools/__init__.py`
   - Check for references in `pipedrive/api/features/<feature_name>/__init__.py`
   - Remove any references found

4. Delete the tool file itself:
   - Remove the file at `pipedrive/api/features/<feature_name>/tools/<tool_name>_tool.py`

5. Remove any tool-specific tests:
   - Delete the test file at `pipedrive/api/features/<feature_name>/tools/tests/test_<tool_name>_tool.py`

6. Check for any references in documentation:
   - Search for tool function name in markdown files
   - Remove or update any documentation references

7. Verify the tool is no longer imported anywhere:
   - Perform a final grep search for the tool function name to ensure all references are removed

8. Report a summary of all changes made to verify complete removal

Remember to be thorough in your search and deletion. The goal is to completely remove the tool without leaving any traces or breaking the codebase.
Validate the removal by running `uv run pytest` and ensure all tests pass.