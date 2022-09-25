# Tests for the command line interface to xfuzz.

import asyncio
import xfuzz._typing as _t
import subprocess as sp
from .utils import xfuzztest
from contextlib import asynccontextmanager
from test import LIVE_HOST, LIVE_PORT
from test.wordlists import path_common, path_subdomains


host: _t.Final[str] = f"http://{LIVE_HOST}:{LIVE_PORT}"
base_opts: _t.Final[_t.List[str]] = ["-w", str(path_common())]


@asynccontextmanager
async def fuzz_proc(fuzz_args, timeout: float = 60):
    """Run ``xfuzz`` in another process and wrap it in an async context. Wait for the process
    to terminate at the end of the context."""

    proc = sp.Popen(fuzz_args.popen_args, stdin=sp.PIPE)
    loop = asyncio.get_event_loop()

    try:
        yield proc
    finally:
        wait = lambda: proc.wait(timeout=timeout)
        try:
            await loop.run_in_executor(None, wait)
        except sp.TimeoutExpired as ex:
            assert False, (
                f"{type(ex).__name__} exception raised after waiting for fuzzer process to terminate.\n"
                f"Command: `{fuzz_args.command}`"
            )


@xfuzztest(["-u", f"{host}"])
async def test_no_specify_fuzz_parameter(fuzz_args):
    async with fuzz_proc(fuzz_args) as proc:
        ...

    assert proc.returncode != 0, (
        "xfuzz return exit code 0 even though no parameter was specified for fuzzing. Make sure that "
        "xfuzz returns a non-zero exit code (e.g. by raising an exception) when FUZZ is not provided.\n"
        f"Command: `{fuzz_args.command}`"
    )


@xfuzztest(base_opts + ["-H", "Content-Type: FUZZ"])
async def test_no_specify_url(fuzz_args):
    """We should get an error when a URL is not provided for xfuzz."""

    async with fuzz_proc(fuzz_args) as proc:
        ...

    assert proc.returncode != 0, (
        "xfuzz returned exit code 0 even though no URL was provided. Make sure that xfuzz returns "
        "a non-zero exit code (e.g. by raising an exception) when the -u / --url flag is not provided.\n"
        f"Command: `{fuzz_args.command}`"
    )


@xfuzztest(base_opts + ["-u", f"{host}/enum/FUZZ", "-mc", "200", "-mc", "307"])
async def test_directory_enumeration(fuzz_args, hooks):
    """Perform directory enumeration using xfuzz."""

    status_codes = {}

    async def check_index(req, resp):
        status_codes["/enum/"] = resp.status_code

    async def check_redirect(req, resp):
        status_codes["/enum/redirect"] = resp.status_code

    hooks.add_hook("/enum/", check_index)
    hooks.add_hook("/enum/redirect", check_redirect)
    async with fuzz_proc(fuzz_args):
        ...

    assert (
        status_codes.get("/enum/") == 200
    ), f"Fuzzing failed: failed to find /enum/ (200)\nCommand: `{fuzz_args.command}`"
    assert (
        status_codes.get("/enum/redirect") == 307
    ), f"Fuzzing failed: failed to find /enum/redirect (307)\nCommand: `{fuzz_args.command}`"


@xfuzztest(["-w", "-", "-u", f"{host}/user/search?uid=FUZZ"])
async def test_fuzz_url_parameter_with_stdin_wordlist(settings, fuzz_args, hooks):
    """Fuzz a URL parameter using inputs passed in to stdin."""

    found_uids = set()
    expected_uids = set([str(settings.user_uid())])

    async def check(req, resp):
        if resp.status_code == 200:
            found_uids.add(req.query_params.get("uid"))

    hooks.add_hook("/user/search", check)

    # Start xfuzz in another process
    async with fuzz_proc(fuzz_args, timeout=5) as proc:
        wordlist = "\n".join(map(str, range(5000))).encode("utf-8")
        comm = lambda msg: proc.communicate(input=msg, timeout=60)
        await asyncio.get_event_loop().run_in_executor(None, comm, wordlist)

    assert found_uids == expected_uids, (
        "Fuzzing failed: failed to fuzz user IDs at /user/search. Expected to find: "
        f"{expected_uids}; found: {found_uids}.\nCommand: `{fuzz_args.command}`"
    )


