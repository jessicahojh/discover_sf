"use strict";

function initMap() {

    // Specify where the map is centered
    // Defining this variable outside of the map optios markers
    // it easier to dynamically change if you need to recenter
    let myLatLng = {lat: 37.601773, lng: -122.202870};

    // Create a map object and specify the DOM element for display.
    let map = new google.maps.Map(document.getElementById('places-map'), {
        center: myLatLng,
        scrollwheel: false,
        zoom: 5,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        styles: MAPSTYLES,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    });


    let infoWindow = new google.maps.InfoWindow({
        width: 150
    });

    // Retrieving the information with AJAX
    $.get('/places_location.json', function (place) {
      // Attach markers to each place location in returned JSON
      // JSON looks like:
      // {
      //  "1": {
      //    "name":"Stern Grove"
      //   },...
      // }
      let place, marker, html;

      for (let key in places) {
            place = place[key];

            // Define the marker
                marker = new google.maps.Marker({
                    position: new google.maps.LatLng(place.capLat, place.capLong),
                    map: map,
                    title: 'Place: ' + place.name,
                });

            // Define the content of the infoWindow
            html = (
              '<div class="window-content">' +
                    '<p><b>Place: </b>' + place.name + '</p>' 
              '</div>');

            // Inside the loop we call bindInfoWindow passing it the marker,
            // map, infoWindow and contentString
            bindInfoWindow(marker, map, infoWindow, html);
      }

    });

    // This function is outside the for loop.
    // When a marker is clicked it closes any currently open infowindows
    // Sets the content for the new marker with the content passed through
    // then it open the infoWindow with the new content on the marker that's clicked
    function bindInfoWindow(marker, map, infoWindow, html) {
        google.maps.event.addListener(marker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);
        });
    }
}

google.maps.event.addDomListener(window, 'load', initMap);