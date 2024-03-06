from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class DatabaseId:
    db_name: str
    host: str
    port: int


@dataclass(frozen=True)
class Credentials:
    user: str
    password: str

    def __repr__(self) -> str:
        return f"Creds(user={self.user})"
