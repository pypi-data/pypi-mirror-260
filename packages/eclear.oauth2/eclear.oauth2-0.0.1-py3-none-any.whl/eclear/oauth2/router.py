import enum

from functools import wraps
from typing import Any, Callable, List

import aiohttp
from fastapi import APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt
from keycloak import KeycloakAuthenticationError, KeycloakOpenID
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from starlette import status

router = APIRouter()


class KeycloakConfiguration(BaseSettings):
    """
    A class used to represent the Keycloak configuration.

    Attributes
    ----------
    server_url : str
        The URL of the Keycloak server. This can be set with the SERVER_URL
        environment variable.
    client_id : str
        The client id for the Keycloak server. This can be set with the
        CLIENT_ID environment variable.
    client_secret_key : str
        The client secret key for the Keycloak server. This can be set with the
        CLIENT_SECRET_KEY environment variable.
    realm_name : str
        The realm name for the Keycloak server, default is "authorization".
        This can be set with the REALM_NAME environment variable.
    users_url : str
        The URL for retrieving user's groups from the Keycloak server. This can
        be set with the USERS_URL environment variable.
    """

    server_url: str = Field(
        ...,
        env="SERVER_URL",
        help="Keycloak server URL",
    )
    client_id: str = Field(
        ...,
        env="CLIENT_ID",
        help="Keycloak client id",
    )
    client_secret_key: str = Field(
        ...,
        env="CLIENT_SECRET_KEY",
        help="Keycloak client secret key",
    )
    realm_name: str = Field(
        "authorization",
        env="REALM_NAME",
    )
    users_url: str = Field(
        ...,
        env="USERS_URL",
        help="Keycloak users url for retrieving user's  groups",
    )


keycloak_configuration = KeycloakConfiguration()
keycloak_configuration_dict = keycloak_configuration.model_dump()
del keycloak_configuration_dict["users_url"]
keycloak = KeycloakOpenID(**keycloak_configuration_dict)
keycloak_public_key = (
    f"-----BEGIN PUBLIC KEY-----\n{keycloak.public_key()}\n-----END PUBLIC KEY-----"
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenResponse(BaseModel):
    """Result from /login call with access and refresh tokens"""

    access_token: str
    refresh_token: str


class TokenInputModel(BaseModel):
    username: str
    password: str


@router.post(
    "/token",
    response_model=TokenResponse,
    summary="Token",
    description="Authenticate given credentials against Keycloak.",
    tags=["OAuth2"],
)
async def login(token_input: TokenInputModel) -> TokenResponse:
    """
    This endpoint allows a user to authenticate by providing their username and password.
    If the credentials are valid, a new access token and a refresh token are returned.

    Args:
        token_input (TokenInputModel): The user's username and password.

    Returns:
        TokenResponse: The new access token and refresh token.

    Raises:
        HTTPException: If the authentication fails.
    """
    try:
        token = keycloak.token(token_input.username, token_input.password)
        access_token = token["access_token"]
        refresh_token = token["refresh_token"]
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    except KeycloakAuthenticationError as auth_error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(auth_error),
        )


class RefreshInputModel(BaseModel):
    refresh_token: str


@router.post(
    "/token/refresh",
    response_model=TokenResponse,
    summary="Refresh Token",
    description="Refresh an existing access token.",
    tags=["OAuth2"],
)
async def refresh_tokens(refresh_input: RefreshInputModel) -> TokenResponse:
    """
    This endpoint allows a user to refresh their access token by providing their refresh token.
    If the refresh token is valid, a new access token and a refresh token are returned.

    Args:
        refresh_input (RefreshInputModel): The user's refresh token.

    Returns:
        TokenResponse: The new access token and refresh token.

    Raises:
        HTTPException: If the refresh fails.
    """
    try:
        new_token_response = keycloak.refresh_token(refresh_input.refresh_token)
        new_access_token = new_token_response["access_token"]
        new_refresh_token = new_token_response["refresh_token"]
        return TokenResponse(
            access_token=new_access_token, refresh_token=new_refresh_token
        )
    except KeycloakAuthenticationError as auth_error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(auth_error),
        )


def protected(roles: List[str]) -> Callable[..., Any]:
    """
    A decorator to protect routes by checking if the user has the required roles.

    Args:
        roles (List[str]): The list of roles required to access the route.

    Returns:
        Callable[..., Any]: The decorated function.

    Raises:
        ValueError: If no dependencies are defined in the method signature.
        HTTPException: If the user does not have the required roles or if the token has expired.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kw: Any) -> Any:
            # wrapped methods using the @protected decorator *must*
            # declare `dependencies` as api.routes.dependencies.router_dependencies!
            dependencies = kw.get("dependencies")
            if not dependencies:
                raise ValueError(
                    "No dependencies defined in method signature - needed for "
                    "@protected decorator"
                )
            user = dependencies.user

            try:
                user_groups = await get_user_groups(user.access_token)

                roles2 = list()
                for role in roles:
                    if isinstance(role, enum.Enum):
                        role = role.value
                        roles2.append(role)

                if not set(user_groups).intersection(roles2):
                    raise HTTPException(status_code=403, detail="Permission denied")
                return await func(*args, **kw)
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")

        return wrapper

    return decorator


async def get_user_groups(access_token: str) -> List[str]:
    """
    Get user groups from Keycloak.

    At this point, the user has already been authenticated and we have an
    access token. We can use this token to retrieve the user's groups from
    Keycloak. Note: this code could be replaced with python keycloak library
    call to get user groups. If the Keycloak user would be a Keycloak
    administrator account.

    See https://stackoverflow.com/questions/49612535/python-keycloak-get-roles-and-groups-of-user

    Args:
        access_token (str): The user's access token.

    Returns:
        List[str]: The user's groups.

    Raises:
        HTTPException: If the request to the user endpoint fails.
    """
    payload = keycloak.decode_token(
        access_token,
        key=keycloak_public_key,
        options={"verify_aud": False},
    )
    current_user = payload.get("sub")
    async with aiohttp.ClientSession() as session:
        # Make an asynchronous GET request to the user endpoint
        async with session.get(
            f"{keycloak_configuration.users_url}/{current_user}",
            headers={"Authorization": f"Bearer {access_token}"},
        ) as response:
            response.raise_for_status()
            user_data = await response.json()
            # Extract user group information and return it as a list of group names
            user_groups = [item["name"] for item in user_data.get("userGroups", [])]
        return user_groups
