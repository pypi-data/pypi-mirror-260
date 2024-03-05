from . import (
    _client_1,
    _temp_creds,
)
from ._core.client import (
    SqlClient,
)
from ._core.connection import (
    DbConnection,
)
from ._core.creds import (
    Credentials,
)
from ._temp_creds import (
    TempCredsUser,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    ResultE,
)
from fa_purity.cmd import (
    Cmd,
)
from logging import (
    Logger,
)


@dataclass(frozen=True)
class SqlClientFactory:
    @staticmethod
    def new_client(connection: DbConnection, log: Logger) -> Cmd[SqlClient]:
        return connection.act_on_cursor(
            lambda c: _client_1.new_sql_client(log, c)
        )


@dataclass(frozen=True)
class LoginUtils:
    @staticmethod
    def get_temp_creds(user: TempCredsUser) -> Cmd[ResultE[Credentials]]:
        return _temp_creds.get_temp_creds(user)
