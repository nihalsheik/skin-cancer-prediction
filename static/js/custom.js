// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();


// client section owl carousel
$(".client_owl-carousel").owlCarousel({
    loop: true,
    margin: 0,
    dots: false,
    nav: true,
    navText: [],
    autoplay: true,
    autoplayHoverPause: true,
    navText: [
        '<i class="fa fa-angle-left" aria-hidden="true"></i>',
        '<i class="fa fa-angle-right" aria-hidden="true"></i>'
    ],
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 1
        },
        1000: {
            items: 2
        }
    }
});



/** google_map js **/
function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

function login() {
    $.ajax({
        url: 'login',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            email: $('#email').val(),
            password: $('#password').val(),
        }),
        success: function (data) {
            if (data.result == true) {
                window.location = "index"
            } else {
                $('#form-error')
                    .text('Invalid Username / Password')
                    .show();
            }
        }
    });
}

function logout() {
  $.ajax({
        url: 'logout',
        method: 'POST',
        contentType: 'application/json',
        success: function (data) {
            window.location = "index"
        }
    });
}