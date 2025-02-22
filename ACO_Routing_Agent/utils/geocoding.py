import osmnx as ox
from geopy.geocoders import Nominatim
from shapely.geometry import box

def geocode_location(location):
    """
    Geocode a location string using Nominatim.
    Returns (latitude, longitude) or None if not found.
    """
    geolocator = Nominatim(user_agent="aco_agent_app")
    try:
        loc = geolocator.geocode(location)
        if loc:
            return (loc.latitude, loc.longitude)
        return None
    except Exception as e:
        print("Geocoding error:", e)
        return None

def get_graph_for_route(start_coords, dest_coords):
    """
    Download a road network from OSM covering both coordinates.
    A margin of about 1km is added.
    """
    margin = 0.01  # roughly 1km at mid-latitudes
    lat1, lon1 = start_coords
    lat2, lon2 = dest_coords
    north = max(lat1, lat2) + margin
    south = min(lat1, lat2) - margin
    east  = max(lon1, lon2) + margin
    west  = min(lon1, lon2) - margin
    
    # Create a polygon using shapely's box function:
    polygon = box(west, south, east, north)
    # Retrieve the graph from the polygon.
    graph = ox.graph_from_polygon(polygon, network_type='drive')
    return graph
