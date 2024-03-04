from __future__ import annotations

import concurrent.futures
import contextlib
import functools
import os
from typing import TYPE_CHECKING, Any, Callable, Mapping, Optional, Sequence, cast

import packaging.version
import pyarrow as pa

from chalk.clogging import chalk_logger
from chalk.features import Feature
from chalk.integrations.named import load_integration_variable
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource, SQLSourceKind, validate_dtypes_for_efficient_execution
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.utils.df_utils import pa_array_to_pl_series
from chalk.utils.executor import DEFAULT_IO_EXECUTOR
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection
    from sqlalchemy.engine.url import URL
    from sqlalchemy.sql.ddl import CreateTable, DropTable
    from sqlalchemy.sql.schema import Table


try:
    import sqlalchemy as sa
except ImportError:
    sa = None

if sa is None:
    _supported_sqlalchemy_types_for_pa_querying = ()
else:
    _supported_sqlalchemy_types_for_pa_querying = (
        sa.BigInteger,
        sa.Boolean,
        sa.BINARY,
        sa.BLOB,
        sa.LargeBinary,
        sa.Float,
        sa.Integer,
        sa.Time,
        sa.String,
        sa.Text,
        sa.VARBINARY,
        sa.DateTime,
        sa.Date,
        sa.SmallInteger,
        sa.BIGINT,
        sa.BOOLEAN,
        sa.CHAR,
        sa.DATETIME,
        sa.FLOAT,
        sa.INTEGER,
        sa.SMALLINT,
        sa.TEXT,
        sa.TIMESTAMP,
        sa.VARCHAR,
    )


@functools.lru_cache(None)
def _has_new_fetch_arrow_all():
    # The api for fetch arrow all changed in v3.7.0 to include force_return_table
    # See https://github.com/snowflakedb/snowflake-connector-python/blob/3cced62f2d31b84299b544222c836a275a6d45a2/src/snowflake/connector/cursor.py#L1344
    import snowflake.connector

    return packaging.version.parse(snowflake.connector.__version__) >= packaging.version.parse("3.7.0")


