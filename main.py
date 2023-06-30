from script import *

app = Flask(__name__)

@app.route("/")
def base():
    map = folium.Map(location=[default_lat, default_long], tiles="Stamen Toner", zoom_start=zoom)
    result = run_query(uri, data, 200, headers)
    bikeStations = [ BikeStation(**station) for station in result["data"]["bikeRentalStations"] ]
    for station in bikeStations:
        draw_marker(map, station.lat, station.lon, f"{station.name}\n{station.stationId}")
    map_html = map._repr_html_()
    return render_template("base_map.html", map_html=map_html)


@app.route("/mylocation/<latitude>/<longitude>/")
def mylocation(latitude, longitude):
    map = folium.Map(location=[latitude, longitude], tiles="Stamen Toner", zoom_start=zoom)
    result = run_query(uri, data, 200, headers)
    bikeStations = [ BikeStation(**station) for station in result["data"]["bikeRentalStations"] ]
    for station in bikeStations:
        draw_marker(map, station.lat, station.lon, f"{station.name}\n{station.stationId}")
    draw_marker(map, latitude, longitude, "My Location", color="blue", icon="user")
    map_html = map._repr_html_()
    return render_template("base_map.html", map_html=map_html)


# @app.route('/process_location', methods=['POST'])
# def process_location():
#     latitude = request.form.get('latitude')
#     longitude = request.form.get('longitude')
#     print(latitude, longitude)
#     return redirect(url_for('mylocation', latitude=latitude, longitude=longitude))


if __name__ == "__main__":
    app.run(debug=True)
