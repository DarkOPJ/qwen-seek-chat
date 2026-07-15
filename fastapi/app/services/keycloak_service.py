import inspect
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import requests
from fastapi import HTTPException
from requests import Response, exceptions

from app.core.exceptions import AppException
from app.core.log import get_error_context, get_full_class_name
from app.core.service_interfaces import AuthServiceInterface
from app.utils import decode_keycloak_token
from config import settings

from .redis_service import RedisService

CLIENT_ID: str = settings.keycloak_client_id
CLIENT_SECRET: str = settings.keycloak_client_secret
URI: str = settings.keycloak_uri
REALM: str = settings.keycloak_realm
REALM_PREFIX: str = "/realms/"
REALM_URL: str = f"{REALM_PREFIX}{REALM}"
ADMIN_REALM_URL: str = "/admin/realms/"
AUTH_ENDPOINT: str = "/protocol/openid-connect/token/"
INTROSPECTION_ENDPOINT = f"{AUTH_ENDPOINT}introspect"
OPENID_CONFIGURATION_ENDPOINT: str = "/.well-known/openid-configuration"
JWT_CERTS_ENDPOINT: str = "/protocol/openid-connect/certs"
JWT_ISSUER: str = f"{URI}{REALM_PREFIX}{REALM}"


@dataclass
class KeycloakAuthService(AuthServiceInterface):
    """
    This class is an intermediary between this service and the IAM service i.e Keycloak.
    It makes authentication and authorization API calls to the IAM service on
    behalf of the application. Use this class when authenticating an entity.
    """

    def __init__(self, redis_service: RedisService):
        self.redis_service = redis_service

    def get_token(self, obj_data: Dict[str, str]) -> Dict[str, str]:
        data: Dict[str, str] = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": obj_data.get("username"),
            "password": obj_data.get("password"),
        }
        url: str = URI + REALM_PREFIX + REALM + AUTH_ENDPOINT
        keycloak_response: Response = self.send_request_to_keycloak(
            method="post", url=url, data=data
        )
        tokens_data: Dict[str, str] = keycloak_response.json()
        result: Dict[str, str] = {
            "access_token": tokens_data.get("access_token"),
            "refresh_token": tokens_data.get("refresh_token"),
        }
        return result

    def refresh_token(self, refresh_token: str) -> Dict[str, str]:
        request_data: Dict[str, str] = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
        }
        introspection: dict = self.inspect_token(refresh_token)
        if not introspection.get("active"):
            raise AppException.BadRequestException(error_message="InactiveRefreshToken")
        url: str = URI + REALM_PREFIX + REALM + AUTH_ENDPOINT
        keycloak_response: Response = self.send_request_to_keycloak(
            method="post", url=url, data=request_data
        )
        data: Dict[str, str] = keycloak_response.json()
        return {
            "access_token": data.get("access_token"),
            "refresh_token": data.get("refresh_token"),
        }

    def decode_token(self, token: str) -> dict:
        return decode_keycloak_token(token)

    def create_user(self, obj_data: dict) -> dict:
        data: Dict[str, Any] = {
            "email": obj_data.get("email"),
            "username": obj_data.get("username"),
            "credentials": [
                {
                    "value": obj_data.get("password"),
                    "type": "password",
                    "temporary": False,
                }
            ],
            "enabled": True,
            "emailVerified": False,
            "access": {
                "manageGroupMembership": True,
                "view": True,
                "mapRoles": True,
                "impersonate": True,
                "manage": True,
            },
        }
        self.keycloak_post(endpoint="/users", data=data)
        user: dict = self.get_keycloak_user(obj_data.get("username"))
        return user

    def update_user(self, obj_data: dict) -> dict:
        user: dict = self.get_keycloak_user(obj_data.get("username"))
        user_attributes: dict = user.get("attributes")
        for field in obj_data:
            if field in user:
                user[field] = obj_data[field]
            elif field in user_attributes:
                user_attributes[field] = obj_data.get(field)
        self.keycloak_put(endpoint=f"/users/{user.get('id')}", data=user)
        updated_user: dict = self.get_keycloak_user(username=obj_data.get("username"))
        return updated_user

    # noinspection PyMethodMayBeStatic
    def auth_service_field(self, obj_id: str, obj_data: dict) -> dict:
        user_data: dict = {"username": obj_id}
        for field in obj_data:
            auth_service_field = field.split("_")
            for index in range(len(auth_service_field)):
                if index > 0:
                    auth_service_field[index]: dict = auth_service_field[
                        index
                    ].capitalize()
            user_data["".join(auth_service_field)]: list = obj_data.get(field)
        user_data.update(obj_data)
        return user_data

    def delete_user(self, user_id: str) -> bool:
        user: dict = self.get_keycloak_user(user_id)
        endpoint: str = f"/users/{user.get('id')}"
        self.keycloak_delete(endpoint)
        return True

    def get_all_groups(self) -> List[Dict[str, str]]:
        url: str = URI + ADMIN_REALM_URL + REALM + "/groups"
        keycloak_response: Response = self.send_request_to_keycloak(
            method="get", url=url, headers=self.get_keycloak_headers()
        )
        return keycloak_response.json()

    def get_keycloak_user(self, username: str) -> Union[dict, None]:
        url: str = URI + ADMIN_REALM_URL + REALM + "/users?username=" + username
        keycloak_response: Response = self.send_request_to_keycloak(
            method="get", url=url, headers=self.get_keycloak_headers()
        )
        user: list = keycloak_response.json()
        return user[0] if user else None

    def assign_group(self, user_id: str, group: dict) -> bool:
        endpoint: str = "/users/" + user_id + "/groups/" + group.get("id")
        url: str = URI + ADMIN_REALM_URL + REALM + endpoint
        self.send_request_to_keycloak(
            method="put", url=url, headers=self.get_keycloak_headers()
        )
        return True

    def change_password(self, data: dict) -> bool:
        username: str = data.get("username")
        new_password: str = data.get("new_password")
        user: dict = self.get_keycloak_user(username)
        url: str = "/users/" + user.get("id") + "/reset-password"
        data: dict = {"type": "password", "value": new_password, "temporary": False}
        self.keycloak_put(url, data)
        return True

    def keycloak_post(self, endpoint: str, data: dict) -> Response:
        url: str = URI + ADMIN_REALM_URL + REALM + endpoint
        keycloak_response: Response = self.send_request_to_keycloak(
            method="post", url=url, headers=self.get_keycloak_headers(), json=data
        )
        return keycloak_response

    def keycloak_put(self, endpoint: str, data: dict) -> Response:
        url: str = URI + ADMIN_REALM_URL + REALM + endpoint
        keycloak_response: Response = self.send_request_to_keycloak(
            method="put", url=url, headers=self.get_keycloak_headers(), json=data
        )
        return keycloak_response

    def keycloak_delete(self, endpoint: str) -> Response:
        url: str = URI + ADMIN_REALM_URL + REALM + endpoint
        keycloak_response: Response = self.send_request_to_keycloak(
            method="delete", url=url, headers=self.get_keycloak_headers()
        )
        return keycloak_response

    def get_admin_token(self) -> str:
        admin_credentials = {
            "username": settings.keycloak_realm_admin_username,
            "password": settings.keycloak_realm_admin_password,
        }
        token_data = self.get_token(admin_credentials)
        return token_data.get("access_token")

    # noinspection PyMethodMayBeStatic
    def validate_token(self, token) -> bool:
        try:
            decode_keycloak_token(token)
            return False
        except HTTPException:
            return True

    def get_keycloak_headers(self) -> dict:
        headers = {
            "Authorization": "Bearer " + self.get_admin_token(),
            "Content-Type": "application/json",
        }
        return headers

    def inspect_token(self, token) -> dict:
        data: Dict[str, str] = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "token": token,
        }
        url: str = URI + REALM_PREFIX + REALM + INTROSPECTION_ENDPOINT
        keycloak_response: Response = self.send_request_to_keycloak(
            method="post", url=url, data=data
        )
        data = keycloak_response.json()
        return data

    def realm_openid_configuration(self) -> dict:
        url: str = URI + REALM_URL + OPENID_CONFIGURATION_ENDPOINT
        keycloak_response: Response = self.send_request_to_keycloak(
            method="get", url=url
        )
        data = keycloak_response.json()
        return data

    # noinspection PyMethodMayBeStatic
    def send_request_to_keycloak(
        self,
        method: str,
        url: str,
        headers: Optional[dict] = None,
        json: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> Response:
        try:
            response = requests.request(
                method=method, url=url, headers=headers, json=json, data=data
            )
            if response.status_code >= 300:
                raise AppException.InternalServerException(
                    error_message=f"KeycloakError{response.json(), }",
                    context=get_error_context(
                        module=__name__,
                        method=inspect.currentframe().f_code.co_name,
                        calling_module=str(inspect.stack()[1]),
                        calling_method=inspect.currentframe().f_back.f_code.co_name,
                        error=response.json(),
                    ),
                )
            return response
        except exceptions.RequestException as exc:
            raise AppException.InternalServerException(
                error_message=f"KeycloakError{exc, }",
                context=get_error_context(
                    exc_class=get_full_class_name(exc),
                    module=__name__,
                    method=inspect.currentframe().f_code.co_name,
                    calling_module=str(inspect.stack()[1]),
                    calling_method=inspect.currentframe().f_back.f_code.co_name,
                    error=str(exc),
                ),
            )
