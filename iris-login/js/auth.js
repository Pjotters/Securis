function checkAuth() {
    const token = localStorage.getItem('auth_token');
    if (token) {
        TokenManager.startTokenRefreshInterval();
        window.location.href = 'dashboard.html';
    }
}

function requireAuth() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
        // Als we niet ingelogd zijn, redirect naar login
        window.location.href = 'index.html';
    }
}

function logout() {
    localStorage.removeItem('auth_token');
    window.location.href = 'index.html';
}

// Token management
class TokenManager {
    static refreshToken() {
        const token = localStorage.getItem('auth_token');
        if (!token) return;

        fetch(`${API_BASE_URL}/api/refresh-token`, {
            method: 'POST',
            headers: {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                localStorage.setItem('auth_token', data.token);
                localStorage.setItem('refresh_token', data.refreshToken);
            }
        });
    }

    static startTokenRefreshInterval() {
        // Ververs token elke 15 minuten
        setInterval(this.refreshToken, 15 * 60 * 1000);
    }
}
