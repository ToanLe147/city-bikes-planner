import requests
import json
from collections import namedtuple


uri = 'https://dev-api.digitransit.fi/routing/v1/routers/hsl/index/graphql'
headers = {
    'digitransit-subscription-key': 'f6cbec0424c842f4a7bc0c8a12908a1f',
    'Content-Type': 'application/graphql'
}
InitStationdata = """{
  bikeRentalStations {
    name
    stationId
    bikesAvailable
    spacesAvailable
    lat
    lon
  }
}
"""
RTStationdata = """{
  bikeRentalStations {
    name
    stationId
    bikesAvailable
    spacesAvailable
  }
}
"""
StationTemplate = {
    "stationId": "default",
    "name": "default",
    "bikesAvailable": 0,
    "spacesAvailable": 0,
    "lat": 0.0,
    "lon": 0.0
}
BikeStation = namedtuple("BikeStation", StationTemplate)


class BikeStationManager:
    def __init__(self) -> None:
        result = run_query(uri, InitStationdata, 200, headers)
        self.bikeStations = [ BikeStation(**station) for station in result["data"]["bikeRentalStations"] ]

    def get_data(self):
        pass


class TripPlanner:
    def __init__(self) -> None:
        pass


def run_query(uri, data, statusCode, headers):
    request = requests.post(uri, data=data, headers=headers)
    if request.status_code != statusCode:
        raise Exception(f"Unexpected status code returned: {request.status_code}")
    return request.json()


def test_query():
    result = run_query(uri, InitStationdata, 200, headers)
    # bikeStation = [ BikeStations(**station) for station in result["data"]["bikeRentalStations"] ]

    for station in result["data"]["bikeRentalStations"]:
        bikeStation = BikeStation(**station)
        print(bikeStation)
