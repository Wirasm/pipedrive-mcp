from typing import Any, Dict, Optional


# Custom Exception for Pipedrive API errors
class PipedriveAPIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_info: Optional[str] = None,
        response_data: Optional[
            Dict[str, Any]
        ] = None,  # Changed from Dict to Dict[str, Any]
    ):
        super().__init__(message)
        self.status_code = status_code
        self.error_info = error_info
        self.response_data = response_data

    def __str__(self):
        base_message = super().__str__()
        details = []
        if self.status_code is not None:
            details.append(f"Status: {self.status_code}")
        if self.error_info:
            details.append(f"Info: {self.error_info}")
        if self.response_data:
            details.append(
                f"Response Data Keys: {list(self.response_data.keys()) if isinstance(self.response_data, dict) else 'Present'}"
            )
        return f"PipedriveAPIError: {base_message} ({', '.join(details)})"
