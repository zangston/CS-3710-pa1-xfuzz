import logging
import xfuzz._typing as _t

# Default configuration options for the live server
LIVE_HOST: _t.Final[str] = "127.0.0.1"
LIVE_PORT: _t.Final[int] = 25373


def getLogger():
    return logging.getLogger("xfuzz-test")
