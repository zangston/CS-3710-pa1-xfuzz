# API router for test cases centered around form data / authentication

from .settings import Settings
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from test import getLogger
from test.wordlists import path_common


class UserLogin(BaseModel):
    username: str
    password: str


def auth_router_factory(settings: Settings) -> APIRouter:
    """Factory to create a new ``fastapi.APIRouter`` instance for testing form data and
    authentication."""

    prefix = "/auth"
    router = APIRouter(prefix=prefix, tags=["POST data fuzzing tests"], responses={404: {"detail": "Not found"}})
    password = settings.auth_router_password()
    getLogger().debug("Using %s for the auth router's password", repr(password))

    async def login(user: UserLogin):
        """Endpoint to simulate a login API. You can use this endpoint to simulate using brute
        force to figure out a user's password. This endpoint returns a 200 response if the data

        ```
        {{"username": "admin", "password": "{password}"}}
        ```

        is provided, and a 403 response otherwise.

        The following `xfuzz` command should identify the correct password:

        ```
        python3 -m xfuzz -w {wordlist} -H 'Content-Type: application/json' \\
            -X POST -mc 200 -d '{{"username": "admin", "password": "FUZZ"}}' \\
            -u $HOST:$PORT{prefix}/login
        ```
        """
        if user.username == "admin" and user.password == password:
            return {"detail": "login succeeded"}
        else:
            raise HTTPException(status_code=403, detail="Access denied")

    login.__doc__ = login.__doc__.format(prefix=prefix, wordlist=str(path_common()), password=password)
    router.add_api_route("/login", login, methods=["POST"])

    return router
