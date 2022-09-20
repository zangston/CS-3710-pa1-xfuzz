import argparse
import pytest
import shlex
import typing as _t
from dataclasses import dataclass
from xfuzz import fuzz
from xfuzz.cmd import parse_args


@dataclass
class FuzzArgs:
    args: _t.List[str]
    parsed_args: argparse.Namespace

    def __init__(self, args):
        self.args = args
        self.parsed_args = parse_args(self.args)

    async def fuzz(self):
        return await fuzz(self.parsed_args)

    @property
    def command(self) -> str:
        return "python3 -m xfuzz " + " ".join(shlex.quote(arg) for arg in self.args)


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
