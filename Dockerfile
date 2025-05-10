FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ARG PORT=8152

WORKDIR /app

# Copy the entire application first
COPY . .

# Create a virtual environment and install dependencies
RUN uv venv .venv && \
    . .venv/bin/activate && \
    uv pip install -e .

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV CONTAINER_MODE="true"

EXPOSE ${PORT}

# Command to run the MCP server
CMD ["uv", "run", "server.py"]