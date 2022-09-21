# API router for testing the -e flag to add an extension

from .settings import Settings
from fastapi import APIRouter
from test import getLogger
from test.wordlists import path_common


def ext_router_factory(settings: Settings) -> APIRouter:
    """Factory to create a new ``fastapi.APIRouter`` instance for testing the -e flag."""

    prefix = "/ext"

    router = APIRouter(
        prefix=prefix,
        tags=["Extension tests"],
        responses={404: {"detail": "Not found"}},
    )
    endpoint = settings.ext_router_endpoint()
    getLogger().debug("Using %s for the ext router endpoint", repr(endpoint))

    async def get_extension_path():
        """Testing endpoint for the `-e` / `--extension` flag. This route should be identifiable
        with the following command:

        ```
        python3 -m xfuzz -w {wordlist} -u $HOST:$PORT{prefix}/FUZZ -e html -e php
        ```
        """
        return {"detail": "found path with extension"}

    get_extension_path.__doc__ = get_extension_path.__doc__.format(wordlist=str(path_common()), prefix=prefix)
    router.add_api_route(f"/{endpoint}.php", get_extension_path)
    router.add_api_route(f"/{endpoint}.html", get_extension_path)

    return router
