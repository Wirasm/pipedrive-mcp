Please analyze the Pipedrive MCP project structure to get a comprehensive understanding of the codebase.

First, get an overview of the project structure:

```bash
tree
```

Now, read the following critical files to understand the project:

1. Read the README.md file to understand the project overview and setup instructions
2. Read the pyproject.toml file to understand dependencies and project configuration
3. Read the server.py file to understand the entry point and MCP server setup
4. Read the core client implementation:
   - pipedrive/api/base_client.py
   - pipedrive/api/pipedrive_client.py
   - pipedrive/api/pipedrive_context.py
5. Examine the person feature implementation for reference:
   - pipedrive/api/features/persons/models/person.py
   - pipedrive/api/features/persons/client/person_client.py
   - pipedrive/api/features/persons/tools/person_create_tool.py
6. Look at shared utilities:
   - pipedrive/api/features/shared/utils.py
   - pipedrive/api/features/shared/conversion/id_conversion.py

Use the Task tool to examine any other files that look important based on your initial analysis.

After studying these files, please provide:

1. A short summary of the project structure and architecture
2. The main components and how they interact
3. The data flow from tool invocation to API interaction
4. Key patterns used in the codebase

IMPORTANT: Always respect the vertical slice architecture when working with this code.
IMPORTANT: Use "think hard" when analyzing complex parts of the codebase.
IMPORTANT: Use existing shared utilities rather than creating duplicates.
IMPORTANT: All features should be organized in their own directory with models, clients, and tools.
IMPORTANT: Co-locate tests with the code they test.