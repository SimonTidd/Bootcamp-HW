
// Store our API endpoint as queryUrl
var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson";

// Perform a GET request to the query URL
d3.json(queryUrl, function(data) {
  createFeatures(data.features);
});

function createFeatures(earthquakeData) {
   
    function onEachFeature(feature, layer) {
        layer.bindPopup("<h3>" + feature.properties.title + " Depth (km)" + feature.properties.depth + "<h3>")
    }

    var earthquakes = L.geoJSON(earthquakeData, {
        onEachFeature: onEachFeature
      });
    
      // Sending earthquakes layer to the createMap function
      createMap(earthquakes);
    }

function createMap(earthquakes) {

  // Create the tile layer that will be the background of map
  var lightmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"http://mapbox.com\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.light",
    accessToken: API_KEY
  });

  // Create a baseMaps object to hold the lightmap layer
  var baseMaps = {
    "Light Map": lightmap
  };


  // Create an overlayMaps object to hold the earthquakes layer
  var overlayMaps = {
    Earthquakes: earthquakes
  };

  // Create the map object with options
  var myMap = L.map("map-id", {
    center: [40.73, -74.0059],
    zoom: 12,
    layers: [baseMaps, overlayMaps]
  });
  createMarkers(earthquakes);

}

// create function to set markersize 

    function markerSize(mag) {
        return 5+(mag*mag);
}  
  //create function to set color based on magnitude
  
  
    function getColor(mag) {
    return mag > 9 ? '#660000' :
        mag > 8 ? '#990000' :
        mag > 7 ? '#e60000' :
        mag > 6 ? '#ff0000' :
        mag > 5 ? '#ff3333' :
        mag > 4 ? '#ff6666' :
        mag > 3 ? '#ff9999' :
        mag > 2 ? '#ffb3b3' :
        mag > 1 ? '#ffcccc' :
        mag > 0 ? '#ffe6e6' :
    
                                '#4d0000';
    } 
  


function createMarkers(data) {

  // Pull the "features" property off of response.data
  var features = data.features;

  // Initialize an array to hold earthquake markers
  var quakeMarkers = [];

  // Loop through the earthquake array
  for (var index = 0; index < features.length; index++) {
    var feature = features[index];

    // For each earthquake, create a marker and bind a popup with the distance from nearest city, maginitude, and depth
    var quakeMarker = L.circle([feature.geometry.coordinates[0], feature.geometry.coordinates[1]], {
    color: "black",
    fillOpacity: 0.75,
    fillColor:getColor(feature.properties.mag),
    radius: markerSize(feature.properties.mag)
    }).bindPopup("<h3>" + feature.properties.title + " Depth (km)" + feature.properties.depth + "<h3>")
    // Add the marker to the earthquake array
   
    quakeMarkers.push(quakeMarker);

  }
   createMap(L.layerGroup(quakeMarkers));
   // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
   L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(myMap);
   // add legend to the map

   var legend = L.control({position: "bottomright"});
   legend.onAdd = function (myMap) { }
   var div = L.DomUtil.create("div", "info legend"),
   grades = [0,1,2,3,4,5,6.7,8,9.10];
   for (var i = 0; i < grades.length; i++) {
    div.innerHTML += "<i style=”background:’ + getColor(grades[i]) + ‘”></i> ‘ + grades[i] + (grades[i + 1] ? ‘&ndash;’ + grades[i + 1] + ‘<br>’ : ‘+’"
    return div;
    };
    legend.addTo(myMap);

   
}
