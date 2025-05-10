# Pipedrive MCP Server

A Model Control Protocol (MCP) server implementation for interacting with the Pipedrive CRM API. This server enables Claude to create, read, update, and delete Pipedrive records through MCP tool calls.

## Features

- Person management (create, read, update, delete, search)
- Async API client with comprehensive error handling
- Vertical slice architecture for maintainability
- Comprehensive test coverage

## Available MCP Tools

| Tool Name | Description |
| --- | --- |
| `create_person_in_pipedrive` | Creates a new person in Pipedrive CRM |
| `get_person_from_pipedrive` | Retrieves details of a specific person by ID |
| `update_person_in_pipedrive` | Updates an existing person in Pipedrive |
| `delete_person_from_pipedrive` | Deletes a person from Pipedrive |
| `search_persons_in_pipedrive` | Searches for persons by name, email, phone, etc. |

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [mcp CLI](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/mcp-concept) - Claude's Model Control Protocol tools
- [Docker](https://www.docker.com/) (optional) - For containerized deployment

### Security Notes

This MCP server implements several security measures:

- Default binding to localhost (127.0.0.1) when running locally
- Proper error handling and logging

When deploying:
- For local development, keep the default host (127.0.0.1)
- For container deployment, set `CONTAINER_MODE=true`

### Clone the Repository

```bash
git clone git@github.com:Wirasm/pipedrive-mcp.git
cd pipedrive-mcp
```

### Setup Environment

1. Create a virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# OR
.venv\Scripts\activate     # On Windows
uv pip install -e .
```

2. Create a `.env` file in the root directory:

```
# API Credentials
PIPEDRIVE_API_TOKEN=your_api_token
PIPEDRIVE_COMPANY_DOMAIN=your_company_domain  # Just the subdomain portion (e.g., "mycompany" from mycompany.pipedrive.com)

# Server Configuration
HOST=127.0.0.1  # Use 127.0.0.1 for local development, 0.0.0.0 only in containers
PORT=8152
TRANSPORT=sse   # "sse" or "stdio"

# Security Settings
CONTAINER_MODE=false
VERIFY_SSL=true  # Set to "false" if you encounter SSL certificate issues (development only)
```

### Run Tests

```bash
uv run pytest
```

### Install to Claude Desktop

```bash
mcp install server.py
```

### Run Locally

```bash
uv run server.py
```

### Using Docker

1. Build the Docker image:

```bash
docker build -t pipedrive-mcp .
```

2. Run the container with environment variables:

```bash
# IMPORTANT: Replace values in quotes with your real Pipedrive credentials
docker run -d -p 8152:8152 \
  -e PIPEDRIVE_API_TOKEN="your-actual-pipedrive-api-token" \
  -e PIPEDRIVE_COMPANY_DOMAIN="your-company-subdomain" \
  -e PORT=8152 \
  -e TRANSPORT=sse \
  -e CONTAINER_MODE=true \
  -e VERIFY_SSL=true \
  --name pipedrive-mcp-server \
  pipedrive-mcp
```

For example, if your Pipedrive domain is `mycompany.pipedrive.com`, you would use:
```
-e PIPEDRIVE_COMPANY_DOMAIN="mycompany"
```

3. Check the container is running and view logs:

```bash
# Check container status
docker ps | grep pipedrive-mcp-server

# View logs
docker logs pipedrive-mcp-server
```

4. Stop and remove the container when done:

```bash
docker stop pipedrive-mcp-server
docker rm pipedrive-mcp-server
```

5. Configure Claude to use the MCP server:

To use this server with Claude Desktop, register the MCP server in Claude desktop settings:
- Server Name: Pipedrive MCP
- Endpoint URL: http://localhost:8152
- Auth: None

If you experience SSL certificate errors, you can disable SSL verification (only for development environments):
```bash
docker run -d -p 8152:8152 \
  -e PIPEDRIVE_API_TOKEN="your-actual-pipedrive-api-token" \
  -e PIPEDRIVE_COMPANY_DOMAIN="your-company-subdomain" \
  -e PORT=8152 \
  -e TRANSPORT=sse \
  -e CONTAINER_MODE=true \
  -e VERIFY_SSL=false \
  --name pipedrive-mcp-server \
  pipedrive-mcp
```

## Project Structure

The project follows a vertical slice architecture where code is organized by features rather than by technical layers:

```
pipedrive/
├── api/
│   ├── base_client.py                   # Core HTTP client
│   ├── features/
│   │   ├── persons/                     # Person feature module
│   │   │   ├── client/                  # Person API client
│   │   │   ├── models/                  # Person domain models
│   │   │   └── tools/                   # Person MCP tools
│   │   └── shared/                      # Shared utilities
│   └── pipedrive_client.py              # Main client facade
└── mcp_instance.py                      # MCP server configuration
```

## Development

For detailed development information, see [CLAUDE.md](CLAUDE.md).

## License

MIT