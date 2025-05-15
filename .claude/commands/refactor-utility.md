I want to refactor a utility function to improve its design or move it to the shared utilities.

Function: $ARGUMENTS

Please:
1. Analyze the current implementation
2. Determine if this should be a shared utility or feature-specific
3. Refactor the function following our established patterns
4. Update all imports and references across the codebase
5. Update tests to reflect the changes
6. Verify everything works by running `uv run pytest`

IMPORTANT: Ensure backward compatibility unless explicitly asked otherwise.
IMPORTANT: Functions used across multiple features should be in shared/ directories.
IMPORTANT: Always maintain or improve test coverage during refactoring.