# API router for test cases centered around form data / authentication

from .settings import Settings
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from test import getLogger


class UserLogin(BaseModel):
    username: str
    password: str


def auth_router_factory(settings: Settings) -> APIRouter:
    """Factory to create a new ``fastapi.APIRouter`` instance for testing form data and
    authentication."""

    router = APIRouter(prefix="/auth", tags=["auth"], responses={404: {"detail": "Not found"}})
    password = settings.auth_router_password()
    getLogger().debug("Using %s for the auth router's password", repr(password))

    @router.post("/login")
    async def login(user: UserLogin):
        """Endpoint to simulate a 'login' URL."""
        if user.username == "admin" and user.password == password:
            return {"detail": "login succeeded"}
        else:
            raise HTTPException(status_code=403, detail="Access denied")

    return router
