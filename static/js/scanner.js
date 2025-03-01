const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const scanButton = document.getElementById('scan');
const result = document.getElementById('result');

// Camera opstarten
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error('Camera toegang mislukt:', err);
    }
}

// Iris scan functie
async function scanIris() {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);
    
    // Converteer naar base64 voor verzending naar backend
    const imageData = canvas.toDataURL('image/jpeg');
    
    // Stuur naar backend voor analyse
    try {
        const response = await fetch('/api/verify-iris', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        const data = await response.json();
        result.textContent = data.authorized ? 'Toegang verleend' : 'Toegang geweigerd';
    } catch (err) {
        console.error('Verificatie mislukt:', err);
    }
} 