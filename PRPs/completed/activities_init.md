name: "Activities API MCP Tools"
description: |

  ## Goal
  Implement a complete set of MCP tools for managing activities in Pipedrive. This project will create tools for:
  1. Getting all activities (with filtering options)
  2. Getting activity details
  3. Creating an activity
  4. Updating an activity
  5. Deleting an activity
  6. Getting all activity types
  7. Creating a custom activity type

  ## Why
  - Provide a complete CRUD interface for Activity entity management through MCP
  - Allow Claude to interact with the Pipedrive calendar and task management system
  - Continue the vertical slice architecture pattern established with Person and Deal entities
  - Enable scheduling and tracking of appointments, tasks, calls, and other activities related to deals, leads, persons, and organizations

  ## What
  Activities in Pipedrive represent appointments, tasks, calls, meetings, and other calendar events that can be associated with deals, leads, persons, and organizations. They are a critical part of CRM workflow management, allowing users to schedule follow-ups, track customer interactions, and manage their daily work.

  This implementation will provide tools to:
  - List and filter activities
  - Get details of specific activities
  - Create new activities of various types
  - Update existing activities (including marking them as done)
  - Delete activities
  - Work with activity types

  ## Endpoints to Implement
  
  **Get All Activities**
  - GET /api/v2/activities
  - Returns all activities with optional filtering and pagination
  
  **Get Activity Details**
  - GET /api/v2/activities/{id}
  - Returns the details of a specific activity with optional fields
  
  **Create Activity**
  - POST /api/v2/activities
  - Creates a new activity with the provided details
  
  **Update Activity**
  - PATCH /api/v2/activities/{id}
  - Updates the properties of an activity
  
  **Delete Activity**
  - DELETE /api/v2/activities/{id}
  - Marks an activity as deleted
  
  **Get Activity Types**
  - GET /v1/activityTypes
  - Returns all activity types
  
  **Add Activity Type**
  - POST /v1/activityTypes
  - Adds a new custom activity type

  ## Current exact directory structure
  ```
  ├── pipedrive
  │   ├── api
  │   │   ├── features
  │   │   │   ├── deals
  │   │   │   │   ├── client
  │   │   │   │   ├── models
  │   │   │   │   └── tools
  │   │   │   ├── persons
  │   │   │   │   ├── client
  │   │   │   │   ├── models
  │   │   │   │   └── tools
  │   │   │   ├── organizations
  │   │   │   │   ├── client
  │   │   │   │   ├── models
  │   │   │   │   └── tools
  │   │   │   ├── leads
  │   │   │   │   ├── client
  │   │   │   │   ├── models
  │   │   │   │   └── tools
  │   │   │   ├── item_search
  │   │   │   │   ├── client
  │   │   │   │   ├── models
  │   │   │   │   └── tools
  │   │   │   └── shared
  │   │   │       ├── conversion
  │   │   │       └── utils.py
  ```

  ## Proposed Directory Structure
  ```
  ├── pipedrive
  │   ├── api
  │   │   ├── features
  │   │   │   ├── activities
  │   │   │   │   ├── __init__.py
  │   │   │   │   ├── activities_tool_registry.py
  │   │   │   │   ├── client
  │   │   │   │   │   ├── __init__.py
  │   │   │   │   │   ├── activity_client.py
  │   │   │   │   │   └── tests
  │   │   │   │   │       ├── __init__.py
  │   │   │   │   │       └── test_activity_client.py
  │   │   │   │   ├── models
  │   │   │   │   │   ├── __init__.py
  │   │   │   │   │   ├── activity.py
  │   │   │   │   │   ├── activity_type.py
  │   │   │   │   │   └── tests
  │   │   │   │   │       ├── __init__.py
  │   │   │   │   │       ├── test_activity.py
  │   │   │   │   │       └── test_activity_type.py
  │   │   │   │   └── tools
  │   │   │   │       ├── __init__.py
  │   │   │   │       ├── activity_create_tool.py
  │   │   │   │       ├── activity_get_tool.py
  │   │   │   │       ├── activity_list_tool.py
  │   │   │   │       ├── activity_update_tool.py
  │   │   │   │       ├── activity_delete_tool.py
  │   │   │   │       ├── activity_type_list_tool.py
  │   │   │   │       ├── activity_type_create_tool.py
  │   │   │   │       └── tests
  │   │   │   │           ├── __init__.py
  │   │   │   │           ├── test_activity_create_tool.py
  │   │   │   │           ├── test_activity_get_tool.py
  │   │   │   │           ├── test_activity_list_tool.py
  │   │   │   │           ├── test_activity_update_tool.py
  │   │   │   │           ├── test_activity_delete_tool.py
  │   │   │   │           ├── test_activity_type_list_tool.py
  │   │   │   │           └── test_activity_type_create_tool.py
  ```

  ## Files to Reference
  - ai_docs/pipedrive_activities.md (read_only) (detailed API reference for Activities endpoints)
  - pipedrive/api/features/deals/ (directory to MIRROR for activities implementation)
  - pipedrive/api/features/persons/client/person_client.py (reference for client implementation)
  - pipedrive/api/features/deals/client/deal_client.py (reference for client implementation)
  - pipedrive/api/features/deals/models/deal.py (reference for model implementation)
  - pipedrive/api/features/deals/tools/deal_create_tool.py (reference for tool implementation)
  - pipedrive/api/features/shared/conversion/id_conversion.py (for ID validation)
  - pipedrive/api/features/shared/utils.py (for response formatting)
  - pipedrive/api/features/tool_registry.py (for feature registry)
  - pipedrive/api/features/tool_decorator.py (for feature-aware tool decorator)
  - pipedrive/mcp_instance.py (for MCP server configuration)

  ## Files to Implement (concept)
  
  ### Models
  1. `activity.py` - Pydantic model representing an activity
     ```python
     class Activity(BaseModel):
         """Activity entity model with Pydantic validation"""
         id: Optional[int] = None
         subject: str
         type: str
         due_date: Optional[str] = None
         due_time: Optional[str] = None
         duration: Optional[str] = None
         # Additional fields...
         
         def to_api_dict(self) -> Dict[str, Any]:
             """Convert to API-compatible dictionary"""
             # Implementation...
         
         @classmethod
         def from_api_dict(cls, data: Dict[str, Any]) -> 'Activity':
             """Create Activity from API response dictionary"""
             # Implementation...
     ```

  2. `activity_type.py` - Pydantic model for activity types
     ```python
     class ActivityType(BaseModel):
         """Activity type model with Pydantic validation"""
         id: Optional[int] = None
         name: str
         icon_key: str
         color: Optional[str] = None
         # Additional fields...
         
         def to_api_dict(self) -> Dict[str, Any]:
             """Convert to API-compatible dictionary"""
             # Implementation...
         
         @classmethod
         def from_api_dict(cls, data: Dict[str, Any]) -> 'ActivityType':
             """Create ActivityType from API response dictionary"""
             # Implementation...
     ```

  ### Client
  1. `activity_client.py` - API client with methods for all activity operations
     ```python
     class ActivityClient:
         """Client for Pipedrive Activity API endpoints"""
         
         def __init__(self, base_client: BaseClient):
             self.base_client = base_client
         
         async def create_activity(self, activity_data: Dict[str, Any]) -> Dict[str, Any]:
             """Create a new activity in Pipedrive"""
             # Implementation...
         
         async def get_activity(self, activity_id: int) -> Dict[str, Any]:
             """Get activity by ID from Pipedrive"""
             # Implementation...
             
         async def list_activities(self, filter_params: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Optional[str]]:
             """List activities with filtering and pagination"""
             # Implementation...
             
         async def update_activity(self, activity_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
             """Update an existing activity"""
             # Implementation...
             
         async def delete_activity(self, activity_id: int) -> Dict[str, Any]:
             """Delete an activity"""
             # Implementation...
             
         async def get_activity_types(self) -> List[Dict[str, Any]]:
             """Get all activity types"""
             # Implementation...
             
         async def create_activity_type(self, type_data: Dict[str, Any]) -> Dict[str, Any]:
             """Create a new activity type"""
             # Implementation...
     ```

  ### Tools
  1. `activity_create_tool.py` - Create a new activity
  2. `activity_get_tool.py` - Get activity details
  3. `activity_list_tool.py` - List/get all activities with filtering
  4. `activity_update_tool.py` - Update an activity
  5. `activity_delete_tool.py` - Delete an activity
  6. `activity_type_list_tool.py` - Get all activity types
  7. `activity_type_create_tool.py` - Create a new activity type

  ### Feature Registry
  1. `activities_tool_registry.py` - Register the activities feature and its tools

  ## Implementation Notes
  
  ### Activity Models
  - The Activity model should include all essential fields: subject, type, owner_id, due_date, due_time, duration, busy flag, done flag, etc.
  - Include fields for associated entities: deal_id, lead_id, person_id, org_id
  - The ActivityType model should include fields: name, icon_key, color, order_nr
  - Both models need proper validation with Pydantic
  - Implement to_api_dict() and from_api_dict() methods for API data conversion

  ### Activity Client
  - For the list_activities method, handle cursor-based pagination correctly
  - Support all filtering parameters: filter_id, owner_id, deal_id, person_id, org_id, etc.
  - The get_activity_types and create_activity_type methods should use the v1 API endpoints
  - All methods should have proper error handling and logging

  ### Activity Tools
  - **create_activity_in_pipedrive**
    - Required parameters: subject, type
    - Optional parameters: owner_id_str, due_date, due_time, duration, busy, done, etc.
    - Requires one of: deal_id_str, lead_id, person_id_str, org_id_str
    - Return created activity details

  - **get_activity_from_pipedrive**
    - Required parameter: id_str
    - Optional parameters: include_fields_str (comma-separated)
    - Return activity details

  - **list_activities_from_pipedrive**
    - Optional parameters: filter_id_str, owner_id_str, deal_id_str, etc.
    - Support pagination with limit and cursor
    - Return list of activities and next_cursor

  - **update_activity_in_pipedrive**
    - Required parameters: id_str, at least one field to update
    - Optional parameters: subject, type, due_date, etc.
    - Return updated activity details

  - **delete_activity_from_pipedrive**
    - Required parameter: id_str
    - Return success response

  - **get_activity_types_from_pipedrive**
    - No required parameters
    - Return list of activity types

  - **create_activity_type_in_pipedrive**
    - Required parameters: name, icon_key
    - Optional parameters: color, order_nr
    - Return created activity type details

  ### Feature Registry
  - Register the activities feature using FeatureMetadata
  - Register all activity tools with the feature

  ## Validation Gates
  - Each model must have proper Pydantic validation
  - Each client method must handle API errors gracefully
  - Each tool must validate all inputs, especially ID conversions
  - Follow the tool_decorator pattern for feature-aware tools
  - All tests must pass when running `uv run pytest`
  - The implementation should be registered with the feature registry system

  ## Implementation Checkpoints/Testing
  
  ### 1. Models & Client
  - Implement Activity and ActivityType models with validation
  - Implement ActivityClient with all required methods
  - Write unit tests for models and client

  ### 2. Basic Activity Tools
  - Implement activity CRUD tools (create, get, list, update, delete)
  - Write tests for each tool

  ### 3. Activity Type Tools
  - Implement activity type tools (list, create)
  - Write tests for each tool

  ### 4. Feature Registry & Integration
  - Create activities_tool_registry.py to register the feature and tools
  - Update any necessary server code
  - Test the complete feature with the registry system

  ## Other Considerations
  
  - Activity types are an important part of the Pipedrive system. Each activity must have a valid type.
  - The v1 API is used for activity types, while v2 is used for activities.
  - Activities can be linked to deals, leads, persons, and organizations, making them a central part of CRM workflows.
  - Support for location data, attendees, and conference links would be valuable additions.
  - Activity due_date and due_time are separate fields in the API.
  - Activities can be marked as "done" to track completion of tasks.