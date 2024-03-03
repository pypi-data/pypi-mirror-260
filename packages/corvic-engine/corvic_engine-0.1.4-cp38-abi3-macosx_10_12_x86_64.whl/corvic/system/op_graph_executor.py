"""Corvic system op graph executeor protocol."""

from collections.abc import Iterable
from typing import Any, Protocol

from corvic import op_graph


class OpGraphExecutor(Protocol):
    """Execute table op graphs."""

    def execute(self, op: op_graph.Op) -> Iterable[dict[str, Any]]:
        """Execute an op pgraph.

        Render the resulting table as a stream of rows.
        """
        ...
