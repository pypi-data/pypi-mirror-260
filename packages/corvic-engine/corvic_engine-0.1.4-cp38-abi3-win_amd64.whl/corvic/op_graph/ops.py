"""Operations that construct tables.

Each operation is the head of a log of one or more operations that when executed
produce a table.

To add a new operation type:

1. Add a protobuf message definition detailing the operations's arguments.

1. Add the operation to the TableComputeOp message as part of the oneof called "op"

1. Write a wrapper class that inherits from corvic.table.ops._Base (in this file).
   The wrapper should include properties for accessing the fields of the message.

1. Add the wrapper class to the "Op" union at the bottom of this file.

1. Note the mapping between the TableComputeOp field name for the new op and the
   wrapper class in corvic.table.ops._COMPUTE_OP_FIELD_NAME_TO_OP (in this file).

1. Add a case to the match statement in corvic.table.ops.from_proto.
"""

from __future__ import annotations

import functools
from abc import abstractmethod
from collections.abc import Mapping, Sequence
from typing import Any, Final, Literal, overload

import pyarrow as pa
from google.protobuf import json_format

from corvic.result import BadArgumentError
from corvic_generated.orm.v1 import table_pb2

from .errors import OpParseError
from .feature_types import FeatureType, ForeignKey
from .feature_types import from_proto as ftype_from_proto
from .proto_wrapper import ProtoOneofWrapper
from .row_filters import RowFilter
from .row_filters import from_proto as row_filters_from_proto


@overload
def from_proto(proto: table_pb2.TableComputeOp) -> Op:
    ...


@overload
def from_proto(proto: table_pb2.SelectFromStagingOp) -> SelectFromStaging:
    ...


@overload
def from_proto(proto: table_pb2.RenameColumnsOp) -> RenameColumns:
    ...


@overload
def from_proto(proto: table_pb2.JoinOp) -> Join:
    ...


@overload
def from_proto(proto: table_pb2.SelectColumnsOp) -> SelectColumns:
    ...


@overload
def from_proto(proto: table_pb2.LimitRowsOp) -> LimitRows:
    ...


@overload
def from_proto(proto: table_pb2.FilterRowsOp) -> FilterRows:
    ...


@overload
def from_proto(proto: table_pb2.UpdateMetadataOp) -> UpdateMetadata:
    ...


@overload
def from_proto(proto: table_pb2.SetMetadataOp) -> SetMetadata:
    ...


@overload
def from_proto(proto: table_pb2.RemoveFromMetadataOp) -> RemoveFromMetadata:
    ...


@overload
def from_proto(proto: table_pb2.UpdateFeatureTypesOp) -> UpdateFeatureTypes:
    ...


@overload
def from_proto(proto: table_pb2.RollupByAggregationOp) -> RollupByAggregation:
    ...


