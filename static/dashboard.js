document.getElementById('logout-button').addEventListener('click', function() {
    // Clear the token from storage
    localStorage.removeItem('authToken');
    // Redirect back to the login page
    window.location.href = '/';
});