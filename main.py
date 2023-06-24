from flask import Flask, render_template, request
import folium

from script import test

app = Flask(__name__)
lat = 60.192059
long = 24.945831
zoom = 14
map = folium.Map(location=[lat, long], tiles="Stamen Toner", zoom_start=zoom)


def draw_marker(map_obj, lat, long, text):
    marker = folium.Marker(
        location=[lat, long],
        popup=text,
        icon=folium.Icon("orange", "white", prefix="fa", icon="bicycle"),
    )
    marker.add_to(map_obj)


@app.route("/", methods=["POST", "GET"])
def base():
    if request.method == "POST":
        search_query = request.form.get("search-input")
        print(search_query)
        print(test(search_query))
        draw_marker(map, lat, long, search_query)

    map_html = map._repr_html_()
    return render_template("base_map.html", map_html=map_html)


if __name__ == "__main__":
    app.run(debug=True)
