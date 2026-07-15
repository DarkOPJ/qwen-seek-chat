import os

import jwt
from jwt.exceptions import PyJWTError

from app.core.exceptions import AppException
from config import settings


def decode_keycloak_token(token: str):
    public_key = f"-----BEGIN PUBLIC KEY-----\n{''.join(config.jwt_public_key.split())}\n-----END PUBLIC KEY-----"  # noqa
    try:
        payload: dict = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=settings.jwt_algorithms,
            audience="account",
            issuer=f"{settings.keycloak_uri}/realms/{settings.keycloak_realm}",
        )
        payload["id"] = payload.get("preferred_username")
        return payload
    except PyJWTError as exc:
        raise AppException.BadRequestException(error_message=exc.args)


def validate_environment(modes: list):
    if os.getenv("APP_ENV") not in modes:
        raise RuntimeError(f"Config variable 'APP_ENV' must be in {modes} mode")
