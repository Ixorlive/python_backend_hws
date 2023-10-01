import pytest

from app.transport_catalogue.request_handler import RequestHandler, TransportRouter
from app.transport_catalogue.transport_catalogue import TransportCatalogue


@pytest.fixture
def transport_catalogue():
    tc = TransportCatalogue()
    tc.add_stop("stop1", 50.4501, 30.5234)
    tc.add_stop("stop2", 50.4502, 30.5235)
    tc.add_stop("stop3", 50.4502, 30.5235)
    tc.add_stop("stop4", 55.4502, 35.5235)
    tc.set_dist_stops("stop1", "stop2", 1000)
    tc.set_dist_stops("stop1", "stop3", 1000)
    tc.set_dist_stops("stop2", "stop3", 1000)
    tc.set_dist_stops("stop3", "stop4", 1000)
    tc.add_bus("bus1", ["stop1", "stop2", "stop3"], False)
    tc.add_bus("bus2", ["stop1", "stop3", "stop4"], True)
    tc.set_route_settings(3, 60)
    return tc


@pytest.fixture
def transport_router(transport_catalogue):
    tr = TransportRouter(transport_catalogue)
    return tr


@pytest.fixture
def request_handler(transport_router):
    return RequestHandler(transport_router)


def test_request_handler(request_handler: RequestHandler):
    route = request_handler.get_route_info("stop3", "stop1")
    assert route is not None
    assert route.total_time == 5
    items = route.items

    assert items[0].is_wait
    assert items[0].time == 3
    assert items[0].bus_or_stop_name == "stop3"

    assert items[1].bus_or_stop_name == "bus1"
    assert items[1].time == 2


def test_request_handler_roundtrip(request_handler: RequestHandler):
    route_none = request_handler.get_route_info("stop4", "stop1")
    assert route_none is None
    route = request_handler.get_route_info("stop1", "stop4")
    assert route is not None
    assert route.total_time == 5
    items = route.items

    assert items[0].is_wait
    assert items[0].time == 3
    assert items[0].bus_or_stop_name == "stop1"

    assert items[1].bus_or_stop_name == "bus2"
    assert items[1].time == 2
