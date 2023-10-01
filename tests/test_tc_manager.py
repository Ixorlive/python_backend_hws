import pytest
from fastapi.testclient import TestClient

from app.app import app


@pytest.fixture
def client():
    stop1 = {
        "name": "stop1",
        "latitude": 43.590317,
        "longitude": 39.746833,
        "road_distances": {"stop2": 10},
    }
    stop2 = {
        "name": "stop2",
        "latitude": 44.590317,
        "longitude": 39.741231,
        "road_distances": {},
    }
    bus = {
        "name": "bus1",
        "stops": ["stop1", "stop2"],
        "is_roundtrip": False,
    }
    client = TestClient(app)
    client.post("/tc/config", json={"bus_wait_time": 2, "bus_velocity": 60})
    client.post("/tc/add_stop", json=stop1)
    client.post("/tc/add_stop", json=stop2)
    client.post("/tc/add_bus", json=bus)
    return client


def test_get_stop(client):
    test_stop_query = {"stop_name": "stop1"}

    response = client.post("/tc/stop", json=test_stop_query)

    assert response.status_code == 200
    assert response.json()["buses"] == ["bus1"]

    response = client.post("/tc/stop", json={"stop_name": "not_exists"})
    assert response.status_code == 404


def test_bus_info(client):
    test_bus_info = {"bus_name": "bus1"}
    response = client.post("/tc/bus_info", json=test_bus_info)

    assert response.status_code == 200
    assert response.json()
    assert response.json()["route_length"] == 20
    assert response.json()["stop_count"] == 3
    assert response.json()["unique_stop_count"] == 2

    not_exists_bus = {"bus_name": "bus2"}
    response = client.post("/tc/bus_info", json=not_exists_bus)
    assert response.status_code == 404


def test_add(client):
    stop2 = {
        "name": "stop3",
        "latitude": 45.590317,
        "longitude": 39.741231,
        "road_distances": {},
    }
    response = client.post("/tc/add_stop", json=stop2)

    assert response.status_code == 200
    assert response.json() == {"status": "Stop stop3 added successfully"}

    test_bus = {
        "name": "TestBus",
        "stops": ["stop2", "stop3"],
        "is_roundtrip": False,
    }

    response = client.post("/tc/add_bus", json=test_bus)

    assert response.status_code == 200
    assert response.json() == {"status": "Bus TestBus added successfully"}
