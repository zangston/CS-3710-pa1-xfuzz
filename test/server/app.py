from fastapi import FastAPI
from test.server import Settings
from test.server.auth import auth_router_factory
from test.server.enum import enum_router_factory
from test.server.ext import ext_router_factory
from test.server.vhost import vhost_router_factory
from test.server.user import user_router_factory


def create_app(settings=Settings()):
    """Factory for instantiating the test server."""

    app = FastAPI(openapi_url=settings.openapi_url)
    app.include_router(auth_router_factory(settings))
    app.include_router(enum_router_factory())
    app.include_router(ext_router_factory(settings))
    app.include_router(vhost_router_factory(settings))
    app.include_router(user_router_factory(settings))

    return app
