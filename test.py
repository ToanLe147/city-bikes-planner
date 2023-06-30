from script import *

result = run_query(uri, data, 200, headers)
bikeStations = [ BikeStation(**station) for station in result["data"]["bikeRentalStations"] ]
for station in bikeStations:
    draw_marker(map, station.lat, station.lon, f"{station.name}\n{station.stationId}")

draw_marker(map, 60.208047, 25.0813858, "My Location", color="blue", icon="user")

map_html = map._repr_html_()

app = Flask(__name__)

@app.route('/')
def map():
    return render_template('test.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    # Create a map centered on the received latitude and longitude
    m = folium.Map(location=[latitude, longitude], zoom_start=13)

    # Add a marker to the map
    folium.Marker([latitude, longitude]).add_to(m)

    # Generate the HTML for the map
    map_html = m._repr_html_()

    return map_html

if __name__ == '__main__':
    app.run()