class SnowflakeSourceImpl(BaseSQLSource):
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        account_identifier: Optional[str] = None,
        warehouse: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        db: Optional[str] = None,
        schema: Optional[str] = None,
        role: Optional[str] = None,
        engine_args: Optional[dict[str, Any]] = None,
        executor: Optional[concurrent.futures.ThreadPoolExecutor] = None,
    ):
        try:
            import snowflake.connector  # noqa
            import snowflake.sqlalchemy  # noqa
        except ModuleNotFoundError:
            raise missing_dependency_exception("chalkpy[snowflake]")
        del snowflake  # unused
        if engine_args is None:
            engine_args = {}
        engine_args.setdefault("pool_size", 20)
        engine_args.setdefault("max_overflow", 60)
        engine_args.setdefault(
            "connect_args",
            {
                "client_prefetch_threads": min((os.cpu_count() or 1) * 2, 32),
                "client_session_keep_alive": True,
                "application_name": "chalkai_featurepipelines",
            },
        )

        self.account_identifier = account_identifier or load_integration_variable(
            integration_name=name, name="SNOWFLAKE_ACCOUNT_ID"
        )
        self.warehouse = warehouse or load_integration_variable(integration_name=name, name="SNOWFLAKE_WAREHOUSE")
        self.user = user or load_integration_variable(integration_name=name, name="SNOWFLAKE_USER")
        self.password = password or load_integration_variable(integration_name=name, name="SNOWFLAKE_PASSWORD")
        self.db = db or load_integration_variable(integration_name=name, name="SNOWFLAKE_DATABASE")
        self.schema = schema or load_integration_variable(integration_name=name, name="SNOWFLAKE_SCHEMA")
        self.role = role or load_integration_variable(integration_name=name, name="SNOWFLAKE_ROLE")
        self.executor = executor or DEFAULT_IO_EXECUTOR
        BaseSQLSource.__init__(self, name=name, engine_args=engine_args, async_engine_args={})

    kind = SQLSourceKind.snowflake

    def get_sqlglot_dialect(self) -> str | None:
        return "snowflake"

    def local_engine_url(self) -> URL:
        from sqlalchemy.engine.url import URL

        query = {
            k: v
            for k, v in (
                {
                    "database": self.db,
                    "schema": self.schema,
                    "warehouse": self.warehouse,
                    "role": self.role,
                }
            ).items()
            if v is not None
        }
        return URL.create(
            drivername="snowflake",
            username=self.user,
            password=self.password,
            host=self.account_identifier,
            query=query,
        )

    def execute_to_result_handles(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
    ):
        # these imports are safe because the only way we end up here is if we have a valid SnowflakeSource constructed,
        # which already gates this import
        import snowflake.connector
        from sqlalchemy.sql import Select

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(finalized_query.query, _supported_sqlalchemy_types_for_pa_querying)

        with (
            self.get_engine().connect() if connection is None else contextlib.nullcontext(connection)
        ) as sqlalchemy_cnx:
            con = cast(snowflake.connector.SnowflakeConnection, sqlalchemy_cnx.connection.dbapi_connection)
            chalk_logger.info("Established connection with Snowflake")
            sql, positional_params, named_params = self.compile_query(finalized_query)
            assert len(positional_params) == 0, "using named param style"
            with con.cursor() as cursor:
                chalk_logger.info("Acquired cursor for Snowflake query. Executing.")
                res = cursor.execute(sql, named_params)
                chalk_logger.info("Executed Snowflake query. Fetching results.")
                chalk_logger.info(f"Compiled query: {sql}")
                assert res is not None

                chalk_logger.info("Fetching result batches from snowflake.")
                ans = cursor.get_result_batches()
                assert ans is not None, "No batches returned"
                return ans

    def execute_to_batches(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
    ):
        for b in self.execute_to_result_handles(finalized_query, columns_to_features, connection):
            chalk_logger.info(f"Fetched batch with {b.uncompressed_size} bytes (uncompressed), {b.rowcount} rows.")
            yield b.to_arrow()

    @contextlib.contextmanager
    def _create_temp_table(
        self,
        create_temp_table: CreateTable,
        temp_table: Table,
        drop_temp_table: DropTable,
        connection: Connection,
        temp_value: pa.Table,
    ):
        from snowflake.connector import pandas_tools
        from snowflake.connector.connection import SnowflakeConnection

        snowflake_cnx = cast(SnowflakeConnection, connection.connection.dbapi_connection)
        with snowflake_cnx.cursor() as cursor:
            chalk_logger.info(f"Creating temporary table {temp_table.name} in Snowflake.")
            cursor.execute(create_temp_table.compile(dialect=self.get_sqlalchemy_dialect()).string)
            try:
                pandas_tools.write_pandas(
                    cursor.connection,
                    temp_value.to_pandas(),
                    str(temp_table.name),
                )
                yield
            finally:
                # "temp table", to snowflake, means that it belongs to the session. However, we keep using the same Snowflake session
                chalk_logger.info(f"Dropping temporary table {temp_table.name} in Snowflake.")
                cursor.execute(drop_temp_table.compile(dialect=self.get_sqlalchemy_dialect()).string)

    def _postprocess_table(self, features: Mapping[str, Feature], tbl: pa.Table):
        columns: list[pa.Array] = []
        column_names: list[str] = []

        for col_name, feature in features.items():
            column = tbl[col_name]
            expected_type = feature.converter.pyarrow_dtype
            actual_type = tbl.schema.field(col_name).type
            if pa.types.is_list(expected_type) or pa.types.is_large_list(expected_type):
                if pa.types.is_string(actual_type) or pa.types.is_large_string(actual_type):
                    series = pa_array_to_pl_series(tbl[col_name])
                    column = series.str.json_extract(feature.converter.polars_dtype).to_arrow().cast(expected_type)
            if actual_type != expected_type:
                column = column.cast(expected_type)
            if isinstance(column, pa.ChunkedArray):
                column = column.combine_chunks()
            columns.append(column)
            column_names.append(feature.root_fqn)

        chalk_logger.info(f"Received a PyArrow table from Snowflake with {len(tbl)} rows; {tbl.nbytes=}")
        return pa.RecordBatch.from_arrays(arrays=columns, names=column_names)

    def _execute_query_efficient(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: Optional[Connection],
        query_execution_parameters: QueryExecutionParameters,
    ):
        # these imports are safe because the only way we end up here is if we have a valid SnowflakeSource constructed,
        # which already gates this import
        import snowflake.connector
        from sqlalchemy.sql import Select

        if isinstance(finalized_query.query, Select):
            validate_dtypes_for_efficient_execution(finalized_query.query, _supported_sqlalchemy_types_for_pa_querying)

        with (
            self.get_engine().connect() if connection is None else contextlib.nullcontext(connection)
        ) as sqlalchemy_cnx:
            con = cast(snowflake.connector.SnowflakeConnection, sqlalchemy_cnx.connection.dbapi_connection)
            chalk_logger.info("Established connection with Snowflake")
            sql, positional_params, named_params = self.compile_query(finalized_query)
            assert len(positional_params) == 0, "using named param style"
            with contextlib.ExitStack() as exit_stack:
                for (
                    _,
                    temp_value,
                    create_temp_table,
                    temp_table,
                    drop_temp_table,
                ) in finalized_query.temp_tables.values():
                    exit_stack.enter_context(
                        self._create_temp_table(
                            create_temp_table, temp_table, drop_temp_table, sqlalchemy_cnx, temp_value
                        )
                    )
                with con.cursor() as cursor:
                    chalk_logger.info(f"Compiled query: {repr(sql)}")
                    res = cursor.execute(sql, named_params)
                    chalk_logger.info("Executed Snowflake query. Fetching results.")
                    assert res is not None

                    chalk_logger.info("Fetching arrow tables from Snowflake.")
                    result_batches = cursor.get_result_batches()
                    assert result_batches is not None
                    yielded = False
                    futures = [self.executor.submit(x.to_arrow) for x in result_batches]
                    for result_batch in concurrent.futures.as_completed(futures):
                        tbl = result_batch.result()
                        if len(tbl) == 0:
                            continue
                        assert isinstance(tbl, pa.Table)
                        features = columns_to_features(tbl.schema.names)
                        yield self._postprocess_table(features, tbl)
                        yielded = True
                    if not yielded and query_execution_parameters.yield_empty_batches:
                        if _has_new_fetch_arrow_all():
                            tbl = cursor.fetch_arrow_all(True)
                            assert isinstance(tbl, pa.Table)
                            features = columns_to_features(tbl.schema.names)
                            yield self._postprocess_table(features, tbl)

    @classmethod
    def register_sqlalchemy_compiler_overrides(cls):
        try:
            from chalk.sql._internal.integrations.snowflake_compiler_overrides import register_snowflake_compiler_hooks
        except ImportError:
            raise missing_dependency_exception("chalkpy[snowflake]")
        register_snowflake_compiler_hooks()
