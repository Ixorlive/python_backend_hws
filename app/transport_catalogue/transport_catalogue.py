from typing import Dict, List, Optional, Set

from app.transport_catalogue.domain.route_settings import RouteSettings
from app.transport_catalogue.geo.coordinates import Coordinates, compute_distance

from .domain.bus import Bus, BusInfo
from .domain.stop import PairStops, Stop


class TransportCatalogue:
    def __init__(self):
        self.stops: List[Stop] = []
        self.buses: List[Bus] = []

        self.stop_indexes: Dict[str, Stop] = {}
        self.bus_indexes: Dict[str, Bus] = {}

        self.buses_in_stop_index: Dict[Stop, Set[str]] = {}

        self.route_settings: RouteSettings = RouteSettings()
        self.dist_stops_index: Dict[PairStops, float] = {}

    def add_stop(self, stop_name: str, lat: float, lon: float):
        self.stops.append(Stop(stop_name, Coordinates(lat, lon)))
        self.stop_indexes[stop_name] = self.stops[-1]

    def add_bus(self, route_name: str, route: List[str], is_roundtrip: bool):
        count_stops = len(route)
        bus_route: List[Stop] = []

        uniq_stops = set()
        length: float = 0.0
        distance_directly: float = 0.0

        pair_stops = PairStops(self.find_stop_by_name(route[0]), None)
        for stop_index in range(1, count_stops):
            pair_stops.stop_to = self.find_stop_by_name(route[stop_index])
            assert pair_stops.stop_from is not None and pair_stops.stop_to is not None
            length += self.get_dist_stops(
                pair_stops.stop_from.name, pair_stops.stop_to.name
            )
            distance_directly += compute_distance(
                pair_stops.stop_from.coordinates, pair_stops.stop_to.coordinates
            )
            if not is_roundtrip:
                length += self.get_dist_stops(
                    pair_stops.stop_to.name, pair_stops.stop_from.name
                )
                distance_directly += compute_distance(
                    pair_stops.stop_to.coordinates, pair_stops.stop_from.coordinates
                )
            bus_route.append(pair_stops.stop_from)
            if pair_stops.stop_from not in self.buses_in_stop_index:
                self.buses_in_stop_index[pair_stops.stop_from] = set()
            self.buses_in_stop_index[pair_stops.stop_from].add(route_name)

            uniq_stops.add(pair_stops.stop_from)
            pair_stops.swap_stops()

        assert pair_stops.stop_from
        uniq_stops.add(pair_stops.stop_from)
        bus_route.append(pair_stops.stop_from)
        if pair_stops.stop_from not in self.buses_in_stop_index:
            self.buses_in_stop_index[pair_stops.stop_from] = set()
        self.buses_in_stop_index[pair_stops.stop_from].add(route_name)

        self.buses.append(Bus(route_name, bus_route, is_roundtrip, BusInfo()))
        self.bus_indexes[route_name] = self.buses[-1]
        # set busInfo
        self.buses[-1].busInfo.length = length
        self.buses[-1].busInfo.curvature = length / distance_directly
        self.buses[-1].busInfo.unique_stops = len(uniq_stops)
        self.buses[-1].busInfo.total_stops = (
            len(bus_route) if is_roundtrip else len(bus_route) * 2 - 1
        )

    def find_stop_by_name(self, stop_name: str) -> Optional[Stop]:
        return self.stop_indexes[stop_name] if stop_name in self.stop_indexes else None

    def find_bus_by_name(self, bus_name: str) -> Optional[Bus]:
        return self.bus_indexes[bus_name] if bus_name in self.bus_indexes else None

    def get_sorted_stops(self) -> List[Stop]:
        return sorted(self.stops, key=lambda stop: stop.name)

    def get_sorted_buses(self):
        return sorted(self.buses, key=lambda bus: bus.name)

    def get_bus_info(self, bus_name: str) -> Optional[BusInfo]:
        if bus_name not in self.bus_indexes:
            return None
        return self.bus_indexes[bus_name].busInfo

    def get_list_buses_by_stop(self, stop_name: str) -> Optional[Set[str]]:
        stop = self.find_stop_by_name(stop_name)
        if stop is None or stop not in self.buses_in_stop_index:
            return None
        return self.buses_in_stop_index[stop]

    def get_count_stops(self) -> int:
        return len(self.stops)

    def set_route_settings(self, bus_wait_time: int, bus_velocity) -> None:
        self.route_settings = RouteSettings(bus_wait_time, bus_velocity)

    def set_dist_stops(self, stop_from: str, stop_to: str, dist: float) -> None:
        pair_stops = PairStops(
            self.find_stop_by_name(stop_from), self.find_stop_by_name(stop_to)
        )
        self.dist_stops_index[pair_stops] = dist

    def get_dist_stops(self, stop_from: str, stop_to: str) -> float:
        pair_stops = PairStops(
            self.find_stop_by_name(stop_from), self.find_stop_by_name(stop_to)
        )
        if pair_stops.stop_from is not None and pair_stops.stop_to is not None:
            if pair_stops in self.dist_stops_index:
                return self.dist_stops_index[pair_stops]
            pair_stops.swap_stops()
            if pair_stops in self.dist_stops_index:
                return self.dist_stops_index[pair_stops]

            return compute_distance(
                pair_stops.stop_from.coordinates, pair_stops.stop_to.coordinates
            )
        return 0.0
