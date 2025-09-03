document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('authToken');
    if (!token) {
        window.location.href = '/';
        return;
    }

    const userInfoSpan = document.getElementById('user-info');
    const proposalsContainer = document.getElementById('proposals-container');
    const availableObservationsColumn = document.querySelector('#available-observations-column .observation-list-container');
    
    let allObservations = [];
    let myProposals = [];
    let currentUser = null;
    let currentPeriod = null; // We'll need to know the current period

    // --- 1. DATA FETCHING ---
    // First, get the current user's info
    fetch('/api/accounts/me/', { headers: { 'Authorization': `Token ${token}` } })
        .then(res => res.json())
        .then(user => {
            currentUser = user;
            userInfoSpan.textContent = `Welcome, ${user.username}`;
            // For now, we assume we are working in the first period.
            // A real implementation would have a way to select the active period.
            currentPeriod = 1; 
            return Promise.all([
                fetch(`/api/observations/admin/?period=${currentPeriod}`, { headers: { 'Authorization': `Token ${token}` } }).then(res => res.json()),
                fetch(`/api/proposals/?period=${currentPeriod}`, { headers: { 'Authorization': `Token ${token}` } }).then(res => res.json())
            ]);
        })
        .then(([obsData, proposalData]) => {
            // Filter for approved observations
            allObservations = obsData.filter(obs => obs.status === 'APPROVED');
            // We only want proposals created by the current user for the current period
            myProposals = proposalData.filter(p => p.proposer.id === currentUser.id);
            renderBoard();
        })
        .catch(error => console.error("Error fetching initial data:", error));

    // --- 2. RENDERING LOGIC ---
    function renderBoard() {
        availableObservationsColumn.innerHTML = '';
        document.querySelectorAll('.cluster-column.proposal').forEach(col => col.remove());

        myProposals.forEach(proposal => {
            const proposalCol = createProposalColumn(proposal);
            proposalsContainer.prepend(proposalCol);
        });
        
        const assignedObsIds = new Set();
        myProposals.forEach(proposal => {
            proposal.observations.forEach(obsId => assignedObsIds.add(obsId));
        });

        allObservations.forEach(obs => {
            if (!assignedObsIds.has(obs.id)) {
                const obsCard = createObservationCard(obs);
                availableObservationsColumn.appendChild(obsCard);
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
            container.addEventListener('dragover', e => {
                e.preventDefault();
            });

            container.addEventListener('drop', e => {
                e.preventDefault();
                const observationId = e.dataTransfer.getData('text/plain');
                const proposalId = container.parentElement.dataset.proposalId;
                const card = document.querySelector(`.observation-card[data-observation-id='${observationId}']`);
                container.appendChild(card);
                updateProposalObservations(observationId, proposalId, container.parentElement.id === 'available-observations-column');
            });
        });
    }

    async function updateProposalObservations(observationId, proposalId, movedToAvailable) {
        let proposalToUpdate = myProposals.find(p => p.id == proposalId);
        
        // Find all proposals this observation is in
        myProposals.forEach(p => {
            const index = p.observations.indexOf(parseInt(observationId));
            if (index > -1) {
                p.observations.splice(index, 1);
            }
        });

        // Add to the new proposal if it's not the "available" column
        if (!movedToAvailable && proposalToUpdate) {
            proposalToUpdate.observations.push(parseInt(observationId));
        }
        
        // We need to send PATCH requests to all affected proposals
        const updatePromises = myProposals.map(p => {
            return fetch(`/api/proposals/${p.id}/`, {
                method: 'PATCH',
                headers: { 'Authorization': `Token ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ observations: p.observations }),
            });
        });

        try {
            await Promise.all(updatePromises);
        } catch (error) {
            console.error("Failed to update one or more proposals", error);
            alert("An error occurred. The board will be refreshed to the last saved state.");
            // Refetch all data to revert UI on error
            Promise.all([
                fetch(`/api/observations/admin/?period=${currentPeriod}`, { headers: { 'Authorization': `Token ${token}` } }).then(res => res.json()),
                fetch(`/api/proposals/?period=${currentPeriod}`, { headers: { 'Authorization': `Token ${token}` } }).then(res => res.json())
            ]).then(([obsData, proposalData]) => {
                allObservations = obsData.filter(obs => obs.status === 'APPROVED' && obs.final_clusters.length === 0);
                myProposals = proposalData.filter(p => p.proposer.id === currentUser.id);
                renderBoard();
            });
        }
    }
    
    // --- 4. MODAL LOGIC ---
    const modal = document.getElementById('add-proposal-modal');
    const addProposalBtn = document.getElementById('add-proposal-btn');
    const closeBtn = document.querySelector('.close-button');
    const addProposalForm = document.getElementById('add-proposal-form');

    if(addProposalBtn) addProposalBtn.onclick = () => modal.classList.remove('hidden');
    if(closeBtn) closeBtn.onclick = () => modal.classList.add('hidden');
    window.onclick = (event) => {
        if (event.target == modal) modal.classList.add('hidden');
    };
    
    if(addProposalForm) addProposalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('proposal-name').value;
        const motivation = document.getElementById('proposal-motivation').value;
        const color = document.getElementById('proposal-color').value;

        try {
            const response = await fetch('/api/proposals/', {
                method: 'POST',
                headers: { 'Authorization': `Token ${token}`, 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, motivation, color, period: currentPeriod })
            });
            if (!response.ok) throw new Error('Failed to create proposal');
            const newProposal = await response.json();
            myProposals.push(newProposal);
            renderBoard();
            modal.classList.add('hidden');
            addProposalForm.reset();
        } catch(error) {
            console.error(error);
            alert('Failed to create proposal.');
        }
    });
});

