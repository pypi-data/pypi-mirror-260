from arch_lint.dag import (
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)
from fa_purity import (
    FrozenList,
)
from typing import (
    Dict,
    FrozenSet,
    TypeVar,
    Union,
)

_dag: Dict[str, FrozenList[Union[FrozenList[str], str]]] = {
    "redshift_client": (
        "client",
        "core",
        "sql_client",
        "_utils",
    ),
    "redshift_client.core": (
        "schema",
        "table",
        "column",
        ("data_type", "id_objs"),
    ),
    "redshift_client.core.data_type": (
        "decode",
        "alias",
        "core",
    ),
    "redshift_client.client": (
        "_factory",
        "_schema",
        "_table",
        "_core",
    ),
    "redshift_client.client._table": (
        ("_new", "_methods"),
        "_encode",
        "_assert",
    ),
    "redshift_client.sql_client": (
        "_factory",
        ("_client_1", "_temp_creds"),
        "_core",
    ),
    "redshift_client.sql_client._core": (
        ("connection", "client"),
        ("primitive", "query", "creds"),
    ),
}
_T = TypeVar("_T")


def raise_or_return(item: Union[Exception, _T]) -> _T:
    if isinstance(item, Exception):
        raise item
    return item


def project_dag() -> DagMap:
    return raise_or_return(DagMap.new(_dag))


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {
        "psycopg2": frozenset(
            [
                "redshift_client.sql_client._client_1",
                "redshift_client.sql_client._core.query",
                "redshift_client.sql_client._core.connection",
            ]
        ),
    }
    return {
        raise_or_return(FullPathModule.from_raw(k)): frozenset(
            raise_or_return(FullPathModule.from_raw(i)) for i in v
        )
        for k, v in _raw.items()
    }
