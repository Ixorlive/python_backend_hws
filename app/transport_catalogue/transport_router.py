from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.transport_catalogue.domain.route_settings import RouteSettings
from app.transport_catalogue.graph.graph import DirectedWeightedGraph, Edge
from app.transport_catalogue.router import Router
from app.transport_catalogue.transport_catalogue import TransportCatalogue


class BusWeight:
    def __init__(self, name: str = "", count_stops: int = 0, time: float = 0.0):
        self.name = name
        self.count_stops = count_stops
        self.time = time

    def __add__(self, other: "BusWeight") -> "BusWeight":
        return BusWeight(self.name, self.count_stops, self.time + other.time)

    def __lt__(self, other: "BusWeight") -> bool:
        return self.time < other.time

    def __gt__(self, other: "BusWeight") -> bool:
        return self.time > other.time


@dataclass
class EdgeInfo:
    start_stop: str
    wair_stop: str


class TransportRouter:
    def __init__(self, db: TransportCatalogue):
        self.graph = DirectedWeightedGraph()
        self.router: Optional[Router] = None
        self.stop_start_to_index = {}
        self.stop_waiting_to_index = {}
        self.route_settings = RouteSettings()
        self.last_index = 0

        if db:
            self.initialize_router(db)

    def add_edge(
        self,
        edge_info: EdgeInfo,
        weight: BusWeight,
        start_from_wait_stop: bool = False,
    ):
        if start_from_wait_stop:
            index_from = self.get_index_from_stop_map(
                self.stop_waiting_to_index, edge_info.wair_stop
            )
            index_to = self.get_index_from_stop_map(
                self.stop_start_to_index, edge_info.start_stop
            )
        else:
            index_from = self.get_index_from_stop_map(
                self.stop_start_to_index, edge_info.start_stop
            )
            index_to = self.get_index_from_stop_map(
                self.stop_waiting_to_index, edge_info.wair_stop
            )

        edge = Edge(index_from, index_to, weight)
        self.graph.add_edge(edge)

    def get_route_info(self, from_stop: str, to_stop: str) -> Optional[Any]:
        if (
            from_stop not in self.stop_waiting_to_index
            or to_stop not in self.stop_waiting_to_index
        ):
            return None
        assert self.router is not None
        return self.router.build_route(
            self.stop_waiting_to_index[from_stop], self.stop_waiting_to_index[to_stop]
        )

    def get_edge(self, id: int) -> Edge:
        return self.graph.get_edge(id)

    def initialize_router(self, db: TransportCatalogue):
        buses = db.get_sorted_buses()
        self.route_settings = db.route_settings
        self.graph = DirectedWeightedGraph[BusWeight](db.get_count_stops() * 2)

        bus_speed = (self.route_settings.bus_velocity * 1000) / 60.0
        for bus in buses:
            stops = bus.route
            count_stops = len(stops) - 1 if bus.is_roundtrip else len(stops)
            for i in range(count_stops):
                weight = BusWeight(stops[i].name, 0, self.route_settings.bus_wait_time)
                self.add_edge(EdgeInfo(stops[i].name, stops[i].name), weight, True)

                distance = 0.0

                for j in range(i + 1, len(stops)):
                    distance += db.get_dist_stops(stops[j - 1].name, stops[j].name)
                    weight = BusWeight(bus.name, j - i, distance / bus_speed)
                    self.add_edge(EdgeInfo(stops[i].name, stops[j].name), weight)

                if not bus.is_roundtrip:
                    distance = 0.0
                    for j in range(i - 1, -1, -1):
                        distance += db.get_dist_stops(stops[j + 1].name, stops[j].name)
                        weight = BusWeight(bus.name, i - j, distance / bus_speed)
                        self.add_edge(EdgeInfo(stops[i].name, stops[j].name), weight)

        self.router = Router(self.graph)

    def get_index_from_stop_map(self, stop_map: Dict[str, int], stop_name: str) -> int:
        if stop_name not in stop_map:
            stop_map[stop_name] = self.last_index
            self.last_index += 1
        return stop_map[stop_name]
