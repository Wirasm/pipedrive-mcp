# Pipedrive MCP Claude Scripts

This directory contains scripts for using Claude with the Pipedrive MCP project. These scripts help automate and streamline development workflows.

## Available Scripts

### `feature_claude_run.py`

Run Claude to implement a feature based on a PRP file.

```bash
# Basic usage (implements deals feature)
./feature_claude_run.py

# Implement a specific feature
./feature_claude_run.py organizations

# Use a specific PRP file
./feature_claude_run.py --prp PRPs/custom_feature.md

# Run in interactive mode
./feature_claude_run.py --interactive

# Configure allowed tools
./feature_claude_run.py --configure-tools
```

### `agentic_loop.py`

Run a self-validating multi-agent review loop for continuous code improvement.

```bash
# Basic usage
./agentic_loop.py your-branch-name

# With verbose logging
./agentic_loop.py your-branch-name --verbose

# Custom iterations and output directory
./agentic_loop.py your-branch-name --max-iterations 5 --output-dir ./loop_output
```

## Slash Commands

These scripts also provide slash commands for use in Claude Code:

- `/project:implement-pipedrive-feature deals` - Implements the specified feature
- `/project:agentic-review-loop your-branch-name` - Runs the agentic review loop on a branch

## Workflow Examples

### Implementing a New Feature

1. Create a PRP file in the PRPs directory (e.g., `PRPs/organizations_init.md`)
2. Run `./scripts/feature_claude_run.py organizations --interactive`
3. Claude will implement the feature following the vertical slice architecture

### Reviewing and Improving Code

1. Create a branch with your changes: `git checkout -b feature-branch`
2. Make your changes and commit them
3. Run the agentic review loop: `./scripts/agentic_loop.py feature-branch`
4. The loop will review, fix issues, validate, and create a PR when ready