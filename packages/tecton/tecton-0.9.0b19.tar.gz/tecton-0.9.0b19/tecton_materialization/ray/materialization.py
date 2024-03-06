import base64
import contextlib
import os
import traceback
import urllib
from functools import partial
from typing import Callable
from typing import List
from typing import Optional

import pendulum
import pyarrow.fs
import ray
from google.protobuf import timestamp_pb2

from tecton_core import conf
from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.fco_container import create_fco_container
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.offline_store import DEFAULT_OPTIONS_PROVIDERS
from tecton_core.query.builder import build_materialization_querytree
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_utils import get_data_source_dialect
from tecton_core.query.node_utils import get_pipeline_dialect
from tecton_core.query.node_utils import pipeline_has_aggregations
from tecton_core.query.node_utils import pipeline_has_odfvs
from tecton_core.query.query_tree_compute import QueryTreeCompute
from tecton_core.query.query_tree_executor import QueryTreeExecutor
from tecton_core.query.snowflake.compute import SnowflakeCompute
from tecton_core.secrets import SecretResolver
from tecton_core.snowflake_context import SnowflakeContext
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_materialization.ray import delta
from tecton_materialization.ray.delta import DeltaConcurrentModificationException
from tecton_materialization.ray.delta import DeltaWriter
from tecton_materialization.ray.delta import OfflineStoreParams
from tecton_materialization.ray.feature_export import get_feature_export_qt
from tecton_materialization.ray.feature_export import get_feature_export_store_params
from tecton_materialization.ray.job_status import JobStatusClient
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_materialization.secrets import MDSSecretResolver
from tecton_proto.materialization.job_metadata_pb2 import TectonManagedStage
from tecton_proto.materialization.params_pb2 import MaterializationTaskParams
from tecton_proto.offlinestore.delta import metadata_pb2
from tecton_proto.online_store_writer.copier_pb2 import DeletionRequest
from tecton_proto.online_store_writer.copier_pb2 import LocalFileStage
from tecton_proto.online_store_writer.copier_pb2 import ObjectCopyRequest
from tecton_proto.online_store_writer.copier_pb2 import OnlineStoreCopierRequest
from tecton_proto.online_store_writer.copier_pb2 import S3Stage
from tecton_proto.online_store_writer.copier_pb2 import StatusUpdateRequest
from tecton_proto.online_store_writer.copier_pb2 import TimestampUnit


FEATURE_EXPORT_TASK_TYPE = "feature_export"


def _get_batch_materialization_plan(
    materialization_task_params: MaterializationTaskParams,
    fd: FeatureDefinitionWrapper,
) -> NodeRef:
    feature_start_time = materialization_task_params.batch_task_info.batch_parameters.feature_start_time.ToDatetime()
    feature_end_time = materialization_task_params.batch_task_info.batch_parameters.feature_end_time.ToDatetime()
    feature_data_time_limits = pendulum.instance(feature_end_time) - pendulum.instance(feature_start_time)

    tree = build_materialization_querytree(
        dialect=Dialect.DUCKDB,
        compute_mode=ComputeMode.RIFT,
        fdw=fd,
        for_stream=False,
        feature_data_time_limits=feature_data_time_limits,
    )
    return AddTimePartitionNode.for_feature_definition(fd, tree)


_DIALECT_TO_STAGE_TYPE = {
    Dialect.PANDAS: TectonManagedStage.PYTHON,
    Dialect.DUCKDB: TectonManagedStage.PYTHON,
    Dialect.SNOWFLAKE: TectonManagedStage.SNOWFLAKE,
}

_DIALECT_TO_UI_STRING = {
    Dialect.PANDAS: "Python",
    Dialect.DUCKDB: "Python",
    Dialect.SNOWFLAKE: "Snowflake",
}

DELTA_COMMIT_MAX_ATTEMPTS = 5


def _get_compute(dialect: Dialect, qt: NodeRef, secret_resolver: Optional[SecretResolver]) -> QueryTreeCompute:
    if dialect == Dialect.SNOWFLAKE:
        if SnowflakeContext.is_initialized():
            return SnowflakeCompute.for_connection(SnowflakeContext.get_instance().get_connection())
        else:
            return SnowflakeCompute.for_query_tree(qt, secret_resolver)
    return QueryTreeCompute.for_dialect(dialect)


