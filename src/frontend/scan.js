// scan.js - Handle policy scan page
document.getElementById('policyForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    try {
        const response = await fetch('http://localhost:8000/v1/shop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        // Store result and redirect to results
        localStorage.setItem('savings', JSON.stringify(result));
        window.location.href = 'results.html';
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

document.getElementById('voiceButton').addEventListener('click', () => {
    // Placeholder for ElevenLabs integration
    // Use Web Speech API for demo
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            // Parse transcript to fill form - placeholder
            alert('Voice input: ' + transcript);
        };

        recognition.start();
    } else {
        alert('Speech recognition not supported');
    }
});