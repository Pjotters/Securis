function checkAuth() {
    const token = localStorage.getItem('auth_token');
    if (token) {
        // Als we al ingelogd zijn, redirect naar dashboard
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
