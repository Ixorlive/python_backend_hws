import pytest

from app.transport_catalogue.graph.graph import DirectedWeightedGraph, Edge


@pytest.fixture
def sample_edge():
    return Edge(0, 1, 2)


@pytest.fixture
def sample_graph():
    return DirectedWeightedGraph[int](5)


def test_add_edge(sample_graph, sample_edge):
    assert sample_graph.add_edge(sample_edge) == 0


def test_get_vertex_count(sample_graph):
    assert sample_graph.get_vertex_count() == 5


def test_get_edge_count(sample_graph, sample_edge):
    sample_graph.add_edge(sample_edge)
    assert sample_graph.get_edge_count() == 1


def test_get_edge(sample_graph, sample_edge):
    sample_graph.add_edge(sample_edge)
    assert sample_graph.get_edge(0) == sample_edge


def test_get_incident_edges(sample_graph, sample_edge):
    sample_graph.add_edge(sample_edge)
    assert sample_graph.get_incident_edges(0) == [0]


def test_get_edges(sample_graph, sample_edge):
    sample_graph.add_edge(sample_edge)
    assert sample_graph.get_edges() == [sample_edge]


def test_get_incidence_list(sample_graph, sample_edge):
    sample_graph.add_edge(sample_edge)
    assert sample_graph.get_incidence_list() == [[0], [], [], [], []]
