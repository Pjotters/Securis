let video = document.getElementById('video');
let canvas = document.getElementById('canvas');
let result = document.querySelector('.scan-status');
let registerBtn = document.getElementById('registerBtn');

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

// Registreer iris
async function registerIris() {
    const userId = prompt('Voer gebruikers-ID in:');
    if (!userId) return;

    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);
    
    const imageData = canvas.toDataURL('image/jpeg');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/register-iris`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                user_id: userId,
                image: imageData 
            })
        });
        const data = await response.json();
        result.textContent = data.message;
    } catch (err) {
        console.error('Registratie mislukt:', err);
        result.textContent = 'Registratie mislukt';
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    startCamera();
    registerBtn.addEventListener('click', registerIris);
}); 