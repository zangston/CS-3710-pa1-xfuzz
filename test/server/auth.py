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

    async def create(user: UserLogin):
        """Endpoint to simulate a user creation API. This endpoint should return a 200 response if
        the provided username does not exist yet, and a 409 Conflict response otherwise.

        This can be used to perform user discovery by filtering out all responses except for the
        status code 409 responses. To test this, you can run

        ```
        python3 -m xfuzz -w {wordlist} -H 'Content-Type: application/json' \\
            -X PUT -mc 409 -d '{{"username": "admin", "password": "FUZZ"}}' \\
            -u $HOST:$PORT{prefix}/create
        ```

        This should reveal the `admin` user.
        """
        if user.username == "admin":
            raise HTTPException(status_code=409, detail="User already exists")
        else:
            return {"detail": "created new user"}

    kwargs = {"prefix": prefix, "wordlist": str(path_common())}
    login.__doc__ = login.__doc__.format(password=password, **kwargs)
    create.__doc__ = create.__doc__.format(**kwargs)
    router.add_api_route("/login", login, methods=["POST"])
    router.add_api_route("/create", create, methods=["PUT"])

    return router
