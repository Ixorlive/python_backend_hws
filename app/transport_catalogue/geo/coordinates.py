import math


class Coordinates:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def __eq__(self, other):
        if isinstance(other, Coordinates):
            return self.lat == other.lat and self.lng == other.lng
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


def compute_distance(from_coord, to_coord):
    """
    Compute distance between two coordinates
    """
    dr = math.pi / 180.0  # converting to radians
    radius_earth = 6371000  # in meters

    lat1_rad = from_coord.lat * dr
    lat2_rad = to_coord.lat * dr
    delta_lng_rad = (to_coord.lng - from_coord.lng) * dr

    distance = (
        math.acos(
            math.sin(lat1_rad) * math.sin(lat2_rad)
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lng_rad)
        )
        * radius_earth
    )

    return distance
