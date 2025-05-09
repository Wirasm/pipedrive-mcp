import json
from typing import Any, Optional


def format_tool_response(
    success: bool, data: Optional[Any] = None, error_message: Optional[str] = None
) -> str:
    return json.dumps(
        {"success": success, "data": data, "error": error_message}, indent=2
    )
