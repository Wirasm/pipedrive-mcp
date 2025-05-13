name: "MCP Tool Documentation and Parameter Handling Improvement"
description: |

  ## Goal
  Standardize and improve MCP tool documentation, parameter handling, and error messaging across all Pipedrive API features to ensure a consistent and clear interface for clients that are consuming our tools.

  ## Why
  - Clients and their LLMS are experiencing confusion when using Pipedrive MCP tools due to inconsistent parameter naming, unclear documentation, and insufficient error messages
  - There are discrepancies between tool documentation and actual API requirements
  - Parameter validation occurs too late in the process, causing cryptic errors
  - Tool descriptions lack clear examples and format requirements
  - Inconsistent parameter naming conventions (_str suffix pattern) create confusion

  ## What
  This PRP proposes a comprehensive overhaul of the MCP tool interfaces including:
  - Standardized docstring format with clear parameter descriptions and examples
  - Improved parameter naming conventions
  - Consistent validation patterns with helpful error messages
  - Enhanced documentation with explicit format requirements and examples
  - Implementation of parameter schema clarification for all tools

  ## Current Issues
  
  1. **Inconsistent Parameter Naming**
   - Some parameters use _str suffix (e.g., owner_id_str) while others don't (e.g., lead_id)
   - No clear convention for distinguishing numeric IDs from UUID strings
   - Confusing for users to remember which format each ID parameter requires

  2. **Unclear Format Requirements**
   - Documentation for time-related fields (due_time, duration) doesn't sufficiently emphasize format requirements
   - Boolean parameters don't specify acceptable format (true/false vs. True/False)
   - Location parameter is documented as a string but the API expects an array or null

  3. **Required vs. Optional Parameters**
   - Some parameters documented as optional behave as required (e.g., subject and type when updating activities)
   - Validation errors don't clearly indicate which parameters are truly required

  4. **Inconsistent ID Handling**
   - Numeric IDs are handled differently from UUID strings
   - No clear distinction in documentation between these types

  5. **Poor Error Messages**
   - Error messages don't provide enough guidance on correct formats
   - Validation failures at the API level return cryptic errors

  ## Current Implementation Pattern

  Current tool implementation follows this pattern:

  ```python
  @tool("feature_name")
  async def action_entity_in_pipedrive(
      ctx: Context,
      required_param: str,
      optional_param_str: Optional[str] = None,
  ) -> str:
      """Short description of what the tool does.

      This tool does something with the Pipedrive API.

      args:
      ctx: Context
      required_param: str - Brief description
      optional_param_str: Optional[str] = None - Brief description
      """
      # Parameter sanitization
      optional_param_str = None if optional_param_str == "" else optional_param_str
      
      pd_mcp_ctx: PipedriveMCPContext = ctx.request_context.lifespan_context
      
      # ID conversion with error handling
      optional_param, error = convert_id_string(optional_param_str, "optional_param")
      if error:
          return format_tool_response(False, error_message=error)
      
      try:
          # Model creation and validation
          entity = Entity(required_param=required_param, optional_param=optional_param)
          
          # Convert to API payload
          payload = entity.to_api_dict()
          
          # API call
          result = await pd_mcp_ctx.pipedrive_client.feature.action_entity(**payload)
          
          # Return formatted response
          return format_tool_response(True, data=result)
          
      except ValidationError as e:
          return format_tool_response(False, error_message=f"Validation error: {str(e)}")
      except PipedriveAPIError as e:
          return format_tool_response(False, error_message=f"Pipedrive API error: {str(e)}")
      except Exception as e:
          return format_tool_response(False, error_message=f"An unexpected error occurred: {str(e)}")
  ```

  ## Proposed Solution

  ### 1. Standardized Docstring Format

  Adopt a comprehensive, consistent docstring format across all tools:

  ```python
  @tool("feature_name")
  async def action_entity_in_pipedrive(
      ctx: Context,
      required_param: str,
      id_param: Optional[str] = None,
      boolean_param: Optional[bool] = None,
  ) -> str:
      """One-line summary of what the tool does.

      Detailed multi-line description explaining the purpose and key functionality.
      Highlight important information or constraints.

      Format requirements:
      - id_param: Must be a numeric string (e.g., "123")
      - time_params: Must use HH:MM:SS format (e.g., "14:30:00")
      - boolean_params: Use lowercase true/false

      Example:
      ```
      action_entity_in_pipedrive(
          required_param="Example value",
          id_param="123",
          boolean_param=true
      )
      ```

      Args:
          ctx: Context object provided by the MCP server
          required_param: Clear description with format requirements if applicable
          id_param: Numeric ID of the entity. Must be a positive integer as a string (e.g., "123")
          boolean_param: Whether to enable a feature. Use lowercase true/false

      Returns:
          JSON formatted response with success/failure status and data or error message
      """
  ```

  ### 2. Parameter Naming Conventions

  Standardize parameter naming conventions:

  - For integer IDs: `entity_id` (not `entity_id_str`) - Document as "string containing an integer"
  - For UUID strings: `entity_id` - Document as "string in UUID format"
  - For all parameters: Use clear, consistent names that match Pipedrive API fields
  - For time parameters: Always document exact format requirements (e.g., "HH:MM:SS")

  ### 3. Consistent Validation Patterns

  Implement consistent validation with better error messages:

  ```python
  # ID conversion with improved error messages
  def convert_id(id_str: Optional[str], field_name: str) -> Tuple[Optional[int], Optional[str]]:
      """Convert string ID to integer with helpful error message"""
      if id_str is None or not id_str.strip():
          return None, None
          
      try:
          value = int(id_str)
          if value <= 0:
              return None, f"{field_name} must be a positive integer (received: {id_str})"
          return value, None
      except ValueError:
          return None, f"{field_name} must be a numeric string (received: {id_str})"
  ```

  ### 4. Enhanced Error Handling

  Improve error messages to provide clear guidance:

  ```python
  # Field format validation with example
  if validation_error:
      error_message = f"Invalid {field_name} format: '{value}'. Expected format: {example_format}"
      return format_tool_response(False, error_message=error_message)
  ```

  ### 5. Parameter Schema Documentation

  For each tool, include explicit schema information in documentation, especially for complex objects:

  ```python
  # Example documentation for nested objects
  """
  location: Location information in one of these formats:
    - String address ("123 Main St, City")
    - JSON object with address field: {"address": "123 Main St, City"}
  """
  ```

  ## Files to Modify

  ### Base Utility Files
  
  1. `pipedrive/api/features/shared/conversion/id_conversion.py` - Enhanced conversion utilities
  2. `pipedrive/api/features/shared/utils.py` - Add docstring utilities and validation helpers

  ### Docstring and Tool Decorator
  
  1. `pipedrive/api/features/tool_decorator.py` - Enhanced decorator with docstring processing
  
  ### Tool Implementation Files
  
  Update all tool files across features to use the new format:
  
  1. Persons feature tools (5 files)
  2. Organizations feature tools (8 files)
  3. Deals feature tools (9 files)
  4. Leads feature tools (9 files)
  5. Activities feature tools (7 files)
  6. Item Search feature tools (2 files)

  ## Implementation Plan

  The implementation will be phased to minimize disruption:

  ### Phase 1: Utilities and Helpers
  
  1. Enhance `id_conversion.py` with improved error messages and examples
  2. Add docstring utilities to `utils.py` for consistent documentation
  3. Update `tool_decorator.py` to support enhanced docstring processing

  ### Phase 2: Documentation Standards
  
  1. Create templates and examples for each type of tool (create, read, update, delete)
  2. Develop a documentation style guide for all tool parameters

  ### Phase 3: Tool Updates
  
  1. Update each tool to use the improved docstrings and validation patterns
  2. Ensure parameter naming is consistent across all tools
  3. Add examples for each tool

  ### Phase 4: Testing and Validation
  
  1. Test tools with Claude to ensure clarity and usability
  2. Validate that all error messages are clear and actionable
  3. Create comprehensive tool documentation for Claude

  ## Implementation Details

  ### 1. Enhanced ID Conversion Utility
  
  ```python
  # pipedrive/api/features/shared/conversion/id_conversion.py
  from typing import Optional, Tuple, Union
  import re
  import uuid

  def convert_id_string(id_str: Optional[str], field_name: str, 
                       example: str = "123") -> Tuple[Optional[int], Optional[str]]:
      """
      Convert a string ID to an integer, with improved error handling.
      
      Args:
          id_str: String ID to convert
          field_name: Name of the field for error messages
          example: Example of valid format for error message
          
      Returns:
          Tuple of (converted_id, error_message)
          If conversion succeeds, error_message is None
          If conversion fails, converted_id is None and error_message contains the error
      """
      if id_str is None or not id_str.strip():
          return None, None
          
      try:
          value = int(id_str)
          if value <= 0:
              return None, f"{field_name} must be a positive integer. Example: '{example}'"
          return value, None
      except ValueError:
          return None, f"{field_name} must be a numeric string. Example: '{example}'"

  def validate_uuid_string(uuid_str: Optional[str], field_name: str, 
                          example: str = "123e4567-e89b-12d3-a456-426614174000") -> Tuple[Optional[str], Optional[str]]:
      """
      Validate a string as a valid UUID, with improved error handling.
      
      Args:
          uuid_str: String UUID to validate
          field_name: Name of the field for error messages
          example: Example of valid format for error message
          
      Returns:
          Tuple of (validated_uuid, error_message)
          If validation succeeds, error_message is None
          If validation fails, validated_uuid is None and error_message contains the error
      """
      if uuid_str is None or not uuid_str.strip():
          return None, None
      
      # UUID pattern (RFC 4122)
      uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
      
      try:
          # First check with regex for performance
          if not re.match(uuid_pattern, uuid_str.lower()):
              return None, f"{field_name} must be a valid UUID string. Example: '{example}'"
          
          # Then validate with the uuid module for completeness
          uuid_obj = uuid.UUID(uuid_str)
          return str(uuid_obj), None
      except ValueError:
          return None, f"{field_name} must be a valid UUID string. Example: '{example}'"
  ```

  ### 2. Documentation Helper Utilities
  
  ```python
  # pipedrive/api/features/shared/utils.py
  import json
  from typing import Any, Dict, List, Optional
  from datetime import date, datetime

  class DateTimeEncoder(json.JSONEncoder):
      """Custom JSON encoder that can handle dates and datetimes."""
      def default(self, obj):
          if isinstance(obj, (date, datetime)):
              return obj.isoformat()
          return super().default(obj)

  def format_tool_response(
      success: bool, data: Optional[Any] = None, error_message: Optional[str] = None
  ) -> str:
      """
      Format a consistent JSON response for tool results.
      
      Args:
          success: Whether the operation was successful
          data: The data to return on success
          error_message: The error message to return on failure
          
      Returns:
          JSON formatted string with success status and data or error
      """
      return json.dumps(
          {"success": success, "data": data, "error": error_message}, 
          indent=2,
          cls=DateTimeEncoder
      )

  def format_validation_error(
      field_name: str, value: str, expected_format: str, example: str
  ) -> str:
      """
      Create a consistent validation error message with example.
      
      Args:
          field_name: Name of the field that failed validation
          value: The invalid value provided
          expected_format: Description of the expected format
          example: Example of valid value
          
      Returns:
          Formatted error message
      """
      return f"Invalid {field_name} format: '{value}'. {expected_format} Example: '{example}'"
  ```

  ### 3. Sample Tool Implementation with New Standards
  
  ```python
  # Example update for an activity creation tool
  @tool("activities")
  async def create_activity_in_pipedrive(
      ctx: Context,
      subject: str,
      type: str,
      owner_id: Optional[str] = None,
      deal_id: Optional[str] = None,
      lead_id: Optional[str] = None,
      person_id: Optional[str] = None,
      org_id: Optional[str] = None,
      due_date: Optional[str] = None,
      due_time: Optional[str] = None,
      duration: Optional[str] = None,
      busy: Optional[bool] = None,
      done: Optional[bool] = None,
      note: Optional[str] = None,
      location: Optional[str] = None,
      public_description: Optional[str] = None,
      priority: Optional[str] = None,
  ) -> str:
      """Creates a new activity in Pipedrive CRM.

      This tool creates a new activity with the specified attributes. Activities track
      tasks, calls, meetings, and other events in Pipedrive.

      Format requirements:
      - All ID fields: Must be numeric strings (e.g., "123")
      - lead_id: Must be a UUID string (e.g., "123e4567-e89b-12d3-a456-426614174000")
      - due_date: Must be in YYYY-MM-DD format (e.g., "2025-01-15")
      - due_time: Must be in HH:MM:SS format (e.g., "14:30:00")
      - duration: Must be in HH:MM:SS format (e.g., "01:00:00")
      - busy, done: Boolean values as lowercase 'true' or 'false'
      - location: A string containing the location address

      Example:
      ```
      create_activity_in_pipedrive(
          subject="Call with client",
          type="call",
          owner_id="123",
          person_id="456",
          due_date="2025-01-15",
          due_time="14:30:00",
          duration="01:00:00",
          busy=true
      )
      ```

      Args:
          ctx: Context object provided by the MCP server
          subject: The subject or title of the activity
          type: The type of activity (must match a valid activity type key)
          owner_id: Numeric ID of the user who owns the activity
          deal_id: Numeric ID of the deal linked to the activity
          lead_id: UUID string of the lead linked to the activity
          person_id: Numeric ID of the person linked to the activity
          org_id: Numeric ID of the organization linked to the activity
          due_date: Due date in YYYY-MM-DD format
          due_time: Due time in HH:MM:SS format (must include seconds)
          duration: Duration in HH:MM:SS format (must include seconds)
          busy: Whether the activity marks the assignee as busy (true/false)
          done: Whether the activity is marked as done (true/false)
          note: Additional notes for the activity
          location: Location of the activity as a string
          public_description: Public description of the activity
          priority: Priority of the activity as a numeric string (e.g., "1")

      Returns:
          JSON formatted response with the created activity data or error message
      """
      # Rest of implementation...
  ```

  ## Validation Gates
  
  - All tools must follow the new documentation standard
  - All parameter names must be consistent across similar functions
  - Error messages must include expected format and examples
  - Documentation must accurately reflect API requirements
  - Tools should validate parameters early with clear error messages
  - Type hints should accurately reflect the expected types
  - Each tool must have at least one usage example

  ## Testing Strategy
  
  1. Create a test script that invokes each tool with:
     - Valid parameters
     - Missing required parameters
     - Invalid format parameters
  
  2. Verify that error messages are clear and helpful
  
  3. Test tools with Claude to ensure it understands how to use them
  
  4. Review docstrings for accuracy and completeness

  ## Backwards Compatibility
  
  - Original parameter names will be maintained for now but with improved documentation
  - Improved error messages will be fully backward compatible
  - Future PRPs may propose full parameter renaming with deprecation notices

  ## Implementation Checkpoints
  
  ### 1. Utility Functions Update
  - Enhance ID conversion with examples
  - Add docstring utilities
  - Verify better error messages 
  
  ### 2. Parameter Documentation Standards
  - Create documentation templates
  - Update sample tool implementations
  - Verify docstring parsing
  
  ### 3. Tool Updates (per feature)
  - Update all tools in a feature module
  - Test with various inputs
  - Verify error message clarity