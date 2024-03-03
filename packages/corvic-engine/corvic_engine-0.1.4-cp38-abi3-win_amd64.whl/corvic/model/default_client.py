"""Utilities to choose a default client when the caller doesn't provide one."""

import functools
import pathlib
import tempfile

from corvic import system, system_sqlite


@functools.cache
def _tmp_directory():
    # with "cache" holding onto the object, this directory
    # will get blown away when the program exits gracefully
    return tempfile.TemporaryDirectory()


# TODO(thunt): add mechanism for library init to override this default
# e.g., when running as corvic-cloud this should return a system_cloud.Client
def get_default_client() -> system.Client:
    """Return a reasonable default implementation of system.Client."""
    return system_sqlite.Client(
        str(pathlib.Path(_tmp_directory().name) / "corvic_data.sqlite3")
    )
