# flake8: noqa: F401

# NOTE: you should not need to edit this file; this is here purely to maintain
# compatibility between the initial skeleton code and older Python versions.

# Wrapper around Python's built-in `typing` module to help maintain compatbility
# with Python before v3.8

import typing as _t
from sys import version_info as _version_info
from typing import *

__all__: List[str] = []
__all__ += _t.__all__   # type: ignore[attr-defined]

_extended_attrs = ["Final"]

if _version_info < (3, 8):
    import typing_extensions as _t_ext

    for attr in filter(lambda attr: attr not in __all__, _extended_attrs):
        globals().update({attr: getattr(_t_ext, attr)})
        __all__.append(attr)
