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

function nav(page) {
    window.location = page;
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

function doSignup() {
    var name = $('#name').val();
    var email = $('#email').val();
    var mobile = $('#mobile').val();
    var password = $('#password').val();

    $.ajax({
        url: 'signup',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            name: name,
            email: email,
            mobile: mobile,
            password: password
        }),
        success: function (data) {
            console.log(data);

            if (data.hasError == false) {
                window.location = "index"
            } else {
                $('#form-error')
                    .text(data.error)
                    .show();
            }
        }
    });
}


function registerPatient() {

    var name = $('#name').val();
    var dob = $('#dob').val();
    var mobile = $('#mobile').val();
    var address = $('#address').val();

    $.ajax({
        url: '/patient/register',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            name: name,
            dob: dob,
            mobile: mobile,
            address: address
        }),
        success: function (data) {
            console.log(data);

            if (data.hasError == false) {
                window.location = "index"
            } else {
                $('#form-error')
                    .text(data.error)
                    .show();
            }
        }
    });
}

function buildDoctorList(result) {
    $.ajax({
        url: '/api/doctors',
        method: 'GET',
        success: function(result) {
            var doctorList = $('#doctorList');
            result.forEach(doctor => {
                var opt = $('<option>').attr('value', doctor.id + ',' + doctor.fees).text(doctor.name);
                doctorList.append(opt);
            });
        }
    });
}

function fillDoctorFees() {
    var doctorList = $('#doctorList');
    var value = doctorList.val();
    var arr = value.split(','); // it will split 102,660 into [101,600]
    var fees = arr[1];
    var feesBox = $('#fees');
    feesBox.val(fees);
}

function searchPatient() {
    var mobile = $('#mobile').val()
     $.ajax({
        url: '/api/patient/search?mobile=' + mobile,
        method: 'GET',
        success: function(patient) {
            var container = $('#patientDetail');
            container.append(patient.name + ", ");
            container.append(patient.address + ", ");
            container.append(patient.mobile);
            $('#patientId').val(patient.id);
        }
    })
}


function bookAppointment() {
    var patientId = $('#patientId').val();
    var doctorId = $('#doctorList').val();
    var date = $('#date').val();
    var fees = $('#fees').val();

    var errorDiv = document.getElementById("form-error");
    var qrDiv = document.getElementById("payment-qr");

    if (patientId == '-1' || doctorId == '-1' || !date || !amount) {
        errorDiv.innerText = "Please fill in all fields!";
        errorDiv.style.display = "block";
        return;
    }
    errorDiv.style.display = "none";
//    qrDiv.style.display = "block";


    $.ajax({
        url: '/api/appointment/book',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            patient_id: patientId,
            doctor_id: doctorId,
            date: date,
            fees: fees
        }),
        success: function (data) {
            debugger;
            if (data.error == null) {
                window.location = "index"
            } else {
                $('#form-error')
                    .text(data.error)
                    .show();
            }
        }
    });

    debugger;
}