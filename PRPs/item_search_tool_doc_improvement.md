name: "Item Search MCP Tool Documentation and Parameter Handling Improvement"
description: |

  ## Goal
  Enhance the Item Search feature MCP tools with standardized documentation, accurate parameter validation, and API-compatible implementations to improve developer experience.

  ## Why
  - Current item search tools have inconsistencies in parameter handling and validation
  - Search term formatting and options lack clear documentation
  - Field-specific search capabilities are not well explained
  - Error messages don't provide clear guidance on search syntax

  ## What
  This PRP proposes targeted improvements to the Item Search feature tools:
  - Clarify search term syntax and formatting requirements
  - Improve documentation for field-specific search options
  - Standardize pagination and result limit parameters
  - Update documentation to accurately reflect API capabilities
  - Ensure consistent validation with helpful error messages

  ## Current Issues

  Based on API review and testing, the following specific issues exist in the Item Search tools:

  1. **Search Term Syntax**:
     - Search term requirements and syntax are not clearly documented
     - Search operators (AND, OR, NOT) usage isn't well explained
     - Exact match vs. partial match behavior isn't clarified
     - Missing examples of complex search queries

  2. **Field-Specific Search Limitations**:
     - Field-specific search constraints are not well documented
     - Searchable vs. non-searchable fields aren't clearly identified
     - Type-specific search considerations (date, number, text) lack examples
     - Error messages don't explain field limitations

  3. **Pagination Handling**:
     - Pagination parameter requirements aren't consistent
     - Documentation doesn't clearly explain result limits
     - Missing examples of navigating large result sets
     - Inconsistent parameter naming between tools

  4. **Result Formatting**:
     - Result structure is not clearly documented
     - Missing explanation of response fields and their meaning
     - No guidance on handling empty results
     - Inconsistent field mapping descriptions

  ## API Documentation Reference

  The Pipedrive API documentation in `ai_docs/pipedrive_item_search.md` provides the following relevant information:

  - Item search allows searching across different entity types
  - Search terms follow specific syntax rules
  - Field-specific search has particular requirements
  - Pagination follows certain patterns

  ## Implementation Plan
  
  ### 1. Tool Updates

  Update all item search feature tools:
  1. `item_field_search_tool.py`
  2. `item_search_tool.py`

  ### 2. Specific Improvements

  #### Search Term Syntax
  - Update documentation to clearly explain search term syntax and operators
  - Add examples of simple and complex search queries
  - Clarify exact match vs. partial match behavior
  - Improve error messages for invalid search syntax
  
  #### Field-Specific Search
  - Document searchable fields for each entity type
  - Clarify type-specific search considerations
  - Add examples of field-specific searches
  - Implement validation for field search parameters
  
  #### Pagination Handling
  - Standardize pagination parameter names and usage
  - Document result limit constraints
  - Include examples of paginated searches
  - Add clear explanations of response metadata
  
  #### Result Formatting
  - Document search result structure thoroughly
  - Add guidance on interpreting results
  - Clarify field mappings in responses
  - Include examples of processing different result types

  ## Testing Strategy

  **RUN THIS BEFORE IMPLEMENTING TO CONFIRM WHAT THE API EXPECTS**
  
  A systematic testing approach will be used:
  the pipedrive api token is in .env

  1. **API Testing Script**:
     ```bash
     # Sample testing commands for Item Search API
     # Test basic search
     curl -X GET "https://api.pipedrive.com/v1/itemSearch?term=test" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN"
     
     # Test field search
     curl -X GET "https://api.pipedrive.com/v1/itemSearch/field?term=test&field_type=dealField&field_key=title&exact_match=0" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN"
     
     # Test with pagination
     curl -X GET "https://api.pipedrive.com/v1/itemSearch?term=test&start=0&limit=10" \
       -H "Authorization: Bearer $PIPEDRIVE_API_TOKEN"
     ```

  2. **Verification Process**:
     - Test search queries with various syntax to determine behavior
     - Document field search capabilities for different entity types
     - Test pagination behavior with different parameters
     - Analyze response structures for documentation
  
  3. **Tool Testing**:
     - After implementation, test each tool through the MCP interface
     - Verify that search parameter validation works as expected
     - Check that error messages are helpful and accurate
     - Ensure documentation matches actual behavior

  ## Success Criteria
  
  The implementation will be successful when:
  1. Search term syntax is clearly documented with examples
  2. Field-specific search capabilities are accurately described
  3. Pagination parameters work consistently
  4. Documentation accurately reflects API capabilities
  5. Error messages provide clear guidance on proper usage
  6. All item search tools pass integration tests with the API

  ## Benefits
  
  These improvements will provide:
  1. Clearer developer experience when working with search capabilities
  2. Better understanding of search syntax and operators
  3. More effective field-specific searching
  4. Improved handling of large result sets
  5. Consistent validation preventing common errors
  6. Documentation that accurately reflects API behavior

  ## Dependencies
  
  This implementation depends on:
  1. Pipedrive API documentation in `ai_docs/pipedrive_item_search.md`
  2. Response formatting utilities in `pipedrive/api/features/shared/utils.py`

  ## Timeline
  
  Estimated implementation: 2 days
  - Day 1: API testing and documentation review
  - Day 2: Implementation, testing and validation