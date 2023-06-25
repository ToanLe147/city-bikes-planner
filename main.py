from collections import namedtuple
from flask import Flask, render_template, request
import folium
import requests


# INITIAL VARIABLES
##### MAP #####
app = Flask(__name__)
lat = 60.192059
long = 24.945831
zoom = 14
map = folium.Map(location=[lat, long], tiles="Stamen Toner", zoom_start=zoom)
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
    bikesAvailable
    spacesAvailable
    lat
    lon
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


result = run_query(uri, data, 200, headers)
bikeStations = [ BikeStation(**station) for station in result["data"]["bikeRentalStations"] ]
for station in bikeStations:
    draw_marker(map, station.lat, station.lon, f"{station.name}\n{station.bikesAvailable}/{station.spacesAvailable + station.bikesAvailable}")

draw_marker(map, 60.208047, 25.0813858, "My Location", color="blue", icon="user")

map_html = map._repr_html_()


@app.route("/", methods=["POST", "GET"])
def base():
    if request.method == "POST":
        search_query = request.form.get("search-input")
        print(search_query)

    return render_template("base_map.html", map_html=map_html)


@app.route("/trip", methods=["POST"])
def trip():
    if request.method == "POST":
        search_query = request.form.get("search-input")
        print(search_query)
        draw_marker(map, lat, long, search_query)


if __name__ == "__main__":
    app.run(debug=True)
