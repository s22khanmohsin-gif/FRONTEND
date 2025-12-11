let predictedRiskLevel = 1;

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const heightInput = document.getElementById('Height');
    const weightInput = document.getElementById('Weight');
    const bmiInput = document.getElementById('BMI');
    const modal = document.getElementById('resultModal');
    const closeModalBtn = document.querySelector('.close-modal');

    // Auto-calculate BMI
    function calculateBMI() {
        const heightCm = parseFloat(heightInput.value);
        const weightKg = parseFloat(weightInput.value);

        if (heightCm > 0 && weightKg > 0) {
            const heightM = heightCm / 100;
            const bmi = (weightKg / (heightM * heightM)).toFixed(2);
            bmiInput.value = bmi;
        } else {
            bmiInput.value = '';
        }
    }

    heightInput.addEventListener('input', calculateBMI);
    weightInput.addEventListener('input', calculateBMI);

    // Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
        submitBtn.disabled = true;

        // Collect data
        const formData = new FormData(form);
        const data = {};

        // Convert FormData to JSON object
        formData.forEach((value, key) => {
            // Handle checkboxes
            if (form.querySelector(`input[name="${key}"][type="checkbox"]`)) {
                data[key] = 1; // Checkbox checked = 1
            } else {
                data[key] = value;
            }
        });

        // Handle unchecked checkboxes (they don't appear in FormData)
        const checkboxes = form.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(cb => {
            if (!data.hasOwnProperty(cb.name)) {
                data[cb.name] = 0;
            }
        });

        console.log("Sending data:", data);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            showResult(result);

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during analysis. Please try again.');
        } finally {
            submitBtn.innerHTML = originalBtnText;
            submitBtn.disabled = false;
        }
    });

    function showResult(result) {
        const riskLevelEl = document.getElementById('riskLevel');
        const riskIconEl = document.getElementById('riskIcon');
        const probFill = document.getElementById('probFill');
        const probValue = document.getElementById('probValue');

        // Update global variable for recommendation redirection
        predictedRiskLevel = result.risk_level;

        const probability = result.probability;
        const percentage = (probability * 100).toFixed(1) + '%';
        
        // Update Modal UI based on Risk Level (1-5)
        let colorStart, colorEnd, iconClass, text;

        if (predictedRiskLevel <= 2) {
            // Low Risk (Level 1-2)
            text = 'Low Risk';
            iconClass = 'fa-heart-circle-check risk-low';
            colorStart = '#34D399'; // Emerald 400
            colorEnd = '#10B981';   // Emerald 500
            riskLevelEl.style.color = '#10B981';
        } else if (predictedRiskLevel === 3) {
            // Moderate Risk
            text = 'Moderate Risk';
            iconClass = 'fa-heart-circle-exclamation'; // Orange warning
            colorStart = '#FBBF24'; // Amber 400
            colorEnd = '#F59E0B';   // Amber 500
            riskLevelEl.style.color = '#F59E0B';
            riskIconEl.innerHTML = `<i class="fa-solid ${iconClass}" style="color: #F59E0B"></i>`;
        } else {
            // High Risk (Level 4-5)
            text = 'High Risk';
            iconClass = 'fa-heart-crack risk-high';
            colorStart = '#F87171'; // Red 400
            colorEnd = '#EF4444';   // Red 500
            riskLevelEl.style.color = '#EF4444';
        }

        riskLevelEl.textContent = text;
        if(predictedRiskLevel !== 3) {
            // Re-apply classes for non-custom styled icons
             riskLevelEl.className = predictedRiskLevel <= 2 ? 'risk-low' : 'risk-high';
             riskIconEl.innerHTML = `<i class="fa-solid ${iconClass}"></i>`;
        }
        
        probFill.style.background = `linear-gradient(90deg, ${colorStart}, ${colorEnd})`;
        probFill.style.width = percentage;
        probValue.textContent = percentage;

        modal.classList.add('visible');
    }

    // Modal closing
    function closeModal() {
        modal.classList.remove('visible');
    }

    closeModalBtn.addEventListener('click', closeModal);
    window.onclick = function (event) {
        if (event.target == modal) {
            closeModal();
        }
    }
    
    // smooth scroll to sections
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const targetElement = document.querySelector(targetId);
            if(targetElement){
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Expose to window for button onclick
    window.closeModal = closeModal;
});

// Outside of DOMContentLoaded to be accessible by inline onclick
function goToRecommendations() {
    window.location.href = "/recommendation/" + predictedRiskLevel;
}
