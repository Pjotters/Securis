document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const status = document.getElementById('status');
    const registerBtn = document.getElementById('registerBtn');

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        status.textContent = 'Plaats je oog voor de camera';
    } catch (err) {
        status.textContent = 'Camera toegang mislukt';
        console.error(err);
    }

    registerBtn.onclick = async () => {
        const userId = prompt('Voer gebruikers-ID in:');
        if (!userId) return;

        try {
            status.textContent = 'Bezig met registreren...';
            
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0);
            
            const imageData = canvas.toDataURL('image/jpeg');
            
            const response = await fetch(`${API_BASE_URL}/api/register-iris`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    user_id: userId,
                    image: imageData 
                })
            });

            const data = await response.json();
            status.textContent = data.message;
            
            if (data.success) {
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 2000);
            }
        } catch (err) {
            status.textContent = 'Registratie mislukt';
            console.error(err);
        }
    };
});   