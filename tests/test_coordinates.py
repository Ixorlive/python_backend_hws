import pytest

from app.transport_catalogue.geo.coordinates import Coordinates, compute_distance


@pytest.mark.parametrize(
    "coord1, coord2, expected",
    [
        (Coordinates(0, 0), Coordinates(0, 0), 0.0),
        (Coordinates(1, 0), Coordinates(0, 1), 157249),
        (Coordinates(44, 23), Coordinates(-44, 23), 9785154),
    ],
)
def test_compute_distance(coord1, coord2, expected):
    result = compute_distance(coord1, coord2)
    assert expected == round(result, 0)
