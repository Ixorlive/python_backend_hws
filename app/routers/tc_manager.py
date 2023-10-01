from typing import Optional

from fastapi import APIRouter, HTTPException

from app.transport_catalogue.request_handler import RequestHandler
from app.transport_catalogue.transport_catalogue import TransportCatalogue
from app.transport_catalogue.transport_router import TransportRouter

from . import models

router = APIRouter()

db = TransportCatalogue()
tc_router: Optional[TransportRouter] = None
req_handler: Optional[RequestHandler] = None


# Set configuration (bus wait time and bus velocity) for the transport router.
# {"bus_wait_time": 0, "bus_velocity": 0}
@router.post("/config")
async def set_config(configuration: models.Config):
    db.set_route_settings(configuration.bus_wait_time, configuration.bus_velocity)
    return {"status": "Configuration updated successfully"}


# Add a new stop to the transport catalogue.
# Example of adding a stop
# {
#                "name": "Liza Chaikina Street",
#                "latitude": 43.590317,
#                "longitude": 39.746833,
#                "road_distances": {
#                    "Electrical networks": 4300,
#                    "Dokuchaev Street": 2000
#                }}
@router.post("/add_stop")
async def add_stop(stop: models.Stop):
    db.add_stop(stop.name, stop.latitude, stop.longitude)
    for stop_name, dist in stop.road_distances.items():
        db.set_dist_stops(stop.name, stop_name, dist)
    return {"status": f"Stop {stop.name} added successfully"}


# Add a new bus to the transport catalogue.
# Example: {
#                "name": "24",
#                "stops": [
#                    "Dokuchaev Street"
#                    "Parallel Street"
#                    "Electric networks",
#                    "Sanatorium Rodina"
#                ],
#                "is_roundtrip": false
# }
@router.post("/add_bus")
async def add_bus(bus: models.Bus):
    db.add_bus(bus.name, bus.stops, bus.is_roundtrip)
    return {"status": f"Bus {bus.name} added successfully"}


# Get a list of buses that stop at a specific stop.
# Example:
# { "buses": [
#      "14",
#      "24"
#  ]}
@router.get("/stop")
async def get_stop(stop_query: models.StopQuery):
    buses = db.get_list_buses_by_stop(stop_query.stop_name)
    if buses is None:
        return {"buses": {}}
    return {"buses": buses}


# Get information about a specific bus's route.
# Example:
# {
#      "curvature": 1.60481,
#      "route_length": 11230,
#      "stop_count": 8,
#      "unique_stop_count": 7
#  },
@router.get("/bus_info")
async def get_route_stops(bus_info_: models.BusInfo):
    bus_info = db.get_bus_info(bus_info_.bus_name)
    if bus_info is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return {
        "curvature": bus_info.curvature,
        "route_length": bus_info.length,
        "stop_count": bus_info.total_stops,
        "unique_stop_count": bus_info.unique_stops,
    }


# Initialize the transport router and return the optimal route between two stops.
# Example:
# "items": [
#      {
#          "stop_name": "Морской вокзал",
#          "time": 2,
#          "type": "Wait"
#      },
#      {
#          "bus": "114",
#          "span_count": 1,
#          "time": 1.7,
#          "type": "Bus"
#      },]
@router.get("/route")
async def get_route(route_query: models.Route):
    global req_handler
    if req_handler is None:
        tc_router = TransportRouter(db)
        req_handler = RequestHandler(tc_router)
    route_info = req_handler.get_route_info(route_query.from_stop, route_query.to_stop)
    if route_info is None:
        raise HTTPException(status_code=404, detail="One of the stops was not found")
    items = []
    for route_item in route_info.items:
        if route_item.is_wait:
            item = {
                "stop_name": route_item.bus_or_stop_name,
                "time": route_item.time,
                "type": "Wait",
            }
        else:
            item = {
                "bus": route_item.bus_or_stop_name,
                "span_count": route_item.span_count,
                "time": route_item.time,
                "type": "Bus",
            }
        items.append(item)

    response = {
        "items": items,
        "total_time": route_info.total_time,
    }

    return response


# Update the transport router, rebuilding graph/router
@router.get("/update_router")
async def update_router():
    """
    Note: Very slow operation (O(n^3), where n - count of stops (2*n))!
    p.s.: We want to give the optimal route very quickly
    - for this we build a transitive closure. Because of this, it will not be possible
    to update the router every time the transport directory is changed.
    Therefore, first we indicate which stops are on our map,
    then which buses go to them, and after we have finished, we can build a router.
    We can continue to change the catalogue, but we must remember
    to update the router afterwards (for example, at night)
    so that users can build routes with new data.
    """
    global tc_router, req_handler
    tc_router = TransportRouter(db)
    req_handler = RequestHandler(tc_router)
    return {"status", "Transport router updated successfully"}
