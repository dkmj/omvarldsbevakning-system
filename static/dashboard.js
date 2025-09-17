document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    window.location.href = "/";
    return;
  }

  const userInfoSpan = document.getElementById("user-info");
  const contributorView = document.getElementById("contributor-view");
  const adminView = document.getElementById("admin-view");
  const participantView = document.getElementById("participant-view");
  const observationList = document.getElementById("observation-list");
  const observationForm = document.getElementById("observation-form");
  const logoutButton = document.getElementById("logout-button");

  Promise.all([
    fetch("/api/accounts/me/", {
      headers: { Authorization: `Token ${token}` },
    }).then((res) => {
      if (!res.ok) throw new Error("User fetch failed");
      return res.json();
    }),
    fetch("/api/periods/", {
      headers: { Authorization: `Token ${token}` },
    }).then((res) => {
        if (!res.ok) throw new Error("Periods fetch failed");
        return res.json();
    }),
  ])
    .then(([user, periodsData]) => {
      const periods = periodsData.results || periodsData;
      userInfoSpan.textContent = `Welcome, ${user.username} (${user.role})`;

      // --- CORRECTED LOGIC HERE ---
      // A user is a participant if they are in a period that is either
      // in the CLUSTERING or MEETING phase.
      const isParticipant = periods.some(
        (period) =>
          (period.status === "CLUSTERING" || period.status === "MEETING") &&
          period.participants.includes(user.id)
      );
      
      const isAdmin = user.role === "DB_ADMIN" || user.role === "SUPER_ADMIN";

      if (isAdmin) {
          adminView.classList.remove("hidden");
      }
      if (isParticipant) {
          participantView.classList.remove("hidden");
      }
      if (user.role === "CONTRIBUTOR") {
          contributorView.classList.remove("hidden");
      }
      
      loadObservations(token);
    })
    .catch((error) => {
        console.error("Error fetching initial data:", error);
        localStorage.removeItem('authToken');
        window.location.href = '/';
    });


  function loadObservations(token) {
    fetch("/api/observations/", {
      headers: { Authorization: `Token ${token}` },
    })
      .then((response) => response.json())
      .then((data) => {
        const observations = data.results || data;
        observationList.innerHTML = "";
        observations.forEach((obs) => {
          const obsDiv = document.createElement("div");
          obsDiv.className = "observation-item";
          let obsHTML = `
              <h4>${obs.title}</h4>
              <p>${obs.interest_reason}</p>
              <small>Status: ${obs.status}</small>
          `;
          if (obs.source_file) {
              obsHTML += `<br><a href="${obs.source_file}" target="_blank">View Uploaded File</a>`;
          }
          obsDiv.innerHTML = obsHTML;
          observationList.appendChild(obsDiv);
        });
      });
  }

  if (observationForm) {
      observationForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const formData = new FormData();
      formData.append("title", document.getElementById("title").value);
      formData.append("interest_reason", document.getElementById("interest_reason").value);
      formData.append("source_link", document.getElementById("source_link").value);
      formData.append("tags", document.getElementById("tags").value);
      
      const fileInput = document.getElementById("source_file");
      if (fileInput.files.length > 0) {
        formData.append("source_file", fileInput.files[0]);
      }
      
      fetch("/api/periods/?status=OPEN", { headers: { Authorization: `Token ${token}` }})
         .then((res) => res.json())
         .then((openPeriodsData) => {
            const openPeriods = openPeriodsData.results || openPeriodsData;
           if (openPeriods.length === 0) {
             alert("There is no period currently open for submissions.");
             return;
           }
           formData.append("period", openPeriods[0].id);

           return fetch("/api/observations/", {
             method: "POST",
             headers: { Authorization: `Token ${token}` },
             body: formData,
           });
         })
        .then((response) => {
            if (response && response.ok) {
                observationForm.reset();
                loadObservations(token);
            } else if (response) {
                alert("Failed to submit observation.");
                response.json().then(err => console.error('Submission Error:', err));
            }
        });
    });
  }
  
  if (logoutButton) {
      logoutButton.addEventListener("click", () => {
      localStorage.removeItem("authToken");
      window.location.href = "/";
    });
  }
});

