# Middleware used by the test harness to ensure that the fuzzer
# has worked correctly.

import xfuzz._typing as _t
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class FuzzcheckHooks:
    def __init__(self) -> None:
        self.reset_hooks()

    def reset_hooks(self) -> None:
        self.hooks = dict()
        self.default_hooks = list()

    def add_hook(self, route: _t.Optional[str], hook) -> None:
        if route is not None:
            self.hooks.setdefault(route, list()).append(hook)
        else:
            self.default_hooks.append(hook)

    def get_hooks(self, route: str):
        return self.hooks.get(route, []) + self.default_hooks


class FuzzcheckMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, hooks: _t.Optional[FuzzcheckHooks] = None) -> None:
        super().__init__(app)
        self._hooks = hooks if hooks is not None else FuzzcheckHooks()

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Apply all hooks that exist for the route
        for hook in self._hooks.get_hooks(request.url.path):
            await hook(request, response)

        return response
