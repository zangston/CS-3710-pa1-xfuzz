# Tests to validate that the CLI works by default.
#
# These tests will pass if the xfuzz code displays the correct behavior
# by default.

import pytest
from .utils import clitest, fuzz_proc


def defaultstest(func):
    """Decorator to apply to all of the CLI defaults tests."""

    func = pytest.mark.asyncio(func)
    return func


@defaultstest
@clitest(["-u", "https://example.org", "-w", "-"])
async def test_no_specify_fuzz_parameter(fuzz_args):
    async with fuzz_proc(fuzz_args) as proc:
        ...

    assert proc.returncode != 0, (
        "xfuzz return exit code 0 even though no parameter was specified for fuzzing. Make sure that "
        "xfuzz returns a non-zero exit code (e.g. by raising an exception) when FUZZ is not provided.\n"
        f"Command: `{fuzz_args.command}`"
    )
