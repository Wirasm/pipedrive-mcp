#!/usr/bin/env -S uv run --script

"""
Agentic Loop System for Pipedrive MCP Development

This script orchestrates a self-validating development loop using multiple Claude instances:
1. Reviewer: Analyzes code/PRs and creates detailed reports
2. Developer: Implements fixes based on review reports
3. Validator: Validates fixes and either approves or returns to Reviewer
4. PR Manager: Creates or updates PRs with approved changes

The system operates as a continuous loop until validation passes or max iterations reached.

Usage:
    uv run python scripts/agentic_loop.py <branch> [options]
    uv run python scripts/agentic_loop.py main --new-branch test-feature --task "Update README"

Options:
    --new-branch NAME    Create a new branch derived from the source branch
    --task DESCRIPTION   Description of the task (used for documentation)
    --output-dir DIR     Directory for output artifacts
    --max-iterations N   Maximum number of improvement iterations (default: 3)
    --verbose            Enable verbose logging
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import shutil
import uuid
from enum import Enum

class Stage(Enum):
    REVIEW = "review"
    DEVELOP = "develop"
    VALIDATE = "validate"
    PR = "pr"

class Role(Enum):
    REVIEWER = "reviewer"
    DEVELOPER = "developer"
    VALIDATOR = "validator"
    PR_MANAGER = "pr_manager"

class AgenticLoop:
    def __init__(self, branch_name, output_dir=None, max_iterations=3, verbose=False, new_branch=None):
        self.source_branch_name = branch_name
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.iteration = 0
        self.current_stage = Stage.REVIEW

        # Create a new derived branch for safety if requested
        if new_branch:
            self.branch_name = new_branch
            self._create_derived_branch()
        else:
            self.branch_name = branch_name

        # Create output directory for artifacts
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path("agentic_loop_output") / self.branch_name / f"{int(time.time())}"

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Set up paths for artifacts
        self.review_file = self.output_dir / "review.md"
        self.development_plan_file = self.output_dir / "development_plan.md"
        self.validation_file = self.output_dir / "validation.md"
        self.pr_file = self.output_dir / "pr.md"

        # Set up temporary directories for each Claude instance
        self.instance_dirs = {
            Role.REVIEWER: self.output_dir / "reviewer_workspace",
            Role.DEVELOPER: self.output_dir / "developer_workspace",
            Role.VALIDATOR: self.output_dir / "validator_workspace",
            Role.PR_MANAGER: self.output_dir / "pr_workspace"
        }

        for dir_path in self.instance_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

        # Set up git configurations
        self._setup_git_worktrees()

        self.log("Initialized AgenticLoop for branch:", self.branch_name)
        self.log("Output directory:", self.output_dir)

    def _create_derived_branch(self):
        """Create a new branch derived from the source branch"""
        try:
            # Check if branch already exists
            result = subprocess.run(
                ["git", "show-ref", "--verify", f"refs/heads/{self.branch_name}"],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )

            if result.returncode == 0:
                self.log(f"Branch {self.branch_name} already exists. Please choose a different branch name.")
                sys.exit(1)

            # Create the new branch
            self.log(f"Creating new branch {self.branch_name} from {self.source_branch_name}")
            subprocess.run(
                ["git", "branch", self.branch_name, self.source_branch_name],
                check=True
            )
        except subprocess.CalledProcessError as e:
            self.log(f"Error creating derived branch: {e}")
            sys.exit(1)

    def log(self, *args, **kwargs):
        """Log messages if verbose mode is enabled"""
        if self.verbose:
            print("[AgenticLoop]", *args, **kwargs)

    def _setup_git_worktrees(self):
        """Set up git worktrees for each Claude instance"""
        # Get repo root
        repo_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        
        for role, dir_path in self.instance_dirs.items():
            # Clean up any existing worktree
            if (dir_path / ".git").exists():
                subprocess.run(["git", "worktree", "remove", str(dir_path)], 
                              stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            
            # Create new worktree for the branch
            role_branch = f"{self.branch_name}-{role.value}"
            
            # Check if branch exists
            branch_exists = subprocess.run(
                ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{role_branch}"],
                stderr=subprocess.DEVNULL
            ).returncode == 0
            
            if not branch_exists:
                # Create branch if it doesn't exist
                subprocess.run(["git", "branch", role_branch, self.branch_name])
            
            # Create worktree
            subprocess.run(["git", "worktree", "add", str(dir_path), role_branch])
            
            self.log(f"Created worktree for {role.value} at {dir_path}")

    def _run_claude_with_prompt(self, role, prompt, think_level="think hard", output_format="text"):
        """Run Claude with a specific prompt in a specific worktree"""
        os.chdir(self.instance_dirs[role])

        # Configure Claude command
        # Note: Extended thinking is triggered by text in the prompt, not by a command line flag
        # We'll add the think_level text to the beginning of the prompt
        enhanced_prompt = f"{think_level}. {prompt}"

        cmd = [
            "claude",
            "-p",
            enhanced_prompt,
            "--allowedTools",
            "Bash,Edit,MultiEdit,Write,NotebookEdit,WebFetch,TodoWrite"
        ]

        if output_format:
            cmd.extend(["--output-format", output_format])

        self.log(f"Running Claude as {role.value}...")
        
        # Run Claude and capture output
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                check=True
            )
            output = result.stdout
            
            self.log(f"Claude {role.value} completed successfully")
            return output
        except subprocess.CalledProcessError as e:
            self.log(f"Error running Claude as {role.value}: {e}")
            self.log(f"stderr: {e.stderr}")
            return None

    def _run_reviewer(self):
        """Run the reviewer Claude instance to analyze code and generate a review"""
        self.log("Starting reviewer phase...")

        # Create reviewer prompt
        reviewer_prompt = f"""
