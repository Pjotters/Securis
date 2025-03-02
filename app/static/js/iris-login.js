class IrisLogin {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
    }
    
    async startLogin() {
        try {
            // Start camera
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            const video = document.createElement('video');
            video.srcObject = stream;
            
            // Maak scan interface
            const loginContainer = this.createLoginInterface(video);
            document.body.appendChild(loginContainer);
            
            // Handle login
            loginContainer.querySelector('#loginBtn').onclick = async () => {
                const imageData = this.captureImage(video);
                const result = await this.verifyIris(imageData);
                
                if (result.success) {
                    // Sla token op
                    localStorage.setItem('auth_token', result.token);
                    // Redirect naar dashboard
                    window.location.href = '/dashboard';
                } else {
                    alert(result.message);
                }
            };
        } catch (err) {
            console.error('Login failed:', err);
        }
    }
    
    async verifyIris(imageData) {
        const response = await fetch(`${this.apiUrl}/api/login-with-iris`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData })
        });
        return response.json();
    }
} 