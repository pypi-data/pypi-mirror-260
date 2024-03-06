from . import (
    _assert,
)
from .._core.client import (
    Limit,
    QueryValues,
    RowData,
    SqlClient,
)
from .._core.primitive import (
    PrimitiveVal,
)
from .._core.query import (
    Query,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Maybe,
    PureIter,
    Result,
    ResultE,
    Stream,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.pure_iter.factory import (
    PureIterFactory,
)
from fa_purity.result import (
    ResultFactory,
)
from fa_purity.stream.factory import (
    StreamFactory,
    unsafe_from_cmd,
)
from fa_purity.utils import (
    cast_exception,
    raise_exception,
)
from logging import (
    Logger,
)
from psycopg2 import (
    DatabaseError,
    DataError,
    extras,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
)
from typing import (
    Any,
    Callable,
    Iterable,
    Optional,
    TYPE_CHECKING,
    TypeVar,
)

if TYPE_CHECKING:
    from psycopg2 import (
        cursor as CursorStub,
    )
else:
    CursorStub = Any


_T = TypeVar("_T")
_F = TypeVar("_F")


def _handle_psycopg_errors(raw: Callable[[], _T]) -> ResultE[_T]:
    try:
        return Result.success(raw())
    except (
        DatabaseError,  # type:ignore[misc]
        OperationalError,  # type:ignore[misc]
        NotSupportedError,  # type:ignore[misc]
        DataError,  # type:ignore[misc]
        ProgrammingError,  # type:ignore[misc]
        InternalError,  # type:ignore[misc]
    ) as err:
        return Result.failure(cast_exception(err))


def _util_empty_or_error(
    stream: Stream[ResultE[Maybe[_T]]],
) -> Stream[ResultE[_T]]:
    """
    Stops stream when value is on of these:
    - successful and empty value
    - failure
    Failure result is the final emitted item, but an empty value is omitted
    """

    def _until(
        items: Iterable[Result[Maybe[_T], _F]]
    ) -> Iterable[Result[_T, _F]]:
        _factory: ResultFactory[_T, _F] = ResultFactory()
        for item in items:
            successful = item.map(lambda _: True).value_or(False)
            if successful:
                inner_item = item.or_else_call(
                    lambda: raise_exception(Exception("Impossible!"))  # type: ignore[misc]
                )
                if inner_item.map(lambda _: False).value_or(True):
                    break
                result = inner_item.or_else_call(
                    lambda: raise_exception(Exception("Impossible!"))  # type: ignore[misc]
                )
                yield _factory.success(result)
            else:
                inner_fail = item.swap().or_else_call(
                    lambda: raise_exception(Exception("Impossible!"))  # type: ignore[misc]
                )
                yield _factory.failure(inner_fail)
                break

    return unsafe_from_cmd(stream.unsafe_to_iter().map(lambda i: _until(i)))


@dataclass(frozen=True)
class _SqlClient_1:
    _log: Logger
    _cursor: CursorStub

    def execute(
        self, query: Query, args: Optional[QueryValues]
    ) -> Cmd[ResultE[None]]:
        _values: FrozenDict[str, PrimitiveVal] = (
            args.values if args else FrozenDict({})
        )
        preview: str = self._cursor.mogrify(  # type: ignore[no-untyped-call]
            query.statement, _values
        )

        def _action() -> ResultE[None]:
            self._log.debug("Executing: %s", preview)
            return _handle_psycopg_errors(
                lambda: self._cursor.execute(query.statement, _values)
            )

        return Cmd.from_cmd(_action)

    def batch(
        self, query: Query, args: FrozenList[QueryValues]
    ) -> Cmd[ResultE[None]]:
        def _action() -> ResultE[None]:
            _args = tuple(v.values for v in args)
            self._log.debug(
                "Batch execution (%s items): %s",
                len(_args),
                query.statement,
            )
            return _handle_psycopg_errors(
                lambda: extras.execute_batch(
                    self._cursor, query.statement, _args
                )
            )

        return Cmd.from_cmd(_action)

    def values(
        self, query: Query, args: PureIter[RowData], limit: Limit
    ) -> Cmd[ResultE[None]]:
        def _action() -> ResultE[None]:
            self._log.debug("Executing query over values: %s", query.statement)
            _args = args.map(lambda r: r.data)
            return _handle_psycopg_errors(
                lambda: extras.execute_values(  # type: ignore[misc]
                    self._cursor,
                    query.statement,
                    _args,
                    page_size=limit.limit,
                )
            )

        return Cmd.from_cmd(_action)

    def fetch_one(self) -> Cmd[ResultE[Maybe[RowData]]]:
        def _action() -> ResultE[Maybe[RowData]]:
            self._log.debug("Fetching one row")
            return (
                _handle_psycopg_errors(
                    lambda: _assert.assert_fetch_one(self._cursor.fetchone())  # type: ignore[misc]
                )
                .bind(lambda r: r)
                .map(lambda m: m.map(RowData))
            )

        return Cmd.from_cmd(_action)

    def fetch_all(self) -> Cmd[ResultE[FrozenList[RowData]]]:
        def _action() -> ResultE[FrozenList[RowData]]:
            self._log.debug("Fetching all rows")
            items = _assert.assert_fetch_list(tuple(self._cursor.fetchall()))  # type: ignore[misc]
            return items.map(lambda i: tuple(map(RowData, i)))

        return Cmd.from_cmd(_action)

    def fetch_chunk(self, chunk: int) -> Cmd[ResultE[FrozenList[RowData]]]:
        def _action() -> ResultE[FrozenList[RowData]]:
            self._log.debug("Fetching %s rows", chunk)
            items = _assert.assert_fetch_list(
                tuple(self._cursor.fetchmany(chunk))  # type: ignore[misc]
            )
            return items.map(lambda i: tuple(map(RowData, i)))

        return Cmd.from_cmd(_action)

    def fetch_chunks_stream(
        self, chunk: int
    ) -> Stream[ResultE[FrozenList[RowData]]]:
        return (
            PureIterFactory.infinite_range(0, 1)
            .map(
                lambda _: self.fetch_chunk(chunk).map(
                    lambda r: r.map(
                        lambda i: Maybe.from_optional(i if i else None)
                    )
                )
            )
            .transform(lambda i: StreamFactory.from_commands(i))
            .transform(lambda s: _util_empty_or_error(s))
        )


def new_sql_client(_log: Logger, _cursor: CursorStub) -> SqlClient:
    _client = _SqlClient_1(_log, _cursor)
    return SqlClient(
        _client.execute,
        _client.batch,
        _client.values,
        _client.fetch_one(),
        _client.fetch_all(),
        _client.fetch_chunk,
        _client.fetch_chunks_stream,
    )