Think hard about this task.

You are a senior code reviewer examining the changes in branch '{self.branch_name}'.
Your task is to provide a thorough, critical review focused on:

1. Consistency with vertical slice architecture patterns
2. API error handling completeness
3. Input/output validation in models
4. Proper use of shared utilities (ID conversion, response formatting)
5. Security issues
6. Performance concerns
7. Test coverage and quality

For each issue found:
1. Mark as CRITICAL, HIGH, MEDIUM, or LOW priority
2. Provide the file path and line number
3. Explain the issue clearly with technical reasoning
4. Suggest a specific, actionable fix

First run 'git diff main...{self.branch_name}' to see all changes.

Then analyze each file in detail for issues and edge cases.

Write your review in markdown format with the following sections:
1. Summary (overall assessment and key themes)
2. Issue List (all issues categorized by priority)
3. Recommendations (strategic suggestions beyond specific fixes)

Save this review to {self.review_file}
"""
        
        # Run Claude as reviewer
        output = self._run_claude_with_prompt(Role.REVIEWER, reviewer_prompt)

        # If output was obtained, write it to the review file
        if output:
            # Create directory if it doesn't exist
            self.review_file.parent.mkdir(parents=True, exist_ok=True)

            # Write the output to the review file
            with open(self.review_file, "w") as f:
                f.write(output)

            self.log(f"Review saved to {self.review_file}")
            return True
        else:
            self.log("Error: Review output not obtained")
            return False

    def _run_developer(self):
        """Run the developer Claude instance to implement fixes"""
        self.log("Starting developer phase...")

        # Read review file
        if not self.review_file.exists():
            self.log("Error: Review file not found")
            return False

        with open(self.review_file, "r") as f:
            review_content = f.read()

        # Create developer prompt
        developer_prompt = f"""
Think hard about this task.

You are a senior developer implementing fixes based on a code review.
Your task is to:

1. Read the review at {self.review_file}
2. Create a plan to address all CRITICAL and HIGH priority issues
3. Implement fixes for these issues one by one
4. Test your changes to ensure they work properly
5. Document your changes clearly
6. Write a development report explaining:
   - What changes you made and why
   - How you addressed each CRITICAL and HIGH issue
   - Any challenges you encountered
   - Any issues that require further discussion

Run 'git diff main...{self.branch_name}' first to understand the current code.
Use the review to guide your fixes.
Make changes using tools like Edit and Bash as needed.
Run tests with 'uv run pytest' to verify your changes.
Commit your changes with clear messages.

Save your development report to {self.development_plan_file}
"""
        
        # Run Claude as developer
        output = self._run_claude_with_prompt(Role.DEVELOPER, developer_prompt)

        # If output was obtained, write it to the development plan file
        if output:
            # Create directory if it doesn't exist
            self.development_plan_file.parent.mkdir(parents=True, exist_ok=True)

            # Write the output to the development plan file
            with open(self.development_plan_file, "w") as f:
                f.write(output)

            self.log(f"Development plan saved to {self.development_plan_file}")
            return True
        else:
            self.log("Error: Development plan output not obtained")
            return False

    def _run_validator(self):
        """Run the validator Claude instance to check fixes"""
        self.log("Starting validator phase...")

        # Read review and development plan
        if not self.review_file.exists() or not self.development_plan_file.exists():
            self.log("Error: Required files not found")
            return False, False

        with open(self.review_file, "r") as f:
            review_content = f.read()

        with open(self.development_plan_file, "r") as f:
            dev_plan_content = f.read()

        # Create validator prompt
        validator_prompt = f"""
Think hard about this task.

You are a validator responsible for ensuring code quality.
Your task is to:

1. Read the original review at {self.review_file}
2. Read the development report at {self.development_plan_file}
3. Run 'git diff main...{self.branch_name}' to see all current changes
4. Verify that ALL CRITICAL and HIGH issues from the review have been fixed
5. Run 'uv run pytest' to ensure all tests pass
6. Evaluate if the code meets our quality standards
7. Write a validation report answering:
   - Have all CRITICAL and HIGH issues been fixed? (Yes/No)
   - Are there any new issues introduced? (Yes/No)
   - Is the code ready for PR? (Yes/No)
   - If not ready, what specific issues remain?

Be rigorous in your assessment - we want high-quality code.
Include specific evidence for your conclusions.

Save your validation report to {self.validation_file}

