# Tests to validate that the CLI works by default.
#
# These tests will pass if the xfuzz code displays the correct behavior
# by default.

import pytest
from .utils import clitest, fuzz_proc
from test.wordlists import path_common


def defaultstest(func):
    """Decorator to apply to all of the CLI defaults tests."""

    func = pytest.mark.asyncio(func)
    return func


@defaultstest
@clitest(["-u", "https://example.org"])
async def test_no_specify_wordlist(fuzz_args):
    async with fuzz_proc(fuzz_args) as proc:
        ...

    assert proc.returncode != 0, (
        "xfuzz return exit code 0 even though no wordlist was specified for fuzzing.\n"
        f"Command: `{fuzz_args.command}`"
    )


@defaultstest
@clitest(["-w", str(path_common())])
async def test_no_specify_url(fuzz_args):
    async with fuzz_proc(fuzz_args) as proc:
        ...

    assert proc.returncode != 0, (
        "xfuzz return exit code 0 even though no URL was specified for fuzzing.\n"
        f"Command: `{fuzz_args.command}`"
    )