def from_proto(  # noqa: PLR0911
    proto: (
        table_pb2.TableComputeOp
        | table_pb2.SelectFromStagingOp
        | table_pb2.RenameColumnsOp
        | table_pb2.JoinOp
        | table_pb2.SelectColumnsOp
        | table_pb2.LimitRowsOp
        | table_pb2.FilterRowsOp
        | table_pb2.UpdateMetadataOp
        | table_pb2.SetMetadataOp
        | table_pb2.RemoveFromMetadataOp
        | table_pb2.UpdateFeatureTypesOp
        | table_pb2.RollupByAggregationOp
    ),
) -> Op:
    """Create an Op wrapper around an Op protobuf message."""
    match proto:
        case table_pb2.TableComputeOp():
            return _from_compute_op(proto)
        case table_pb2.SelectFromStagingOp():
            return SelectFromStaging(
                table_pb2.TableComputeOp(select_from_staging=proto)
            )
        case table_pb2.RenameColumnsOp():
            return RenameColumns(table_pb2.TableComputeOp(rename_columns=proto))
        case table_pb2.JoinOp():
            return Join(table_pb2.TableComputeOp(join=proto))
        case table_pb2.SelectColumnsOp():
            return SelectColumns(table_pb2.TableComputeOp(select_columns=proto))
        case table_pb2.LimitRowsOp():
            return LimitRows(table_pb2.TableComputeOp(limit_rows=proto))
        case table_pb2.FilterRowsOp():
            return FilterRows(table_pb2.TableComputeOp(filter_rows=proto))
        case table_pb2.UpdateMetadataOp():
            return UpdateMetadata(table_pb2.TableComputeOp(update_metadata=proto))
        case table_pb2.SetMetadataOp():
            return SetMetadata(table_pb2.TableComputeOp(set_metadata=proto))
        case table_pb2.RemoveFromMetadataOp():
            return RemoveFromMetadata(
                table_pb2.TableComputeOp(remove_from_metadata=proto)
            )
        case table_pb2.UpdateFeatureTypesOp():
            return UpdateFeatureTypes(
                table_pb2.TableComputeOp(update_feature_types=proto)
            )
        case table_pb2.RollupByAggregationOp():
            return RollupByAggregation(
                table_pb2.TableComputeOp(rollup_by_aggregation=proto)
            )


def from_bytes(serialized_proto: bytes) -> Op:
    """Deserialize an Op protobuf meesage directly into a wrpper."""
    proto = table_pb2.TableComputeOp()
    proto.ParseFromString(serialized_proto)
    return from_proto(proto)


def from_staging(
    blob_names: Sequence[str],
    arrow_schema: pa.Schema,
    feature_types: Sequence[FeatureType],
    expected_rows: int,
) -> SelectFromStaging:
    """Build a SeletctFromStaging Op."""
    if len(arrow_schema) != len(feature_types):
        raise BadArgumentError(
            "length of arrow_schema must match length of feature_types"
        )
    if any(
        isinstance(feature, ForeignKey) and not feature.referenced_source_id
        for feature in feature_types
    ):
        raise BadArgumentError("referenced_source_id cannot be empty in foreign key")
    return from_proto(
        table_pb2.SelectFromStagingOp(
            blob_names=blob_names,
            arrow_schema=arrow_schema.serialize().to_pybytes(),
            feature_types=[feature_type.to_proto() for feature_type in feature_types],
            expected_rows=expected_rows,
        )
    )


def _from_compute_op(proto: table_pb2.TableComputeOp) -> Op:
    field_name = proto.WhichOneof(_Base.oneof_name())
    new_op_type = _COMPUTE_OP_FIELD_NAME_TO_OP.get(field_name)
    if new_op_type is None:
        raise BadArgumentError("unsupported operation type", operation_type=field_name)
    return new_op_type(proto)


