from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.api_key import APIKeyHeader

from app.core.exceptions import AppException

from .utils import decode_keycloak_token


class KeycloakJwtAuthentication(HTTPBearer):
    def __init__(self, raise_exception=True):
        self.raise_exception = raise_exception
        super().__init__(auto_error=False)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AppException.UnauthorizedException(
                    error_message=f"AuthenticationSchemeError({credentials.scheme})"
                )
            payload = decode_keycloak_token(token=credentials.credentials)
            return payload
        if self.raise_exception:
            raise AppException.UnauthorizedException(
                error_message="AuthenticationRequired"
            )
        return None


class ApiKeyAuthentication(APIKeyHeader):
    def __init__(self, raise_exception: bool = True, auto_error: bool = False):
        self.raise_exception = raise_exception
        super().__init__(name="X-Api-Key", auto_error=auto_error)

    async def __call__(self, request: Request):
        apikey: str = await super().__call__(request)
        if not apikey and self.raise_exception:
            raise AppException.UnauthorizedException(
                error_message="AuthenticationRequired",
            )
        return apikey
