import pytest

from app.transport_catalogue.geo.coordinates import Coordinates, compute_distance
from app.transport_catalogue.transport_catalogue import TransportCatalogue


@pytest.fixture
def transport_catalogue():
    tc = TransportCatalogue()
    tc.add_stop("stop1", 50.4501, 30.5234)
    tc.add_stop("stop2", 50.4502, 30.5235)
    tc.add_bus("bus1", ["stop1", "stop2"], True)
    tc.add_bus("bus2", ["stop1", "stop2"], False)
    return tc


@pytest.mark.parametrize(
    "stop_name, expected_lat, expected_lon",
    [
        ("stop1", 50.4501, 30.5234),
        ("stop2", 50.4502, 30.5235),
    ],
)
def test_find_stop_by_name(transport_catalogue, stop_name, expected_lat, expected_lon):
    stop = transport_catalogue.find_stop_by_name(stop_name)
    assert stop is not None
    assert stop.name == stop_name
    assert stop.coordinates == Coordinates(expected_lat, expected_lon)


@pytest.mark.parametrize(
    "bus_name, expected_is_roundtrip",
    [
        ("bus1", True),
        ("bus2", False),
    ],
)
def test_find_bus_by_name(transport_catalogue, bus_name, expected_is_roundtrip):
    bus = transport_catalogue.find_bus_by_name(bus_name)
    assert bus is not None
    assert bus.name == bus_name
    assert bus.is_roundtrip == expected_is_roundtrip


def test_get_sorted_stops(transport_catalogue):
    sorted_stops = transport_catalogue.get_sorted_stops()
    assert len(sorted_stops) == 2
    assert sorted_stops[0].name == "stop1"
    assert sorted_stops[1].name == "stop2"


def test_get_sorted_buses(transport_catalogue):
    sorted_buses = transport_catalogue.get_sorted_buses()
    assert len(sorted_buses) == 2
    assert sorted_buses[0].name == "bus1"
    assert sorted_buses[1].name == "bus2"


def test_dist_stops(transport_catalogue):
    transport_catalogue.add_stop("stop3", 0, 0)
    transport_catalogue.set_dist_stops("stop1", "stop2", 1)
    assert transport_catalogue.get_dist_stops("stop1", "stop2") == 1
    assert transport_catalogue.get_dist_stops("stop1", "stop3") == compute_distance(
        Coordinates(50.4501, 30.5234), Coordinates(0, 0)
    )


def test_bus_info(transport_catalogue):
    transport_catalogue.set_dist_stops("stop1", "stop2", 5)
    transport_catalogue.add_bus("bus3", ["stop1", "stop2"], False)
    transport_catalogue.add_bus("bus4", ["stop1", "stop2"], True)
    bus_info1 = transport_catalogue.get_bus_info("bus3")
    bus_info2 = transport_catalogue.get_bus_info("bus4")

    assert bus_info1 is not None and bus_info2 is not None
    assert bus_info1.total_stops == 3  # stop1 -> stop2 -> stop1
    assert bus_info1.length == 10
    assert bus_info2.total_stops == 2  # stop1 -> stop2
    assert bus_info2.length == 5
