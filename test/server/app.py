from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from test.server import Settings
from test.server.auth import auth_router_factory
from test.server.ext import ext_router_factory
from test.server.vhost import vhost_router_factory


def create_app(settings=Settings()):
    """Factory for instantiating the test server."""

    app = FastAPI(openapi_url=settings.openapi_url)
    app.include_router(auth_router_factory(settings))
    app.include_router(ext_router_factory(settings))
    app.include_router(vhost_router_factory(settings))

    @app.get("/enum/")
    async def index():
        """Simple landing page. Returns a 200 OK response."""
        return {"detail": "hello, world!"}

    @app.get("/enum/redirect", response_class=RedirectResponse, status_code=307)
    async def redirect():
        """Endpoint to simulate a redirection."""
        return "/enum/"

    @app.get("/user")
    async def get_user(id: int):
        """Endpoint to simulate a user search API."""
        if id == 1337:
            return {"username": "admin"}
        else:
            raise HTTPException(status_code=404, detail="User not found")

    return app
