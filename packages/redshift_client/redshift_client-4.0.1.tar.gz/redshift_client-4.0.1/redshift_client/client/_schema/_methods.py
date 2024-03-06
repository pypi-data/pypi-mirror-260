from fa_purity import (
    Result,
    ResultE,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
)
from fa_purity.pure_iter.factory import (
    PureIterFactory,
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
from redshift_client.client._table import (
    new_table_client,
)
from redshift_client.core.id_objs import (
    DbTableId,
    Identifier,
    SchemaId,
    TableId,
)
from redshift_client.core.schema import (
    Quota,
    SchemaPolicy,
)
from redshift_client.sql_client import (
    PrimitiveVal,
    Query,
    QueryValues,
    SqlClient,
)
from typing import (
    Callable,
    Dict,
    FrozenSet,
)


def all_schemas(client: SqlClient) -> Cmd[ResultE[FrozenSet[SchemaId]]]:
    _stm = (
        "SELECT s.nspname AS table_schema",
        "FROM pg_catalog.pg_namespace s",
        "JOIN pg_catalog.pg_user u ON u.usesysid = s.nspowner",
        "ORDER BY table_schema",
    )
    stm = " ".join(_stm)
    return _utils.chain_results(
        client.execute(Query.new_query(stm), None),
        client.fetch_all.map(
            lambda r: r.map(
                lambda i: PureIterFactory.from_list(i).map(
                    lambda e: _utils.get_index(e.data, 0).bind(
                        lambda v: JsonPrimitiveFactory.from_any(v)
                        .bind(JsonPrimitiveUnfolder.to_str)
                        .map(lambda s: SchemaId(Identifier.new(s)))
                    )
                )
            ).bind(lambda i: all_ok(i.to_list()).map(lambda s: frozenset(s)))
        ),
    )


def table_ids(
    client: SqlClient, schema: SchemaId
) -> Cmd[ResultE[FrozenSet[DbTableId]]]:
    _stm = (
        "SELECT tables.table_name FROM information_schema.tables",
        "WHERE table_schema = %(schema_name)s",
    )
    stm = " ".join(_stm)
    args: Dict[str, PrimitiveVal] = {"schema_name": schema.name.to_str()}
    return _utils.chain_results(
        client.execute(Query.new_query(stm), QueryValues(FrozenDict(args))),
        client.fetch_all.map(
            lambda r: r.map(
                lambda i: PureIterFactory.from_list(i).map(
                    lambda e: _utils.get_index(e.data, 0).bind(
                        lambda v: JsonPrimitiveFactory.from_any(v)
                        .bind(JsonPrimitiveUnfolder.to_str)
                        .map(
                            lambda s: DbTableId(
                                schema, TableId(Identifier.new(s))
                            )
                        )
                    )
                )
            ).bind(lambda i: all_ok(i.to_list()).map(lambda s: frozenset(s)))
        ),
    )


def exist(client: SqlClient, schema: SchemaId) -> Cmd[ResultE[bool]]:
    _stm = (
        "SELECT EXISTS",
        "(SELECT 1 FROM pg_namespace",
        "WHERE nspname = %(schema_name)s)",
    )
    stm = " ".join(_stm)
    args: Dict[str, PrimitiveVal] = {"schema_name": schema.name.to_str()}
    get_result = client.fetch_one.map(
        lambda r: r.bind(
            lambda m: m.map(
                lambda p: _utils.get_index(p.data, 0).bind(
                    lambda v: JsonPrimitiveFactory.from_any(v).bind(
                        JsonPrimitiveUnfolder.to_bool
                    )
                )
            ).value_or(
                Result.failure(
                    cast_exception(TypeError("Expected not None")), bool
                )
            )
        )
    )
    return _utils.chain_results(
        client.execute(Query.new_query(stm), QueryValues(FrozenDict(args))),
        get_result,
    )


def delete(
    client: SqlClient, schema: SchemaId, cascade: bool
) -> Cmd[ResultE[None]]:
    opt = " CASCADE" if cascade else ""
    stm: str = "DROP SCHEMA {schema_name}" + opt
    return client.execute(
        Query.dynamic_query(
            stm, FrozenDict({"schema_name": schema.name.to_str()})
        ),
        None,
    )


def rename(
    client: SqlClient, old: SchemaId, new: SchemaId
) -> Cmd[ResultE[None]]:
    stm = "ALTER SCHEMA {from_schema} RENAME TO {to_schema}"
    return client.execute(
        Query.dynamic_query(
            stm,
            FrozenDict(
                {
                    "from_schema": old.name.to_str(),
                    "to_schema": new.name.to_str(),
                }
            ),
        ),
        None,
    )


def create(
    client: SqlClient, schema: SchemaId, if_not_exist: bool = False
) -> Cmd[ResultE[None]]:
    not_exist = " IF NOT EXISTS " if if_not_exist else ""
    stm = f"CREATE SCHEMA {not_exist} {{schema}}"
    return client.execute(
        Query.dynamic_query(stm, FrozenDict({"schema": schema.name.to_str()})),
        None,
    )


def recreate(
    client: SqlClient, schema: SchemaId, cascade: bool
) -> Cmd[ResultE[None]]:
    nothing = Cmd.from_cmd(lambda: Result.success(None, Exception))
    _exists = _utils.chain(
        exist(client, schema),
        lambda b: delete(client, schema, cascade) if b else nothing,
    ).map(lambda r: r.bind(lambda x: x))
    return _utils.chain_results(_exists, create(client, schema))


def _move(
    client: SqlClient,
    source: SchemaId,
    target: SchemaId,
    move_op: Callable[[DbTableId, DbTableId], Cmd[ResultE[None]]],
) -> Cmd[ResultE[None]]:
    move_tables = _utils.chain(
        table_ids(client, source),
        lambda t: PureIterFactory.from_list(tuple(t))
        .map(lambda t: move_op(t, DbTableId(target, t.table)))
        .transform(lambda x: _utils.extract_fail(x)),
    ).map(lambda r: r.bind(lambda x: x))
    return _utils.chain(
        move_tables, lambda _: delete(client, source, False)
    ).map(lambda r: r.bind(lambda x: x))


def migrate(
    client: SqlClient, source: SchemaId, target: SchemaId
) -> Cmd[ResultE[None]]:
    tb = new_table_client(client)
    return _move(client, source, target, tb.migrate)


def move(
    client: SqlClient, source: SchemaId, target: SchemaId
) -> Cmd[ResultE[None]]:
    tb = new_table_client(client)
    return _move(client, source, target, tb.move)


def set_policy(
    client: SqlClient, schema: SchemaId, policy: SchemaPolicy
) -> Cmd[ResultE[None]]:
    stm = "ALTER SCHEMA {schema} OWNER TO {owner}"
    stm2 = (
        f"ALTER SCHEMA {{schema}} QUOTA %(quota)s {policy.quota.unit.value}"
        if isinstance(policy.quota, Quota)
        else "ALTER SCHEMA {schema} QUOTA UNLIMITED"
    )
    set_owner = client.execute(
        Query.dynamic_query(
            stm,
            FrozenDict(
                {"schema": schema.name.to_str(), "owner": policy.owner}
            ),
        ),
        None,
    )
    id_args: Dict[str, str] = {"schema": schema.name.to_str()}
    args: Dict[str, PrimitiveVal] = (
        {"quota": policy.quota.value}
        if isinstance(policy.quota, Quota)
        else {}
    )
    set_quota = client.execute(
        Query.dynamic_query(stm2, FrozenDict(id_args)),
        QueryValues(FrozenDict(args)),
    )
    return _utils.chain_results(set_owner, set_quota)
