document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("authToken");
    if (!token) {
        window.location.href = "/";
        return;
    }

    // --- DOM Element References ---
    const userInfoSpan = document.getElementById("user-info");
    const pageTitle = document.getElementById("page-title");
    const proposalsContainer = document.getElementById("proposals-container");
    const availableObservationsColumn = document.querySelector("#available-observations-column .observation-list-container");
    const modal = document.getElementById("add-proposal-modal");
    const addProposalBtn = document.getElementById("add-proposal-btn");
    const closeBtn = document.querySelector(".close-button");
    const addProposalForm = document.getElementById("add-proposal-form");

    // --- Global State ---
    let allObservations = [];
    let myProposals = [];
    let currentUser = null;
    let activePeriod = null;

    // --- 1. DATA FETCHING ---
    async function initializeBoard() {
        try {
            // Step 1: Get the current user
            const userRes = await fetch("/api/accounts/me/", { headers: { Authorization: `Token ${token}` } });
            if (!userRes.ok) throw new Error("Could not fetch user.");
            currentUser = await userRes.json();
            userInfoSpan.textContent = `Welcome, ${currentUser.username}`;

            // Step 2: Find the active period for clustering
            const periodsRes = await fetch("/api/periods/?status=CLUSTERING", { headers: { Authorization: `Token ${token}` } });
            if (!periodsRes.ok) throw new Error("Could not fetch periods.");
            const activePeriods = await periodsRes.json();
            
            if (activePeriods.length === 0) {
                document.querySelector('.clustering-board').innerHTML = "<h2>No period is currently open for clustering.</h2>";
                return;
            }
            activePeriod = activePeriods[0];
            pageTitle.textContent = `Clustering Preparation for ${activePeriod.name}`;

            // Step 3: Fetch all data needed for the board, using the active period ID
            const [obsData, proposalData] = await Promise.all([
                fetch(`/api/observations/participant/?period_id=${activePeriod.id}`, { headers: { Authorization: `Token ${token}` } }).then(res => res.json()),
                fetch(`/api/proposals/?period_id=${activePeriod.id}`, { headers: { Authorization: `Token ${token}` } }).then(res => res.json())
            ]);
            
            allObservations = obsData.results || obsData;
            myProposals = proposalData.results || proposalData;
            
            renderBoard();

        } catch (error) {
            console.error("Error initializing board:", error);
            document.querySelector('.clustering-board').innerHTML = `<h2>Error loading data. Please try again later.</h2><p>${error.message}</p>`;
        }
    }

    // --- 2. RENDERING LOGIC ---
    function renderBoard() {
        availableObservationsColumn.innerHTML = '';
        document.querySelectorAll('.cluster-column.proposal').forEach(col => col.remove());

        myProposals.forEach(proposal => {
            const proposalCol = createProposalColumn(proposal);
            proposalsContainer.prepend(proposalCol);
        });
        
        const assignedObsIds = new Set(myProposals.flatMap(p => p.observations));

        allObservations.forEach(obs => {
            if (!assignedObsIds.has(obs.id)) {
                availableObservationsColumn.appendChild(createObservationCard(obs));
            }
        });
        
        myProposals.forEach(proposal => {
            const proposalCol = document.querySelector(`[data-proposal-id='${proposal.id}'] .observation-list-container`);
            proposal.observations.forEach(obsId => {
                const observation = allObservations.find(o => o.id === obsId);
                if (observation) {
                     proposalCol.appendChild(createObservationCard(observation));
                }
            });
        });

        addDragAndDropListeners();
    }
    
    function createProposalColumn(proposal) {
        const col = document.createElement('div');
        col.className = 'cluster-column proposal';
        col.dataset.proposalId = proposal.id;
        col.innerHTML = `
            <h2 style="border-bottom-color: ${proposal.color};">${proposal.name}</h2>
            <div class="observation-list-container"></div>
        `;
        return col;
    }

    function createObservationCard(obs) {
        const card = document.createElement('div');
        card.className = 'observation-card';
        card.draggable = true;
        card.dataset.observationId = obs.id;
        card.innerHTML = `
            <h4>${obs.title}</h4>
            <p>${obs.interest_reason.substring(0, 100)}...</p>
            <small>By: ${obs.author.username}</small>
        `;
        return card;
    }
    
    // --- 3. DRAG AND DROP LOGIC ---
    function addDragAndDropListeners() {
        const cards = document.querySelectorAll('.observation-card');
        const containers = document.querySelectorAll('.observation-list-container');

        cards.forEach(card => {
            card.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', card.dataset.observationId);
                setTimeout(() => card.classList.add('dragging'), 0);
            });
            card.addEventListener('dragend', () => card.classList.remove('dragging'));
        });

        containers.forEach(container => {
            container.addEventListener('dragover', e => e.preventDefault());
            container.addEventListener('drop', e => {
                e.preventDefault();
                const observationId = e.dataTransfer.getData('text/plain');
                const proposalId = container.parentElement.dataset.proposalId;
                const card = document.querySelector(`[data-observation-id='${observationId}']`);
                container.appendChild(card);
                updateProposalObservations(observationId, proposalId);
            });
        });
    }

    async function updateProposalObservations(observationId, proposalId) {
        if (!proposalId) return; // Dropped in the 'available' column, no API call needed yet
        const proposal = myProposals.find(p => p.id == proposalId);
        let updatedObsIds = [...proposal.observations, parseInt(observationId)];
        
        try {
            await fetch(`/api/proposals/${proposalId}/`, {
                method: 'PATCH',
                headers: { 'Authorization': `Token ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ observations: updatedObsIds }),
            });
            initializeBoard(); // Refresh the whole board on success
        } catch (error) {
            console.error(error);
            alert("Failed to move observation. Reverting.");
            renderBoard();
        }
    }
    
    // --- 4. MODAL LOGIC ---
    addProposalBtn.onclick = () => modal.classList.remove('hidden');
    closeBtn.onclick = () => modal.classList.add('hidden');
    window.onclick = (event) => {
        if (event.target == modal) modal.classList.add('hidden');
    };
    
    addProposalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('proposal-name').value;
        const motivation = document.getElementById('proposal-motivation').value;
        const color = document.getElementById('proposal-color').value;

        try {
            const response = await fetch('/api/proposals/', {
                method: 'POST',
                headers: { 'Authorization': `Token ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, motivation, color, period: activePeriod.id })
            });
            if (!response.ok) throw new Error('Failed to create proposal');
            initializeBoard(); // Refresh board to show new proposal
            modal.classList.add('hidden');
            addProposalForm.reset();
        } catch(error) {
            console.error(error);
            alert('Failed to create proposal.');
        }
    });

    // --- Initial Load ---
    initializeBoard();
});

