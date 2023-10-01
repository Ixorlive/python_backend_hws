from dataclasses import dataclass
from typing import List

from .stop import Stop


@dataclass
class BusInfo:
    total_stops: int = 0
    unique_stops: int = 0
    curvature: float = 0
    length: float = 0


@dataclass
class Bus:
    name: str
    route: List[Stop]
    is_roundtrip: bool
    busInfo: BusInfo
