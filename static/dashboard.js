document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('authToken');
    if (!token) {
        window.location.href = '/';
        return;
    }

    const userInfoSpan = document.getElementById('user-info');
    const contributorView = document.getElementById('contributor-view');
    const adminView = document.getElementById('admin-view');
    const observationList = document.getElementById('observation-list');
    const observationForm = document.getElementById('observation-form');
    const logoutButton = document.getElementById('logout-button');

    fetch('/api/accounts/me/', {
        headers: { 'Authorization': `Token ${token}` }
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to fetch user data');
        return response.json();
    })
    .then(user => {
        userInfoSpan.textContent = `Welcome, ${user.username} (${user.role})`;
        if (user.role === 'CONTRIBUTOR') {
            contributorView.classList.remove('hidden');
            loadObservations(token);
        } else if (user.role === 'DB_ADMIN' || user.role === 'SUPER_ADMIN') {
            adminView.classList.remove('hidden');
        }
    })
    .catch(error => {
        console.error('Error fetching user data:', error);
        localStorage.removeItem('authToken');
        window.location.href = '/';
    });

    function loadObservations(token) {
        fetch('/api/observations/', {
            headers: { 'Authorization': `Token ${token}` }
        })
        .then(response => response.json())
        .then(data => {
            observationList.innerHTML = '';
            data.forEach(obs => {
                const obsDiv = document.createElement('div');
                obsDiv.className = 'observation-item';
                
                // --- MODIFIED LOGIC HERE ---
                // Start building the HTML for the observation
                let obsHTML = `
                    <h4>${obs.title}</h4>
                    <p>${obs.interest_reason}</p>
                    <small>Status: ${obs.status}</small>
                `;
                
                // If a file was uploaded, add a link to it
                if (obs.source_file) {
                    obsHTML += `<br><a href="${obs.source_file}" target="_blank">View Uploaded File</a>`;
                }
                
                obsDiv.innerHTML = obsHTML;
                observationList.appendChild(obsDiv);
            });
        });
    }

    if (observationForm) {
        observationForm.addEventListener('submit', (event) => {
            event.preventDefault();
            
            const formData = new FormData();
            formData.append('title', document.getElementById('title').value);
            formData.append('interest_reason', document.getElementById('interest_reason').value);
            formData.append('source_link', document.getElementById('source_link').value);
            formData.append('tags', document.getElementById('tags').value);

            const fileInput = document.getElementById('source_file');
            if (fileInput.files.length > 0) {
                formData.append('source_file', fileInput.files[0]);
            }

            fetch('/api/observations/', {
                method: 'POST',
                headers: { 'Authorization': `Token ${token}` },
                body: formData,
            })
            .then(response => {
                if (response.ok) {
                    observationForm.reset();
                    loadObservations(token);
                } else {
                    alert('Failed to submit observation. Please check the console for errors.');
                    response.json().then(err => console.error('Submission Error:', err));
                }
            });
        });
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            localStorage.removeItem('authToken');
            window.location.href = '/';
        });
    }
});