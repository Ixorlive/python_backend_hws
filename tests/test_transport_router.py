import pytest

from app.transport_catalogue.transport_catalogue import TransportCatalogue
from app.transport_catalogue.transport_router import TransportRouter


@pytest.fixture
def transport_catalogue():
    tc = TransportCatalogue()
    tc.add_stop("stop1", 50.4501, 30.5234)
    tc.add_stop("stop2", 50.4502, 30.5235)
    tc.add_stop("stop3", 50.4502, 30.5235)
    tc.set_dist_stops("stop1", "stop2", 1000)
    tc.set_dist_stops("stop2", "stop3", 1000)
    tc.add_bus("bus1", ["stop1", "stop2", "stop3"], True)
    tc.add_bus("bus2", ["stop1", "stop2", "stop3"], False)
    tc.set_route_settings(3, 60)
    return tc


def test_router(transport_catalogue):
    router = TransportRouter(transport_catalogue)
    route = router.get_route_info("stop1", "stop3")
    assert route is not None
    # wait bus1 (3 min), stop1 -> (1 min) -> stop2 -> (1 min) -> stop3
    assert route.weight.time == 1 + 1 + 3
