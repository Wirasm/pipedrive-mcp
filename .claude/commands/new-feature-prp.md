I want you to help me draft a new PRP based on the PRP structure in the PRPs/ directory.

PRP name: $ARGUMENTS

The user might have pasted relevant documentation in the ai_docs/ directory. ALWAYS Start by checking the ai_docs/ directory for any relevant documentation related to the PRP name and read it.

Please:
1. Analyze existing PRPs to understand our patterns, particularly looking at PRPs/deals_init.md and PRPs/persons_init.md
2. Draft a new PRP based on the PRP structure in the PRPs/ directory
3. Pipe necessary documentation into the ai_docs/ directory and reference it as (read_only) in the PRP
4. Reference existing code files and their relative paths that have similar patterns we want to MIRROR

The base structure of a PRP (Product Requirement Prompt) is as follows:

```markdown
## Goal
   Always include a clear goal for the PRP
## Why
   Always include a clear reason for the PRP, and justify why it is needed and who needs it
## What
   Always include a clear description of what the PRP is about
## Endpoints to Implement
   Always include a clear description of the endpoints/features to implement
## Current exact directory structure
   Always include a clear description of the current directory structure
## Proposed Directory Structure
   Always include a clear description of the proposed directory structure
## Files to Reference
   Always include a clear description of the files to reference
## Files to Implement (concept)
   Always include a clear description of the files to implement (concept)
## Implementation Notes
   Always include implementation notes and quirks of the implementation

## Validation Gates
   Always uncludes a valudation gate run "uv run pytest" to ensure all tests pass
   And specific run commands and expected output for each validation gate

## Implementation Checkpoints/Testing
   Always include a clear description of the implementation checkpoints and testing

## Other Considerations

```

IMPORTANT: Read relevant files from the directory to help you understand the current structure and patterns
IMPORTANT: It's important that you reference important files and directories to help the ai coder understand the current structure and patterns
IMPORTANT: Follow the same structure as already implemented PRPs
IMPORTANT: PRP are the main context for ai engineering tools, and context is king for these tools
IMPORTANT: Ensure that we give the prp all the needed context, by referencing the ai_docs, URL's for library documentation, etc
IMPORTANT: Provide clear and relevant example implementation, refernece in which file we want the code to be placed and reference existing code files that have similar patterns we want to MIRROR

*** REMEMBER: CONTEXT IS KING and PRP IS KING OF CONTEXT, THE AI NEEDS TO UNDERSTAND THE CONTEXT TO BE ABLE TO IMPLEMENT THE PRP do not assume what it has access to, and reference everything it will need access to by referencing files or URL's.***
