I want you to help me create a new feature following our vertical slice architecture.

Feature name: $ARGUMENTS

Please:
1. Analyze existing features to understand our patterns, particularly looking at persons feature
2. Create the folder structure for this feature:
   - client/ with feature-specific client
   - models/ with Pydantic models
   - tools/ with MCP tools
3. Update pipedrive_client.py to initialize and provide access to the new feature client
4. Implement basic CRUD operations for the feature
5. Add comprehensive tests co-located with implementation files
6. Update necessary documentation

IMPORTANT: Follow strict vertical slice architecture - all feature code should be in its own directory.
IMPORTANT: Reuse shared utilities from pipedrive/api/features/shared/ - never duplicate functionality.
IMPORTANT: Ensure all models use Pydantic v2 for validation.
IMPORTANT: All tests should be placed in tests/ directories adjacent to the code they test.