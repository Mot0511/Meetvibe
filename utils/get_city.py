from geopy.geocoders import Nominatim

def get_city(latitude: str, longitude: str) -> str:
    geolocator = Nominatim(user_agent='meetvibe')
    location = geolocator.reverse(f"{latitude}, {longitude}", language='ru').raw
    return location['address']['town']