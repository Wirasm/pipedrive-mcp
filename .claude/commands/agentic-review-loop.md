# Agentic Review Loop

Run a self-validating multi-agent review loop for the $ARGUMENTS branch. This uses multiple Claude instances working together to:

1. **Reviewer**: Conduct thorough code review
2. **Developer**: Implement fixes for issues
3. **Validator**: Verify all critical issues are fixed
4. **PR Manager**: Create a pull request when validation passes

The system works as an iterative feedback loop until all critical issues are fixed or we reach the maximum iterations.

Each agent works in its own git worktree to prevent conflicts, and detailed reports are generated at each stage.

## Process

The agentic loop follows these steps:

1. Reviewer analyzes code and creates a detailed review report
2. Developer implements fixes for CRITICAL and HIGH priority issues
3. Validator verifies fixes and either approves or returns to step 1
4. When approved, PR Manager creates a pull request

## Output

The loop produces detailed artifacts at each stage:
- Review report with prioritized issues
- Development report documenting changes
- Validation report confirming fixes
- PR description with comprehensive change summary

All artifacts are saved to a timestamped directory for reference.

Let me know when you'd like to start the review process, and I'll execute the agentic loop on your branch!