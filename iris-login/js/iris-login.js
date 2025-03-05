document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const status = document.getElementById('status');
    const loginBtn = document.getElementById('loginBtn');

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        status.textContent = 'Plaats je oog voor de camera';
    } catch (err) {
        status.textContent = 'Camera toegang mislukt';
        console.error(err);
    }

    loginBtn.onclick = async () => {
        try {
            status.textContent = 'Scanning...';
            
            const context = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            context.drawImage(video, 0, 0);
            
            const imageData = canvas.toDataURL('image/jpeg');
            
            const response = await fetch(`${API_BASE_URL}/api/login-with-iris`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageData })
            });

            const data = await response.json();
            
            if (data.success) {
                localStorage.setItem('auth_token', data.token);
                status.textContent = 'Login succesvol!';
                window.location.href = 'dashboard.html';
            } else {
                status.textContent = '❌ ' + data.message;
            }
        } catch (err) {
            status.textContent = '❌ Login mislukt';
            console.error(err);
        }
    };

    // Voeg backup login toe aan bestaande login interface
    const backupLoginBtn = document.createElement('button');
    backupLoginBtn.textContent = 'Login met Backup Code';
    backupLoginBtn.onclick = async () => {
        const backupCode = prompt('Voer je backup code in:');
        if (!backupCode) return;
        
        try {
            const response = await fetch(`${API_BASE_URL}/api/backup-login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ backup_code: backupCode })
            });
            
            const data = await response.json();
            if (data.success) {
                localStorage.setItem('auth_token', data.token);
                window.location.href = 'dashboard.html';
            } else {
                alert('Ongeldige backup code');
            }
        } catch (err) {
            console.error('Backup login mislukt:', err);
        }
    };
});
