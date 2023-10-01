from dataclasses import dataclass
from typing import Optional

from app.transport_catalogue.geo.coordinates import Coordinates


@dataclass
class Stop:
    name: str
    coordinates: Coordinates

    def __eq__(self, other):
        if isinstance(other, Stop):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash((self.name, self.coordinates.lat, self.coordinates.lng))


class PairStops:
    def __init__(self, stop_from: Optional[Stop], stop_to: Optional[Stop]) -> None:
        self.stop_from = stop_from
        self.stop_to = stop_to

    def swap_stops(self):
        self.stop_from, self.stop_to = self.stop_to, self.stop_from

    def __eq__(self, other) -> bool:
        if isinstance(other, PairStops):
            return self.stop_from == other.stop_from and self.stop_to == other.stop_to
        return False

    def __hash__(self):
        return hash((self.stop_from, self.stop_to))
