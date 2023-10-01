from typing import Generic, List, TypeVar

T = TypeVar("T")


class Edge(Generic[T]):
    def __init__(self, from_vertex: int, to_vertex: int, weight: T):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight


class DirectedWeightedGraph(Generic[T]):
    def __init__(self, vertex_count: int = 0):
        self.edges: List[Edge[T]] = []
        self.incidence_lists: List[List[int]] = [[] for _ in range(vertex_count)]

    def add_edge(self, edge: Edge[T]) -> int:
        edge_id = len(self.edges)
        self.edges.append(edge)
        self.incidence_lists[edge.from_vertex].append(edge_id)
        return edge_id

    def get_vertex_count(self) -> int:
        return len(self.incidence_lists)

    def get_edge_count(self) -> int:
        return len(self.edges)

    def get_edge(self, edge_id: int) -> Edge[T]:
        return self.edges[edge_id]

    def get_incident_edges(self, vertex: int) -> List[int]:
        return self.incidence_lists[vertex]

    def get_edges(self) -> List[Edge[T]]:
        return self.edges

    def get_incidence_list(self) -> List[List[int]]:
        return self.incidence_lists
