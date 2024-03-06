from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.json_2.primitive import (
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.result import (
    ResultE,
)
from redshift_client import (
    _utils,
)
from redshift_client.core.column import (
    Column,
    ColumnId,
)
from redshift_client.core.data_type.decode import (
    decode_type,
)
from redshift_client.core.id_objs import (
    Identifier,
)
from redshift_client.sql_client import (
    PrimitiveVal,
)
from typing import (
    Tuple,
)


def to_column(
    raw: FrozenList[PrimitiveVal],
) -> ResultE[Tuple[ColumnId, Column]]:
    _type = _utils.get_index(raw, 2).bind(
        lambda p: JsonPrimitiveFactory.from_any(p).bind(
            JsonPrimitiveUnfolder.to_str
        )
    )
    _precision = (
        _utils.get_index(raw, 3)
        .bind(
            lambda p: JsonPrimitiveFactory.from_any(p).bind(
                JsonPrimitiveUnfolder.to_opt_int
            )
        )
        .map(lambda v: Maybe.from_optional(v))
    )
    _scale = (
        _utils.get_index(raw, 4)
        .bind(
            lambda p: JsonPrimitiveFactory.from_any(p).bind(
                JsonPrimitiveUnfolder.to_opt_int
            )
        )
        .map(lambda v: Maybe.from_optional(v))
    )
    _nullable = (
        _utils.get_index(raw, 5)
        .bind(
            lambda p: JsonPrimitiveFactory.from_any(p).bind(
                JsonPrimitiveUnfolder.to_str
            )
        )
        .map(lambda v: v.upper() == "YES")
    )
    _default = _utils.get_index(raw, 6)
    _data_type = _type.bind(
        lambda t: _precision.bind(
            lambda p: _scale.map(lambda s: decode_type(t, p, s))
        )
    )
    _column = _data_type.bind(
        lambda dt: _nullable.bind(
            lambda n: _default.map(lambda d: Column(dt, n, d))
        )
    )
    _name = _utils.get_index(raw, 1).bind(
        lambda p: JsonPrimitiveFactory.from_any(p).bind(
            JsonPrimitiveUnfolder.to_str
        )
    )
    return _name.bind(
        lambda n: _column.map(lambda c: (ColumnId(Identifier.new(n)), c))
    )