class _Base(ProtoOneofWrapper[table_pb2.TableComputeOp]):
    """Base type for all log operations.

    Each operation is the head of a log, potentially referencing other operations
    to construct the table.

    These operations are convenience wrappers for reading and writing protobufs
    that describe table operations.
    """

    @classmethod
    def oneof_name(cls) -> str:
        return "op"

    @classmethod
    def expected_oneof_field(cls) -> str:
        """Returns the name of field for this type in the root proto op type."""
        if cls not in _OP_TO_COMPUTE_OP_FIELD_NAME:
            raise OpParseError(
                "operation field name must registered in _COMPUTE_OP_FIELD_NAME_TO_OP"
            )
        return _OP_TO_COMPUTE_OP_FIELD_NAME[cls]

    @abstractmethod
    def sources(self) -> list[Op]:
        """Returns the source tables that this operation depends on (empty if none)."""

    def join(
        self,
        right: Op,
        left_on: Sequence[str] | str,
        right_on: Sequence[str] | str,
        how: table_pb2.JoinType | Literal["inner", "left outer"],
    ) -> Join:
        if isinstance(how, str):
            match how:
                case "inner":
                    how = table_pb2.JOIN_TYPE_INNER
                case "left outer":
                    how = table_pb2.JOIN_TYPE_LEFT_OUTER
        if how == table_pb2.JOIN_TYPE_UNSPECIFIED:
            raise BadArgumentError("how must be specified")

        if isinstance(left_on, str):
            left_on = [left_on]

        if isinstance(right_on, str):
            right_on = [right_on]

        if not right_on:
            raise BadArgumentError("right_on cannot be empty")
        if not left_on:
            raise BadArgumentError("left_on cannot be empty")

        if not len(left_on) == len(right_on):
            raise BadArgumentError("number of matching columns must be the same")

        return from_proto(
            table_pb2.JoinOp(
                left_source=self.to_proto(),
                right_source=right.to_proto(),
                left_join_columns=left_on,
                right_join_columns=right_on,
                how=how,
            )
        )

    def rename_columns(self, old_name_to_new: Mapping[str, str]):
        return from_proto(
            table_pb2.RenameColumnsOp(
                source=self._proto, old_names_to_new=old_name_to_new
            )
        )

    def select_columns(self, columns: Sequence[str]) -> SelectColumns:
        if isinstance(columns, str):
            # N.B. if we dont explicitly handle the lone string type like this
            # we end up in the unfortuname situation where keys_to_remove
            # silently becomes a list of one character string.
            # I.e., a string is a valid sequence of strings
            columns = [columns]
        return from_proto(
            table_pb2.SelectColumnsOp(source=self._proto, columns=columns)
        )

    def limit_rows(self, num_rows: int) -> LimitRows:
        if num_rows <= 0:
            raise BadArgumentError("num_rows must be positive")
        if isinstance(self, LimitRows):
            proto = self.to_proto().limit_rows
            proto.num_rows = min(proto.num_rows, num_rows)
        else:
            proto = table_pb2.LimitRowsOp(source=self._proto, num_rows=num_rows)
        return from_proto(proto)

    def update_metadata(self, metadata_updates: Mapping[str, Any]) -> UpdateMetadata:
        proto = table_pb2.UpdateMetadataOp(source=self._proto)
        proto.metadata_updates.update(metadata_updates)
        return from_proto(proto)

    def set_metadata(self, new_metadata: Mapping[str, Any]) -> SetMetadata:
        proto = table_pb2.SetMetadataOp(source=self._proto)
        proto.new_metadata.update(new_metadata)
        return from_proto(proto)

    def remove_from_metadata(self, keys_to_remove: Sequence[str]) -> RemoveFromMetadata:
        if isinstance(keys_to_remove, str):
            # N.B. if we dont explicitly handle the lone string type like this
            # we end up in the unfortuname situation where keys_to_remove
            # silently becomes a list of one character string.
            # I.e., a string is a valid sequence of strings
            keys_to_remove = [keys_to_remove]
        proto = table_pb2.RemoveFromMetadataOp(
            source=self._proto, keys_to_remove=keys_to_remove
        )
        return from_proto(proto)

    def update_feature_types(
        self, new_feature_types: Mapping[str, FeatureType]
    ) -> UpdateFeatureTypes:
        if any(
            isinstance(feature, ForeignKey) and not feature.referenced_source_id
            for feature in new_feature_types.values()
        ):
            raise BadArgumentError(
                "referenced_source_id cannot be empty in foreign key"
            )

        new_feature_types_proto = {
            k: v.to_proto() for k, v in new_feature_types.items()
        }

        if isinstance(self, UpdateFeatureTypes):
            old_feature_types = dict(
                self.to_proto().update_feature_types.new_feature_types
            )
            old_feature_types.update(new_feature_types_proto)
            new_feature_types_proto = old_feature_types

        proto = table_pb2.UpdateFeatureTypesOp(
            source=self._proto, new_feature_types=new_feature_types_proto
        )
        return from_proto(proto=proto)

    def rollup_by_aggregation(
        self,
        group_by: Sequence[str] | str,
        target: str,
        aggregation: (
            table_pb2.AggregationType
            | Literal["count", "avg", "mode", "min", "max", "sum"]
        ),
    ) -> RollupByAggregation:
        if isinstance(aggregation, str):
            match aggregation:
                case "count":
                    aggregation = table_pb2.AGGREGATION_TYPE_COUNT
                case "avg":
                    aggregation = table_pb2.AGGREGATION_TYPE_AVG
                case "mode":
                    aggregation = table_pb2.AGGREGATION_TYPE_MODE
                case "min":
                    aggregation = table_pb2.AGGREGATION_TYPE_MIN
                case "max":
                    aggregation = table_pb2.AGGREGATION_TYPE_MAX
                case "sum":
                    aggregation = table_pb2.AGGREGATION_TYPE_SUM

        if aggregation == table_pb2.AGGREGATION_TYPE_UNSPECIFIED:
            raise BadArgumentError("aggregation must be specified")

        if isinstance(group_by, str):
            group_by = [group_by]

        return from_proto(
            table_pb2.RollupByAggregationOp(
                source=self.to_proto(),
                group_by_column_names=group_by,
                target_column_name=target,
                aggregation_type=aggregation,
            )
        )

    def filter_rows(self, row_filter: RowFilter) -> FilterRows:
        return from_proto(
            table_pb2.FilterRowsOp(
                source=self.to_proto(), row_filter=row_filter.to_proto()
            )
        )


