document.addEventListener('DOMContentLoaded', () => {
    // API Base URL - update this based on environment
    // Use relative path for production (Docker Compose networking) or localhost for dev
    const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:';
    const API_URL = isLocal ? 'http://localhost:5002/api' : '/api';

    // DOM Elements
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');
    const apiStatusText = document.getElementById('api-status-text');
    const statusIndicator = document.querySelector('.status-indicator');

    // Form Elements
    const diagnosisForm = document.getElementById('diagnosis-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.spinner');

    // Result Elements
    const resultContainer = document.getElementById('result-container');
    const resultDate = document.getElementById('result-date');
    const aiResponseContent = document.getElementById('ai-response-content');

    // History Elements
    const historyTableBody = document.getElementById('history-table-body');
    const modal = document.getElementById('history-modal');
    const modalCloseBtn = document.querySelector('.close-btn');
    const modalBodyContent = document.getElementById('modal-body-content');

    // Global state
    let consultationHistory = [];

    // Initialize
    checkApiStatus();
    setupNavigation();
    setupForm();
    setupModal();

    // 1. Navigation Logic
    function setupNavigation() {
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                // Remove active class from all
                navItems.forEach(nav => nav.classList.remove('active'));
                sections.forEach(sec => sec.classList.remove('active'));

                // Add active to clicked
                item.classList.add('active');
                const targetId = item.getAttribute('data-target');
                document.getElementById(targetId).classList.add('active');

                // If history section clicked, fetch data
                if (targetId === 'history-section') {
                    fetchHistory();
                }
            });
        });
    }

    // 2. Health Check
    async function checkApiStatus() {
        try {
            const res = await fetch(`${API_URL}/health`);
            if (res.ok) {
                statusIndicator.className = 'status-indicator online';
                apiStatusText.textContent = 'API Online';
            } else {
                throw new Error('API not ok');
            }
        } catch (error) {
            statusIndicator.className = 'status-indicator offline';
            apiStatusText.textContent = 'API Offline';
            console.error('Health check failed:', error);
        }
    }

    // 3. Form Submission
    function setupForm() {
        diagnosisForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const patientName = document.getElementById('patientName').value;
            const patientAge = parseInt(document.getElementById('patientAge').value);
            const symptoms = document.getElementById('symptoms').value;

            // UI Loading state
            setLoading(true);
            resultContainer.classList.add('hidden');

            try {
                const response = await fetch(`${API_URL}/diagnose`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        patient_name: patientName,
                        patient_age: patientAge,
                        symptoms: symptoms
                    })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Failed to generate diagnosis');
                }

                // Render Success
                renderDiagnosisResult(data.data);
                diagnosisForm.reset();

            } catch (error) {
                alert(`Error: ${error.message}`);
                console.error(error);
            } finally {
                setLoading(false);
            }
        });
    }

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        if (isLoading) {
            btnText.classList.add('hidden');
            spinner.classList.remove('hidden');
        } else {
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
        }
    }

    function renderDiagnosisResult(data) {
        resultContainer.classList.remove('hidden');

        const date = data.created_at ? new Date(data.created_at).toLocaleString() : new Date().toLocaleString();
        resultDate.textContent = date;

        // Parse markdown from Gemini
        aiResponseContent.innerHTML = marked.parse(data.ai_analysis);

        // Smooth scroll to results
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // 4. History Fetching & Rendering
    async function fetchHistory() {
        try {
            historyTableBody.innerHTML = `<tr><td colspan="5" class="text-center">Loading history...</td></tr>`;

            const res = await fetch(`${API_URL}/history`);
            const data = await res.json();

            if (!res.ok) throw new Error(data.error || 'Failed to fetch');

            consultationHistory = data.data;
            renderHistoryTable(consultationHistory);

        } catch (error) {
            historyTableBody.innerHTML = `<tr><td colspan="5" class="text-center" style="color: var(--danger)">Error loading history: ${error.message}</td></tr>`;
        }
    }

    function renderHistoryTable(records) {
        if (!records || records.length === 0) {
            historyTableBody.innerHTML = `<tr><td colspan="5" class="text-center">No consultation history found.</td></tr>`;
            return;
        }

        historyTableBody.innerHTML = '';
        records.forEach(record => {
            // Jika data item rusak/null, lewati agar loop tidak crash di tengah jalan
            if (!record) return;

            const tr = document.createElement('tr');

            // 1. Amankan penanganan tanggal agar tidak corrupt/invalid
            const dateObj = record.created_at ? new Date(record.created_at) : new Date();
            const date = isNaN(dateObj.getTime()) ? 'No Date' : dateObj.toLocaleDateString();

            // 2. Berikan fallback string kosong jika ada field yang bernilai null
            const pName = record.patient_name || 'Unknown';
            const pAge = record.patient_age || '-';
            const pSymptoms = record.symptoms || 'No symptoms reported';
            const rId = record.id || 0;

            tr.innerHTML = `
                <td>${date}</td>
                <td>${pName}</td>
                <td>${pAge}</td>
                <td><div class="text-truncate" title="${pSymptoms}">${pSymptoms}</div></td>
                <td>
                    <button class="btn btn-small view-btn" data-id="${rId}">View Details</button>
                </td>
            `;
            historyTableBody.appendChild(tr);
        });

        // Pasang ulang event listener untuk tombol view detail di setiap baris
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.target.getAttribute('data-id'));
                const record = consultationHistory.find(r => r.id === id);
                if (record) openModal(record);
            });
        });
    }

    // 5. Modal Logic
    function setupModal() {
        modalCloseBtn.addEventListener('click', () => {
            modal.classList.add('hidden');
        });

        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });
    }

    function openModal(record) {
        const date = new Date(record.created_at).toLocaleString();

        modalBodyContent.innerHTML = `
            <div style="margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid var(--surface-border);">
                <p><strong>Patient:</strong> ${record.patient_name} (Age: ${record.patient_age})</p>
                <p><strong>Date:</strong> ${date}</p>
            </div>
            <div style="margin-bottom: 1.5rem;">
                <h4 style="margin-bottom: 0.5rem;">Reported Symptoms:</h4>
                <p style="color: var(--text-muted); background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 8px;">${record.symptoms}</p>
            </div>
            <div>
                <h4 style="margin-bottom: 0.5rem;">AI Analysis:</h4>
                <div class="markdown-body" style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 8px;">
                    ${marked.parse(record.ai_analysis)}
                </div>
            </div>
        `;

        modal.classList.remove('hidden');
    }
});
