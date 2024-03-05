from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.json.primitive.core import (
    is_primitive,
    Primitive,
)
from fa_purity.result import (
    ResultE,
    ResultFactory,
    UnwrapError,
)
from typing import (
    Callable,
    cast,
    TypeVar,
)

PrimitiveVal = Primitive | datetime
_A = TypeVar("_A")
_T = TypeVar("_T")
_R = TypeVar("_R")


@dataclass(frozen=True)
class PrimitiveFactory:
    @staticmethod
    def to_prim_val(raw: _T) -> ResultE[PrimitiveVal]:
        factory: ResultFactory[PrimitiveVal, Exception] = ResultFactory()
        if is_primitive(raw) or isinstance(raw, datetime):
            return factory.success(raw)
        return factory.failure(
            TypeError(f"Got {type(raw)}; expected a PrimitiveVal"),
        ).alt(Exception)

    @staticmethod
    def to_list_of(
        items: _A, assertion: Callable[[_T], ResultE[_R]]
    ) -> ResultE[FrozenList[_R]]:
        factory: ResultFactory[FrozenList[_R], Exception] = ResultFactory()
        try:
            if isinstance(items, tuple):
                return factory.success(
                    tuple(assertion(i).unwrap() for i in items)
                )
            return factory.failure(TypeError("Expected tuple")).alt(Exception)
        except UnwrapError as err:
            error: UnwrapError[_R, Exception] = cast(
                UnwrapError[_R, Exception], err
            )
            return factory.failure(error.container.unwrap_fail()).alt(
                Exception
            )