class SelectFromStaging(_Base):
    """Construct a table by selecting rows from the staging collection.

    These operations are leaf operations that describe data sources.
    """

    @property
    def blob_names(self) -> Sequence[str]:
        return self._proto.select_from_staging.blob_names

    @property
    def columns(self) -> Sequence[str]:
        return self._proto.select_from_staging.columns

    @functools.cached_property
    def arrow_schema(self) -> pa.Schema:
        return pa.ipc.read_schema(
            pa.py_buffer(self._proto.select_from_staging.arrow_schema)
        )

    @functools.cached_property
    def feature_types(self) -> Sequence[FeatureType]:
        return [
            ftype_from_proto(feature_type)
            for feature_type in self._proto.select_from_staging.feature_types
        ]

    @property
    def expected_rows(self) -> int:
        return self._proto.select_from_staging.expected_rows

    def sources(self):
        return list[Op]()


class RenameColumns(_Base):
    """Rename the columns in the result of another operation.

    Useful for resolving conflicts that would happen during joins,
    or just for adjusting poor source names.
    """

    @property
    def source(self) -> Op:
        return from_proto(self._proto.rename_columns.source)

    @property
    def old_name_to_new(self) -> Mapping[str, str]:
        return self._proto.rename_columns.old_names_to_new

    def sources(self):
        return [self.source]


class UpdateFeatureTypes(_Base):
    """Patch FeatureType of a table schema."""

    @property
    def source(self) -> Op:
        return from_proto(self._proto.update_feature_types.source)

    @functools.cached_property
    def new_feature_types(self) -> Mapping[str, FeatureType]:
        return {
            k: ftype_from_proto(v)
            for k, v in self._proto.update_feature_types.new_feature_types.items()
        }

    def sources(self):
        return [self.source]


class Join(_Base):
    """Join two tables together to produce a new table.

    All unique columns from the constituent tables appear in the
    results. Order matters, left columns will be preferred on conflict
    and the names for left columns will be preferred when names for
    the join columns differ.
    """

    @property
    def left_source(self) -> Op:
        return from_proto(self._proto.join.left_source)

    @property
    def right_source(self) -> Op:
        return from_proto(self._proto.join.right_source)

    @property
    def left_join_columns(self) -> Sequence[str]:
        return self._proto.join.left_join_columns

    @property
    def right_join_columns(self) -> Sequence[str]:
        return self._proto.join.right_join_columns

    @property
    def how(self):
        return self._proto.join.how

    def sources(self):
        return [self.left_source, self.right_source]


