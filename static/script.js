// Global variable to store parsed criteria data
let parsedCriteria = [];
let screeningInProgress = false;

// Load config when page loads
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/get_config');
        if (!response.ok) {
            throw new Error('Failed to load configuration');
        }
        const config = await response.json();
        
        // Populate form fields with config values
        if (config.model_to_use) {
            document.getElementById('aiModel').value = config.model_to_use;
            showApiFields(config.model_to_use);
        }
        
        if (config.n_agents) {
            document.getElementById('numAgents').value = config.n_agents;
        }
        
        // Load criteria if available
        const criteriaList = document.getElementById('criteriaList');
        criteriaList.innerHTML = ''; // Clear default criteria
        
        if (config.criteria && config.criteria.length > 0) {
            config.criteria.forEach(criterion => {
                const li = document.createElement('li');
                li.className = 'criteria-item';
                li.innerHTML = `
                    <input type="text" class="criteria-input" placeholder="Enter screening criterion" required value="${criterion}">
                    <button type="button" class="remove-criteria" onclick="removeCriteria(this)">Remove</button>
                `;
                criteriaList.appendChild(li);
            });
        } else {
            // Add one empty criterion field if none exist
            addCriteria();
        }
        
    } catch (error) {
        console.error('Error loading config:', error);
        // Add one empty criterion field if config load fails
        addCriteria();
    }
});

function showApiFields(model) {
    // Hide all fields first
    document.querySelector('.google-fields').style.display = 'none';
    document.querySelector('.groq-fields').style.display = 'none';
    document.querySelector('.anthropic-fields').style.display = 'none';
    document.querySelector('.aws-fields').style.display = 'none';
    document.querySelector('.openai-fields').style.display = 'none';

    // Show relevant fields based on selection
    if (model === 'gemini') {
        document.querySelector('.google-fields').style.display = 'block';
    } else if (model === 'mixtral' || model === 'llama3' || model === 'gemma2') {
        document.querySelector('.groq-fields').style.display = 'block';
    } else if (model === 'claude') {
        document.querySelector('.anthropic-fields').style.display = 'block';
    } else if (model === 'aws_claude') {
        document.querySelector('.aws-fields').style.display = 'block';
    } else if (model === 'openai') {
        document.querySelector('.openai-fields').style.display = 'block';
    }
}

document.getElementById('aiModel').addEventListener('change', function(e) {
    showApiFields(e.target.value);
});

function addCriteria() {
    const list = document.getElementById('criteriaList');
    const li = document.createElement('li');
    li.className = 'criteria-item';
    li.innerHTML = `
        <input type="text" class="criteria-input" placeholder="Enter screening criterion" required>
        <button type="button" class="remove-criteria" onclick="removeCriteria(this)">Remove</button>
    `;
    list.appendChild(li);
}

function removeCriteria(button) {
    const list = document.getElementById('criteriaList');
    if (list.children.length > 1) {
        button.parentElement.remove();
    }
}

function showStatus(message, isError = false) {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = 'status ' + (isError ? 'error' : 'success');
}

document.getElementById('screeningForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Processing...';
    
    const formData = new FormData(e.target);
    
    // Include parsed criteria data if available, otherwise use manually entered criteria
    if (parsedCriteria.length > 0) {
        formData.append('criteria', JSON.stringify(parsedCriteria));
    } else {
        const manualCriteria = Array.from(document.querySelectorAll('.criteria-input')).map(input => input.value);
        formData.append('criteria', JSON.stringify(manualCriteria));
    }

    // Add pilot screen percentage to form data
    const pilotPercentage = document.getElementById('pilotPercentage').value;
    formData.append('pilot_percentage', pilotPercentage);

    try {
        const response = await fetch('/screen', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus('Screening process started successfully! Check the output folder for results.');
            screeningInProgress = true;
            document.getElementById('screeningProgress').style.display = 'block';
            fetchScreeningProgress();
        } else {
            showStatus(data.error || 'Error starting screening process', true);
        }
    } catch (error) {
        console.error('Error:', error);
        showStatus('Error submitting form: ' + error.message, true);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Start Screening';
    }
});

// Updated function to handle template file upload
function handleTemplateUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const data = new Uint8Array(e.target.result);
            const workbook = XLSX.read(data, {type: 'array'});
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            const jsonData = XLSX.utils.sheet_to_json(worksheet, {header: 1});
            
            // Clear existing criteria
            const criteriaList = document.getElementById('criteriaList');
            criteriaList.innerHTML = '';

            // Reset parsed criteria
            parsedCriteria = [];

            // Populate criteria from the uploaded template
            jsonData.forEach((row, index) => {
                if (index === 0) return; // Skip header row
                const criteriaType = row[0];
                const included = row[1];
                const excluded = row[2];

                // Store parsed criteria
                parsedCriteria.push({
                    type: criteriaType,
                    included: included,
                    excluded: excluded
                });

                const li = document.createElement('li');
                li.className = 'criteria-item';
                li.innerHTML = `
                    <input type="text" class="criteria-input" value="${criteriaType}: Included - ${included}, Excluded - ${excluded}" required readonly>
                    <button type="button" class="remove-criteria" onclick="removeCriteria(this)" disabled>Remove</button>
                `;
                criteriaList.appendChild(li);
            });
        };
        reader.readAsArrayBuffer(file);
    }
}

// Add event listener for template file upload
document.getElementById('templateFile').addEventListener('change', handleTemplateUpload);

// New function to fetch and display screening progress
async function fetchScreeningProgress() {
    if (!screeningInProgress) return;

    try {
        const response = await fetch('/screening_progress');
        if (!response.ok) {
            throw new Error('Failed to fetch screening progress');
        }
        const progressData = await response.json();

        // Update the progress table
        const progressBody = document.getElementById('progressBody');
        progressBody.innerHTML = ''; // Clear existing rows

        progressData.forEach(paper => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${paper.paper_number}</td>
                <td>${paper.title}</td>
                <td>${paper.decision}</td>
            `;
            progressBody.appendChild(row);
        });

        // Check if screening is complete
        if (progressData.length > 0 && progressData[progressData.length - 1].decision === 'Complete') {
            screeningInProgress = false;
            showStatus('Screening process completed!');
        } else {
            // Schedule the next update
            setTimeout(fetchScreeningProgress, 5000); // Update every 5 seconds
        }
    } catch (error) {
        console.error('Error fetching screening progress:', error);
        showStatus('Error fetching screening progress: ' + error.message, true);
    }
}
