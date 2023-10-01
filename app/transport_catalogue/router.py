from typing import Any, List, Optional

from .graph.graph import DirectedWeightedGraph


class Router:
    class RouteInternalData:
        def __init__(self, weight: Any, prev_edge: Optional[int]):
            self.weight = weight
            self.prev_edge = prev_edge

    class RouteInfo:
        def __init__(self, weight: Any, edges: List[int]):
            self.weight = weight
            self.edges = edges

    def __init__(self, graph: "DirectedWeightedGraph"):
        self.graph = graph
        vertex_count = graph.get_vertex_count()
        self.routes_internal_data: List[List[Optional[Router.RouteInternalData]]] = [
            [None for _ in range(vertex_count)] for _ in range(vertex_count)
        ]
        self.initialize_routes_internal_data(graph)

        for vertex_through in range(vertex_count):
            self.relax_routes_internal_data_through_vertex(vertex_count, vertex_through)

    def initialize_routes_internal_data(self, graph: "DirectedWeightedGraph"):
        vertex_count = graph.get_vertex_count()
        zero_weight = type(self.graph.get_edges()[0].weight)()

        for vertex in range(vertex_count):
            self.routes_internal_data[vertex][vertex] = self.RouteInternalData(
                zero_weight, None
            )
            for edge_id in graph.get_incident_edges(vertex):
                edge = graph.get_edge(edge_id)
                if edge.weight < zero_weight:
                    raise ValueError("Edges' weights should be non-negative")

                route_internal_data = self.routes_internal_data[vertex][edge.to_vertex]
                if (
                    route_internal_data is None
                    or route_internal_data.weight > edge.weight
                ):
                    self.routes_internal_data[vertex][
                        edge.to_vertex
                    ] = self.RouteInternalData(edge.weight, edge_id)

    def relax_route(
        self,
        vertex_from: int,
        vertex_to: int,
        route_from: "Router.RouteInternalData",
        route_to: "Router.RouteInternalData",
    ):
        route_relaxing = self.routes_internal_data[vertex_from][vertex_to]
        candidate_weight = route_from.weight + route_to.weight
        if route_relaxing is None or candidate_weight < route_relaxing.weight:
            self.routes_internal_data[vertex_from][vertex_to] = self.RouteInternalData(
                candidate_weight,
                route_to.prev_edge
                if route_to.prev_edge is not None
                else route_from.prev_edge,
            )

    def relax_routes_internal_data_through_vertex(
        self, vertex_count: int, vertex_through: int
    ):
        for vertex_from in range(vertex_count):
            route_from = self.routes_internal_data[vertex_from][vertex_through]
            if route_from is not None:
                for vertex_to in range(vertex_count):
                    route_to = self.routes_internal_data[vertex_through][vertex_to]
                    if route_to is not None:
                        self.relax_route(vertex_from, vertex_to, route_from, route_to)

    def build_route(
        self, from_vertex: int, to_vertex: int
    ) -> Optional["Router.RouteInfo"]:
        route_internal_data = self.routes_internal_data[from_vertex][to_vertex]
        if route_internal_data is None:
            return None

        weight = route_internal_data.weight
        edges = []
        edge_id = route_internal_data.prev_edge
        while edge_id is not None:
            edges.append(edge_id)
            to_vertex = self.graph.get_edge(
                edge_id
            ).from_vertex  # Assuming get_edge returns an object with a 'from' attribute
            edge_id = self.routes_internal_data[from_vertex][to_vertex].prev_edge

        edges.reverse()
        return self.RouteInfo(weight, edges)
