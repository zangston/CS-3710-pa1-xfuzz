# User API test router.

from .settings import Settings
from fastapi import APIRouter, HTTPException


def user_router_factory(settings: Settings) -> APIRouter:
    """Factory to create a new ``fastapi.APIRouter`` instance for testing fuzzing a
    user API."""

    prefix = "/user"
    router = APIRouter(prefix=prefix, tags=["User API fuzzing tests"], responses={404: {"detail": "Not found"}})
    admin_uid = settings.user_uid()

    def search_endpoint(uid: int):
        """Endpoint to simulate a user search API. Returns a 200 response if the UID
        {admin_uid} is found, and a 404 response otherwise.

        The following command should identify the valid UIDs:

        ```
        seq 1 5000 | python3 -m xfuzz -w - -u $HOST:$PORT{prefix}/search?uid=FUZZ
        ```
        """

        if uid == admin_uid:
            return {"username": "admin", "uid": uid}
        raise HTTPException(status_code=404, detail="User not found")

    search_endpoint.__doc__ = search_endpoint.__doc__.format(prefix=prefix, admin_uid=admin_uid)
    router.add_api_route("/search", search_endpoint)

    return router
