# Pipedrive MCP Server

A Model Control Protocol (MCP) server implementation for interacting with the Pipedrive CRM API. This server enables Claude to create, read, update, and delete Pipedrive records through MCP tool calls.

## Features

This MCP server implements the following Pipedrive features:

- **Persons** - Create, read, update, delete, and search person entities
- **Organizations** - Manage organizations and their followers
- **Deals** - Create, manage, and search deals, including deal products
- **Leads** - Create, manage, and search leads including lead labels
- **Activities** - Track and manage activities and activity types
- **Item Search** - Global and field-specific search across Pipedrive entities

Additional features:

- Async API client with comprehensive error handling
- Feature flags to enable/disable specific modules
- Vertical slice architecture for maintainability
- Comprehensive test coverage

## Quick Start with Claude Code

The fastest way to get started with the Pipedrive MCP Server and set it up in your claude desktop app:

### 1. Install Required Tools

Open your terminal or command prompt and run these commands:

```bash
# Install Python's uv package manager (if not already installed)
curl -sSf https://install.python-uv.org/uv | python3 -
```

For more detailed installation instructions for uv, visit: [Astral's UV Installation Documentation](https://github.com/astral-sh/uv/blob/main/README.md#installation)

### 2. Download the Code

**No GitHub account required!** Just run these commands in your terminal:

Select a folder where you want the code to be downloaded to and run these commands:

```bash
# Clone the repository (download the code)
git clone https://github.com/Wirasm/pipedrive-mcp.git

# Move into the project folder
cd pipedrive-mcp
```

### 3. Install Python Dependencies

Open your terminal and run this command exactly as written:

```bash
# Install all required packages
uv sync
```

### 4. Set Up Your Pipedrive Credentials

1. Find the `.env.example` file in the project folder
2. Make a copy and rename it to just `.env`
3. Open the `.env` file in any text editor
4. Replace the placeholders with your actual Pipedrive information:

```
PIPEDRIVE_API_TOKEN=your_api_token
PIPEDRIVE_COMPANY_DOMAIN=your_company_domain
```

All other configurations you see in the .env file are optional and can be left as is.

**To get your Pipedrive API Token:**
1. Log in to your Pipedrive account
2. Click on your profile picture in the top-right corner
3. Select "Personal preferences"
4. Go to the "API" tab
5. Click "Generate new token" if you don't already have one
6. Copy the generated token and paste it in the `.env` file

**For the company domain:**
If your Pipedrive URL is `https://mycompany.pipedrive.com/pipeline`, then your domain is `mycompany`

### 5. Install the MCP Server in Claude Desktop

Open your terminal and run this command:

```bash
# Install the MCP server
mcp install server.py
```

This will automatically register the Pipedrive tools with Claude Desktop. 

### 6. Start Using Pipedrive with Claude

1. **Important:** Restart Claude Desktop app if it was already running
2. Open Claude Desktop
3. Start a new chat, and Claude can now interact with your Pipedrive CRM!

Try asking Claude to "Show me my recent deals" or "Create a new contact here are the details: ..." to get started.

## Available MCP Tools

### Person Tools
| Tool Name | Description |
| --- | --- |
| `create_person_in_pipedrive` | Creates a new person in Pipedrive CRM |
| `get_person_from_pipedrive` | Retrieves details of a specific person by ID |
| `update_person_in_pipedrive` | Updates an existing person in Pipedrive |
| `delete_person_from_pipedrive` | Deletes a person from Pipedrive |
| `search_persons_in_pipedrive` | Searches for persons by name, email, phone, etc. |

### Organization Tools
| Tool Name | Description |
| --- | --- |
| `create_organization_in_pipedrive` | Creates a new organization in Pipedrive |
| `get_organization_from_pipedrive` | Retrieves organization details by ID |
| `update_organization_in_pipedrive` | Updates an existing organization |
| `delete_organization_from_pipedrive` | Deletes an organization |
| `list_organizations_in_pipedrive` | Lists organizations with filtering and pagination |
| `search_organizations_in_pipedrive` | Searches for organizations by name or other criteria |
| `add_follower_to_organization` | Adds a user as a follower of an organization |
| `delete_follower_from_organization` | Removes a follower from an organization |

### Deal Tools
| Tool Name | Description |
| --- | --- |
| `create_deal_in_pipedrive` | Creates a new deal |
| `get_deal_from_pipedrive` | Retrieves deal details by ID |
| `update_deal_in_pipedrive` | Updates an existing deal |
| `delete_deal_from_pipedrive` | Deletes a deal |
| `list_deals_in_pipedrive` | Lists deals with filtering and pagination |
| `search_deals_in_pipedrive` | Searches for deals by title or other criteria |
| `add_product_to_deal` | Adds a product to a deal |
| `update_deal_product` | Updates a product associated with a deal |
| `delete_product_from_deal` | Removes a product from a deal |

### Lead Tools
| Tool Name | Description |
| --- | --- |
| `create_lead_in_pipedrive` | Creates a new lead |
| `get_lead_from_pipedrive` | Retrieves lead details by ID |
| `update_lead_in_pipedrive` | Updates an existing lead |
| `delete_lead_from_pipedrive` | Deletes a lead |
| `list_leads_in_pipedrive` | Lists leads with filtering and pagination |
| `search_leads_in_pipedrive` | Searches for leads by title or other criteria |
| `get_lead_labels` | Retrieves available lead labels |
| `get_lead_sources` | Retrieves available lead sources |

### Item Search Tools
| Tool Name | Description |
| --- | --- |
| `search_items_in_pipedrive` | Global search across multiple item types |
| `search_field_in_pipedrive` | Searches for specific field values in a given entity type |

## Feature Modules

The project follows a vertical slice architecture with each feature having its own directory:

- **persons/** - Person entity management
- **organizations/** - Organization entity management
- **deals/** - Deal management including products
- **leads/** - Lead management including labels
- **activities/** - Activity tracking and management
- **item_search/** - Cross-entity search functionality
- **shared/** - Common utilities used across features

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

# Feature Flags (optional)
PIPEDRIVE_FEATURE_PERSONS=true
PIPEDRIVE_FEATURE_DEALS=true
PIPEDRIVE_FEATURE_ORGANIZATIONS=true
PIPEDRIVE_FEATURE_LEADS=true
PIPEDRIVE_FEATURE_ITEM_SEARCH=true
PIPEDRIVE_FEATURE_ACTIVITIES=true
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

## Project Structure

The project follows a vertical slice architecture where code is organized by features rather than by technical layers:

```
pipedrive/
├── api/
│   ├── base_client.py                   # Core HTTP client
│   ├── pipedrive_api_error.py           # API error handling
│   ├── pipedrive_client.py              # Main client facade
│   ├── pipedrive_context.py             # Client lifecycle management
│   ├── features/
│   │   ├── tool_registry.py             # Feature registry system
│   │   ├── tool_decorator.py            # Feature-aware tool decorator
│   │   ├── persons/                     # Person feature module
│   │   │   ├── client/                  # Person API client
│   │   │   ├── models/                  # Person domain models
│   │   │   └── tools/                   # Person MCP tools
│   │   ├── organizations/               # Organization feature module
│   │   ├── deals/                       # Deal feature module
│   │   ├── leads/                       # Lead feature module
│   │   ├── activities/                  # Activity feature module
│   │   ├── item_search/                 # Search feature module
│   │   └── shared/                      # Shared utilities
├── feature_config.py                    # Feature configuration management
└── mcp_instance.py                      # MCP server configuration
```

## Development

For detailed development information, see [CLAUDE.md](CLAUDE.md).

## License

MIT