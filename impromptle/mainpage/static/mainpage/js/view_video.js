document.addEventListener('DOMContentLoaded', function() {
    const videoId = document.getElementById('videoId').value; // Make sure this is correctly set in your HTML

    // Function to get CSRF token, useful for any POST requests you might add later
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Fetch the transcription for the video
    fetch(`/video/${videoId}/`) // Make sure this URL matches your Django URL pattern for the transcription view
    .then(response => response.json())
    .then(data => {
        // Once the transcription is received, display it
        const transcriptionText = data.transcription;
        document.querySelector('.transcript-section').innerHTML = `<h3>Transcription</h3><p>${transcriptionText}</p>`;
    })
    .catch(error => console.error('Error fetching transcription:', error));
});
