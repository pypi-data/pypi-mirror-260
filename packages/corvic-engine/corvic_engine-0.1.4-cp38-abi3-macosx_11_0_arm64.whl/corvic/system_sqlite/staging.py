"""Sqlite backed staging system."""

import functools
import uuid
from collections.abc import Iterable
from typing import Any

import duckdb
import pyarrow.parquet as pq
import sqlglot

from corvic.system import StorageManager


class DuckDBStaging:
    """Access to data staged in a local database like sqlite."""

    def __init__(
        self,
        storage_manager: StorageManager,
        db_conn: duckdb.DuckDBPyConnection,
    ):
        self._storage_manager = storage_manager
        self._db_conn = db_conn

    def _table_exists(self, table_name: str) -> bool:
        with self._db_conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_name = '{table_name}'
                """
            )
            result = cur.fetchone()
        if not result:
            return False
        return result[0] >= 1

    def stage_blobs(self):
        prefix = self._storage_manager.tabular.prefix
        bucket = self._storage_manager.bucket
        blobs = bucket.list_blobs()
        table_blobs = [
            (blob, blob.name.removeprefix(prefix))
            for blob in blobs
            if blob.name.startswith(prefix)
        ]
        for blob, table_name in table_blobs:
            if self._table_exists(table_name):
                continue
            with blob.open("rb") as stream:
                self._db_conn.from_arrow(pq.read_table(stream)).create(
                    f'"{table_name}"'
                )
        return [table_name for _, table_name in table_blobs]

    def count_ingested_rows(self, blob_name: str, *other_blob_names: str) -> int:
        staged_blob_names = self.stage_blobs()
        blobs_to_query = [
            blob for blob in (blob_name, *other_blob_names) if blob in staged_blob_names
        ]
        if not blobs_to_query:
            return 0
        table_queries = [f"SELECT * FROM '{name}'" for name in blobs_to_query]
        with self._db_conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT COUNT(*)
                    FROM ({" UNION_ALL ".join(table_queries)})
                """
            )
            result = cur.fetchone()
        if not result:
            return 0
        return result[0]

    def query_for_blobs(
        self, blob_names: list[str], column_names: list[str]
    ) -> sqlglot.exp.Subqueryable:
        columns = [
            sqlglot.column(sqlglot.exp.to_identifier(name, quoted=True))
            for name in column_names
        ]
        tables = [
            sqlglot.to_identifier(blob_name, quoted=True) for blob_name in blob_names
        ]

        query = sqlglot.select(*columns)

        if len(tables) == 1:
            return query.from_(tables[0])

        staging_union_table = sqlglot.to_identifier(
            f"staging-{uuid.uuid4().hex}", quoted=True
        )

        union = functools.reduce(
            lambda x, y: x.union(y, distinct=False),
            (
                sqlglot.select(*column_names).from_(
                    sqlglot.table(sqlglot.to_identifier(table_name, quoted=True))
                )
                for table_name in blob_names
            ),
        )
        return (
            sqlglot.select(*column_names)
            .from_(staging_union_table)
            .with_(staging_union_table, as_=union)
        )

    def run_select_query(
        self, query: sqlglot.exp.Subqueryable
    ) -> Iterable[dict[str, Any]]:
        """Run a select query to extract and transform staging data.

        N.B. this behaves a little differently than rockset would.
        Rockset has one super-wide table, so it would silently omit data. This
        implementation will complain loudly if the query references an unstaged blob.
        That tradeoff is somewhat reasonable since if data isn't staged in this case it
        means the caller is doing something wrong (in Rockset's case there's some
        asynchrony which could lead to the data not being staged).
        """
        self.stage_blobs()
        with self._db_conn.cursor() as cur:
            cur.execute(query.sql(dialect="duckdb"))
            result = cur.fetch_arrow_table()
        return result.to_pylist()
