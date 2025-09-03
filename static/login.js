document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    const username = this.username.value;
    const password = this.password.value;
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = ''; // Clear previous errors

    try {
        const response = await fetch('/api/auth/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (response.ok) {
            // Login successful
            console.log('Login successful:', data);
            localStorage.setItem('authToken', data.key); // Store the token
            // Redirect to a new page (we'll create this next)
            window.location.href = '/dashboard/'; 
        } else {
            // Handle login errors (e.g., wrong password)
            errorMessage.textContent = 'Login failed. Please check your credentials.';
            console.error('Login failed:', data);
        }
    } catch (error) {
        errorMessage.textContent = 'An error occurred. Please try again.';
        console.error('Network or other error:', error);
    }
});