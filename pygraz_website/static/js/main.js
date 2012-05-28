$(function() {
    if (typeof google === 'undefined') {
        console.log("Google Maps not available");
        return;
    }
    var geocoder = new google.maps.Geocoder();

    $('.meetup-data').each(function() {
        var meetup = $(this);
        var address = $('.address', meetup);
        if (address.length) {
            var addrStr = address.text();
            var mapContainer = $('<div>').addClass("map").css({'width': '285px', 'height': '250px'});
            mapContainer.insertAfter(address);

            geocoder.geocode({'address': addrStr}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var mapOpts = {
                        center: results[0].geometry.location,
                        zoom: 14,
                        mapTypeId: google.maps.MapTypeId.ROADMAP
                    };
                    var map = new google.maps.Map(mapContainer[0], mapOpts);
                    var marker = new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location
                    });
                } else {
                    alert("Geocode was not successful for the following reason: " + status);
                }
            });
        }
    });
});