class SelectColumns(_Base):
    """Enumerate the columns from a source table that should be kept."""

    @property
    def columns(self) -> Sequence[str]:
        return self._proto.select_columns.columns

    @property
    def source(self) -> Op:
        return from_proto(self._proto.select_columns.source)

    def sources(self):
        return [self.source]


class LimitRows(_Base):
    """Limit the number of rows in a table."""

    @property
    def num_rows(self) -> int:
        return self._proto.limit_rows.num_rows

    @property
    def source(self) -> Op:
        return from_proto(self._proto.limit_rows.source)

    def sources(self):
        return [self.source]


class FilterRows(_Base):
    """Filter rows by applying a predicate."""

    @property
    def source(self) -> Op:
        return from_proto(self._proto.filter_rows.source)

    @property
    def row_filter(self) -> RowFilter:
        return row_filters_from_proto(self._proto.filter_rows.row_filter)

    def sources(self):
        return [self.source]


class UpdateMetadata(_Base):
    """Update table-wide metadata, overwriting old values."""

    @functools.cached_property
    def metadata_updates(self) -> Mapping[str, Any]:
        return json_format.MessageToDict(self._proto.update_metadata.metadata_updates)

    @property
    def source(self) -> Op:
        return from_proto(self._proto.update_metadata.source)

    def sources(self):
        return [self.source]


class SetMetadata(_Base):
    """Update table-wide metadata, overwriting old values."""

    @functools.cached_property
    def new_metadata(self) -> Mapping[str, Any]:
        return json_format.MessageToDict(self._proto.set_metadata.new_metadata)

    @property
    def source(self) -> Op:
        return from_proto(self._proto.set_metadata.source)

    def sources(self):
        return [self.source]


class RemoveFromMetadata(_Base):
    """Update table-wide metadata, overwriting old values."""

    @property
    def keys_to_remove(self) -> Sequence[str]:
        return self._proto.remove_from_metadata.keys_to_remove

    @property
    def source(self) -> Op:
        return from_proto(self._proto.remove_from_metadata.source)

    def sources(self):
        return [self.source]


class RollupByAggregation(_Base):
    """Compute an aggregation rollup and add it as a new column."""

    @property
    def source(self) -> Op:
        return from_proto(self._proto.rollup_by_aggregation.source)

    @property
    def group_by_column_names(self) -> Sequence[str]:
        return self._proto.rollup_by_aggregation.group_by_column_names

    @property
    def target_column_name(self) -> str:
        return self._proto.rollup_by_aggregation.target_column_name

    @property
    def aggregation_type(self):
        return self._proto.rollup_by_aggregation.aggregation_type

    def sources(self):
        return [self.source]


Op = (
    SelectFromStaging
    | RenameColumns
    | Join
    | SelectColumns
    | LimitRows
    | FilterRows
    | UpdateMetadata
    | SetMetadata
    | RemoveFromMetadata
    | UpdateFeatureTypes
    | RollupByAggregation
)

_COMPUTE_OP_FIELD_NAME_TO_OP: Final = {
    "select_from_staging": SelectFromStaging,
    "rename_columns": RenameColumns,
    "join": Join,
    "select_columns": SelectColumns,
    "limit_rows": LimitRows,
    "filter_rows": FilterRows,
    "update_metadata": UpdateMetadata,
    "set_metadata": SetMetadata,
    "remove_from_metadata": RemoveFromMetadata,
    "update_feature_types": UpdateFeatureTypes,
    "rollup_by_aggregation": RollupByAggregation,
}

_OP_TO_COMPUTE_OP_FIELD_NAME: Final[dict[type[Any], str]] = {
    op: name for name, op in _COMPUTE_OP_FIELD_NAME_TO_OP.items()
}
