name: "Persons MCP Tool Documentation and Parameter Handling Improvement"
description: |

  ## Goal
  Enhance the Persons feature MCP tools with standardized documentation, accurate parameter validation, and API-compatible implementations to improve developer experience.

  ## Why
  - Current persons tools have inconsistencies in parameter handling and documentation
  - Contact information formatting requirements are not clearly documented
  - Entity associations (like organization links) need clearer guidance
  - Developers experience confusion when managing complex person fields

  ## What
  This PRP proposes targeted improvements to all tools in the Persons feature:
  - Clarify email and phone number formatting requirements
  - Improve organization association documentation and validation
  - Standardize visible_to parameter handling
  - Enhance validation for custom fields
  - Update documentation to accurately reflect API requirements

  ## Current Issues
  
  Based on API review and testing, the following specific issues exist in the Persons tools:

  1. **Contact Information Formatting**:
     - Email and phone parameters lack clear format documentation
     - Validation doesn't properly handle arrays of contact objects
     - Error messages don't guide users to the correct structure

  2. **Organization Association**:
     - Organization ID linking has inconsistent validation
     - No clear guidance on how to properly associate organizations
     - Missing examples of correct association patterns

  3. **Visibility Settings**:
     - The `visible_to` parameter lacks clear documentation on acceptable values
     - Validation doesn't enforce the 1-4 range requirement
     - No examples of how visibility affects access control

  4. **Custom Fields Handling**:
     - Lack of guidance on custom field format requirements
     - No validation for complex custom field structures
     - Missing examples of common custom field types

  ## API Documentation Reference

  The Pipedrive API documentation in `ai_docs/pipedrive_persons.md` provides the following relevant information:

  - Persons represent individual contacts in the CRM
  - Contact information has specific formatting requirements for emails and phones
  - Organization associations require specific ID handling
  - Custom fields have type-specific format requirements

  ## Implementation Plan
  
  ### 1. Tool Updates

  Update all persons feature tools:
  1. `person_create_tool.py`
  2. `person_delete_tool.py`
  3. `person_get_tool.py`
  4. `person_search_tool.py`
  5. `person_update_tool.py`

  ### 2. Specific Improvements

  #### Contact Information Handling
  - Update documentation to clearly explain email and phone structure
  - Add validation utilities for contact information arrays
  - Implement conversion between simple inputs and API-required formats
  - Add examples of various contact information scenarios
  
  #### Organization Association
  - Clarify organization ID requirements and validation
  - Add examples of creating persons with organization links
  - Improve error messages for organization relationship issues
  - Ensure consistent handling across all tools
  
  #### Visibility Settings
  - Document the valid range for visibility settings (1-4)
  - Add specific examples of each visibility level
  - Implement proper validation with clear error messages
  - Consistent handling in create and update operations
  
  #### Custom Fields
  - Add documentation on custom field format requirements
  - Implement validation for common custom field types
  - Include examples of handling different field types
  - Add clear error messages for format issues

  ## Testing Strategy
  
  A systematic testing approach will be used:

  1. **API Testing Script**:
     ```bash
     # Sample testing commands for Persons API
     # Test basic person creation
     curl -X POST "https://api.pipedrive.com/v1/persons" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"name": "Test Person"}'
     
     # Test contact info format
     curl -X POST "https://api.pipedrive.com/v1/persons" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"name": "Contact Test", "email":[{"value":"test@example.com", "primary":true, "label":"work"}]}'
     
     # Test organization association
     curl -X POST "https://api.pipedrive.com/v1/persons" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"name": "Org Test", "org_id": 123}'
     ```

  2. **Verification Process**:
     - Test each parameter with various formats
     - Document successful formats for incorporation into validation
     - Test error scenarios to ensure helpful error messages
     - Verify all entity association methods
  
  3. **Tool Testing**:
     - After implementation, test each tool through the MCP interface
     - Verify that validation properly handles both simple and complex inputs
     - Check that error messages are helpful and accurate
     - Ensure documentation matches actual behavior

  ## Success Criteria
  
  The implementation will be successful when:
  1. Contact information is properly handled in all operations
  2. Organization associations work correctly and are well-documented
  3. Visibility settings are properly validated with clear documentation
  4. Custom fields can be handled with appropriate guidance
  5. All error messages provide clear direction for correction
  6. All persons tools pass integration tests with the API

  ## Benefits
  
  These improvements will provide:
  1. Clearer guidance on contact information formatting
  2. Simplified organization association process
  3. Better understanding of visibility settings
  4. Improved handling of custom fields
  5. Consistent validation preventing common errors
  6. Documentation that accurately reflects API behavior

  ## Dependencies
  
  This implementation depends on:
  1. Pipedrive API documentation in `ai_docs/pipedrive_persons.md`
  2. Base validation utilities in `pipedrive/api/features/shared/conversion/id_conversion.py`
  3. Response formatting utilities in `pipedrive/api/features/shared/utils.py`

  ## Timeline
  
  Estimated implementation: 2 days
  - Day 1: API testing and implementation of contact info and organization association improvements
  - Day 2: Implementation of visibility and custom field improvements, testing