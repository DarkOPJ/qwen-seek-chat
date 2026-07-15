from typing import Any, Dict

from app.core.exceptions import exception_message

openapi_responses = {
    400: {
        "description": "OperationError",
        "content": {
            "application/json": {
                "example": exception_message(
                    error="OperationError", message="an error occurred"
                )
            }
        },
    },
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": exception_message(
                    error="Unauthorized", message="not authenticated"
                )
            }
        },
    },
    403: {
        "description": "PermissionError",
        "content": {
            "application/json": {
                "example": exception_message(
                    error="PermissionError", message="not enough permission"
                )
            }
        },
    },
    404: {
        "description": "ResourceDoesNotExist",
        "content": {
            "application/json": {
                "example": exception_message(
                    error="ResourceDoesNotExist", message="resource not found"
                )
            }
        },
    },
    422: {
        "description": "ValidationException",
        "content": {
            "application/json": {
                "example": exception_message(
                    error="ValidationError", message="invalid request data"
                )
            }
        },
    },
    500: {
        "description": "InternalServerError",
        "content": {
            "application/json": {
                "example": exception_message(
                    error="InternalServerError", message="server error"
                )
            }
        },
    },
}


def get_openapi_responses(*status_codes: int) -> Dict[int, Dict[str, Any]]:
    """
    Pick specific OpenAPI response definitions by status code.

    Example:
        @app.get("/resource/{resource_id}", responses=get_responses(401, 404, 500))
    """
    return {
        code: openapi_responses[code]
        for code in status_codes
        if code in openapi_responses
    }
