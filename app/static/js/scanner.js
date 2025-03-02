let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let result = document.querySelector('.scan-status');
let scanButton = document.getElementById('scan');

// API endpoint configuratie
const API_BASE_URL = 'https://securis-m7bb.onrender.com'; // Update dit met je Render URL

// Start camera
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error('Camera toegang mislukt:', err);
        result.textContent = 'Camera toegang mislukt';
    }
}

// Verify iris
async function verifyIris() {
    try {
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0);
        
        const imageData = canvas.toDataURL('image/jpeg');
        
        const response = await fetch(`${API_BASE_URL}/api/verify-iris`, {
            method: 'POST',
            mode: 'cors',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        result.textContent = data.authorized ? 'Toegang verleend' : 'Toegang geweigerd';
    } catch (err) {
        console.error('Verificatie mislukt:', err);
        result.textContent = 'Verificatie mislukt: ' + err.message;
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    startCamera();
    scanButton.addEventListener('click', verifyIris);
}); 