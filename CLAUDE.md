# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The mcp-concept project is a Model Control Protocol (MCP) server implementation for interacting with the Pipedrive CRM API. It provides a way for Claude to access and manipulate Pipedrive data through tool calls.

## Environment Setup

1. Create a `.env` file in the root directory with the following environment variables:
   ```
   PIPEDRIVE_API_TOKEN=your_api_token
   PIPEDRIVE_COMPANY_DOMAIN=your_company_domain
   HOST=0.0.0.0  # Optional, defaults to 0.0.0.0
   PORT=8152     # Optional, defaults to 8152
   TRANSPORT=stdio  # or "sse", defaults to "stdio"
   ```

## Commands

### Installation

To install the MCP server to Claude desktop:
```bash
cd mcp-concept
mcp install server.py
```

### Running

To run the server locally:
```bash
uv run server.py
```

### Testing

To run tests:
```bash
uv run pytest
```

To run specific tests:
```bash
uv run pytest tests/test_file.py::TestClass::test_function -v
```

### Package Management

This project uses `uv` for package management:

```bash
uv pip install -e .  # Install package in development mode
```

## Project Architecture

### Core Components

1. **MCP Server:** Defined in `server.py`, sets up the main MCP server instance.

2. **Pipedrive Client:** Implemented in `pipedrive/api/pipedrive_client.py`, provides Python bindings for Pipedrive API v2.

3. **MCP Tools:** Located in `pipedrive/tools/`, these are the functions that Claude can call through the MCP protocol to interact with Pipedrive.

4. **Pipedrive Context:** Defined in `pipedrive/api/pipedrive_context.py`, manages the lifecycle of the Pipedrive client within the MCP server.

### Key Features

- **Asynchronous API Client:** The Pipedrive client uses `httpx` for async HTTP requests.
- **Tool Interface:** Provides tools for creating and managing Pipedrive entities (currently persons).
- **Error Handling:** Comprehensive error handling via the `PipedriveAPIError` class.

### Data Flow

1. Claude calls an MCP tool function
2. The function accesses the Pipedrive client via context
3. The client makes an API request to Pipedrive
4. Results are processed and returned to Claude in a standardized JSON format

### Adding New Tools

When creating new tools (e.g., for deals, organizations):
1. Create a new module in `pipedrive/tools/`
2. Define functions with the `@mcp.tool()` decorator
3. Import in `server.py` to register the tool with the MCP server
4. Use the `format_tool_response` utility for consistent response formatting