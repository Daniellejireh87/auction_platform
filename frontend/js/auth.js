// Authentification - Register et Login

async function register() {
    const name = document.getElementById('reg_name').value;
    const email = document.getElementById('reg_email').value;
    const password = document.getElementById('reg_password').value;

    const res = await fetch('http://localhost:8011/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password })
    });

    const data = await res.json();
    alert(data.message || data.detail);
}


    const data = await res.json();
    alert(data.message || data.detail);

    if (res.ok) {
        window.location.href = "index.html"; // Redirection après inscription
    }


async function login() {
    const email = document.getElementById('login_email').value;
    const password = document.getElementById('login_password').value;

    const res = await fetch('http://localhost:8011/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (data.access_token) {
        localStorage.setItem('token', data.access_token);
        alert("Connexion réussie !");
        window.location.href = "create.html"; // Redirection après login
    } else {
        alert(data.detail || "Échec de la connexion");
    }
}
