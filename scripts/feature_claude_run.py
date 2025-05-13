#!/usr/bin/env -S uv run --script

"""
Feature Claude Run - Script to run Claude for Pipedrive feature implementation

This script:
1. Configures allowed tools for Claude
2. Runs Claude to implement a feature based on a PRP file
3. Supports both interactive and non-interactive modes

Usage:
    # Run in interactive mode (recommended for development)
    uv run python scripts/feature_claude_run.py --prp PRPs/deals_init.md --interactive

    # Run in non-interactive (headless) mode
    uv run python scripts/feature_claude_run.py --prp PRPs/deals_init.md

    # Configure allowed tools in project settings (one-time setup)
    uv run python scripts/feature_claude_run.py --configure-tools

    # Configure allowed tools in global settings
    uv run python scripts/feature_claude_run.py --configure-tools --global-config

    # Specify a feature by name (will use PRPs/{feature}_init.md)
    uv run python scripts/feature_claude_run.py --feature organizations --interactive

Examples:
    # Implement the deals feature interactively
    uv run python scripts/feature_claude_run.py --prp PRPs/deals_init.md --interactive

    # Implement the organizations feature in headless mode
    uv run python scripts/feature_claude_run.py --prp PRPs/organizations_init.md

    # Configure tools once, then run using feature name
    uv run python scripts/feature_claude_run.py --configure-tools
    uv run python scripts/feature_claude_run.py --feature deals --interactive

Notes:
    - Interactive mode allows real-time interaction with Claude
    - Non-interactive mode runs Claude and captures output automatically
    - Default feature is 'deals' if not specified
    - Default PRP file is PRPs/{feature}_init.md if not specified
    - Configure tools once before running to avoid permission prompts
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def setup_allowed_tools(project_config=True):
    """Set up allowed tools configuration for Claude"""
    # Define all tools to allow
    allowed_tools = {
        # Tools requiring permissions
        "Bash": {"allowed": True},
        "Edit": {"allowed": True},
        "MultiEdit": {"allowed": True},
        "Write": {"allowed": True},
        "NotebookEdit": {"allowed": True},
        "WebFetch": {"allowed": True},
        # Tools that don't require permissions are included for completeness
        # (though they're already allowed by default)
        "Agent": {"allowed": True},
        "Glob": {"allowed": True},
        "Grep": {"allowed": True},
        "LS": {"allowed": True},
        "Read": {"allowed": True},
        "NotebookRead": {"allowed": True},
        "TodoRead": {"allowed": True},
        "TodoWrite": {"allowed": True},
        "WebSearch": {"allowed": True},
    }

    # Get the project root directory
    project_root = Path(__file__).parent.parent.absolute()

    if project_config:
        # Create/update .claude/settings.json in the project directory
        config_dir = project_root / ".claude"
        config_dir.mkdir(exist_ok=True)
        config_path = config_dir / "settings.json"
    else:
        # Create/update ~/.claude.json for global settings
        config_path = Path.home() / ".claude.json"

    # Read existing settings if they exist
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except json.JSONDecodeError:
            config = {}
    else:
        config = {}

    # Update allowed tools
    if "allowedTools" not in config:
        config["allowedTools"] = {}

    config["allowedTools"].update(allowed_tools)

    # Write updated settings
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Updated allowed tools configuration in {config_path}")


def run_claude_for_feature(prp_file, interactive=False):
    """Run Claude with the specified PRP file"""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.absolute()

    # Change to project root directory
    os.chdir(project_root)

    # Ensure the PRP file path is relative to the project root
    if not prp_file.startswith("PRPs/"):
        prp_file = f"PRPs/{prp_file}"
        if not prp_file.endswith(".md"):
            prp_file = f"{prp_file}.md"

    prp_path = project_root / prp_file

    # Check if PRP file exists
    if not prp_path.exists():
        print(f"Error: PRP file not found at {prp_path}")
        return

    prompt = f"""
Think hard about this task.

I need you to implement the feature described in the PRP file: {prp_file}

First:
1. Read and thoroughly understand the PRP file related to the feature
2. Read the referenced files and payinh special attention to the ai_docs/ directory with files referencing the specific feature to understand the API and existing patterns
3. MIRROR the directory structure and implementation patterns from the existing features in pipedrive/api/features
Then:
4. Create a detailed implementation plan
5. Use subagents where needed to explore complex aspects of the codebase
6. Implement the entire feature following the vertical slice architecture:
   - Models with proper validation
   - Client methods for API interaction
   - MCP tools that use the client
   - Comprehensive tests

Remember to:
- Follow existing code patterns and naming conventions
- Use shared utilities for ID conversion and response formatting
- Test your implementation thoroughly
- Update server.py to register all new tools

