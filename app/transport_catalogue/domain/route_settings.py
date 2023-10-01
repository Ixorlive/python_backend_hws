from dataclasses import dataclass


@dataclass
class RouteSettings:
    bus_wait_time: int = 3
    bus_velocity: int = 20
