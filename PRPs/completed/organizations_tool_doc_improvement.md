name: "Organizations MCP Tool Documentation and Parameter Handling Improvement"
description: |

  ## Goal
  Enhance the Organizations feature MCP tools with standardized documentation, accurate parameter validation, and API-compatible implementations to improve developer experience.

  ## Why
  - Current organization tools have inconsistencies in parameter handling
  - Address and location formatting requirements are not clearly documented
  - Follower associations need clearer guidance
  - Custom field handling lacks proper examples and validation

  ## What
  This PRP proposes targeted improvements to all tools in the Organizations feature:
  - Clarify address and location formatting requirements
  - Improve follower association documentation and handling
  - Standardize visible_to parameter validation
  - Enhance validation for industry and other specialized fields
  - Update documentation to accurately reflect API requirements

  ## Current Issues
  
  Based on API review and testing, the following specific issues exist in the Organizations tools:

  1. **Address Formatting**:
     - The API requires addresses in a specific format, but validation doesn't enforce it
     - Documentation doesn't clearly explain the required structure
     - Error messages don't properly guide users to the correct format

  2. **Follower Associations**:
     - Follower association endpoints have inconsistent parameter naming
     - Validation doesn't properly enforce required fields
     - Documentation lacks clear examples of follower operations

  3. **Industry Classification**:
     - Industry field lacks validation against accepted values
     - No clear guidance on industry classification options
     - Missing examples of proper industry assignment

  4. **Custom Field Handling**:
     - Lack of guidance on custom field format requirements
     - No validation for complex custom field structures
     - No examples of setting various custom field types

  ## API Documentation Reference

  The Pipedrive API documentation in `ai_docs/pipedrive_organizations.md` provides the following relevant information:

  - Organizations represent companies in the CRM
  - Address information requires specific formatting
  - Follower associations have specific requirements
  - Industry classifications follow certain patterns

  ## Implementation Plan
  
  ### 1. Tool Updates

  Update all organizations feature tools:
  1. `organization_create_tool.py`
  2. `organization_delete_tool.py`
  3. `organization_follower_add_tool.py`
  4. `organization_follower_delete_tool.py`
  5. `organization_get_tool.py`
  6. `organization_list_tool.py`
  7. `organization_search_tool.py`
  8. `organization_update_tool.py`

  ### 2. Specific Improvements

  #### Address Format Handling
  - Update documentation to clearly explain address structure requirements
  - Add validation utilities for address format
  - Implement conversion between simple inputs and API-required formats
  - Add examples of different address scenarios
  
  #### Follower Association
  - Standardize parameter naming and validation for follower operations
  - Add clear examples of adding and removing followers
  - Improve error messages for follower association issues
  - Ensure consistent handling across related tools
  
  #### Industry Classification
  - Document acceptable industry classifications if applicable
  - Add validation for industry values
  - Include examples of setting industry values
  - Implement clear error messages for invalid values
  
  #### Custom Fields
  - Add documentation on custom field format requirements
  - Implement validation for common custom field types
  - Include examples of handling different field types
  - Add clear error messages for format issues

  ## Testing Strategy
  
  A systematic testing approach will be used:

  1. **API Testing Script**:
     ```bash
     # Sample testing commands for Organizations API
     # Test basic organization creation
     curl -X POST "https://api.pipedrive.com/v1/organizations" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"name": "Test Organization"}'
     
     # Test address format
     curl -X POST "https://api.pipedrive.com/v1/organizations" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"name": "Address Test", "address":"123 Main St, City, Country"}'
     
     # Test follower association
     curl -X POST "https://api.pipedrive.com/v1/organizations/{id}/followers" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"user_id": 123}'
     ```

  2. **Verification Process**:
     - Test each parameter with various formats
     - Document successful formats for incorporation into validation
     - Test error scenarios to ensure helpful error messages
     - Verify all follower association operations
  
  3. **Tool Testing**:
     - After implementation, test each tool through the MCP interface
     - Verify that address validation works properly
     - Check that follower operations work as expected
     - Ensure documentation matches actual behavior

  ## Success Criteria
  
  The implementation will be successful when:
  1. Address information is properly handled in all operations
  2. Follower associations work correctly and are well-documented
  3. Industry classifications have proper validation if applicable
  4. Custom fields can be handled with appropriate guidance
  5. All error messages provide clear direction for correction
  6. All organizations tools pass integration tests with the API

  ## Benefits
  
  These improvements will provide:
  1. Clearer guidance on address formatting
  2. Simplified follower management
  3. Better support for industry classification
  4. Improved handling of custom fields
  5. Consistent validation preventing common errors
  6. Documentation that accurately reflects API behavior

  ## Dependencies
  
  This implementation depends on:
  1. Pipedrive API documentation in `ai_docs/pipedrive_organizations.md`
  2. Base validation utilities in `pipedrive/api/features/shared/conversion/id_conversion.py`
  3. Response formatting utilities in `pipedrive/api/features/shared/utils.py`

  ## Timeline
  
  Estimated implementation: 2.5 days
  - Day 1: API testing and implementation of address and follower improvements
  - Day 2: Implementation of industry and custom field improvements
  - Day 2.5: Testing and finalization