@xfuzztest(base_opts + ["-u", f"{host}/ext/FUZZ", "-e", "html"])
async def test_get_html_extension(settings, fuzz_args, hooks):
    """Test the -e / --extension flag for xfuzz."""

    endpoint = settings.ext_router_endpoint()
    hit_routes = set()

    async def check(req, resp):
        hit_routes.add((req.url.path, resp.status_code))

    hooks.add_hook(f"/ext/{endpoint}.html", check)
    async with fuzz_proc(fuzz_args):
        ...

    assert hit_routes == set(
        [(f"/ext/{endpoint}.html", 200)]
    ), f"Fuzzing failed: did not find /ext/{endpoint}.html.\nCommand: `{fuzz_args.command}`"


@xfuzztest(base_opts + ["-u", f"{host}/ext/FUZZ", "-e", "html"])
async def test_get_single_extension(settings, fuzz_args, hooks):
    """Test using the -e / --extension flag to indicate a single extension to test."""

    endpoint = settings.ext_router_endpoint()
    html_ep = f"/ext/{endpoint}.html"

    hit_routes = set()
    expected_routes = set([html_ep])

    async def check(req, resp):
        if resp.status_code == 200:
            hit_routes.add(req.url.path)

    hooks.add_hook(None, check)
    async with fuzz_proc(fuzz_args):
        ...

    assert hit_routes == expected_routes, (
        f"Fuzzing failed: expected to return HTTP 200 responses for {hit_routes}, instead received "
        f"200 responses for: {hit_routes}.\n"
        f"Command: `{fuzz_args.command}`"
    )


@xfuzztest(base_opts + ["-u", f"{host}/ext/FUZZ", "-e", "html", "-e", "php"])
async def test_get_multiple_extensions(settings, fuzz_args, hooks):
    """Test using the -e / --extension flag multiple times."""

    hit_routes = set()
    endpoint = settings.ext_router_endpoint()
    html_ep = f"/ext/{endpoint}.html"
    php_ep = f"/ext/{endpoint}.php"

    async def check(req, resp):
        hit_routes.add(req.url.path)

    hooks.add_hook(html_ep, check)
    hooks.add_hook(php_ep, check)
    async with fuzz_proc(fuzz_args):
        ...

    assert hit_routes == set(
        [html_ep, php_ep]
    ), f"Fuzzing failed: did not find both {html_ep} and {php_ep}.\nCommand: `{fuzz_args.command}`"


_opts = base_opts + [
    "-u",
    f"{host}/auth/login",
    "-H",
    "Content-Type: application/json",
    "-X",
    "POST",
    "-mc",
    "200",
    "-d",
    '{"username": "admin", "password": "FUZZ"}',
]


@xfuzztest(_opts)
async def test_bruteforce_login(settings, fuzz_args, hooks):
    """Test bruteforcing a login API using xfuzz."""

    creds = set()

    async def check(req, resp):
        if resp.status_code == 200:
            creds.add(200)

    hooks.add_hook("/auth/login", check)
    async with fuzz_proc(fuzz_args):
        ...

    assert creds == set([200]), (
        "Login brute force failed: did not get a 200 response for the correct username and password.\n"
        f"Command: `{fuzz_args.command}`"
    )


@xfuzztest(["-w", str(path_subdomains()), "-u", f"{host}/vhost/", "-H", "Host: FUZZ.example.org"])
async def test_fuzz_vhost(settings, fuzz_args, hooks):
    vhosts = set()
    true_vhost = settings.vhost_router_domain()

    async def check(req, resp):
        if resp.status_code == 200:
            vhosts.add(req.headers.get("host"))

    hooks.add_hook("/vhost/", check)

    async with fuzz_proc(fuzz_args):
        ...

    assert vhosts == set([true_vhost]), (
        f"Virtual host enumeration failed: expected to find vhost {true_vhost}, found: {vhosts}.\n"
        f"Command: `{fuzz_args.command}`"
    )
