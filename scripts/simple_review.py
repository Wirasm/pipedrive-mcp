#!/usr/bin/env -S uv run --script

"""
Simple Reviewer for Code Analysis

This script runs a Claude instance to analyze code and generate a review report.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

def run_review(branch_name, output_file, verbose=False):
    """Run Claude to review code and generate a report"""
    # Create output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Log if verbose
    if verbose:
        print(f"Running code review for branch: {branch_name}")
        print(f"Output will be saved to: {output_file}")

    # Create reviewer prompt
    reviewer_prompt = f"""
Think hard about this task.

You are a senior code reviewer examining ONLY the changes in branch '{branch_name}' compared to main.
Your task is to provide a thorough, critical review STRICTLY LIMITED to the changes made in this branch.

Focus your review on these aspects:
1. Consistency with vertical slice architecture patterns
2. API error handling completeness
3. Input/output validation in models
4. Proper use of shared utilities (ID conversion, response formatting)
5. Security issues
6. Performance concerns
7. Test coverage and quality

For each issue found:
1. Mark as CRITICAL, HIGH, MEDIUM, or LOW priority
2. Provide the file path and line number (preferably of changed code)
3. Clearly indicate if the issue is in changed code or in related context
4. Explain the issue with technical reasoning
5. Suggest a specific, actionable fix

First run:
1. 'git diff main...{branch_name} --name-only' to see which files were changed
2. 'git diff main...{branch_name}' to see the actual line-by-line changes

Focus primarily on reviewing the changed lines and files, as these are what need to be evaluated for the PR/diff.

You may examine related files and code when necessary to understand the context of changes, but:
1. Your feedback should focus on issues in the changed code
2. Only mention issues in unchanged code if they directly impact the changes being reviewed
3. Always prioritize reviewing the actual diff changes first

Your primary job is to review what changed in the diff, while having the freedom to explore context when it helps your analysis.

Start by running these commands to understand what has changed:
```bash
git diff main...{branch_name} --name-only   # Lists all changed files
git diff main...{branch_name} --stat        # Shows a summary of changes
```

Then examine the specific changes in each file before writing your review.

Write your review in markdown format with the following sections:
1. Summary (overall assessment and key themes)
2. Issue List (all issues categorized by priority)
   - 2.1 Issues in Changed Code
   - 2.2 Context-Related Issues (if any)
3. Recommendations (strategic suggestions beyond specific fixes)

Your review will be automatically saved to a file, so focus on creating a detailed, helpful review.
"""

    # Run Claude with the prompt
    if verbose:
        print("Running Claude with review prompt...")

    try:
        # Configure Claude command
        cmd = [
            "claude",
            "-p",
            reviewer_prompt,
            "--allowedTools",
            "Bash,Grep,Read,LS,Glob,Task",
            "--output-format",
            "text"
        ]

        # Run Claude and capture output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=1200  # 20 minute timeout
        )
        output = result.stdout

        # Write output to file
        with open(output_file, "w") as f:
            f.write(output)

        if verbose:
            print("Review complete!")
            print(f"Full review saved to: {output_file}")
            
            # Print a preview
            lines = output.split('\n')
            preview = '\n'.join(lines[:15]) + '\n...'
            print(f"\nPreview of review:\n{preview}")

        return True
    except subprocess.TimeoutExpired:
        print(f"Error: Claude review process timed out after 20 minutes")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error running Claude: {e}")
        print(f"stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run code review with Claude")
    parser.add_argument("branch", help="Git branch to review (compared to main)")
    parser.add_argument("--output", help="Output file path for the review (default: review_<branch>.md)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Set default output file if not specified
    output_file = args.output if args.output else f"review_{args.branch}.md"
    
    # Run the review
    success = run_review(args.branch, output_file, args.verbose)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()