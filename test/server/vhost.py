# Test server routes that return a different response based on the 'Host' HTTP
# header you pass in to them. These routes are used to test virtual host
# fuzzing in HTTP headers.

import xfuzz._typing as _t
from .settings import Settings
from fastapi import APIRouter, Header, HTTPException


def vhost_router_factory(settings: Settings) -> APIRouter:
    """Factory to create a new ``fastapi.Router`` instance for testing header fuzzing."""

    router = APIRouter(prefix="/vhost", tags=["vhost"])
    vhost = settings.vhost_router_domain()

    @router.get("/")
    def get_vhost(host: _t.Union[str, None] = Header(default=None)):
        f"""Returns a 200 response if the Host header is set to {host}, and a 404
        response otherwise."""

        if host == vhost:
            return {"detail": "Found virtual host!"}
        else:
            raise HTTPException(status_code=404, detail="Virtual host not found")

    return router
