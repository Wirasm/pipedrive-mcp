name: "Leads MCP Tool Documentation and Parameter Handling Improvement"
description: |

  ## Goal
  Enhance the Leads feature MCP tools with standardized documentation, accurate parameter validation, and API-compatible implementations to improve developer experience.

  ## Why
  - Current leads tools have inconsistencies in parameter handling and validation
  - Label and source field requirements are not clearly documented
  - Owner and visibility parameters have unclear requirements
  - Error messages don't provide clear guidance on correct formats

  ## What
  This PRP proposes targeted improvements to all tools in the Leads feature:
  - Clarify label and source field requirements
  - Improve person and organization association validation
  - Standardize owner and visibility parameter handling
  - Update documentation to accurately reflect API requirements
  - Ensure consistent validation with helpful error messages

  ## Current Issues

  Based on API review and testing, the following specific issues exist in the Leads tools:

  1. **Label and Title Formatting**:
     - Lead label requirements are not clearly documented
     - Title field validation is inconsistent
     - Error messages don't guide users to the correct formats
     - Missing examples of proper label usage

  2. **Person and Organization Association**:
     - Association with person and organization entities lacks clear documentation
     - Validation doesn't enforce relationship requirements
     - Missing examples of proper entity associations
     - Error messages don't explain association constraints

  3. **Owner and Visibility Settings**:
     - Owner ID and visibility parameters have unclear requirements
     - Documentation doesn't explain valid visibility options
     - Missing validation for owner permissions
     - Error messages don't guide users to correct settings

  4. **Expected Value Handling**:
     - Value and currency fields lack clear documentation
     - Validation doesn't properly enforce numeric constraints
     - Missing examples of proper value formatting
     - Inconsistent handling across create and update operations

  ## API Documentation Reference

  The Pipedrive API documentation in `ai_docs/pipedrive_leads.md` provides the following relevant information:

  - Leads represent early-stage sales opportunities
  - Labels and sources have specific formatting requirements
  - Person and organization associations follow certain patterns
  - Owner and visibility settings affect access control

  ## Implementation Plan
  
  ### 1. Tool Updates

  Update all leads feature tools:
  1. `lead_create_tool.py`
  2. `lead_delete_tool.py`
  3. `lead_get_tool.py`
  4. `lead_label_get_tool.py`
  5. `lead_list_tool.py`
  6. `lead_search_tool.py`
  7. `lead_source_get_tool.py`
  8. `lead_update_tool.py`

  ### 2. Specific Improvements

  #### Label and Title Handling
  - Update documentation to clearly explain label requirements
  - Add validation utilities for label formats
  - Include examples of valid title and label usage
  - Improve error messages for format issues
  
  #### Person and Organization Association
  - Clarify requirements for associating persons and organizations
  - Add validation for association parameters
  - Provide examples of proper association syntax
  - Update error messages to guide users to correct formats
  
  #### Owner and Visibility Settings
  - Document owner ID requirements and validation
  - Clarify visibility options and their meanings
  - Add examples of setting ownership and visibility
  - Implement proper validation with clear error messages
  
  #### Expected Value Handling
  - Document value and currency format requirements
  - Implement validation for numeric values and currencies
  - Include examples of setting expected values
  - Add clear error messages for format issues

  ## Testing Strategy

  **RUN THIS BEFORE IMPLEMENTING TO CONFIRM WHAT THE API EXPECTS**
  
  A systematic testing approach will be used:
  the pipedrive api token is in .env

  1. **API Testing Script**:
     ```bash
     # Sample testing commands for Leads API
     # Test basic lead creation
     curl -X POST "https://api.pipedrive.com/v1/leads" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"title": "Test Lead"}'
     
     # Test with labels
     curl -X POST "https://api.pipedrive.com/v1/leads" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"title": "Label Test", "label_ids": [1]}'
     
     # Test person association
     curl -X POST "https://api.pipedrive.com/v1/leads" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"title": "Person Test", "person_id": 123}'
     ```

  2. **Verification Process**:
     - Test each parameter with various formats to determine exact API requirements
     - Document successful formats for incorporation into tool validation
     - Test error scenarios to ensure helpful error messages
     - Verify relationship between leads and other entities
  
  3. **Tool Testing**:
     - After implementation, test each tool through the MCP interface
     - Verify that validation properly accepts valid inputs and rejects invalid ones
     - Check that error messages are helpful and accurate
     - Ensure documentation matches actual behavior

  ## Success Criteria
  
  The implementation will be successful when:
  1. Label and title formatting works correctly with proper validation
  2. Person and organization associations are properly documented and validated
  3. Owner and visibility settings are clearly documented and enforced
  4. Value fields are properly formatted and validated
  5. All error messages provide clear guidance on correct usage
  6. All leads tools pass integration tests with the API

  ## Benefits
  
  These improvements will provide:
  1. Clearer developer experience when working with leads
  2. Better understanding of label and source requirements
  3. Simplified person and organization association
  4. Improved handling of ownership and visibility
  5. Consistent validation preventing common errors
  6. Documentation that accurately reflects API behavior

  ## Dependencies
  
  This implementation depends on:
  1. Pipedrive API documentation in `ai_docs/pipedrive_leads.md`
  2. Base validation utilities in `pipedrive/api/features/shared/conversion/id_conversion.py`
  3. Response formatting utilities in `pipedrive/api/features/shared/utils.py`

  ## Timeline
  
  Estimated implementation: 2.5 days
  - Day 1: API testing and documentation review
  - Day 2: Implementation of improved tools
  - Day 2.5: Testing and validation