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


def test_complex_route():
    # Create a new TransportCatalogue
    tc = TransportCatalogue()
    tc.set_route_settings(2, 30)

    # Add stops
    stops_data = [
        {
            "name": "Улица Лизы Чайкиной",
            "latitude": 43.590317,
            "longitude": 39.746833,
            "road_distances": {"Электросети": 4300, "Улица Докучаева": 2000},
        },
        {
            "name": "Морской вокзал",
            "latitude": 43.581969,
            "longitude": 39.719848,
            "road_distances": {"Ривьерский мост": 850},
        },
        {
            "name": "Электросети",
            "latitude": 43.598701,
            "longitude": 39.730623,
            "road_distances": {
                "Санаторий Родина": 4500,
                "Параллельная улица": 1200,
                "Ривьерский мост": 1900,
            },
        },
        {
            "name": "Ривьерский мост",
            "latitude": 43.587795,
            "longitude": 39.716901,
            "road_distances": {"Морской вокзал": 850, "Гостиница Сочи": 1740},
        },
        {
            "name": "Гостиница Сочи",
            "latitude": 43.578079,
            "longitude": 39.728068,
            "road_distances": {"Кубанская улица": 320},
        },
        {
            "name": "Кубанская улица",
            "latitude": 43.578509,
            "longitude": 39.730959,
            "road_distances": {"По требованию": 370},
        },
        {
            "name": "По требованию",
            "latitude": 43.579285,
            "longitude": 39.733742,
            "road_distances": {"Улица Докучаева": 600},
        },
        {
            "name": "Улица Докучаева",
            "latitude": 43.585586,
            "longitude": 39.733879,
            "road_distances": {"Параллельная улица": 1100},
        },
        {
            "name": "Параллельная улица",
            "latitude": 43.590041,
            "longitude": 39.732886,
            "road_distances": {},
        },
        {
            "name": "Санаторий Родина",
            "latitude": 43.601202,
            "longitude": 39.715498,
            "road_distances": {},
        },
    ]

    for stop_data in stops_data:
        tc.add_stop(stop_data["name"], stop_data["latitude"], stop_data["longitude"])
        if "road_distances" in stop_data:
            for target_stop, distance in stop_data["road_distances"].items():
                tc.set_dist_stops(stop_data["name"], target_stop, distance)

    # Add buses
    buses_data = [
        {
            "type": "Bus",
            "name": "14",
            "stops": [
                "Улица Лизы Чайкиной",
                "Электросети",
                "Ривьерский мост",
                "Гостиница Сочи",
                "Кубанская улица",
                "По требованию",
                "Улица Докучаева",
                "Улица Лизы Чайкиной",
            ],
            "is_roundtrip": True,
        },
        {
            "type": "Bus",
            "name": "24",
            "stops": [
                "Улица Докучаева",
                "Параллельная улица",
                "Электросети",
                "Санаторий Родина",
            ],
            "is_roundtrip": False,
        },
        {
            "type": "Bus",
            "name": "114",
            "stops": ["Морской вокзал", "Ривьерский мост"],
            "is_roundtrip": False,
        },
    ]

    for bus_data in buses_data:
        tc.add_bus(bus_data["name"], bus_data["stops"], bus_data["is_roundtrip"])

    tc_router = TransportRouter(tc)
    req_handler = RequestHandler(tc_router)

    route_info = req_handler.get_route_info("Морской вокзал", "Параллельная улица")

    # TODO: think about other tests
    expected_items = [
        {"stop_name": "Морской вокзал", "time": 2, "type": "Wait"},
        {"bus": "114", "span_count": 1, "time": 1.7, "type": "Bus"},
        {"stop_name": "Ривьерский мост", "time": 2, "type": "Wait"},
        {"bus": "14", "span_count": 4, "time": 6.06, "type": "Bus"},
        {"stop_name": "Улица Докучаева", "time": 2, "type": "Wait"},
        {"bus": "24", "span_count": 1, "time": 2.2, "type": "Bus"},
    ]
    expected_total_time = 15.96
    assert route_info is not None
    assert expected_total_time == pytest.approx(route_info.total_time)
    for i, item in enumerate(route_info.items):
        if item.is_wait:
            assert expected_items[i]["type"] == "Wait"
            assert expected_items[i]["stop_name"] == item.bus_or_stop_name
            assert expected_items[i]["time"] == pytest.approx(item.time)
        else:
            assert expected_items[i]["type"] == "Bus"
            assert expected_items[i]["bus"] == item.bus_or_stop_name
            assert expected_items[i]["time"] == pytest.approx(item.time)
            assert expected_items[i]["span_count"] == item.span_count
