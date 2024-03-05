from collections.abc import Mapping, Sequence
from typing import TypedDict

from typing_extensions import NotRequired


class ApiVersion(TypedDict):
    id: str
    restPath: str
    wsPath: NotRequired[str]


class ServerApi(TypedDict):
    versions: Sequence[ApiVersion]


class ServerVersions(TypedDict):
    version: int
    serverVersion: str
    apis: Mapping[str, ServerApi]
