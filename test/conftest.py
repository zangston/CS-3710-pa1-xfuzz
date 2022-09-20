# PyTest configuration options.

import logging
import pytest
from httpx import AsyncClient
from rich.logging import RichHandler
from test import getLogger
from test.live_server import UvicornTestServer
from test.server.app import create_app
from test.server.settings import Settings
from test.server.middleware import FuzzcheckMiddleware, FuzzcheckHooks
from test.utils import FuzzArgs


def pytest_addoption(parser):
    """Add additional command-line options for PyTest."""

    parser.addoption(
        "--server-tests",
        action="store_true",
        default=False,
        dest="servertests",
        help="Only run tests for the test harness server.",
    )

    parser.addoption(
        "--test-loglevel",
        default="error",
        dest="test_loglevel",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the loglevel for the test suite's logger",
    )

    return parser


# Fixture definitions


@pytest.fixture(params=[], scope="function")
def cliargs(request):
    """Parse command-line arguments from the provided parameters."""

    return request.param


@pytest.fixture
def fuzz_args(cliargs):
    return FuzzArgs(cliargs)


@pytest.fixture(scope="session", autouse=True)
def logger(pytestconfig):
    """Fixture for using the testing logger."""

    logger = getLogger()
    loglevel = pytestconfig.getoption("test_loglevel").upper()

    ch = RichHandler()
    ch.setLevel(loglevel)

    formatter = logging.Formatter("%(name)s: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(loglevel)


@pytest.fixture(scope="session")
def settings():
    """Fixture for test settings."""

    return Settings(openapi_url="")


@pytest.fixture(scope="module", autouse=True)
def hooks():
    return FuzzcheckHooks()


@pytest.fixture(scope="function", autouse=True)
def reset_hooks(hooks):
    """Fixture to automatically reset the middleware hooks after each test."""

    hooks.reset_hooks()


@pytest.fixture(scope="module")
def app(settings, hooks):
    """Fixture for the test server, as a ``fastapi.FastAPI`` instance."""

    app = create_app(settings=settings)
    app.add_middleware(FuzzcheckMiddleware, hooks=hooks)
    return app


@pytest.fixture
async def client(app):
    """Fixture for generating a test client to connect to the server."""

    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


@pytest.fixture(autouse=True)
async def live_server(app):
    """Fixture for generating a live server to run during the test."""

    getLogger().debug("Starting live test server")
    async with UvicornTestServer(app) as server:
        yield server

    getLogger().debug("Stopping live test server")
