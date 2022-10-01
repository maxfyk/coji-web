$(function () {
    var video = $('body > video')[0];

    navigator.getMedia = (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);

    navigator.getMedia({audio: false, video: {facingMode: {ideal: 'environment'},}}, function (stream) {
        if ('srcObject' in video) {
            video.srcObject = stream;
        } else {
            video.src = vu.createObjectURL(stream);
        }
        video.play();
    }, function (error) {
        if (window.console)
            console.error(error);
    });

});

/*Scan button*/
var btnCapture = document.getElementById("scan-button");
var stream = document.getElementById("stream");
btnCapture.addEventListener("click", scanCode);

function scanCode() {
    btnCapture.style.background = "transparent url('/static/icons/scan-loading.gif') no-repeat top left";
    btnCapture.style.backgroundSize = "cover";
    var img = new Image();
    var capture = document.createElement('canvas');

    if (null != stream) {
        var ctx = capture.getContext('2d');

        ctx.drawImage(stream, 0, 0, capture.width, capture.height);
    }
    var base64Img = capture.toDataURL();

    const data = {
        'decode-type': 'image',
        'in-data': base64Img,
        'user-id': 'asd22',
        'style-info': {
            'name': 'geom-original',
        }
    }
    fetch(`{{API_URL}}/coji-code/decode`, options = {
        method: "GET", mode: "no-cors", json: data, headers: {'content-type': 'application/json'},
    })
        .then(function (response) {
            return response.text();
        }).then(function (text) {
        console.log('GET response text:');
        console.log(text);
    });
    btnCapture.style.background = "transparent url('/static/icons/scan-button.png') no-repeat top left";
    btnCapture.style.backgroundSize = "cover";
}


/*Permissions*/
if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true})
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err0r) {
            console.log("Something went wrong with permissions!");
        });
}