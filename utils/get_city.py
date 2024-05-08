from geopy.geocoders import Nominatim

def get_city(latitude: str, longitude: str) -> str:
    geolocator = Nominatim(user_agent='meetvibe')  # geolocator init
    location = geolocator.reverse(f"{latitude}, {longitude}", language='ru').raw  # getting location
    return location['address']['city'] if location['address']['city'] else location['address']['town']  # returning city or town