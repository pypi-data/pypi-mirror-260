from . import (
    _encode,
)
from ._assert import (
    to_column,
)
from fa_purity import (
    PureIter,
    ResultE,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
)
from fa_purity.pure_iter.factory import (
    PureIterFactory,
)
from fa_purity.result import (
    Result,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.utils import (
    cast_exception,
)
from redshift_client import (
    _utils,
)
from redshift_client.client._core import (
    AwsRole,
    NanHandler,
    S3Prefix,
)
from redshift_client.core.column import (
    Column,
    ColumnId,
    ColumnObj,
)
from redshift_client.core.id_objs import (
    DbTableId,
    Identifier,
    TableId,
)
from redshift_client.core.table import (
    ManifestId,
    Table,
)
from redshift_client.sql_client import (
    Limit,
    PrimitiveVal,
    Query,
    QueryValues,
    RowData,
    SqlClient,
)
from typing import (
    Dict,
    TypeVar,
)

_T = TypeVar("_T")


def _assert_bool(raw: _T) -> bool:
    if isinstance(raw, bool):
        return raw
    raise TypeError("Expected bool")


def unload(
    client: SqlClient, table: DbTableId, prefix: S3Prefix, role: AwsRole
) -> Cmd[ResultE[ManifestId]]:
    """
    prefix: a s3 uri prefix
    role: an aws role id-arn
    """
    stm = """
        UNLOAD ('SELECT * FROM {schema}.{table}')
        TO %(prefix)s iam_role %(role)s MANIFEST ESCAPE
    """
    args: Dict[str, PrimitiveVal] = {
        "prefix": prefix.prefix,
        "role": role.role,
    }
    return client.execute(
        Query.dynamic_query(
            stm,
            FrozenDict(
                {
                    "schema": table.schema.name.to_str(),
                    "table": table.table.name.to_str(),
                }
            ),
        ),
        QueryValues(FrozenDict(args)),
    ).map(lambda r: r.map(lambda _: ManifestId(f"{prefix}manifest")))


def load(
    client: SqlClient,
    table: DbTableId,
    manifest: ManifestId,
    role: AwsRole,
    nan_handler: NanHandler,
) -> Cmd[ResultE[None]]:
    """
    If `nan_handler` is disabled, ensure that the table does not contain NaN values on float columns
    """
    nan_fix = "NULL AS 'nan'" if nan_handler.enabled else ""
    stm = f"""
        COPY {{schema}}.{{table}} FROM %(manifest_file)s
        iam_role %(role)s MANIFEST ESCAPE {nan_fix}
    """
    args: Dict[str, PrimitiveVal] = {
        "manifest_file": manifest.uri,
        "role": role.role,
    }
    return client.execute(
        Query.dynamic_query(
            stm,
            FrozenDict(
                {
                    "schema": table.schema.name.to_str(),
                    "table": table.table.name.to_str(),
                }
            ),
        ),
        QueryValues(FrozenDict(args)),
    )


def get(client: SqlClient, table: DbTableId) -> Cmd[ResultE[Table]]:
    stm = """
        SELECT ordinal_position,
            column_name,
            data_type,
            CASE WHEN character_maximum_length IS not null
                    THEN character_maximum_length
                    ELSE numeric_precision end AS max_length,
            numeric_scale,
            is_nullable,
            column_default AS default_value
        FROM information_schema.columns
        WHERE table_schema = %(table_schema)s
            AND table_name = %(table_name)s
        ORDER BY ordinal_position
    """
    args: Dict[str, PrimitiveVal] = {
        "table_schema": table.schema.name.to_str(),
        "table_name": table.table.name.to_str(),
    }
    exe = client.execute(
        Query.new_query(stm),
        QueryValues(FrozenDict(args)),
    )
    results = client.fetch_all

    def _extract(raw: FrozenList[RowData]) -> ResultE[Table]:
        columns_pairs = all_ok(
            PureIterFactory.from_list(raw)
            .map(lambda c: to_column(c.data))
            .to_list()
        )
        columns = columns_pairs.map(lambda i: FrozenDict(dict(i)))
        order = columns_pairs.map(
            lambda i: PureIterFactory.from_list(i).map(lambda c: c[0])
        )
        return columns.bind(
            lambda c: order.bind(
                lambda o: Table.new(o.to_list(), c, frozenset())
            )
        )

    return _utils.chain_results(exe, results).map(lambda r: r.bind(_extract))


def exist(client: SqlClient, table: DbTableId) -> Cmd[ResultE[bool]]:
    stm = """
        SELECT EXISTS (
            SELECT * FROM information_schema.tables
            WHERE table_schema = %(table_schema)s
            AND table_name = %(table_name)s
        );
    """
    args: Dict[str, PrimitiveVal] = {
        "table_schema": table.schema.name.to_str(),
        "table_name": table.table.name.to_str(),
    }
    return _utils.chain_results(
        client.execute(Query.new_query(stm), QueryValues(FrozenDict(args))),
        client.fetch_one.map(
            lambda r: r.bind(
                lambda m: m.to_result()
                .alt(lambda _: cast_exception(TypeError("Expected not None")))
                .bind(
                    lambda v: JsonPrimitiveFactory.from_any(v).bind(
                        JsonPrimitiveUnfolder.to_bool
                    )
                )
            )
        ),
    )


def insert(
    client: SqlClient,
    table_id: DbTableId,
    table: Table,
    items: PureIter[RowData],
    limit: Limit,
) -> Cmd[ResultE[None]]:
    _fields = ",".join(f"{{field_{i}}}" for i, _ in enumerate(table.order))
    stm = f"""
        INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES %s
    """
    identifiers: Dict[str, str] = {
        "schema": table_id.schema.name.to_str(),
        "table": table_id.table.name.to_str(),
    }
    for i, c in enumerate(table.order):
        identifiers[f"field_{i}"] = c.name.to_str()
    return client.values(
        Query.dynamic_query(stm, FrozenDict(identifiers)), items, limit
    )


def rename(
    client: SqlClient, table_id: DbTableId, new_name: str
) -> Cmd[ResultE[TableId]]:
    stm = """
        ALTER TABLE {schema}.{table} RENAME TO {new_name}
    """
    identifiers: Dict[str, str] = {
        "schema": table_id.schema.name.to_str(),
        "table": table_id.table.name.to_str(),
        "new_name": new_name,
    }
    return client.execute(
        Query.dynamic_query(stm, FrozenDict(identifiers)), None
    ).map(lambda r: r.map(lambda _: TableId(Identifier.new(new_name))))


def delete(
    client: SqlClient, table_id: DbTableId, cascade: bool
) -> Cmd[ResultE[None]]:
    _cascade = "CASCADE" if cascade else ""
    stm = f"""
        DROP TABLE {{schema}}.{{table}} {_cascade}
    """
    identifiers: Dict[str, str] = {
        "schema": table_id.schema.name.to_str(),
        "table": table_id.table.name.to_str(),
    }
    return client.execute(
        Query.dynamic_query(stm, FrozenDict(identifiers)), None
    )


def add_column(
    client: SqlClient, table_id: DbTableId, column: ColumnObj
) -> Cmd[ResultE[None]]:
    stm = f"""
        ALTER TABLE {{table_schema}}.{{table_name}}
        ADD COLUMN {{column_name}}
        {_encode.encode_data_type(column.column.data_type)} DEFAULT %(default_val)s
    """
    identifiers: Dict[str, str] = {
        "table_schema": table_id.schema.name.to_str(),
        "table_name": table_id.table.name.to_str(),
        "column_name": column.id_obj.name.to_str(),
    }
    args: Dict[str, PrimitiveVal] = {
        "default_val": column.column.default,
    }
    return client.execute(
        Query.dynamic_query(stm, FrozenDict(identifiers)),
        QueryValues(FrozenDict(args)),
    )


def add_columns(
    client: SqlClient,
    table: DbTableId,
    columns: FrozenDict[ColumnId, Column],
) -> Cmd[ResultE[None]]:
    return (
        PureIterFactory.from_list(tuple(columns.items()))
        .map(lambda c: ColumnObj(c[0], c[1]))
        .map(lambda c: add_column(client, table, c))
        .transform(lambda x: _utils.extract_fail(x))
    )


def create_like(
    client: SqlClient, blueprint: DbTableId, new_table: DbTableId
) -> Cmd[ResultE[None]]:
    stm = """
        CREATE TABLE {new_schema}.{new_table} (
            LIKE {blueprint_schema}.{blueprint_table}
        )
    """
    identifiers: Dict[str, str] = {
        "blueprint_schema": blueprint.schema.name.to_str(),
        "blueprint_table": blueprint.table.name.to_str(),
        "new_schema": new_table.schema.name.to_str(),
        "new_table": new_table.table.name.to_str(),
    }
    return client.execute(
        Query.dynamic_query(stm, FrozenDict(identifiers)), None
    )


def move_data(
    client: SqlClient, source: DbTableId, target: DbTableId
) -> Cmd[ResultE[None]]:
    """
    This method moves data from source to target.
    - After the operation source will be empty.
    - Both tables must exists.
    """
    stm = """
        ALTER TABLE {target_schema}.{target_table}
        APPEND FROM {source_schema}.{source_table}
    """
    identifiers: Dict[str, str] = {
        "source_schema": source.schema.name.to_str(),
        "source_table": source.table.name.to_str(),
        "target_schema": target.schema.name.to_str(),
        "target_table": target.table.name.to_str(),
    }
    return client.execute(
        Query.dynamic_query(stm, FrozenDict(identifiers)), None
    )


def move(
    client: SqlClient, source: DbTableId, target: DbTableId
) -> Cmd[ResultE[None]]:
    """
    - create target if not exist
    - move_data (append) data from source into target
    - delete source table (that will be empty)
    """
    nothing: Cmd[ResultE[None]] = Cmd.from_cmd(lambda: Result.success(None))
    create = _utils.chain(
        exist(client, target),
        lambda b: create_like(client, source, target) if not b else nothing,
    ).map(lambda r: r.bind(lambda v: v))
    return _utils.chain_results(
        _utils.chain_results(create, move_data(client, source, target)),
        delete(client, source, True),
    )


def migrate(
    client: SqlClient, source: DbTableId, target: DbTableId
) -> Cmd[ResultE[None]]:
    """
    - delete target if exist
    - move source into target (see move method)
    """
    nothing: Cmd[ResultE[None]] = Cmd.from_cmd(lambda: Result.success(None))
    _delete = _utils.chain(
        exist(client, target),
        lambda b: delete(client, target, True) if b else nothing,
    ).map(lambda r: r.bind(lambda v: v))
    return _utils.chain_results(_delete, move(client, source, target))