def _prepare_qt_executor(
    qt: NodeRef, job_status_client: JobStatusClient, secret_resolver: Optional[SecretResolver], task_type: str
) -> "QueryTreeExecutor":
    monitor_for_stage = partial(job_status_client.create_stage_monitor)
    agg_compute = QueryTreeCompute.for_dialect(Dialect.DUCKDB)
    odfv_compute = QueryTreeCompute.for_dialect(Dialect.PANDAS)

    if task_type == FEATURE_EXPORT_TASK_TYPE:
        data_source_compute = QueryTreeCompute.for_dialect(Dialect.DUCKDB)
        pipeline_monitor = monitor_for_stage(
            _DIALECT_TO_STAGE_TYPE[Dialect.DUCKDB],
            "Processing data in the staging offline store.",
        )
        pipeline_compute = QueryTreeCompute.for_dialect(Dialect.DUCKDB).with_monitoring_ctx(pipeline_monitor)
    else:
        ds_dialect = get_data_source_dialect(qt)
        ds_monitor = monitor_for_stage(
            _DIALECT_TO_STAGE_TYPE[ds_dialect], f"Loading dataset from {_DIALECT_TO_UI_STRING[ds_dialect]}"
        )
        data_source_compute = _get_compute(ds_dialect, qt, secret_resolver).with_monitoring_ctx(ds_monitor)
        # No pipeline dialect happens in the case of e.g. stream ingest api
        pipeline_dialect = get_pipeline_dialect(qt) or Dialect.PANDAS
        if pipeline_dialect == ds_dialect:
            pipeline_compute = data_source_compute
        else:
            pipeline_monitor = monitor_for_stage(
                _DIALECT_TO_STAGE_TYPE[pipeline_dialect],
                f"Processing dataset from {_DIALECT_TO_UI_STRING[pipeline_dialect]}",
            )
            pipeline_compute = _get_compute(pipeline_dialect, qt, secret_resolver).with_monitoring_ctx(pipeline_monitor)

        if pipeline_has_aggregations(qt):
            agg_compute = agg_compute.with_monitoring_ctx(
                monitor_for_stage(TectonManagedStage.StageType.AGGREGATE, "Compute aggregations")
            )

        if pipeline_has_odfvs(qt):
            odfv_compute = odfv_compute.with_monitoring_ctx(
                monitor_for_stage(TectonManagedStage.StageType.PYTHON, "Compute on-demand features")
            )

    executor = QueryTreeExecutor(
        data_source_compute=data_source_compute,
        pipeline_compute=pipeline_compute,
        agg_compute=agg_compute,
        odfv_compute=odfv_compute,
        offline_store_options_providers=DEFAULT_OPTIONS_PROVIDERS,
    )

    return executor


def _delta_writer(
    params: MaterializationTaskParams,
    progress_callback: Callable[[float], None],
    store_params_override: Optional[OfflineStoreParams] = None,
    table_uri_override: Optional[str] = None,
) -> DeltaWriter:
    role = params.dynamodb_cross_account_role if params.HasField("dynamodb_cross_account_role") else None
    fd = _get_feature_definition(params)

    return delta.DeltaWriter(
        store_params=store_params_override if store_params_override else OfflineStoreParams.for_feature_definition(fd),
        table_uri=table_uri_override if table_uri_override else params.offline_store_path,
        dynamodb_log_table_name=params.delta_log_table,
        dynamodb_log_table_region=params.dynamodb_table_region,
        dynamodb_cross_account_role=role,
        progress_callback=progress_callback,
    )


