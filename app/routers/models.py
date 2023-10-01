from typing import Dict, List

from pydantic import BaseModel


class Stop(BaseModel):
    name: str
    latitude: float
    longitude: float
    road_distances: Dict[str, float]


class Bus(BaseModel):
    name: str
    stops: List[str]
    is_roundtrip: bool


class Config(BaseModel):
    bus_wait_time: int
    bus_velocity: int


class Route(BaseModel):
    from_stop: str
    to_stop: str


class BusInfo(BaseModel):
    bus_name: str


class StopQuery(BaseModel):
    stop_name: str
