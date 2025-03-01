let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let result = document.querySelector('.scan-status');
let scanButton = document.getElementById('scan');

// Start camera
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error('Camera toegang mislukt:', err);
    }
}

// Verify iris
async function verifyIris() {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);
    
    const imageData = canvas.toDataURL('image/jpeg');
    
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
        result.textContent = 'Verificatie mislukt';
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', startCamera);
scanButton.addEventListener('click', verifyIris); 