import os

PLANET_API_KEY = os.environ.get('PLANET_API_KEY')
PLANET_URL = "https://api.planet.com/basemaps/v1/mosaics"

class PlanetAPI():
    def __init__(self, api_key=PLANET_API_KEY, api_url=PLANET_URL):
        self.api_key = api_key
        self.api_url = api_url







