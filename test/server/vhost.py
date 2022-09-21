# Test server routes that return a different response based on the 'Host' HTTP
# header you pass in to them. These routes are used to test virtual host
# fuzzing in HTTP headers.

import xfuzz._typing as _t
from .settings import Settings
from fastapi import APIRouter, Header, HTTPException
from test.wordlists import path_subdomains


def vhost_router_factory(settings: Settings) -> APIRouter:
    """Factory to create a new ``fastapi.Router`` instance for testing header fuzzing."""

    prefix = "/vhost"
    router = APIRouter(prefix=prefix, tags=["vhost"])
    vhost = settings.vhost_router_domain()

    def get_vhost(host: _t.Union[str, None] = Header(default=None)):
        """Returns a 200 response if the `Host` header is set to `Host: {host}`, and a 404
        response otherwise.

        This subdomain should be identifiable with the following command:

        ```
        python3 -m xfuzz -w {wordlist} -H 'Host: FUZZ.example.org' -u $HOST:$PORT{prefix}/
        ```
        """

        if host == vhost:
            return {"detail": "Found virtual host!"}
        else:
            raise HTTPException(status_code=404, detail="Virtual host not found")

    get_vhost.__doc__ = get_vhost.__doc__.format(host=vhost, wordlist=str(path_subdomains()), prefix=prefix)
    router.add_api_route("/", endpoint=get_vhost)

    return router
