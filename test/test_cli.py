# Tests for the command line interface to xfuzz.

import asyncio
import xfuzz._typing as _t
import subprocess as sp
from .utils import xfuzztest
from test import LIVE_HOST, LIVE_PORT
from test.wordlists import path_common, path_subdomains


host: _t.Final[str] = f"http://{LIVE_HOST}:{LIVE_PORT}"
base_opts: _t.Final[_t.List[str]] = ["-w", str(path_common())]


def fuzz_proc(fuzz_args):
    """Run ``xfuzz`` in another process."""

    cmd = ["python3", "-m", "xfuzz"] + fuzz_args.args
    return sp.Popen(cmd, stdin=sp.PIPE)


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
    await fuzz_args.fuzz()

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
    proc = fuzz_proc(fuzz_args)

    wordlist = "\n".join(map(str, range(5000))).encode("utf-8")
    loop = asyncio.get_event_loop()
    comm = lambda msg: proc.communicate(input=msg, timeout=30)
    await loop.run_in_executor(None, comm, wordlist)
    await loop.run_in_executor(None, proc.wait)

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
    await fuzz_args.fuzz()

    assert hit_routes == set(
        [(f"/ext/{endpoint}.html", 200)]
    ), f"Fuzzing failed: did not find /ext/{endpoint}.html.\nCommand: `{fuzz_args.command}`"


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
    await fuzz_args.fuzz()

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
    await fuzz_args.fuzz()

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

    await fuzz_args.fuzz()

    assert vhosts == set([true_vhost]), (
        f"Virtual host enumeration failed: expected to find vhost {true_vhost}, found: {vhosts}.\n"
        f"Command: `{fuzz_args.command}`"
    )
