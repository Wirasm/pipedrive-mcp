name: "Deals MCP Tool Documentation and Parameter Handling Improvement"
description: |

  ## Goal
  Enhance the Deals feature MCP tools with standardized documentation, accurate parameter validation, and API-compatible implementations to improve developer experience.

  ## Why
  - Current deals tools have inconsistencies in parameter handling and validation
  - Product association and pricing information lacks clear documentation
  - Stage and pipeline parameters have unclear requirements
  - Error messages don't provide clear guidance on correct formats

  ## What
  This PRP proposes targeted improvements to all tools in the Deals feature:
  - Clarify product association and pricing format requirements
  - Improve stage and pipeline parameter validation
  - Standardize monetary value and currency handling
  - Update documentation to accurately reflect API requirements
  - Ensure consistent validation with helpful error messages

  ## Current Issues

  Based on API review and testing, the following specific issues exist in the Deals tools:

  1. **Product Association Complexity**:
     - Deal product association requires complex parameter structures
     - Documentation doesn't clearly explain required product fields
     - Validation doesn't properly enforce required product parameters
     - Error messages don't guide users to the correct structure

  2. **Stage and Pipeline Handling**:
     - Stage and pipeline IDs have unclear documentation
     - Relationship between stages and pipelines is not well-explained
     - Missing validation for stage/pipeline compatibility
     - Error messages don't indicate when stages and pipelines conflict

  3. **Monetary Value Formatting**:
     - Inconsistent handling of deal values and currencies
     - Documentation doesn't clarify format expectations
     - Missing examples of proper value formatting
     - Validation doesn't properly enforce numeric constraints

  4. **Custom Fields for Deals**:
     - Lack of guidance on deal-specific custom field formats
     - No validation for complex custom field structures
     - Missing examples of common custom field types for deals

  ## API Documentation Reference

  The Pipedrive API documentation in `ai_docs/pipedrive_deals.md` provides the following relevant information:

  - Deals represent sales opportunities in the CRM
  - Products can be associated with deals using specific structures
  - Stages and pipelines have explicit relationships
  - Deal values must follow specific formatting requirements

  ## Implementation Plan
  
  ### 1. Tool Updates

  Update all deals feature tools:
  1. `deal_create_tool.py`
  2. `deal_delete_tool.py`
  3. `deal_get_tool.py`
  4. `deal_list_tool.py`
  5. `deal_product_add_tool.py`
  6. `deal_product_delete_tool.py`
  7. `deal_product_update_tool.py`
  8. `deal_search_tool.py`
  9. `deal_update_tool.py`

  ### 2. Specific Improvements

  #### Product Association Handling
  - Update documentation to clearly explain product association requirements
  - Add validation utilities for product parameters (price, quantity, etc.)
  - Implement conversion between simple inputs and API-required formats
  - Add examples of adding and updating products on deals
  
  #### Stage and Pipeline Management
  - Clarify the relationship between stages and pipelines
  - Add validation to ensure stage/pipeline compatibility
  - Provide examples of proper stage transitions
  - Improve error messages for stage/pipeline conflicts
  
  #### Monetary Value Formatting
  - Document value and currency format requirements
  - Implement proper validation for numeric values
  - Add clear examples of formatting monetary values
  - Ensure consistent handling across create and update operations
  
  #### Custom Fields
  - Add documentation on deal-specific custom field formats
  - Implement validation for common custom field types
  - Include examples of handling different field types
  - Add clear error messages for format issues

  ## Testing Strategy

  **RUN THIS BEFORE IMPLEMENTING TO CONCLUDE IF THE IMPROVEMENTS ARE NEEDED**
  
  A systematic testing approach will be used:

  1. **API Testing Script**:
     ```bash
     # Sample testing commands for Deals API
     # Test basic deal creation
     curl -X POST "https://api.pipedrive.com/v1/deals" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"title": "Test Deal", "value": 1000, "currency": "USD"}'
     
     # Test stage and pipeline
     curl -X POST "https://api.pipedrive.com/v1/deals" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"title": "Stage Test", "stage_id": 1, "pipeline_id": 1}'
     
     # Test product association
     curl -X POST "https://api.pipedrive.com/v1/deals/{deal_id}/products" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"product_id": 123, "item_price": 100, "quantity": 1}'
     ```

  2. **Verification Process**:
     - Test each parameter with various formats to determine exact API requirements
     - Document successful formats for incorporation into tool validation
     - Test error scenarios to ensure helpful error messages
     - Verify product association methods
  
  3. **Tool Testing**:
     - After implementation, test each tool through the MCP interface
     - Verify that validation properly accepts valid inputs and rejects invalid ones
     - Check that error messages are helpful and accurate
     - Ensure documentation matches actual behavior

  ## Success Criteria
  
  The implementation will be successful when:
  1. Product associations work correctly with proper validation
  2. Stage and pipeline relationships are clearly documented and validated
  3. Monetary values are properly formatted and validated
  4. Documentation accurately describes all parameter formats and requirements
  5. Error messages provide clear guidance on correct usage
  6. All deals tools pass integration tests with the API

  ## Benefits
  
  These improvements will provide:
  1. Clearer developer experience when working with deals
  2. Simplified product association process
  3. Better understanding of stage and pipeline relationships
  4. Improved handling of monetary values
  5. Consistent validation that prevents common errors
  6. Documentation that accurately reflects API behavior

  ## Dependencies
  
  This implementation depends on:
  1. Pipedrive API documentation in `ai_docs/pipedrive_deals.md`
  2. Base validation utilities in `pipedrive/api/features/shared/conversion/id_conversion.py`
  3. Response formatting utilities in `pipedrive/api/features/shared/utils.py`

  ## Timeline
  
  Estimated implementation: 3 days
  - Day 1: API testing and documentation review
  - Day 2: Implementation of product, stage/pipeline improvements
  - Day 3: Implementation of value formatting, testing and validation