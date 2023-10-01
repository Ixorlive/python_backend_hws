from dataclasses import dataclass
from typing import List, Optional

from .router import Router
from .transport_router import TransportRouter


class RequestHandler:
    @dataclass
    class RouteItem:
        is_wait: bool
        time: float
        bus_or_stop_name: str
        span_count: int

    @dataclass
    class RouteInfo:
        total_time: float
        items: List["RequestHandler.RouteItem"]

    def __init__(self, transport_router: TransportRouter):
        self.transport_router: TransportRouter = transport_router

    def get_route_info(
        self, stop_from: str, stop_to: str
    ) -> Optional["RequestHandler.RouteInfo"]:
        route_info: Optional[Router.RouteInfo] = self.transport_router.get_route_info(
            stop_from, stop_to
        )
        if route_info is None:
            return None
        result: List["RequestHandler.RouteItem"] = []

        for edge_id in route_info.edges:
            edge = self.transport_router.get_edge(edge_id)

            if edge.weight.count_stops == 0:
                result.append(
                    RequestHandler.RouteItem(
                        True, edge.weight.time, edge.weight.name, 0
                    )
                )
            else:
                result.append(
                    RequestHandler.RouteItem(
                        False,
                        edge.weight.time,
                        edge.weight.name,
                        edge.weight.count_stops,
                    )
                )

        return RequestHandler.RouteInfo(route_info.weight.time, result)
