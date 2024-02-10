document.addEventListener('DOMContentLoaded', function() {
    const webcamElement = document.getElementById('webcam');
    const startButton = document.getElementById('startButton');
    const timerDisplay = document.getElementById('timer');
    let recording = false;
    let recorder;
    let stream;
    let startTime;

    const updateTimer = () => {
        const elapsedTime = Date.now() - startTime;
        const totalSeconds = Math.floor(elapsedTime / 1000);
        const minutes = String(Math.floor(totalSeconds / 60)).padStart(2, '0');
        const seconds = String(totalSeconds % 60).padStart(2, '0');
        timerDisplay.textContent = `${minutes}:${seconds}`;

        if (recording) {
            requestAnimationFrame(updateTimer);
        }
    };

    async function startRecording() {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        webcamElement.srcObject = stream;
        recorder = new MediaRecorder(stream);
        const chunks = [];

        recorder.ondataavailable = e => chunks.push(e.data);
        recorder.onstop = async () => {
            const completeBlob = new Blob(chunks, { type: chunks[0].type });
            console.log('Recording stopped, data available for download or upload.');
            // Here you can handle the blob (completeBlob) as needed, e.g., uploading to the server
        };

        recorder.start();
        console.log('Recording started');
        recording = true;
        startTime = Date.now();
        updateTimer();
    }

    function stopRecording() {
        if (recorder && recording) {
            recorder.stop();
            stream.getTracks().forEach(track => track.stop());
            recording = false;
        }
    }

    startButton.addEventListener('click', function() {
        if (recording) {
            stopRecording();
            startButton.textContent = 'Start';
        } else {
            startRecording();
            startButton.textContent = 'Stop';
        }
    });
});
