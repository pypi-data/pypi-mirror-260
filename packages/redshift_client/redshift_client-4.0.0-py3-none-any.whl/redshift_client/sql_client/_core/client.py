from .primitive import (
    PrimitiveVal,
)
from .query import (
    Query,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    Maybe,
    PureIter,
    ResultE,
    Stream,
)
from typing import (
    Callable,
)


@dataclass(frozen=True)
class RowData:
    data: FrozenList[PrimitiveVal]


@dataclass(frozen=True)
class QueryValues:
    values: FrozenDict[str, PrimitiveVal]


@dataclass(frozen=True)
class Limit:
    limit: int


@dataclass(frozen=True)
class SqlClient:
    execute: Callable[[Query, QueryValues | None], Cmd[ResultE[None]]]
    batch: Callable[[Query, FrozenList[QueryValues]], Cmd[ResultE[None]]]
    values: Callable[[Query, PureIter[RowData], Limit], Cmd[ResultE[None]]]
    fetch_one: Cmd[ResultE[Maybe[RowData]]]
    fetch_all: Cmd[ResultE[FrozenList[RowData]]]
    fetch_chunk: Callable[[int], Cmd[ResultE[FrozenList[RowData]]]]
    fetch_chunks_stream: Callable[[int], Stream[ResultE[FrozenList[RowData]]]]
