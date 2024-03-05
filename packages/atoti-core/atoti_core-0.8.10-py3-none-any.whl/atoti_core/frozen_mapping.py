from collections.abc import Mapping
from typing import Annotated

from pydantic import AfterValidator

from .frozendict import _FrozenDict, _Key, _Value

FrozenMapping = Annotated[
    Mapping[_Key, _Value],
    # Normalizing to a `_FrozenDict` to ensure runtime immutability of `FrozenMapping` fields on frozen dataclasses.
    # This allows such dataclasses to be hashed and used as keys in a mapping.
    # Using `_FrozenDict` instead of `frozendict` to get back an instance inheriting from `dict` since Pydantic would not know how to serialize the result of `frozendict`.
    AfterValidator(_FrozenDict),
]
