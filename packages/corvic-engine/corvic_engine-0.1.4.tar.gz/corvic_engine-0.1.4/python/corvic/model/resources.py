"""Resources."""
import uuid
from collections.abc import Iterable
from typing import TypeAlias

import polars as pl
from typing_extensions import Self

from corvic import orm, result, system
from corvic.model.default_client import get_default_client
from corvic.model.wrapped_orm import WrappedOrmObject

ResourceID: TypeAlias = orm.ResourceID


class Resource(WrappedOrmObject[ResourceID, orm.Resource]):
    """Resources represent import data."""

    def _make(self, orm_self: orm.Resource, derived_from_id: ResourceID) -> Self:
        return type(self)(self._client, orm_self, derived_from_id)

    def _sub_orm_objects(self, orm_object: orm.Resource) -> Iterable[orm.Base]:
        _ = (orm_object,)
        return []

    @property
    def url(self) -> str:
        return self._orm_self.url

    @property
    def name(self) -> str:
        return self._orm_self.name

    @classmethod
    def from_blob(
        cls,
        name: str,
        blob: system.Blob,
        client: system.Client | None,
        original_path: str = "",
        description: str = "",
    ) -> Self:
        client = client or get_default_client()
        blob.reload()
        md5 = blob.md5_hash
        size = blob.size

        if not md5 or not size:
            raise result.Error("failed to get metadata from blob store")

        orm_resource = orm.Resource(
            name=name,
            mime_type=blob.content_type,
            url=blob.url,
            md5=md5,
            size=size,
            original_path=original_path,
            description=description,
        )
        return cls(client, orm_resource, ResourceID())

    @classmethod
    def from_polars(
        cls, data_frame: pl.DataFrame, client: system.Client | None = None
    ) -> Self:
        client = client or get_default_client()
        blob = client.storage_manager.tabular.blob(f"polars_dataframe/{uuid.uuid4()}")

        with blob.open(mode="wb") as stream:
            data_frame.write_parquet(stream)

        blob.content_type = "application/octet-stream"
        blob.patch()
        return cls.from_blob(blob.url, blob, client)
