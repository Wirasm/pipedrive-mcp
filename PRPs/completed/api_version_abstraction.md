name: "API Version Abstraction"
description: |

  ## Goal
  Create an abstraction layer for handling different Pipedrive API versions in the base client. This will allow feature-specific clients to seamlessly work with both v1 and v2 endpoints without duplicating code or implementing temporary workarounds.

  ## Why
  - Pipedrive's API has endpoints in both v1 and v2 with some features only available in one version
  - Our current client architecture is optimized for v2 API endpoints
  - We need a consistent way to work with both API versions (v1 and v2)
  - This abstraction will reduce code duplication and simplify future implementations
  - Current use case: Leads API uses v1 endpoints while our existing client targets v2

  ## What
  This PRP will:
  1. Refactor the BaseClient to support version-specific endpoint construction
  2. Add version specification capability to request methods
  3. Create utilities for handling format differences between API versions
  4. Update existing clients to use the new abstraction (if needed)
  
  ## Endpoints to Consider
  
  **v1 Endpoints coming soon**
  - `/v1/leads`, `/v1/leadLabels`, `/v1/leadSources` (with Lead feature)
  - Any other v1-specific endpoints in future features
  
  **v2 Endpoints**
  - `/api/v2/deals`, `/api/v2/persons`, etc. (existing implementation)
  - Any future v2 endpoints
  
  ## Current Implementation
  The current BaseClient always constructs URLs with `/api/v2/` prefix bit we will soo implement v1 endpoints with the leads feature:
  
  ```python
  # In BaseClient.__init__
  self.base_url = f"https://{company_domain}.pipedrive.com/api/v2"
  
  # In BaseClient.request
  url = f"{self.base_url}{endpoint}"
  ```
  
  This works fine for v2 endpoints but requires workarounds for v1 endpoints.

  ## Proposed Solution

  ### Enhanced BaseClient
  
  Modify BaseClient to support version specification:
  
  ```python
  class BaseClient:
      def __init__(self, api_token: str, company_domain: str, http_client: httpx.AsyncClient):
          # ... existing initialization ...
          self.domain = f"https://{company_domain}.pipedrive.com"
          # Default to v2 for backward compatibility
          self.api_version = "v2"
      
      def get_url(self, endpoint: str, version: Optional[str] = None) -> str:
          """
          Construct URL with proper version prefix.
          
          Args:
              endpoint: API endpoint (e.g., /deals)
              version: API version to use (v1 or v2), defaults to client's default version
              
          Returns:
              Fully qualified URL
          """
          version = version or self.api_version
          
          if version == "v2":
              return f"{self.domain}/api/v2{endpoint}"
          elif version == "v1":
              return f"{self.domain}/v1{endpoint}"
          else:
              raise ValueError(f"Unsupported API version: {version}")
              
      async def request(
          self,
          method: str,
          endpoint: str,
          query_params: Optional[Dict[str, Any]] = None,
          json_payload: Optional[Dict[str, Any]] = None,
          version: Optional[str] = None,
      ) -> Dict[str, Any]:
          """
          Make a request to the Pipedrive API with version control
          
          Args:
              method: HTTP method (GET, POST, PATCH, DELETE)
              endpoint: API endpoint (e.g., /persons)
              query_params: URL query parameters
              json_payload: JSON request body
              version: API version to use (v1 or v2), defaults to client's default version
          """
          url = self.get_url(endpoint, version)
          # ... rest of the implementation remains the same ...
  ```

  ## Key Benefits
  
  1. **Simplicity**: Client code can specify API version directly in requests
  2. **Consistency**: Uniform approach for all API endpoints
  3. **Backward Compatibility**: Default behavior preserves existing v2 functionality
  4. **Flexibility**: Feature-specific clients can mix and match v1/v2 endpoints as needed
  
  ## Usage Examples
  
  ### In Feature-Specific Clients
  
  ```python
  class LeadClient:
      def __init__(self, base_client: BaseClient):
          self.base_client = base_client
          
      async def create_lead(self, title: str, ...):
          """Create a new lead in Pipedrive"""
          payload = {"title": title, ...}
          # Explicitly use v1 for this endpoint
          return await self.base_client.request("POST", "/leads", json_payload=payload, version="v1")
          
      async def search_leads(self, term: str, ...):
          """Search for leads in Pipedrive"""
          # This endpoint is available in v2
          return await self.base_client.request("GET", "/leads/search", 
                                               query_params={"term": term, ...}, 
                                               version="v2")
  ```
  
  ### Setting Default Version
  
  For clients that work primarily with one version:
  
  ```python
  class LeadClient:
      def __init__(self, base_client: BaseClient):
          self.base_client = base_client
          # Store original version to restore after
          self._original_version = self.base_client.api_version
          # Set default version for this client
          self.base_client.api_version = "v1"
          
      # Methods that use the default version automatically
      
      def __del__(self):
          # Restore original version when client is destroyed
          if hasattr(self, "base_client") and hasattr(self, "_original_version"):
              self.base_client.api_version = self._original_version
  ```
  
  ## Implementation Plan
  
  1. Refactor BaseClient:
     - Add domain and api_version properties
     - Implement get_url method
     - Update request method to accept version parameter
     
  2. Create utils for version-specific format handling:
     - Add version-specific response parsing if needed
     - Handle data format differences between v1 and v2
     
  3. Update existing clients (if needed):
     - Ensure existing code works with the new abstraction
     - Add version parameters where appropriate
     
  4. Add tests:
     - Test URL construction with different versions
     - Test requests to both v1 and v2 endpoints
     - Ensure backward compatibility
     
  ## Migration Strategy
  
  - Implement changes in BaseClient with default behavior matching current implementation
  - Update existing tests to verify behavior doesn't change
  - Add new tests for v1 endpoint handling
  - Document the new functionality and provide usage examples

  ## Implementation Notes
  
  1. Any feature-specific client can use either v1 or v2 endpoints as needed
  2. The default version remains v2 for backward compatibility
  3. Custom format handling may be needed for some endpoints due to response structure differences
  4. Consider adding version-specific adapter methods if format differences are substantial
  
  ## Validation Gates
  
  - All existing tests must pass with the refactored BaseClient
  - New tests must verify v1 endpoint URL construction
  - Test both v1 and v2 API responses
  - Run `uv run pytest` to ensure all tests pass
  
  ## Files to Modify
  
  1. `pipedrive/api/base_client.py` - Add version handling
  2. `pipedrive/api/pipedrive_client.py` - Update if needed to maintain compatibility
  3. Test files for both components

  ## Future Considerations
  
  - Handling API deprecations and migrations
  - Version-specific error handling or response parsing
  - Automatic API version detection or negotiation