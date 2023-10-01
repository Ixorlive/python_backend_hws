from typing import Optional
from unittest.mock import Mock

import pytest

from app.transport_catalogue.router import Router


@pytest.fixture
def mock_graph():
    graph = Mock()
    graph.get_vertex_count.return_value = 3

    edge0 = Mock(from_vertex=0, to_vertex=1, weight=1)
    edge1 = Mock(from_vertex=1, to_vertex=2, weight=2)

    graph.get_edges.return_value = [edge0, edge1]
    graph.get_incident_edges.side_effect = (
        lambda vertex: [0] if vertex == 0 else [1] if vertex == 1 else []
    )
    graph.get_edge.side_effect = lambda edge_id: edge0 if edge_id == 0 else edge1

    return graph


@pytest.mark.parametrize(
    "from_vertex, to_vertex, expected_route_info",
    [
        (0, 2, Router.RouteInfo(3, [0, 1])),
        (0, 1, Router.RouteInfo(1, [0])),
        (1, 0, None),
    ],
)
def test_build_route(mock_graph, from_vertex, to_vertex, expected_route_info):
    router = Router(mock_graph)

    route_info: Optional[Router.RouteInfo] = router.build_route(from_vertex, to_vertex)

    if expected_route_info is None:
        assert route_info is None
    else:
        assert route_info.weight == expected_route_info.weight
        assert route_info.edges == expected_route_info.edges
