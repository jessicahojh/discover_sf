"use strict";


// function initMap() {
//     // The location of Uluru
//     var uluru = {lat: -25.344, lng: 131.036};
//     // The map, centered at Uluru
//     var map = new google.maps.Map(
//         document.getElementById('places-map'), {zoom: 4, center: uluru});
//     // The marker, positioned at Uluru
//     var marker = new google.maps.Marker({position: uluru, map: map});
//     // getRequest();
// }



function getLat(locationData, placeId) {


    return locationData[placeId]['p_lat'];


}


function getLng(locationData, placeId) {

    return locationData[placeId]['p_long'];
}


function getRequest() {

    $.get('/places-location.json', (locationData) => {  // makes ajax call, saving the data into locationData which is the response from the API call


        let placeId = $('#place_id').text();
        placeId = parseInt(placeId)

        console.log(placeId) 



        let latitude = getLat(locationData, placeId);
        let longitude = getLng(locationData, placeId);


        let currentLocation = {lat: parseFloat(latitude), lng: parseFloat(longitude) * -1}

    
        var map = new google.maps.Map(
            document.getElementById('places-map'), {zoom: 10, center: currentLocation});
        
        var marker = new google.maps.Marker({position: currentLocation, map: map});
        
    });
        
  }   


function initMap() {
    getRequest();
}  
