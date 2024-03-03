"""Parse table operation logs into sql statements."""

import functools
from typing import Protocol

import sqlglot

from corvic import op_graph
from corvic_generated.orm.v1 import table_pb2


class StagingQueryGenerator(Protocol):
    """A callable that generates a staging query for some backend."""

    def __call__(
        self, blob_names: list[str], column_names: list[str]
    ) -> sqlglot.exp.Subqueryable:
        ...


class _OpLogParser:
    def __init__(self, make_staging_query: StagingQueryGenerator):
        self._make_staging_query = make_staging_query
        self._id = 0

    @staticmethod
    def _quote(val: str):
        return sqlglot.to_identifier(val, quoted=True)

    def _next_name_id(self):
        val = self._id
        self._id += 1
        return val

    def _unique_name(self, name: str):
        return self._quote(f"{name}-{self._next_name_id()}")

    def _select_from_staging_to_sql(
        self, op: op_graph.op.SelectFromStaging
    ) -> sqlglot.exp.Subqueryable:
        columns = [field.name for field in op.arrow_schema]
        query = self._make_staging_query(list(op.blob_names), columns)

        def _promote_select(
            expr: sqlglot.Expression,
        ) -> sqlglot.exp.Column | sqlglot.exp.Alias:
            match expr:
                case sqlglot.exp.Column():
                    return expr
                case sqlglot.exp.Literal():
                    return sqlglot.column(
                        sqlglot.to_identifier(expr.output_name, quoted=True)
                    )
                case sqlglot.exp.Alias():
                    return expr
                case _:
                    raise op_graph.OpParseError(
                        "select must be a literal, a column type, or an alias"
                    )

        return query.select(
            *(_promote_select(expr) for expr in query.selects), append=False
        )

    def _rename_columns_to_sql(
        self,
        op: op_graph.op.RenameColumns,
    ) -> sqlglot.exp.Subqueryable:
        source_query = self.parse(op.source)

        def replace_select_if_needed(expr: sqlglot.Expression) -> sqlglot.Expression:
            if expr.output_name not in op.old_name_to_new:
                return expr
            return expr.unalias().as_(op.old_name_to_new[expr.output_name])

        return source_query.select(
            *(replace_select_if_needed(expr) for expr in source_query.selects),
            append=False,
        )

    def _join_to_sql(
        self,
        op: op_graph.op.Join,
    ) -> sqlglot.exp.Subqueryable:
        left_subquery = self.parse(op.left_source)
        left_table_name = self._unique_name("left_table")
        right_subquery = self.parse(op.right_source)
        right_table_name = self._unique_name("right_table")

        match op.how:
            case table_pb2.JOIN_TYPE_INNER:
                join_type = "INNER"
            case table_pb2.JOIN_TYPE_LEFT_OUTER:
                join_type = "LEFT OUTER"
            case _:
                join_type = "INNER"

        left_columns = (
            sqlglot.column(name, left_table_name) for name in op.left_join_columns
        )
        right_columns = (
            sqlglot.column(name, right_table_name) for name in op.right_join_columns
        )

        on_clause = functools.reduce(
            lambda first, second: first.and_(second),
            (
                left_col.eq(right_col)
                for left_col, right_col in zip(left_columns, right_columns, strict=True)
            ),
        )

        name_to_column: dict[str, sqlglot.exp.Column | sqlglot.exp.Alias] = {
            name: sqlglot.column(name, left_table_name).as_(name)
            for name in left_subquery.named_selects
        }
        for name in right_subquery.named_selects:
            if name in op.right_join_columns:
                continue
            if name not in name_to_column:
                name_to_column[name] = sqlglot.column(name, right_table_name).as_(name)

        return (
            sqlglot.select(*name_to_column.values())
            .from_(left_table_name)
            .join(
                right_table_name,
                on=on_clause,
                join_type=join_type,
            )
            .with_(left_table_name, as_=left_subquery)
            .with_(right_table_name, as_=right_subquery)
        )

    def _select_columns_to_sql(
        self,
        op: op_graph.op.SelectColumns,
    ) -> sqlglot.exp.Subqueryable:
        sub_table_name = self._unique_name("sub_table")
        return (
            sqlglot.select(
                *(
                    sqlglot.exp.column(
                        sqlglot.exp.to_identifier(name, quoted=True), sub_table_name
                    )
                    for name in op.columns
                )
            )
            .from_(sub_table_name)
            .with_(sub_table_name, as_=self.parse(op.source))
        )

    def _limit_rows_to_sql(
        self,
        op: op_graph.op.LimitRows,
    ) -> sqlglot.exp.Subqueryable:
        return self.parse(op.source).limit(op.num_rows)

    def _row_filter_to_condition(  # noqa: PLR0911
        self, row_filter: op_graph.RowFilter, table_name: sqlglot.exp.Identifier
    ) -> sqlglot.exp.Condition:
        match row_filter:
            case op_graph.row_filter.CompareColumnToLiteral():
                column = sqlglot.column(
                    sqlglot.to_identifier(row_filter.column_name, quoted=True),
                    table_name,
                )
                match row_filter.comparison_type:
                    case table_pb2.COMPARISON_TYPE_EQ:
                        return column.eq(row_filter.literal)
                    case table_pb2.COMPARISON_TYPE_NE:
                        return column.neq(row_filter.literal)
                    case table_pb2.COMPARISON_TYPE_LT:
                        return column < row_filter.literal
                    case table_pb2.COMPARISON_TYPE_GT:
                        return column > row_filter.literal
                    case table_pb2.COMPARISON_TYPE_LE:
                        return column <= row_filter.literal
                    case table_pb2.COMPARISON_TYPE_GE:
                        return column >= row_filter.literal
                    case _:
                        raise op_graph.OpParseError(
                            "unknown comparison type value in row filter",
                            value=row_filter.comparison_type,
                        )
            case op_graph.row_filter.CombineFilters():
                sub_filters = (
                    self._row_filter_to_condition(sub_filter, table_name)
                    for sub_filter in row_filter.row_filters
                )
                match row_filter.combination_op:
                    case table_pb2.LOGICAL_COMBINATION_ANY:
                        return functools.reduce(
                            lambda left, right: left.or_(right), sub_filters
                        )
                    case table_pb2.LOGICAL_COMBINATION_ALL:
                        return functools.reduce(
                            lambda left, right: left.and_(right), sub_filters
                        )
                    case _:
                        raise op_graph.OpParseError(
                            "unknown logical combination op value in row filter",
                            value=row_filter.combination_op,
                        )

    def _filter_rows_to_sql(
        self,
        op: op_graph.op.FilterRows,
    ) -> sqlglot.exp.Subqueryable:
        table_name = self._unique_name("filter_rows_table")
        where_cond = self._row_filter_to_condition(op.row_filter, table_name)
        sub_table = self.parse(op.source)
        return (
            sqlglot.select(*sub_table.named_selects)
            .from_(table_name)
            .where(where_cond)
            .with_(table_name, as_=sub_table)
        )

    def _rollup_by_aggregation_to_sql(
        self, op: op_graph.op.RollupByAggregation
    ) -> sqlglot.exp.Subqueryable:
        table_name = self._unique_name("rollup_table")
        agg_mapping = {
            table_pb2.AGGREGATION_TYPE_MODE: "mode",
            table_pb2.AGGREGATION_TYPE_COUNT: "count",
            table_pb2.AGGREGATION_TYPE_MAX: "max",
            table_pb2.AGGREGATION_TYPE_MIN: "min",
            table_pb2.AGGREGATION_TYPE_AVG: "avg",
            table_pb2.AGGREGATION_TYPE_SUM: "sum",
        }

        match op.aggregation_type:
            case table_pb2.AGGREGATION_TYPE_MODE:
                agg = agg_mapping.get(op.aggregation_type)
                expr = (
                    f"FIRST_VALUE({op.target_column_name}) OVER(PARTITION BY "
                    f"{','.join(str(i) for i in op.group_by_column_names)} "
                    f"ORDER BY COUNT(*) DESC) "
                    f"{agg}_{op.target_column_name}_{'_'.join(op.group_by_column_names)}"
                )
                query = (
                    sqlglot.select(*op.group_by_column_names, expr)
                    .distinct()
                    .group_by(*op.group_by_column_names, op.target_column_name)
                )
            case table_pb2.AGGREGATION_TYPE_COUNT:
                agg = agg_mapping.get(op.aggregation_type)
                expr = sqlglot.func(
                    str(agg), sqlglot.func("DISTINCT", op.target_column_name)
                ).as_(
                    f"{agg}_{op.target_column_name}_{'_'.join(op.group_by_column_names)}"
                )
                query = (
                    sqlglot.select(*op.group_by_column_names, expr)
                    .distinct()
                    .group_by(*op.group_by_column_names)
                )
            case (
                table_pb2.AGGREGATION_TYPE_MAX
                | table_pb2.AGGREGATION_TYPE_MIN
                | table_pb2.AGGREGATION_TYPE_AVG
                | table_pb2.AGGREGATION_TYPE_SUM
            ):
                agg = agg_mapping.get(op.aggregation_type)
                expr = sqlglot.func(str(agg), op.target_column_name).as_(
                    f"{agg}_{op.target_column_name}_{'_'.join(op.group_by_column_names)}"
                )
                query = (
                    sqlglot.select(*op.group_by_column_names, expr)
                    .distinct()
                    .group_by(*op.group_by_column_names)
                )
            case _:
                query = sqlglot.select()
        return query.from_(table_name).with_(table_name, as_=self.parse(op.source))

    def parse(  # noqa: PLR0911
        self,
        op: op_graph.Op,
    ) -> sqlglot.exp.Subqueryable:
        """Parse the op log into a sql query."""
        match op:
            case op_graph.op.SelectFromStaging():
                return self._select_from_staging_to_sql(op)
            case op_graph.op.RenameColumns():
                return self._rename_columns_to_sql(op)
            case op_graph.op.Join():
                return self._join_to_sql(op)
            case op_graph.op.SelectColumns():
                return self._select_columns_to_sql(op)
            case op_graph.op.LimitRows():
                return self._limit_rows_to_sql(op)
            case op_graph.op.FilterRows():
                return self._filter_rows_to_sql(op)
            case (
                op_graph.op.SetMetadata()
                | op_graph.op.UpdateMetadata()
                | op_graph.op.RemoveFromMetadata()
                | op_graph.op.UpdateFeatureTypes()
            ):
                return self.parse(op.source)
            case op_graph.op.RollupByAggregation() as op:
                return self._rollup_by_aggregation_to_sql(op)


def parse_op_graph(
    op: op_graph.Op | table_pb2.TableComputeOp,
    make_staging_query: StagingQueryGenerator,
) -> sqlglot.exp.Subqueryable:
    """Parse the op log into a sql query."""
    if isinstance(op, table_pb2.TableComputeOp):
        op = op_graph.op.from_proto(op)

    return _OpLogParser(make_staging_query).parse(op)