def _write_to_online_store(
    materialization_task_params: MaterializationTaskParams,
    fd: FeatureDefinitionWrapper,
    stage_uri_str: str,
) -> None:
    stage_uri = urllib.parse.urlparse(stage_uri_str)
    if stage_uri.scheme in ("file", ""):
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=materialization_task_params.online_store_writer_config,
            feature_view=materialization_task_params.feature_view,
            object_copy_request=ObjectCopyRequest(
                local_file_stage=LocalFileStage(location=stage_uri.path), timestamp_units=TimestampUnit.MICROS
            ),
        )
    elif stage_uri.scheme == "s3":
        key = stage_uri.path
        if key.startswith("/"):
            key = key[1:]
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=materialization_task_params.online_store_writer_config,
            feature_view=materialization_task_params.feature_view,
            object_copy_request=ObjectCopyRequest(
                s3_stage=S3Stage(
                    bucket=stage_uri.netloc,
                    key=key,
                ),
                timestamp_units=TimestampUnit.MICROS,
            ),
        )
    else:
        msg = f"Unexpected staging uri scheme: {stage_uri.scheme}"
        raise NotImplementedError(msg)
    _run_online_store_copier(request)

    # Issue status update
    if fd.is_temporal or fd.is_continuous:
        status_update = StatusUpdateRequest(
            materialized_raw_data_end_time=materialization_task_params.batch_task_info.batch_parameters.feature_end_time
        )
    else:
        anchor_time = (
            materialization_task_params.batch_task_info.batch_parameters.feature_end_time.ToDatetime()
            - fd.aggregate_slide_interval.ToTimedelta()
        )
        anchor_time_pb = timestamp_pb2.Timestamp()
        anchor_time_pb.FromDatetime(anchor_time)
        status_update = StatusUpdateRequest(anchor_time=anchor_time_pb)
    status_request = OnlineStoreCopierRequest(
        online_store_writer_configuration=materialization_task_params.online_store_writer_config,
        feature_view=materialization_task_params.feature_view,
        status_update_request=status_update,
    )
    _run_online_store_copier(status_request)


def _delete_from_online_store(
    materialization_task_params: MaterializationTaskParams, job_status_client: JobStatusClient
) -> None:
    online_stage_monitor = job_status_client.create_stage_monitor(
        TectonManagedStage.StageType.ONLINE_STORE,
        "Unload features to online store",
    )
    with online_stage_monitor() as progress_callback:
        if materialization_task_params.deletion_task_info.deletion_parameters.HasField("online_join_keys_path"):
            deletion_request = DeletionRequest(
                online_join_keys_path=materialization_task_params.deletion_task_info.deletion_parameters.online_join_keys_path,
            )
        else:
            deletion_request = DeletionRequest(
                online_join_keys_full_path=materialization_task_params.deletion_task_info.deletion_parameters.online_join_keys_full_path,
            )
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=materialization_task_params.online_store_writer_config,
            feature_view=materialization_task_params.feature_view,
            deletion_request=deletion_request,
        )
        _run_online_store_copier(request)
    progress_callback(1.0)


def _delete_from_offline_store(params: MaterializationTaskParams, job_status_client: JobStatusClient):
    offline_uri = params.deletion_task_info.deletion_parameters.offline_join_keys_path
    fs, path = pyarrow.fs.FileSystem.from_uri(offline_uri)
    keys_table = pyarrow.dataset.dataset(source=path, filesystem=fs).to_table()
    offline_stage_monitor = job_status_client.create_stage_monitor(
        TectonManagedStage.StageType.OFFLINE_STORE, "Delete keys from offline store"
    )
    with offline_stage_monitor() as progress_callback:
        delta_writer = _delta_writer(params, progress_callback)
        delta_writer.delete_keys(keys_table)
        delta_writer.commit()


def _run_online_store_copier(request):
    request_bytes = request.SerializeToString()
    runner_function = ray.cross_language.java_function(
        "com.tecton.onlinestorewriter.OnlineStoreCopier", "runFromSerializedRequest"
    )
    job = runner_function.remote(request_bytes, None)
    ray.get(job)


