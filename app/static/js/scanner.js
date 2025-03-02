let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let result = document.querySelector('.scan-status');
let scanButton = document.getElementById('scan');

// Start camera
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
        result.textContent = 'Bezig met scannen...';
        
        const response = await fetch(`${API_BASE_URL}/api/verify-iris`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });

        const data = await response.json();
        
        if (data.success) {
            result.textContent = data.authorized ? 
                '✅ Toegang verleend - Iris herkend' : 
                '❌ Toegang geweigerd - Iris niet herkend';
        } else {
            result.textContent = '❌ ' + data.message;
        }
    } catch (err) {
        console.error('Verificatie mislukt:', err);
        result.textContent = '❌ Verificatie mislukt: ' + err.message;
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    startCamera();
    scanButton.addEventListener('click', verifyIris);
}); 