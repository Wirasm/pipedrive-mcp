#!/usr/bin/env -S uv run --script

"""
Feature Claude Run - Script to run Claude for Pipedrive feature implementation

This script:
1. Configures allowed tools for Claude
2. Runs Claude to implement a feature based on a PRP file
3. Supports both interactive and non-interactive modes
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
I need you to implement the feature described in the PRP file: {prp_file}

First:
1. Read and thoroughly understand the PRP file
2. Read the referenced files and ai_docs/pipedrive_deals.md to understand the API and existing patterns
3. MIRROR the directory structure and implementation patterns from the persons feature

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

Let's approach this methodically, exploring the codebase first before implementing anything.
"""

    if interactive:
        # Run interactively - user can interact with Claude
        try:
            print(f"Starting interactive Claude session for {prp_file}...")
            print(f"Working directory: {os.getcwd()}")
            subprocess.run(
                ["claude", "--think-hard"], input=prompt.encode(), check=True
            )
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
            "--think-hard",
            "--allowedTools",
            allowed_tools,
        ]
        try:
            print(f"Running Claude in non-interactive mode for {prp_file}...")
            print(f"Working directory: {os.getcwd()}")
            process = subprocess.run(
                command, check=True, capture_output=True, text=True
            )
            print(process.stdout)
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
        help="Feature name to implement (default: deals)"
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