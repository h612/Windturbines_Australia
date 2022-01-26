// var myMap = L.map("map", {
//   center: [40.7128, -74.0059],
//   zoom: 2
// });
// map.invalidateSize();

// // // Adding tile layer
// L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
//     attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
//     maxZoom: 18,
//     id: "mapbox.satellite",
//     accessToken: API_KEY
// }).addTo(myMap);

// Earthquakes GeoJSON URL Variables
console.log("HERE!!")
// var bushfiresURL = "../map_data"//"//"/fetch/mapData"// 
var link = "/map_data"//"../data/lat_lng_file.geojson"
// // var wt_layer = new L.LayerGroup();

var satelliteMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.satellite",
    accessToken: API_KEY
});
var darkMap =  L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "dark-v10",
    accessToken: API_KEY
});

var grayscaleMap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "light-v10",
    accessToken: API_KEY
});

// // Define baseMaps Object to Hold Base Layers
var baseMaps = {
    "Satellite": satelliteMap,
    "Grayscale": grayscaleMap,
    "Dark Map": darkMap
};

// var wtIcon = L.icon({
//   iconUrl: 'static/js/wt.png',
//   iconSize: [37, 53], // size of the icon
// });
list_1=[]
// // Grab the data with d3
d3.json(link, function(response) {
    console.log("inside HERE")
    console.log(response)
    console.log(link)
    console.log(response['lat'].length)
//     // L.marker([31, -115]).addTo(myMap);
    for (var i = 0; i < response['lat'].length; i+=1) {
        
      console.log("THIS",response['lat'][0])
      var location =[response['lat'][i],response['long'][i]];//
      console.log(location)  
//         if(typeof location === 'undefined'){
//           // element does not exist
//           console.log('undefined')
//         }
    
//         else {
//           if(typeof location[0] === 'undefined'){
//             console.log('undefined lat')
//           }
//           if(typeof location[1] === 'undefined'){
//             console.log('undefined lng')
//           }
//           if(location[0] != null && location[1] != null && location.length == 2){
            list_1.push(L.marker(location))//.bindPopup("<h1>" + "location" + "</h1>")
//             // list_1.push(L.marker(location, {icon: wtIcon}))//.bindPopup("<h1>" + "location" + "</h1>")

            // list_1.push(L.marker(location).bindPopup("<h1>" + "location" + "</h1>"))
//             // L.marker([location[0], location[1]]).addTo(myMap);
//             console.log('worked')
//           }
//         }
        
      }
      var wt_layer = L.layerGroup(list_1);
//       // Create Overlay Object to Hold Overlay Layers
      var overlayMaps = {
          "WindTurbines": wt_layer
      };
//       // Create Map, Passing In satelliteMap & wt_layer as Default Layers to Display on Load
      var myMap = L.map("map", {
          center: [-25.274398, 133.775136],
          zoom: 4,
          layers: [satelliteMap, wt_layer]//use addtomymap
      });
//       var geojson;
//       // Create a dropdown Layer Control + Pass in baseMaps and overlayMaps + Add the Layer Control to the Map
      L.control.layers(baseMaps, overlayMaps).addTo(myMap);

//       satelliteMap
    
    

});