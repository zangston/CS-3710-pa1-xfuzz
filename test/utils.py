import asyncio
import platform
import pytest
import shlex
import subprocess as sp
import typing as _t
from contextlib import asynccontextmanager
from dataclasses import dataclass


@dataclass
class FuzzArgs:
    args: _t.List[str]

    def __init__(self, args):
        self.args = args

    @property
    def popen_args(self) -> _t.List[str]:
        """Return a list of string arguments for ``subprocess.Popen`` so that these arguments
        can be used to run ``xfuzz`` in another process."""

        if platform.system().lower() == "windows":
            python = "py3"
        else:
            python = "python3"

        return [python, "-m", "xfuzz"] + self.args

    @property
    def command(self) -> str:
        return " ".join(shlex.quote(arg) for arg in self.popen_args)


def clitest(args):
    """Decorator to apply for CLI tests."""

    return lambda f: pytest.mark.parametrize("cliargs", [args])(f)


def servertest(func):
    """Decorator to apply to all of the server-related tests."""
    func = pytest.mark.asyncio(func)
    return func


def xfuzztest(args):
    """Decorator to apply to all of the xfuzz command line interface tests."""

    def decorator(f):
        f = clitest(args)(f)
        f = pytest.mark.skipif("config.getoption('skip_cli_tests')")(f)
        f = pytest.mark.asyncio(f)

        return f

    return decorator


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
