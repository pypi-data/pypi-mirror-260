from . import (
    _schema,
    _table,
)
from ._core import (
    SchemaClient,
    TableClient,
)
from dataclasses import (
    dataclass,
)
from redshift_client.sql_client import (
    SqlClient,
)


@dataclass(frozen=True)
class ClientFactory:
    @staticmethod
    def new_table_client(sql: SqlClient) -> TableClient:
        return _table.new_table_client(sql)

    @staticmethod
    def new_schema_client(sql: SqlClient) -> SchemaClient:
        return _schema.new_schema_client(sql)
