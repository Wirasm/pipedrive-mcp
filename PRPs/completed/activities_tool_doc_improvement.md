name: "Activities MCP Tool Documentation and Parameter Handling Improvement"
description: |

  ## Goal
  Improve the Activities feature MCP tools by standardizing documentation, enhancing parameter validation, and ensuring API compatibility to provide a better developer experience.

  ## Why
  - Current activities tools have inconsistencies in parameter handling and validation
  - Documentation does not accurately describe API requirements for time formats, locations, and participant handling
  - Error messages are sometimes unclear or contradictory
  - Developers experience confusion when working with time-related fields and entity associations

  ## What
  This PRP proposes targeted improvements to all tools in the Activities feature:
  - Fix time format handling to match API expectations
  - Implement proper participant handling for person associations
  - Enhance location parameter formatting
  - Update documentation to accurately reflect API requirements
  - Ensure consistent validation with helpful error messages

  ## Current Issues

  Based on API testing, the following specific issues have been identified in the Activity tools:

  1. **Time Format Inconsistencies**:
     - `due_time` parameter causes errors in various formats including ISO format
     - Error messages are inconsistent about the expected format
     - Documentation suggests HH:MM:SS but API rejects this format

  2. **Duration Format Conflict**:
     - Conflicting validation messages about duration format
     - Documentation and code suggest both "HH:MM:SS format" and "seconds as a numeric string"
     - Neither format works reliably with the API

  3. **Entity Association Challenges**:
     - `person_id` is marked as a read-only field by the API
     - No clear mechanism to associate persons via the required participants field
     - Documentation doesn't explain the correct approach for entity associations

  4. **Location Format Requirements**:
     - API requires location in array format
     - Tool accepts and validates a string input
     - No conversion between string input and required array format

  ## API Documentation Reference

  The Pipedrive API documentation in `ai_docs/pipedrive_activities.md` provides the following relevant information:

  - Activities represent calendar items like calls, meetings, or tasks
  - Entity associations should use participant fields rather than direct ID references
  - Time formats follow specific patterns that don't match our current implementation
  - Location data has a specific structure not currently implemented in our tools

  ## Implementation Plan
  
  ### 1. Tool Updates

  Update all activities feature tools:
  1. `activity_create_tool.py`
  2. `activity_delete_tool.py`
  3. `activity_get_tool.py`
  4. `activity_list_tool.py`
  5. `activity_type_create_tool.py`
  6. `activity_type_list_tool.py`
  7. `activity_update_tool.py`

  ### 2. Specific Improvements

  #### Time Format Handling
  - Update validation utilities to properly handle Pipedrive's expected time format
  - Modify documentation to accurately describe required formats
  - Create conversion functions to transform common time inputs to API-compatible formats
  - Add clear examples in documentation
  
  #### Participant Handling
  - Add a new `participants` parameter to relevant tools
  - Implement proper JSON structure for participant data
  - Add clear documentation with examples of associating entities
  - Update error messages to guide users toward correct participant usage
  
  #### Location Format
  - Update location parameter to accept proper format or convert from string
  - Document the expected structure clearly
  - Add validation with helpful error messages
  
  #### Error Messaging
  - Ensure all error messages include correct format examples
  - Make error messages consistent with actual API requirements
  - Add contextual information when API errors occur

  ## Testing Strategy

  **RUN THIS BEFORE IMPLEMENTING TO CONFIRM WHAT THE API EXPECTS**
  
  A systematic testing approach will be used:
  the pipedrive api token is in .env

  1. **API Testing Script**:
     ```bash
     # Sample testing commands for Activities API
     # Test basic creation
     curl -X POST "https://api.pipedrive.com/v1/activities" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"subject": "Test Activity", "type": "call"}'
     
     # Test time formats
     curl -X POST "https://api.pipedrive.com/v1/activities" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"subject": "Time Test", "type": "call", "due_date": "2025-01-15", "due_time": "FORMAT_TO_TEST"}'
     
     # Test participants
     curl -X POST "https://api.pipedrive.com/v1/activities" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"subject": "Participant Test", "type": "call", "participants": [{"person_id": 123, "primary_flag": true}]}'
     ```

  2. **Verification Process**:
     - Test each parameter with various formats to determine exact API requirements
     - Document successful formats for incorporation into tool validation
     - Test error scenarios to ensure helpful error messages
     - Verify all entity association methods
  
  3. **Tool Testing**:
     - After implementation, test each tool through the MCP interface
     - Verify that validation properly accepts valid inputs and rejects invalid ones
     - Check that error messages are helpful and accurate
     - Ensure documentation matches actual behavior

  ## Success Criteria
  
  The implementation will be successful when:
  1. All time-related parameters work correctly with the API
  2. Entity associations via participants work as expected
  3. Location formatting is consistent with API requirements
  4. Documentation accurately describes all parameter formats and requirements
  5. Error messages provide clear guidance on correct usage
  6. All activities tools pass integration tests with the API

  ## Benefits
  
  These improvements will provide:
  1. Clearer developer experience when working with activities
  2. Reduced confusion about parameter formats and requirements
  3. More helpful error messages that guide toward correct usage
  4. Documentation that accurately reflects the API behavior
  5. Consistent validation that prevents common errors

  ## Dependencies
  
  This implementation depends on:
  1. Pipedrive API documentation in `ai_docs/pipedrive_activities.md`
  2. Base validation utilities in `pipedrive/api/features/shared/conversion/id_conversion.py`
  3. Response formatting utilities in `pipedrive/api/features/shared/utils.py`

  ## Timeline
  
  Estimated implementation: 3 days
  - Day 1: API testing and documentation review
  - Day 2: Implementation of improved tools
  - Day 3: Testing and validation