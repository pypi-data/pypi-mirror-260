from enum import Enum
from typing import Optional, TypedDict


class ScrollDirection(Enum):
    UP = 1
    DOWN = 2


class ProxySettings(TypedDict, total=False):
    server: str
    bypass: Optional[str]
    username: Optional[str]
    password: Optional[str]


class StealthModeConfig(TypedDict):
    vendor: Optional[str]
    renderer: Optional[str]
    nav_user_agent: Optional[str]