def _write_to_offline_store(
    delta_writer: DeltaWriter, materialized_data: pyarrow.Table, interval: delta.TimeInterval, is_overwrite: bool
) -> List[str]:
    transaction_metadata = metadata_pb2.TectonDeltaMetadata(feature_start_time=interval.start)
    transaction_exists = delta_writer.transaction_exists(is_overwrite, transaction_metadata)

    # if the transaction exists, we can skip commit. Files may still be needed for online writer.
    if transaction_exists:
        print(
            f"Found previous commit with metadata {transaction_metadata} for data in range {interval.start} - {interval.end}. Skipping writing to delta table."
        )
        return delta_writer.write(materialized_data)

    for attempt in range(1, DELTA_COMMIT_MAX_ATTEMPTS + 1):
        delta_writer.maybe_delete_time_range(interval, is_overwrite)
        parts = delta_writer.write(materialized_data)

        try:
            delta_writer.commit(transaction_metadata)
        except DeltaConcurrentModificationException:
            if attempt == DELTA_COMMIT_MAX_ATTEMPTS:
                raise

            print(f"Delta commit attempt {attempt} failed. Retrying...")
        else:
            return parts


def _should_write_to_online_store(materialization_params: MaterializationTaskParams):
    return materialization_params.batch_task_info.batch_parameters.write_to_online_feature_store


def _feature_export(
    fd: FeatureDefinitionWrapper,
    task_params: MaterializationTaskParams,
    job_status_client: JobStatusClient,
    secret_resolver: Optional[SecretResolver],
):
    export_params = task_params.feature_export_info.feature_export_parameters
    start_time = export_params.feature_start_time.ToDatetime()
    end_time = export_params.feature_end_time.ToDatetime()
    table_uri = export_params.export_store_path
    store_params = get_feature_export_store_params(fd)

    qt, interval = get_feature_export_qt(fd, start_time, end_time)
    executor = _prepare_qt_executor(qt, job_status_client, secret_resolver, FEATURE_EXPORT_TASK_TYPE)
    feature_data = executor.exec_qt(qt, secret_resolver).result_table

    delta_write_monitor = job_status_client.create_stage_monitor(
        TectonManagedStage.StageType.OFFLINE_STORE,
        "Write full features to offline store.",
    )

    try:
        with delta_write_monitor() as progress_callback:
            delta_writer = _delta_writer(
                task_params, progress_callback, store_params_override=store_params, table_uri_override=table_uri
            )
            # TODO (TEC-18865): add support for is_overwrite flag for feature_export jobs
            _write_to_offline_store(
                delta_writer=delta_writer,
                materialized_data=feature_data,
                interval=interval,
                is_overwrite=True,
            )
    finally:
        if delta_writer:
            delta_writer.abort()


@contextlib.contextmanager
def _ray():
    print(f"Initializing Ray from classpath: {os.environ['CLASSPATH']}")
    ray.init(
        job_config=ray.job_config.JobConfig(code_search_path=os.environ["CLASSPATH"].split(":")),
        include_dashboard=False,
    )
    try:
        yield
    finally:
        ray.shutdown()


def run_materialization(materialization_task_params: MaterializationTaskParams) -> None:
    conf.set("DUCKDB_DEBUG", "true")
    conf.set("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE", "rift")
    conf.set("TECTON_RUNTIME_MODE", "MATERIALIZATION")
    assert materialization_task_params.feature_view.schemas.HasField("materialization_schema"), "missing schema"
    job_status_client = JobStatusClient(JobMetadataClient.for_params(materialization_task_params))
    try:
        with _ray():
            run_ray_job(materialization_task_params, job_status_client)
    except Exception:
        job_status_client.set_current_stage_failed(
            TectonManagedStage.ErrorType.UNEXPECTED_ERROR,
            traceback.format_exc(),
        )
        raise


