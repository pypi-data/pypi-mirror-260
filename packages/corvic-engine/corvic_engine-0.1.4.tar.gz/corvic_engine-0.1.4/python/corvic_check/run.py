"""Wrappers around common subprocess functionality."""

import subprocess
from typing import Any, Literal, cast, overload


@overload
def run(
    *args: Any, text: Literal[True], **kwargs: Any
) -> subprocess.CompletedProcess[str]:
    ...


@overload
def run(
    *args: Any, text: Literal[None, False] = None, **kwargs: Any
) -> subprocess.CompletedProcess[bytes]:
    ...


def run(*args: Any, **kwargs: Any) -> ...:
    """Wrapper for subprocess.run which sets check=True."""
    check = kwargs.pop("check", True)

    # Type annotations for non-trivial decorators is not easy to support.
    #
    # Grab bag of issues:
    # - The return value of subprocess.run depends on its arguments but there
    #   is no importable representation of its arguments so they would need to be
    #   reproduced fully here to infer the return value
    # - Type manipulations on kwargs is not fully supported:
    #   https://peps.python.org/pep-0612/#concatenating-keyword-parameters
    #
    # Instead cast extra arguments to Any and assert/cast expected return value
    ret_val = cast(
        subprocess.CompletedProcess[Any], subprocess.run(*args, check=check, **kwargs)
    )
    return ret_val
