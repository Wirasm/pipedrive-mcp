# Implement Pipedrive Feature

Please implement the $ARGUMENTS feature for the Pipedrive MCP server following these steps:

1. Read and analyze the PRP file in the PRPs/ directory that matches the feature name (e.g., PRPs/deals_init.md)
2. Read the corresponding API documentation in ai_docs/ directory (e.g., ai_docs/pipedrive_deals.md)
3. MIRROR the structure of existing features (especially persons/) and adapt for this feature
4. Follow the vertical slice architecture pattern:
   - Create models with Pydanticv2 validation
   - Implement client methods for API interaction
   - Build MCP tools for Claude to use
   - Write comprehensive tests

Throughout the implementation:
- Use subagents to explore complex parts of the codebase
- Use existing shared utilities (ID conversion, response formatting)
- Follow naming conventions from existing features
- Create tests for all components
- Update server.py to register new tools

Validation:
- always confirm with the user which feature is being implemented and which prp and ai_docs file to read before you start
- always run `uv run pytest` ensuring all tests pass before you finish

When done, provide a summary of what was implemented and instructions for testing.