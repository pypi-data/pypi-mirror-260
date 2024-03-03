"""Utilities for discovering information about the current project."""

import pathlib

from corvic_check import errors


def root(*, outside_project_root: bool = False) -> pathlib.Path:
    """Return the path to the project root."""
    if outside_project_root:
        raise errors.CheckError("must be run within corvic-engine")
    cur = pathlib.Path.cwd()
    fs_root = pathlib.Path(cur.anchor)
    while True:
        # Pick an sentinel file that should be present even in "chroot"
        # scenarios like a docker container (c.f. .git/ which is often excluded
        # from container file systems).
        sentinel = cur / "poetry.lock"
        if sentinel.exists():
            return cur
        cur = cur.parent
        if cur == fs_root:
            break
    raise errors.CheckError("poetry.lock not found inside project root")