YOUR VALIDATION REPORT MUST END WITH ONE OF THESE LINES:
- VALIDATION: PASSED (if all critical and high issues are fixed with no new issues)
- VALIDATION: FAILED (if any critical/high issues remain or new issues were introduced)
"""
        
        # Run Claude as validator
        output = self._run_claude_with_prompt(Role.VALIDATOR, validator_prompt)

        # If output was obtained, write it to the validation file
        if output:
            # Create directory if it doesn't exist
            self.validation_file.parent.mkdir(parents=True, exist_ok=True)

            # Write the output to the validation file
            with open(self.validation_file, "w") as f:
                f.write(output)

            # Check validation result
            passed = "VALIDATION: PASSED" in output
            self.log(f"Validation {'PASSED' if passed else 'FAILED'}")

            return True, passed
        else:
            self.log("Error: Validation output not obtained")
            return False, False

    def _run_pr_manager(self):
        """Run the PR manager Claude instance to create or update PR"""
        self.log("Starting PR manager phase...")

        # Check all required files exist
        if not self.review_file.exists() or not self.development_plan_file.exists() or not self.validation_file.exists():
            self.log("Error: Required files not found")
            return False

        # Create PR manager prompt
        pr_manager_prompt = f"""
Think hard about this task.

You are a PR manager responsible for preparing pull requests.
Your task is to:

1. Read the validation report at {self.validation_file} to ensure validation passed
2. Read the original review at {self.review_file}
3. Read the development report at {self.development_plan_file}
4. Run 'git diff main...{self.branch_name}' to see all changes
5. Create a comprehensive PR description including:
   - Summary of changes
   - List of issues fixed
   - Testing performed
   - Any known limitations or future work

If validation failed, do not create a PR and instead write a report explaining why.

For a successful PR:
1. Create a new branch for the PR if needed
2. Write a detailed PR description
3. Use 'gh pr create' to submit the PR

Save your PR report to {self.pr_file}
"""
        
        # Run Claude as PR manager
        output = self._run_claude_with_prompt(Role.PR_MANAGER, pr_manager_prompt)

        # If output was obtained, write it to the PR file
        if output:
            # Create directory if it doesn't exist
            self.pr_file.parent.mkdir(parents=True, exist_ok=True)

            # Write the output to the PR file
            with open(self.pr_file, "w") as f:
                f.write(output)

            self.log(f"PR report saved to {self.pr_file}")
            return True
        else:
            self.log("Error: PR report output not obtained")
            return False

    def _cleanup_worktrees(self):
        """Clean up temporary git worktrees"""
        for dir_path in self.instance_dirs.values():
            if (dir_path / ".git").exists():
                subprocess.run(["git", "worktree", "remove", "--force", str(dir_path)], 
                              stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                
        self.log("Cleaned up git worktrees")

    def run(self):
        """Run the full agentic loop workflow"""
        self.log(f"Starting agentic loop for branch: {self.branch_name}")
        
        while self.iteration < self.max_iterations:
            self.iteration += 1
            self.log(f"\n=== Starting iteration {self.iteration}/{self.max_iterations} ===")
            
            # Run review phase
            review_success = self._run_reviewer()
            if not review_success:
                self.log("Review phase failed. Stopping loop.")
                break
                
            # Run development phase
            dev_success = self._run_developer()
            if not dev_success:
                self.log("Development phase failed. Stopping loop.")
                break
                
            # Run validation phase
            validation_success, validation_passed = self._run_validator()
            if not validation_success:
                self.log("Validation phase failed. Stopping loop.")
                break
                
            # If validation passed, run PR phase and exit
            if validation_passed:
                self.log("Validation passed! Running PR phase.")
                pr_success = self._run_pr_manager()
                if pr_success:
                    self.log("PR phase completed successfully.")
                else:
                    self.log("PR phase failed.")
                break
            else:
                self.log("Validation failed. Starting next iteration.")
                
        # Clean up
        self._cleanup_worktrees()
        
        if self.iteration == self.max_iterations and not validation_passed:
            self.log(f"Reached maximum iterations ({self.max_iterations}) without passing validation.")
        
        self.log(f"Agentic loop completed. Output artifacts are in: {self.output_dir}")
        
        # Return success if validation passed
        return validation_passed if 'validation_passed' in locals() else False

def main():
    parser = argparse.ArgumentParser(description="Run agentic loop for Pipedrive MCP development")
    parser.add_argument("branch", help="Git branch to review and improve")
    parser.add_argument("--output-dir", help="Directory for output artifacts")
    parser.add_argument("--max-iterations", type=int, default=3,
                        help="Maximum number of improvement iterations")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--new-branch", help="Create a new branch derived from the source branch")
    parser.add_argument("--task", help="Description of the task (used for documentation)")

    args = parser.parse_args()

    loop = AgenticLoop(
        branch_name=args.branch,
        output_dir=args.output_dir,
        max_iterations=args.max_iterations,
        verbose=args.verbose,
        new_branch=args.new_branch
    )
    
    try:
        success = loop.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error during agentic loop execution: {e}")
        # Ensure worktrees are cleaned up even if an exception occurs
        loop._cleanup_worktrees()
        sys.exit(1)

if __name__ == "__main__":
    main()