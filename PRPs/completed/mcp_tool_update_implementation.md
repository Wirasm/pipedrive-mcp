CONCEPT, WILL NOT BE IMPLEMENTED

name: "MCP Tool Update Implementation"
description: |

  ## Goal
  Implement the standardized MCP tool documentation and parameter handling across all Pipedrive API features according to the improvements established in PRP mcp_tool_improvement.md.

  ## Why
  - The foundation for improved MCP tools has been implemented but only applied to one example tool
  - Consistent implementation across all tools is needed for a unified developer experience
  - All tools should follow the same parameter naming conventions, validation patterns, and documentation standards
  - The benefits of improved error messages and format examples should be available in all tools

  ## What
  This PRP proposes updating all remaining tool implementations to align with the improved standards:
  - Update parameter naming conventions in all tools (remove _str suffixes)
  - Enhance tool docstrings according to the standardized templates
  - Implement consistent validation with proper examples
  - Apply the input sanitization utilities
  - Standardize error handling patterns

  ## Current State
  
  The foundation for improved MCP tools has been implemented with:
  
  1. Enhanced utility functions for validation:
     - `pipedrive/api/features/shared/conversion/id_conversion.py` - Improved ID, UUID, date, and time validation
     - `pipedrive/api/features/shared/utils.py` - Added input sanitization and error formatting
  
  2. Documentation templates for all tool types:
     - `pipedrive/api/features/shared/tool_templates.md` - Templates for create, get, update, delete, list, and search tools
  
  3. Enhanced tool decorator with docstring validation:
     - `pipedrive/api/features/tool_decorator.py` - Automatic docstring validation
  
  4. Example implementation of the new standards:
     - `pipedrive/api/features/activities/tools/activity_create_tool.py` - Updated to demonstrate the improved pattern
  
  5. Comprehensive tests for all new functionality:
     - `pipedrive/api/features/shared/conversion/tests/test_id_conversion.py`
     - `pipedrive/api/features/shared/tests/test_utils.py`
     - `pipedrive/api/features/tests/test_tool_decorator.py`
  
  ## Implementation Plan
  
  The implementation will systematically update all tools across all feature modules:
  
  ### Feature Modules to Update
  1. Persons feature tools (5 files)
  2. Organizations feature tools (8 files)
  3. Deals feature tools (9 files)
  4. Leads feature tools (9 files)
  5. Activities feature tools (6 remaining files)
  6. Item Search feature tools (2 files)
  
  ### Update Process for Each Tool
  1. Refactor parameter naming to remove _str suffixes
  2. Update docstrings according to the standardized templates in `tool_templates.md`
  3. Implement early validation with examples using the enhanced utilities
  4. Apply the `sanitize_inputs` utility for consistent input handling
  5. Standardize error handling with appropriate error messages
  
  ### Example of Updated Tool Pattern
  
  The standardized tool pattern follows this template (based on the example implementation):
  
  ```python
  @tool("feature_name")
  async def action_entity_in_pipedrive(
      ctx: Context,
      required_param: str,
      id_param: Optional[str] = None,
      # other parameters...
  ) -> str:
      """One-line summary of what the tool does.
  
      Detailed description explaining the purpose and key functionality.
  
      Format requirements:
      - id_param: Must be a numeric string (e.g., "123")
      - other format requirements...
  
      Example:
      ```
      action_entity_in_pipedrive(
          required_param="value",
          id_param="123"
      )
      ```
  
      Args:
          ctx: Context object provided by the MCP server
          required_param: Description with format requirements if applicable
          id_param: Numeric ID of the entity. Must be a positive integer as a string (e.g., "123")
  
      Returns:
          JSON formatted response with success/failure status and data or error message
      """
      # Log inputs with appropriate redaction
      logger.debug(f"Tool '{action_entity_in_pipedrive.__name__}' ENTERED with raw args: ...")
  
      # Sanitize inputs using the utility
      inputs = {
          "required_param": required_param,
          "id_param": id_param,
          # other parameters...
      }
      sanitized = sanitize_inputs(inputs)
      required_param = sanitized["required_param"]
      id_param = sanitized["id_param"]
      
      # Validate required fields
      if not required_param:
          error_message = "The 'required_param' field is required and cannot be empty."
          return format_tool_response(False, error_message=error_message)
      
      # Convert and validate parameters using enhanced utilities
      id_value, id_error = convert_id_string(id_param, "id_param", "123")
      if id_error:
          return format_tool_response(False, error_message=id_error)
      
      # Rest of implementation...
  ```
  
  ## Files to Modify
  
  ### Persons Feature
  1. `pipedrive/api/features/persons/tools/person_create_tool.py`
  2. `pipedrive/api/features/persons/tools/person_delete_tool.py`
  3. `pipedrive/api/features/persons/tools/person_get_tool.py`
  4. `pipedrive/api/features/persons/tools/person_search_tool.py`
  5. `pipedrive/api/features/persons/tools/person_update_tool.py`
  
  ### Organizations Feature
  1. `pipedrive/api/features/organizations/tools/organization_create_tool.py`
  2. `pipedrive/api/features/organizations/tools/organization_delete_tool.py`
  3. `pipedrive/api/features/organizations/tools/organization_follower_add_tool.py`
  4. `pipedrive/api/features/organizations/tools/organization_follower_delete_tool.py`
  5. `pipedrive/api/features/organizations/tools/organization_get_tool.py`
  6. `pipedrive/api/features/organizations/tools/organization_list_tool.py`
  7. `pipedrive/api/features/organizations/tools/organization_search_tool.py`
  8. `pipedrive/api/features/organizations/tools/organization_update_tool.py`
  
  ### Deals Feature
  1. `pipedrive/api/features/deals/tools/deal_create_tool.py`
  2. `pipedrive/api/features/deals/tools/deal_delete_tool.py`
  3. `pipedrive/api/features/deals/tools/deal_get_tool.py`
  4. `pipedrive/api/features/deals/tools/deal_list_tool.py`
  5. `pipedrive/api/features/deals/tools/deal_product_add_tool.py`
  6. `pipedrive/api/features/deals/tools/deal_product_delete_tool.py`
  7. `pipedrive/api/features/deals/tools/deal_product_update_tool.py`
  8. `pipedrive/api/features/deals/tools/deal_search_tool.py`
  9. `pipedrive/api/features/deals/tools/deal_update_tool.py`
  
  ### Leads Feature
  1. `pipedrive/api/features/leads/tools/lead_create_tool.py`
  2. `pipedrive/api/features/leads/tools/lead_delete_tool.py`
  3. `pipedrive/api/features/leads/tools/lead_get_tool.py`
  4. `pipedrive/api/features/leads/tools/lead_label_get_tool.py`
  5. `pipedrive/api/features/leads/tools/lead_list_tool.py`
  6. `pipedrive/api/features/leads/tools/lead_search_tool.py`
  7. `pipedrive/api/features/leads/tools/lead_source_get_tool.py`
  8. `pipedrive/api/features/leads/tools/lead_update_tool.py`
  
  ### Activities Feature (Remaining Tools)
  1. `pipedrive/api/features/activities/tools/activity_delete_tool.py`
  2. `pipedrive/api/features/activities/tools/activity_get_tool.py`
  3. `pipedrive/api/features/activities/tools/activity_list_tool.py`
  4. `pipedrive/api/features/activities/tools/activity_type_create_tool.py`
  5. `pipedrive/api/features/activities/tools/activity_type_list_tool.py`
  6. `pipedrive/api/features/activities/tools/activity_update_tool.py`
  
  ### Item Search Feature
  1. `pipedrive/api/features/item_search/tools/item_field_search_tool.py`
  2. `pipedrive/api/features/item_search/tools/item_search_tool.py`
  
  ## Implementation Timeline
  
  The implementation will follow a module-by-module approach to ensure systematic updates:
  
  1. Update Person feature tools (5 files) - 1 day
  2. Update Organization feature tools (8 files) - 1.5 days
  3. Update Deals feature tools (9 files) - 1.5 days
  4. Update Leads feature tools (9 files) - 1.5 days
  5. Update remaining Activities feature tools (6 files) - 1 day
  6. Update Item Search feature tools (2 files) - 0.5 day
  
  Total implementation time: 7 days
  
  ## Testing Strategy
  
  Each updated tool will be tested to ensure:
  1. Parameter validation works correctly
  2. Error messages are clear and include examples
  3. Required parameters are properly enforced
  4. Docstrings follow the standardized format
  5. The tool functions correctly with the API
  
  Tests will include:
  - Unit tests for new validation utilities
  - Integration tests for the updated tools
  - Error handling tests with invalid inputs
  
  ## Success Criteria
  
  The implementation will be considered successful when:
  1. All tools follow the standardized pattern
  2. All docstrings are compliant with the template format
  3. All parameter names are consistent (no _str suffixes)
  4. All tools provide clear error messages with examples
  5. All tests pass with the updated implementation
  
  ## Dependencies
  
  This implementation depends on:
  1. The enhanced utility functions in `pipedrive/api/features/shared/conversion/id_conversion.py`
  2. The validation and sanitization utilities in `pipedrive/api/features/shared/utils.py`
  3. The documentation templates in `pipedrive/api/features/shared/tool_templates.md`
  4. The enhanced tool decorator in `pipedrive/api/features/tool_decorator.py`
  
  ## Risks and Mitigations
  
  **Risk**: Breaking changes to tool interfaces
  **Mitigation**: Ensure backward compatibility by maintaining the same parameter functionality
  
  **Risk**: Inconsistent implementation across tools
  **Mitigation**: Use the already-updated tool as a reference and follow a systematic approach
  
  **Risk**: Missing validation for specific parameter types
  **Mitigation**: Identify and implement any additional validation utilities needed
  
  **Risk**: Mismatch between client validation and API expectations
  **Mitigation**: For each tool, test with the API to ensure our validation rules match what the API expects

  ## Known Issues to Address

  Based on testing, the following specific issues need to be addressed during implementation:

  1. **Time Format Handling**:
     - The Pipedrive API rejects HH:MM:SS format for `due_time` and `duration` despite our validation accepting it
     - Need to investigate and document the exact format the API expects for time fields
     - Modify validation utilities to match the API's expected format

  2. **Entity Association Fields**:
     - Some fields like `person_id` are read-only according to the API
     - Update documentation to clarify proper methods for entity association (e.g., using participants)
     - Identify all similar read-only fields across all entity types

  3. **Complex Parameter Requirements**:
     - Identify parameters with special formatting requirements (like `location`)
     - Create specific validation rules and examples for these parameters
     - Document alternative approaches when direct assignment isn't supported

  4. **API Error Translation**:
     - Enhance error handling to provide more context when API errors occur
     - Map common API error messages to user-friendly guidance
     - Include specific examples of correct formats in error messages
  
  ## Backward Compatibility
  
  - Parameter names will change (removing _str suffixes) but the functionality will remain the same
  - All tools will continue to accept the same input formats
  - Error messages will be more detailed but follow the same response format
  - The changes are focused on improving developer experience, not changing behavior