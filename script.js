let ws;

function showSignup() {
    document.getElementById('loginPage').classList.add('hidden');
    document.getElementById('signupPage').classList.remove('hidden');
}

function showLogin() {
    document.getElementById('signupPage').classList.add('hidden');
    document.getElementById('loginPage').classList.remove('hidden');
}

function loginUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Basic validation (you should use HTTPS and proper server-side validation in production)
    if (!username || !password) {
        document.getElementById('loginMessage').textContent = 'Username and password are required.';
        return false;
    }
    fetch('http://localhost:8080/login', {
        method: 'POST',
        headers: {
            'content-type': 'application/json',
        },
        body: JSON.stringify({username, password},)
    })
        .then(response => {
            if (response.ok) {
                document.getElementById('loginMessage').textContent = '';
                document.getElementById('loginPage').classList.add('hidden');
                document.getElementById('chatPage').classList.remove('hidden');

                // Connect WebSocket after successful login
                ws = new WebSocket('ws://localhost:8080/ws');

                ws.onmessage = function (event) {
                    const messages = document.getElementById('messages');
                    const message = document.createElement('div');
                    message.textContent = event.data;
                    messages.appendChild(message);
                };

                return false; // Prevent form submission
            } else {
                throw new Error('Invalid username or password.');
            }
        })
        .catch(error => {
            document.getElementById('loginMessage').textContent = error.message;
            return false;
        });

    return false; // Prevent form submission
}

function signupUser() {
    const username = document.getElementById('signupUsername').value;
    const password = document.getElementById('signupPassword').value;

    // Basic validation (you should use HTTPS and proper server-side validation in production)
    if (!username || !password) {
        document.getElementById('signupMessage').textContent = 'Username and password are required.';
        return false;
    }
    fetch('http://localhost:8080/signup', {
        method: 'POST',
        headers: {
            'content-type': 'application/json',
        },
        body: JSON.stringify({username, password},)
    })
        .then(response => {
            if (response.ok) {
                document.getElementById('signupMessage').textContent = '';
                document.getElementById('signupPage').classList.add('hidden');
                document.getElementById('chatPage').classList.remove('hidden');

                // Connect WebSocket after successful sign-up (same as login)
                ws = new WebSocket('ws://localhost:8080/ws');

                ws.onmessage = function (event) {
                    const messages = document.getElementById('messages');
                    const message = document.createElement('div');
                    message.textContent = event.data;
                    messages.appendChild(message);
                };
                return false; // Prevent form submission
            }
            else {
                throw new Error('Invalid username or password.');
            }
        })
        .catch(error => {
            document.getElementById('signupMessage').textContent = error.message;
            return false;
        });
    return false;
}

function sendMessage() {
    const input = document.getElementById('messageInput');
    ws.send(input.value);
    input.value = '';
}

function logoutUser() {
    ws.close();
    document.getElementById('chatPage').classList.add('hidden');
    document.getElementById('loginPage').classList.remove('hidden');
}

