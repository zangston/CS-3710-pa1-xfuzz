# Extra tests that can be enabled with the --extra-tests flag

import xfuzz._typing as _t
from .utils import xfuzztest, fuzz_proc
from test import LIVE_HOST, LIVE_PORT
from test.wordlists import path_common

host: _t.Final[str] = f"http://{LIVE_HOST}:{LIVE_PORT}"
base_opts: _t.Final[_t.List[str]] = ["-w", str(path_common())]


@xfuzztest(base_opts + ["-u", f"{host}/enum/FUZZ", "-H", "Content-Type: FUZZ"])
async def test_specify_fuzz_multiple_times(fuzz_args):
    """We should get an error when FUZZ is provided multiple times."""

    async with fuzz_proc(fuzz_args) as proc:
        ...

    assert proc.returncode != 0, (
        "xfuzz returned exit code 0 even though FUZZ was specified multiple times. Make sure that xfuzz "
        "returns a non-zero exit code (e.g. by raising an exception) when FUZZ is specified for "
        f"multiple parameters.\nCommand: `{fuzz_args.command}`"
    )
