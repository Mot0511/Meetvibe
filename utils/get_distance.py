from geopy.distance import geodesic

def get_distance(location1: list, location2: list) -> int:
    return int(geodesic(location1, location2).m)