def run_ray_job(materialization_task_params: MaterializationTaskParams, job_status_client: JobStatusClient) -> None:
    fd = _get_feature_definition(materialization_task_params)
    secret_resolver = _get_secret_resolver(materialization_task_params)
    task_type = _get_task_type(materialization_task_params)

    if task_type == "deletion_task":
        _delete_from_offline_store(materialization_task_params, job_status_client)
        _delete_from_online_store(materialization_task_params, job_status_client)
        return

    if task_type == "delta_maintenance_task":
        delta_writer = _delta_writer(materialization_task_params, progress_callback=lambda p: None)
        maintenance_params = materialization_task_params.delta_maintenance_task_info.delta_maintenance_parameters
        delta_log_table_name = materialization_task_params.delta_log_table
        delta_log_table_region = materialization_task_params.dynamodb_table_region
        cross_account_role = (
            materialization_task_params.dynamodb_cross_account_role
            if materialization_task_params.HasField("dynamodb_cross_account_role")
            else None
        )
        delta_writer.run_maintenance(
            maintenance_params.execute_compaction,
            maintenance_params.vacuum,
            delta_log_table_name,
            delta_log_table_region,
            cross_account_role,
        )
        return

    if task_type == FEATURE_EXPORT_TASK_TYPE:
        _feature_export(fd, materialization_task_params, job_status_client, secret_resolver)
        return

    if task_type != "batch_task":
        msg = f"Task type {task_type} is not supported by Ray materialization job"
        raise ValueError(msg)

    assert fd.writes_to_offline_store, f"Offline materialization is required for FeatureView {fd.id} ({fd.name})"
    assert fd.has_delta_offline_store, f"Delta is required for FeatureView {fd.id} ({fd.name})"

    qt = _get_batch_materialization_plan(materialization_task_params, fd)
    executor = _prepare_qt_executor(qt, job_status_client, secret_resolver, task_type)
    offline_stage_monitor = job_status_client.create_stage_monitor(
        TectonManagedStage.StageType.OFFLINE_STORE,
        "Unload features to offline store",
    )
    online_stage_monitor = (
        job_status_client.create_stage_monitor(
            TectonManagedStage.StageType.ONLINE_STORE,
            "Unload features to online store",
        )
        if _should_write_to_online_store(materialization_task_params)
        else None
    )

    materialized_data = executor.exec_qt(qt, secret_resolver).result_table

    interval = delta.TimeInterval(
        start=materialization_task_params.batch_task_info.batch_parameters.feature_start_time,
        end=materialization_task_params.batch_task_info.batch_parameters.feature_end_time,
    )
    is_overwrite = materialization_task_params.batch_task_info.batch_parameters.is_overwrite

    try:
        with offline_stage_monitor() as progress_callback:
            delta_writer = _delta_writer(materialization_task_params, progress_callback)
            parts = _write_to_offline_store(
                delta_writer,
                materialized_data,
                interval,
                is_overwrite,
            )

        if _should_write_to_online_store(materialization_task_params):
            with online_stage_monitor() as progress_callback:
                # TODO(meastham): Probably should send these all at once to the online store copier
                for uri in parts:
                    _write_to_online_store(materialization_task_params, fd, uri)

                progress_callback(1.0)
    finally:
        # cleaning up any left-over files and state that weren't part of a successful commit
        if delta_writer:
            delta_writer.abort()


def _get_feature_definition(materialization_task_params: MaterializationTaskParams) -> FeatureDefinitionWrapper:
    fco_container = create_fco_container(
        list(materialization_task_params.virtual_data_sources)
        + list(materialization_task_params.transformations)
        + list(materialization_task_params.entities),
        deserialize_funcs_to_main=True,
    )
    fv_spec = specs.create_feature_view_spec_from_data_proto(materialization_task_params.feature_view)
    fd = FeatureDefinitionWrapper(fv_spec, fco_container)
    return fd


def _get_task_type(materialization_task_params: MaterializationTaskParams) -> str:
    return materialization_task_params.WhichOneof("task_info")[:-5]  # removesuffix("_info")


def _get_secret_resolver(materialization_task_params: MaterializationTaskParams) -> SecretResolver:
    if materialization_task_params.secrets_api_service_url:
        assert materialization_task_params.secret_access_api_key
        return MDSSecretResolver(
            materialization_task_params.secrets_api_service_url, materialization_task_params.secret_access_api_key
        )
    else:
        return None


def main():
    params = MaterializationTaskParams()
    params.ParseFromString(base64.standard_b64decode(os.environ["MATERIALIZATION_TASK_PARAMS"]))
    run_materialization(params)


if __name__ == "__main__":
    main()
