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

    video.addEventListener('canplay', function (ev) {
        if (!streaming) {
            height = video.videoHeight / (video.videoWidth / width);
            video.setAttribute('width', width);
            video.setAttribute('height', height);
            streaming = !0;
        }
    }, !1);
});

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({video: true})
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err0r) {
            console.log("Something went wrong!");
        });
}