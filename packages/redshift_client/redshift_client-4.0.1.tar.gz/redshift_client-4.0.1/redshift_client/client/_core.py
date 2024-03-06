from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    PureIter,
    ResultE,
)
from fa_purity.frozen import (
    FrozenDict,
)
from redshift_client.core.column import (
    Column,
    ColumnObj,
)
from redshift_client.core.id_objs import (
    ColumnId,
    DbTableId,
    SchemaId,
    TableId,
)
from redshift_client.core.schema import (
    SchemaPolicy,
)
from redshift_client.core.table import (
    ManifestId,
    Table,
    TableAttrs,
)
from redshift_client.sql_client import (
    Limit,
    RowData,
)
from typing import (
    Callable,
    FrozenSet,
)


@dataclass(frozen=True)
class SchemaClient:
    all_schemas: Cmd[ResultE[FrozenSet[SchemaId]]]
    table_ids: Callable[[SchemaId], Cmd[ResultE[FrozenSet[DbTableId]]]]
    exist: Callable[[SchemaId], Cmd[ResultE[bool]]]
    delete: Callable[[SchemaId], Cmd[ResultE[None]]]
    delete_cascade: Callable[[SchemaId], Cmd[ResultE[None]]]
    _rename: Callable[[SchemaId, SchemaId], Cmd[ResultE[None]]]
    create: Callable[[SchemaId], Cmd[ResultE[None]]]
    create_if_not_exist: Callable[[SchemaId], Cmd[ResultE[None]]]
    recreate: Callable[[SchemaId], Cmd[ResultE[None]]]
    recreate_cascade: Callable[[SchemaId], Cmd[ResultE[None]]]
    _migrate: Callable[[SchemaId, SchemaId], Cmd[ResultE[None]]]
    _move: Callable[[SchemaId, SchemaId], Cmd[ResultE[None]]]
    set_policy: Callable[[SchemaId, SchemaPolicy], Cmd[ResultE[None]]]

    def rename(self, old: SchemaId, new: SchemaId) -> Cmd[ResultE[None]]:
        return self._rename(old, new)

    def migrate(
        self, source: SchemaId, target: SchemaId
    ) -> Cmd[ResultE[None]]:
        """
        Moves all tables from `source` to `target` overwriting `target` data.
        Deletes empty source after success.
        """
        return self._migrate(source, target)

    def move(self, source: SchemaId, target: SchemaId) -> Cmd[ResultE[None]]:
        """
        Moves all tables from `source` to `target`.
        It does not overwrite target data.
        Deletes empty source after success.
        """
        return self._move(source, target)


@dataclass(frozen=True)
class AwsRole:
    role: str


@dataclass(frozen=True)
class S3Prefix:
    prefix: str


@dataclass(frozen=True)
class NanHandler:
    enabled: bool


@dataclass(frozen=True)
class TableClient:
    "Table client interface"
    unload: Callable[[DbTableId, S3Prefix, AwsRole], Cmd[ResultE[ManifestId]]]
    load: Callable[
        [DbTableId, ManifestId, AwsRole, NanHandler], Cmd[ResultE[None]]
    ]
    get: Callable[[DbTableId], Cmd[ResultE[Table]]]
    exist: Callable[[DbTableId], Cmd[ResultE[bool]]]
    insert: Callable[
        [DbTableId, Table, PureIter[RowData], Limit], Cmd[ResultE[None]]
    ]
    rename: Callable[[DbTableId, str], Cmd[ResultE[TableId]]]
    delete: Callable[[DbTableId], Cmd[ResultE[None]]]
    delete_cascade: Callable[[DbTableId], Cmd[ResultE[None]]]
    add_column: Callable[[DbTableId, ColumnObj], Cmd[ResultE[None]]]
    add_columns: Callable[
        [DbTableId, FrozenDict[ColumnId, Column]], Cmd[ResultE[None]]
    ]
    new: Callable[[DbTableId, Table, TableAttrs], Cmd[ResultE[None]]]
    new_if_not_exist: Callable[
        [DbTableId, Table, TableAttrs], Cmd[ResultE[None]]
    ]
    _create_like: Callable[[DbTableId, DbTableId], Cmd[ResultE[None]]]
    _move_data: Callable[[DbTableId, DbTableId], Cmd[ResultE[None]]]
    _move: Callable[[DbTableId, DbTableId], Cmd[ResultE[None]]]
    _migrate: Callable[[DbTableId, DbTableId], Cmd[ResultE[None]]]

    def create_like(
        self, blueprint: DbTableId, new_table: DbTableId
    ) -> Cmd[ResultE[None]]:
        return self._create_like(blueprint, new_table)

    def move_data(
        self, source: DbTableId, target: DbTableId
    ) -> Cmd[ResultE[None]]:
        """
        This method moves data from source to target.
        - After the operation source will be empty.
        - Both tables must exists.
        """
        return self._create_like(source, target)

    def move(self, source: DbTableId, target: DbTableId) -> Cmd[ResultE[None]]:
        """
        - create target if not exist
        - move_data (append) data from source into target
        - delete source table (that will be empty)
        """
        return self._move(source, target)

    def migrate(
        self, source: DbTableId, target: DbTableId
    ) -> Cmd[ResultE[None]]:
        """
        - delete target if exist
        - move source into target (see move method)
        """
        return self._migrate(source, target)
