"""Sqlite backed system client."""

import sqlite3

import duckdb
import sqlalchemy as sa

import corvic.orm
from corvic.system import StorageManager
from corvic.system_sqlite.blob_store import RDBMSClient
from corvic.system_sqlite.executor import Executor
from corvic.system_sqlite.staging import DuckDBStaging


@sa.event.listens_for(sa.Engine, "connect")
def set_sqlite_pragma(dbapi_connection: sqlite3.Connection | None, _) -> None:
    """Tell sqlite to respect foreign key constraints.

    By default, sqlite doesn't check foreign keys. It can though if you tell it to.
    Postresql always does
    """
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


class Client:
    """Client for the sqlite system implementation."""

    def __init__(self, sqlite_file: str):
        self._sa_engine = sa.create_engine(f"sqlite:///{sqlite_file}")
        blob_client = RDBMSClient(self._sa_engine)
        bucket = blob_client.bucket("blob_data")
        if not bucket.exists():
            bucket.create()
        self._storage_manager = StorageManager(
            blob_client,
            bucket.name,
            "unstructured_data",
            "tabular_data",
        )
        corvic.orm.Base.metadata.create_all(self._sa_engine)
        duck_db_conn = duckdb.connect(":memory:")
        self._staging_db = DuckDBStaging(self._storage_manager, duck_db_conn)
        self._executor = Executor(self._staging_db)

    @property
    def storage_manager(self) -> StorageManager:
        return self._storage_manager

    @property
    def sa_engine(self) -> sa.Engine:
        return self._sa_engine

    @property
    def staging_db(self) -> DuckDBStaging:
        return self._staging_db

    @property
    def executor(self) -> Executor:
        return self._executor
