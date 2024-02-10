document.addEventListener('DOMContentLoaded', function () {
    const startButton = document.getElementById('startButton');
    const video = document.getElementById('webcam');

    // Constraints for the video stream
    const constraints = {
        video: true
    };

    // Function to start the webcam feed
    function startWebcam() {
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia(constraints)
                .then(function (stream) {
                    video.srcObject = stream;
                })
                .catch(function (error) {
                    console.error(`Error accessing the webcam: ${error}`);
                });
        } else {
            alert('Sorry, your browser does not support accessing the webcam.');
        }
    }

    // Event listener for the start button
    startButton.addEventListener('click', startWebcam);
});
