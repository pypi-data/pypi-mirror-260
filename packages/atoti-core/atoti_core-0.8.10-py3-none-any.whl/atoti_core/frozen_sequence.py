from collections.abc import Sequence
from typing import Annotated, TypeVar

from pydantic import AfterValidator

_ElementT = TypeVar("_ElementT")

FrozenSequence = Annotated[
    Sequence[_ElementT],
    # Normalizing to a `tuple` to ensure runtime immutability of `FrozenSequence` fields on frozen dataclasses.
    # This allows such dataclasses to be hashed and used as keys in a mapping.
    AfterValidator(tuple),
]