** After you have implemented the feature, run the tests to make sure everything works as expected.**
** After the tests pass, stage the changes and write a clear commit message. DO NOT COMMIT to allow the user to review the files.**

Let's approach this methodically, exploring the codebase first before implementing anything.
"""

    if interactive:
        # Run interactively - user can interact with Claude
        try:
            print(f"Starting interactive Claude session for {prp_file}...")
            print(f"Working directory: {os.getcwd()}")
            subprocess.run(["claude"], input=prompt.encode(), check=True)
        except FileNotFoundError:
            print(
                "Error: Claude executable not found. Make sure it's installed and in your PATH."
            )
            return
        except subprocess.CalledProcessError as e:
            print(f"Error running Claude in interactive mode: {e}")
            return
    else:
        # Run non-interactively with allowed tools pre-configured
        # Include all tools that require permissions
        allowed_tools = "Bash,Edit,MultiEdit,Write,NotebookEdit,WebFetch,TodoWrite"
        command = [
            "claude",
            "-p",
            prompt,
            "--allowedTools",
            allowed_tools,
        ]
        try:
            print(f"Running Claude in non-interactive mode for {prp_file}...")
            print(f"Working directory: {os.getcwd()}")
            process = subprocess.run(
                command, check=True, capture_output=True, text=True
            )

            # Check for created files to provide a simple summary
            feature_name = Path(prp_file).stem.split("_")[0]
            feature_dir = project_root / "pipedrive" / "api" / "features" / feature_name
            if feature_dir.exists():
                files_created = list(feature_dir.glob("**/*.py"))
                num_files = len(files_created)
                print(
                    f"\n✅ Success! Created {num_files} Python files in {feature_dir.relative_to(project_root)}"
                )
                print(f"Key files created:")

                # Show key implementation files for context
                for pattern in ["client/*.py", "models/*.py", "tools/*.py"]:
                    for file in feature_dir.glob(pattern):
                        if not file.name.startswith("__") and not file.name.startswith(
                            "test_"
                        ):
                            print(f"  - {file.relative_to(project_root)}")

                # Check if import statements were added to server.py and pipedrive_client.py
                server_updated = False
                client_updated = False

                # Check server.py for imports of the new feature
                server_file = project_root / "server.py"
                if server_file.exists():
                    with open(server_file, "r") as f:
                        server_content = f.read()
                        if f"{feature_name}" in server_content:
                            server_updated = True

                # Check pipedrive_client.py for imports of the new feature
                client_file = project_root / "pipedrive" / "api" / "pipedrive_client.py"
                if client_file.exists():
                    with open(client_file, "r") as f:
                        client_content = f.read()
                        if f"{feature_name}" in client_content:
                            client_updated = True

                if server_updated:
                    print("✅ Updated server.py with new tools")
                if client_updated:
                    print("✅ Updated pipedrive_client.py with new client")

                print(
                    "\nVerify implementation with: uv run pytest pipedrive/api/features/"
                    + feature_name
                )
            else:
                print(
                    "⚠️ Implementation may not be complete. Check Claude's output for details."
                )

            # Don't print raw stdout unless there's an explicit debug flag
        except subprocess.CalledProcessError as e:
            print(f"Claude process failed: {e}")
            if e.stderr:
                print(f"Error output: {e.stderr}")


def main():
    parser = argparse.ArgumentParser(
        description="Run Claude to implement a Pipedrive feature"
    )
    parser.add_argument(
        "feature",
        nargs="?",
        default="deals",
        help="Feature name to implement (default: deals)",
    )
    parser.add_argument(
        "--prp",
        help="Path to the PRP file (default: PRPs/{feature}_init.md)",
    )
    parser.add_argument(
        "--interactive", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument(
        "--configure-tools",
        action="store_true",
        help="Configure allowed tools in project settings",
    )
    parser.add_argument(
        "--global-config",
        action="store_true",
        help="Configure allowed tools in global settings (~/.claude.json)",
    )

    args = parser.parse_args()

    # Configure allowed tools if requested
    if args.configure_tools:
        setup_allowed_tools(not args.global_config)
        print(
            "Tools configuration complete. You can now run Claude without permission prompts."
        )
        print(
            "You can now use /project:implement-pipedrive-feature deals in Claude Code."
        )
        print("Run with --interactive flag to start an interactive session.")
        return

    # Determine PRP file
    prp_file = args.prp if args.prp else f"PRPs/{args.feature}_init.md"

    if not args.configure_tools:
        run_claude_for_feature(prp_file, args.interactive)


if __name__ == "__main__":
    main()
