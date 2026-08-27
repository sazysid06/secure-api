const API_URL = "http://localhost:8000";

let tokens = {
    access_token: null,
    refresh_token: null
};

// Toggle between signup and login forms
function toggleForm() {
    document.getElementById('signup-form').classList.toggle('hidden');
    document.getElementById('login-form').classList.toggle('hidden');
    clearMessages();
}

// Clear all messages
function clearMessages() {
    document.getElementById('signup-message').textContent = '';
    document.getElementById('login-message').textContent = '';
    document.getElementById('dashboard-message').textContent = '';
}

// Show message
function showMessage(elementId, message, type = 'info') {
    const messageEl = document.getElementById(elementId);
    messageEl.textContent = message;
    messageEl.className = `message ${type}`;
}

// Signup
async function signup() {
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

    if (!username || !email || !password) {
        showMessage('signup-message', 'All fields required', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/users/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('signup-message', 'Signup successful! Please login.', 'success');
            document.getElementById('signup-username').value = '';
            document.getElementById('signup-email').value = '';
            document.getElementById('signup-password').value = '';
            setTimeout(() => toggleForm(), 2000);
        } else {
            showMessage('signup-message', data.detail || 'Signup failed', 'error');
        }
    } catch (error) {
        showMessage('signup-message', 'Error: ' + error.message, 'error');
    }
}

// Login
async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
        showMessage('login-message', 'Email and password required', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/users/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            tokens.access_token = data.access_token;
            tokens.refresh_token = data.refresh_token;

            // Decode token to get user info
            const userInfo = parseJwt(data.access_token);

            showMessage('login-message', 'Login successful!', 'success');

            // Show dashboard
            document.getElementById('login-form').classList.add('hidden');
            document.getElementById('dashboard').classList.remove('hidden');
            document.getElementById('user-name').textContent = userInfo.email;
            document.getElementById('user-role').textContent = userInfo.role;

        } else {
            showMessage('login-message', data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        showMessage('login-message', 'Error: ' + error.message, 'error');
    }
}

// Fetch my posts (protected route)
async function fetchMyPosts() {
    if (!tokens.access_token) {
        showMessage('dashboard-message', 'Not authenticated', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/posts/my-posts`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${tokens.access_token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('dashboard-message', 'Posts fetched!', 'success');
            const postsContainer = document.getElementById('posts-container');
            postsContainer.innerHTML = `<p>${data.message}</p>`;
        } else {
            showMessage('dashboard-message', data.detail || 'Failed to fetch posts', 'error');
        }
    } catch (error) {
        showMessage('dashboard-message', 'Error: ' + error.message, 'error');
    }
}

// Logout
function logout() {
    tokens.access_token = null;
    tokens.refresh_token = null;

    document.getElementById('dashboard').classList.add('hidden');
    document.getElementById('login-form').classList.remove('hidden');

    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';

    showMessage('login-message', 'Logged out successfully', 'success');
}

// Parse JWT token to get user info
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (error) {
        console.error('Error parsing token:', error);
        return {};
    }
}