import pytest
import shlex
import typing as _t
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

        return ["python3", "-m", "xfuzz"] + self.args

    @property
    def command(self) -> str:
        return " ".join(shlex.quote(arg) for arg in self.popen_args)


def servertest(func):
    """Decorator to apply to all of the server-related tests."""
    func = pytest.mark.skipif("not config.getoption('servertests')")(func)
    func = pytest.mark.asyncio(func)
    return func


def xfuzztest(args):
    """Decorator to apply to all of the xfuzz command line interface tests."""

    def decorator(func):
        f = pytest.mark.skipif("config.getoption('servertests')")(func)
        f = pytest.mark.parametrize("cliargs", [args])(f)
        f = pytest.mark.asyncio(f)

        return f

    return decorator


def extratests(func):
    """Decorator for extra tests that should only be enabled if the --extra-tests flag
    is passed in."""
    func = pytest.mark.skipif("not config.getoption('extratests')")(func)
    return func
