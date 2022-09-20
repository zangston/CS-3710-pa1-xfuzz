# Live server that can be run during integration tests.

import asyncio
import uvicorn
from fastapi import FastAPI
from test import getLogger, LIVE_PORT


class UvicornTestServer(uvicorn.Server):
    def __init__(self, app: FastAPI, host: str = "127.0.0.1", port: int = LIVE_PORT):
        # Event that only gets triggered at the end of the startup() function, which
        # lets us know that the live server is ready.
        self._startup_done = asyncio.Event()

        getLogger().debug("Starting server on host = %s, port = %d", repr(host), port)

        config = uvicorn.Config(app, host=host, port=port, log_level="error")
        super().__init__(config=config)

    async def startup(self, **kwargs) -> None:
        await super().startup(**kwargs)
        self.config.setup_event_loop()
        self._startup_done.set()

    async def __aenter__(self) -> "UvicornTestServer":
        self._task = asyncio.create_task(self.serve())
        await self._startup_done.wait()
        return self

    async def __aexit__(self, *args) -> None:
        self.should_exit = True
        await self._task
