# API router for enumeration tests

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from test.wordlists import path_common


def enum_router_factory() -> APIRouter:
    """Factory to create a new ``fastapi.APIRouter`` instance for testing directory
    enumeration with the fuzzer."""

    prefix = "/enum"

    router = APIRouter(
        prefix=prefix,
        tags=["Directory enumeration tests"],
    )

    async def index():
        """Index page for the directory. This route should be identifiable with the
        following command:

        ```
        python3 -m xfuzz -w {wordlist} -u $HOST:$PORT{prefix}/FUZZ -mc 307
        ```
        """

        return {"detail": "Enumeration index page"}

    async def redirect():
        """A page that automatically redirects to the index page of the enumeration
        directory. This route should be identifiable with the following command:

        ```
        python3 -m xfuzz -w {wordlist} -u $HOST:$PORT{prefix}/FUZZ
        ```
        """

        return "/enum/"

    index.__doc__ = index.__doc__.format(wordlist=str(path_common()), prefix=prefix)
    redirect.__doc__ = redirect.__doc__.format(wordlist=str(path_common()), prefix=prefix)
    router.add_api_route("/", index)
    router.add_api_route("/redirect", redirect, response_class=RedirectResponse, status_code=307)

    return router
