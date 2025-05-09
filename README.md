# Pipedrive MCP Server

A Model Control Protocol (MCP) server implementation for interacting with the Pipedrive CRM API. This server enables Claude to create, read, update, and delete Pipedrive records through MCP tool calls.

## Features

- Person management (create, read, update, delete)
- Async API client with comprehensive error handling
- Vertical slice architecture for maintainability
- Comprehensive test coverage

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [mcp CLI](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/mcp-concept) - Claude's Model Control Protocol tools

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
PIPEDRIVE_API_TOKEN=your_api_token
PIPEDRIVE_COMPANY_DOMAIN=your_company_domain
HOST=0.0.0.0
PORT=8152
TRANSPORT=sse
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