"""JSON serialization utilities for OpenStudio MCP Server."""

import json
from typing import Any


def ensure_json_response(result: Any) -> str:
    """
    Ensures that the result is returned as a valid JSON string.

    Handles raw Python lists/dicts by serializing them properly.
    Prevents JSON parsing errors in Claude Desktop caused by Python
    string representations (e.g., ['item'] vs ["item"]).

    Args:
        result: Any Python object (dict, list, str, etc.)

    Returns:
        Properly JSON-serialized string

    Examples:
        >>> ensure_json_response({"status": "success", "data": [1, 2, 3]})
        '{"status": "success", "data": [1, 2, 3]}'

        >>> ensure_json_response("Simple message")
        '{"status": "success", "message": "Simple message"}'
    """
    try:
        # If it's already a string, try to parse it to see if it's valid JSON
        if isinstance(result, str):
            try:
                json.loads(result)
                return result  # It's valid JSON string
            except json.JSONDecodeError:
                # It's a raw string message, wrap it
                return json.dumps({"status": "success", "message": result}, indent=2)

        # If it's a list, dict, or other object, serialize it properly
        # Use default=str to handle objects that aren't normally JSON serializable
        return json.dumps(result, indent=2, default=str)

    except Exception as e:
        # Fallback for unserializable objects (Safe, no recursion)
        return json.dumps(
            {"status": "error", "error": f"Serialization error: {str(e)}"},
            indent=2
        )
