from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import attrs
from pypika.functions import Cast
from pypika.terms import Term

from tecton_core.aggregation_utils import get_aggregation_function_result_type
from tecton_core.data_types import ArrayType
from tecton_core.data_types import DataType
from tecton_core.data_types import Float32Type
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int32Type
from tecton_core.data_types import Int64Type
from tecton_core.data_types import StringType
from tecton_core.query import nodes
from tecton_core.query.node_interface import QueryNode


class DuckDBArray(Term):
    def __init__(self, element_type: Union[str, Term]) -> None:
        super().__init__()
        self.element_type = element_type

    def get_sql(self, **kwargs):
        element_type_sql = (
            self.element_type.get_sql(**kwargs) if isinstance(self.element_type, Term) else self.element_type
        )
        return f"{element_type_sql}[]"


DATA_TYPE_TO_DUCKDB_TYPE: Dict[DataType, str] = {
    Int32Type(): "INT32",
    Int64Type(): "INT64",
    Float32Type(): "FLOAT",
    Float64Type(): "DOUBLE",
    StringType(): "VARCHAR",
}


def _data_type_to_duckdb_type(data_type: DataType) -> Union[str, Term]:
    if not isinstance(data_type, ArrayType):
        return DATA_TYPE_TO_DUCKDB_TYPE.get(data_type, str(data_type))

    return DuckDBArray(_data_type_to_duckdb_type(data_type.element_type))


@attrs.frozen
class PartialAggDuckDBNode(nodes.PartialAggNode):
    @classmethod
    def from_query_node(cls, query_node: nodes.PartialAggNode) -> QueryNode:
        return cls(
            dialect=query_node.dialect,
            compute_mode=query_node.compute_mode,
            input_node=query_node.input_node,
            fdw=query_node.fdw,
            window_start_column_name=query_node.window_start_column_name,
            window_end_column_name=query_node.window_end_column_name,
            aggregation_anchor_time=query_node.aggregation_anchor_time,
        )

    def _get_partial_agg_columns_and_names(self) -> List[Tuple[Term, str]]:
        """
        Primarily overwritten to do additional type casts to make DuckDB's post-aggregation types consistent with Spark

        The two main cases:
        - Integer SUMs: DuckDB will automatically convert all integer SUMs to cast to DuckDB INT128's, regardless
        of its original type. Note that when copying this out into parquet, DuckDB will convert these to doubles.
        - Averages: DuckDB will always widen the precision to doubles

        Spark, in contrast, maintains the same type for both of these cases
        """
        normal_agg_cols_with_names = super()._get_partial_agg_columns_and_names()
        schema = self.fdw.materialization_schema.to_dict()

        final_agg_cols = []
        for col, alias in normal_agg_cols_with_names:
            data_type = schema[alias]
            sql_type = _data_type_to_duckdb_type(data_type)

            final_agg_cols.append((Cast(col, sql_type), alias))

        return final_agg_cols


@attrs.frozen
class AsofJoinFullAggNodeDuckDBNode(nodes.AsofJoinFullAggNode):
    @classmethod
    def from_query_node(cls, query_node: nodes.AsofJoinFullAggNode) -> QueryNode:
        return cls(
            dialect=query_node.dialect,
            compute_mode=query_node.compute_mode,
            spine=query_node.spine,
            partial_agg_node=query_node.partial_agg_node,
            fdw=query_node.fdw,
            enable_spine_time_pushdown_rewrite=query_node.enable_spine_time_pushdown_rewrite,
            enable_spine_entity_pushdown_rewrite=query_node.enable_spine_entity_pushdown_rewrite,
        )

    def _get_aggregations(self, window_order_col: str, partition_cols: List[str]) -> List[Term]:
        aggregations = super()._get_aggregations(window_order_col, partition_cols)
        features = self.fdw.fv_spec.aggregate_features
        view_schema = self.fdw.view_schema.to_dict()

        casted_aggregations = []
        for aggregation, feature in zip(aggregations, features):
            input_type = view_schema[feature.input_feature_name]
            result_type = get_aggregation_function_result_type(feature.function, input_type)
            sql_type = _data_type_to_duckdb_type(result_type)
            casted_aggregations.append(Cast(aggregation, sql_type).as_(feature.output_feature_name))

        return casted_aggregations
