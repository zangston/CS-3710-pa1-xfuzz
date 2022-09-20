# API router for testing the -e flag to add an extension

from .settings import Settings
from fastapi import APIRouter
from test import getLogger


def ext_router_factory(settings: Settings) -> APIRouter:
    """Factory to create a new ``fastapi.APIRouter`` instance for testing the -e flag."""

    router = APIRouter(
        prefix="/ext",
        tags=["ext"],
        responses={404: {"detail": "Not found"}},
    )
    endpoint = settings.ext_router_endpoint()
    getLogger().debug("Using %s for the ext router endpoint", repr(endpoint))

    @router.get(f"/{endpoint}.php")
    async def get_php():
        return {"detail": "found file with PHP extension!"}

    @router.get(f"/{endpoint}.html")
    async def get_html():
        return {"detail": "found file with HTML extension!"}

    return router
