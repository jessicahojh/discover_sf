"use strict";

function initMap() {

    // Specify where the map is centered
    // Defining this variable outside of the map optios markers
    // it easier to dynamically change if you need to recenter
    let myLatLng = {lat: 37.7525, lng: -122.4476};

    // Create a map object and specify the DOM element for display.
    let map = new google.maps.Map(document.getElementById('places-map'), {
        center: myLatLng,
        scrollwheel: false,
        zoom: 12,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
    });



    // // Retrieving the information with AJAX
    // $.get('/places_location.json', function (places) {
    //   // Attach markers to each place location in returned JSON

    //   let place, marker, html;

    //   for (let key in places) {
    //     place = places[key];

    //     // Define the marker
    //         marker = new google.maps.Marker({
    //             position: new google.maps.LatLng(place.p_lat, place.p_long),
    //             map: map,
    //             title: 'Place: ' + place.placename,
    //         });

    //     bindInfoWindow(marker, map, infoWindow, html);

    //   }
    // });
}