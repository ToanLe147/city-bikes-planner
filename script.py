from collections import namedtuple
from flask import Flask, render_template, request, redirect, url_for
import folium
import requests


# INITIAL VARIABLES
##### MAP #####
default_lat = 60.192059
default_long = 24.945831
zoom = 14
##### HSL api #####
uri = 'https://dev-api.digitransit.fi/routing/v1/routers/hsl/index/graphql'
headers = {
    'digitransit-subscription-key': 'f6cbec0424c842f4a7bc0c8a12908a1f',
    'Content-Type': 'application/graphql'
}
data = """{
  bikeRentalStations {
    name
    stationId
    lat
    lon
  }
}
"""
StationTemplate = {
    "stationId": "default",
    "name": "default",
    "lat": 0.0,
    "lon": 0.0
}
BikeStation = namedtuple("BikeStation", StationTemplate)


def run_query(uri, data, statusCode, headers):
    request = requests.post(uri, data=data, headers=headers)
    if request.status_code != statusCode:
        raise Exception(f"Unexpected status code returned: {request.status_code}")
    return request.json()


def draw_marker(map_obj, lat, long, text, color="orange", icon="bicycle"):
    marker = folium.Marker(
        location=[lat, long],
        popup=text,
        icon=folium.Icon(color, "white", prefix="fa", icon=icon),
    )
    marker.add_to(map_obj)
