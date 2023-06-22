const myApp = Object.create(null)

// ======================= MAP =========================

var lat = 60.192059;
var long = 24.945831;
var zoom = 13;

function drawRectInCenter(x, y, width, height) {
	return [x - width / 2, y - height / 2, width, height]
}

function initmap(lat, long, zoom) {
	var stamen = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.{ext}', {
		attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
		subdomains: 'abcd',
		minZoom: 1,
		maxZoom: 16,
		ext: 'png'
	});

	return L.map('map-id', { layers: [stamen] }).setView([lat, long], zoom);
}


function loadStations() {
	alert("Alo alo")
	var marker = L.marker([60.2, 24.95]).addTo(myApp.map);
	// var circle = L.circle([60.2, 24.95], {
	// 	color: 'red',
	// 	fillColor: '#f03',
	// 	fillOpacity: 0.5,
	// 	radius: 300, renderer: fpRender
	// }).addTo(myApp.map).bindPopup("Station: ABC. 12/20 bikes");
}


L.Canvas.FPCanvas = L.Canvas.extend({
	options: {
		width: 1,
		height: 1
	},
	initialize: function (name, options) {
		this.name = name;
		L.setOptions(this, options);
		L.Canvas.prototype.initialize.call(this, { padding: 0.5 })
	},
	_draw: function () {
		var layer, bounds = this._redrawBounds;
		this._ctx.save();
		if (bounds) {
			var size = bounds.getSize();
			this._ctx.beginPath();
			this._ctx.rect(bounds.min.x, bounds.min.y, size.x, size.y);
			this._ctx.clip();
		}

		this._drawing = true;

		for (var order = this._drawFirst; order; order = order.next) {
			layer = order.layer;
			if (!bounds || (layer._pxBounds && layer._pxBounds.intersects(bounds))) {
				layer._updatePath();
			}
		}
		this._drawing = false;
		this._ctx.restore();  // Restore state before clipping.
	},
});
L.canvas.fpCanvas = function (id, options) {
	return new L.Canvas.FPCanvas(id, options)
}

// ==================== ON LOAD ======================

var loaded = function () {
	console.clear()
	var myRenderer = L.canvas({ padding: 0.5 });
	// Handler when the DOM is fully loaded
	myApp.map = initmap(lat, long, zoom);

	var fpRender = L.canvas.fpCanvas({ padding: 0.5 })
};

loaded()
document.getElementById("ConfirmBtn").onclick = loadStations()