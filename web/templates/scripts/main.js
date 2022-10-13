var video = $('.video-preview')[0];

/*permissions*/
if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment'}})
        .then(function (stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function (err0r) {
            console.log("Something went wrong with permissions!");
        });
}

const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization',
    'Access-Control-Request-Method': 'GET, POST, DELETE, PUT, OPTIONS',
};

/*Scan button*/
document.getElementById("scan-button").addEventListener("click", function () {
    scanCode();
});

var stream = document.getElementById("stream");

async function scanCode() {
    var btnCapture = document.getElementById("scan-button");

    btnCapture.style.background = "transparent url('/static/icons/scan-loading.gif') no-repeat top left";
    btnCapture.style.backgroundSize = "cover";
    var img = new Image();
    var capture = document.createElement('canvas');
    console.log(stream);
    if (null != stream) {
        var ctx = capture.getContext('2d');

        ctx.drawImage(stream, 0, 0, capture.width, capture.height);
    }
    var base64Img = capture.toDataURL('image/jpeg', 1.0);

    var data = {
        'decode-type': 'image',
        'in-data': base64Img,
        'user-id': null,
        'style-info': {
            'name': 'geom-original',
        }
    }
    await fetch(`{{API_URL}}/coji-code/decode`, options = {
        method: "POST", body: JSON.stringify(data), headers: headers,
    })
        .then(await function (response) {
            return response.text();
        }).then(await function (text) {
            btnCapture.style.background = "transparent url('/static/icons/scan-button.png') no-repeat top left";
            btnCapture.style.backgroundSize = "cover";

            console.log('POST response text:');
            console.log(text);

            var resp = JSON.parse(text);
            if (resp['error']) {
                alert(resp['text'])
            } else {
                window.location.replace('data-preview/' + resp['code-id']);
            }
        });

    btnCapture.style.background = "transparent url('/static/icons/scan-button.png') no-repeat top left";
    btnCapture.style.backgroundSize = "cover";
}