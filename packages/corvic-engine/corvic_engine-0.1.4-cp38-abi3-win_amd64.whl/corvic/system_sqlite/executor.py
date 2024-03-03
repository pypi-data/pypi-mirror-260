"""Sqlite backed system executor."""

from collections.abc import Iterable
from typing import Any

from corvic import op_graph, sql
from corvic.system import StagingDB


class Executor:
    """Single process, sqlite/duckdb backed executor."""

    def __init__(self, staging_db: StagingDB):
        self._staging_db = staging_db

    def _staging_query_generator(self, blob_names: list[str], column_names: list[str]):
        return self._staging_db.query_for_blobs(blob_names, column_names)

    def execute(self, op: op_graph.Op) -> Iterable[dict[str, Any]]:
        query = sql.parse_op_graph(op, self._staging_query_generator)
        return self._staging_db.run_select_query(query)
