/*
   ReThread - Sustainable Fashion Analyzer
   JavaScript Frontend Logic
   
   This file handles all client-side interactions:
   - Form submission and validation
   - API calls to the backend
   - Dynamic result rendering
   - User interface interactions
*/

// ============================================================================
// DOM ELEMENTS - Cache frequently used DOM elements for performance
// ============================================================================

const materialForm = document.getElementById('materialForm');
const materialInput = document.getElementById('materialInput');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorContainer = document.getElementById('errorContainer');
const resultsSection = document.getElementById('resultsSection');
const analyzeAnotherBtn = document.getElementById('analyzeAnotherBtn');

// Navbar toggle elements
const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');

// Result display elements
const materialName = document.getElementById('materialName');
const sustainabilityRating = document.getElementById('sustainabilityRating');
const environmentalImpact = document.getElementById('environmentalImpact');
const waterUsage = document.getElementById('waterUsage');
const biodegradable = document.getElementById('biodegradable');
const alternativesList = document.getElementById('alternativesList');
const aiExplanationCard = document.getElementById('aiExplanationCard');
const aiExplanation = document.getElementById('aiExplanation');

// ============================================================================
// EVENT LISTENERS - Set up event handlers for user interactions
// ============================================================================

// Navbar toggle functionality
menu.addEventListener('click', function() {
    menu.classList.toggle('is-active');
    menuLinks.classList.toggle('active');
});

/**
 * Handle form submission
 * When user clicks "Analyze", this function:
 * 1. Prevents default form behavior
 * 2. Gets the material name from input
 * 3. Sends it to the backend
 * 4. Displays results
 */
materialForm.addEventListener('submit', function(event) {
    // Prevent the form from actually submitting
    event.preventDefault();
    
    // Call the analyze function to process the material
    analyzeMaterial();
});

/**
 * Handle "Analyze Another Material" button click
 * Resets the form and results to allow new analysis
 */
analyzeAnotherBtn.addEventListener('click', function() {
    // Clear the input field
    materialInput.value = '';
    
    // Hide the results section
    resultsSection.style.display = 'none';
    
    // Hide any error messages
    errorContainer.style.display = 'none';
    
    // Focus on the input field so user can type immediately
    materialInput.focus();
});

// ============================================================================
// MAIN FUNCTIONS
// ============================================================================

/**
 * Main function to analyze a material
 * Gets the material name, validates it, and sends it to the backend
 */
function analyzeMaterial() {
    // Get the material name and remove extra whitespace
    const material = materialInput.value.trim();
    
    // Validate that the input is not empty
    if (!material) {
        showError('Please enter a material name to analyze');
        return;
    }
    
    // Hide any previous error messages
    errorContainer.style.display = 'none';
    
    // Hide results section (will show again after API response)
    resultsSection.style.display = 'none';
    
    // Show loading spinner
    loadingSpinner.style.display = 'block';
    
    // Call the API and process the response
    fetchMaterialAnalysis(material);
}

/**
 * Fetch material analysis from the backend API
 * Sends a POST request to "/analyze" endpoint
 * 
 * @param {string} material - The material name to analyze
 */
async function fetchMaterialAnalysis(material) {
    try {
        // Create the request payload (JSON object with material name)
        const payload = {
            material: material
        };
        
        // Send POST request to the backend
        const response = await fetch('/analyze', {
            // Use POST method for sending data
            method: 'POST',
            // Specify that we're sending JSON
            headers: {
                'Content-Type': 'application/json'
            },
            // Convert the payload to JSON string
            body: JSON.stringify(payload)
        });
        
        // Parse the response as JSON
        const data = await response.json();
        
        // Hide loading spinner
        loadingSpinner.style.display = 'none';
        
        // Check if the request was successful
        if (response.ok && data.success) {
            // Display the results on the page
            displayResults(data);
        } else {
            // Show error message from API or generic error
            const errorMsg = data.error || 'An error occurred while analyzing the material';
            showError(errorMsg);
        }
        
    } catch (error) {
        // Hide loading spinner
        loadingSpinner.style.display = 'none';
        
        // Log the error to browser console for debugging
        console.error('Error:', error);
        
        // Show user-friendly error message
        showError('Failed to connect to the server. Please try again.');
    }
}

/**
 * Display the analysis results on the page
 * Takes the API response and renders all the material information
 * 
 * @param {object} data - The API response object containing material data
 */
function displayResults(data) {
    // Set the material name in the results
    materialName.textContent = data.material;
    
    // Display sustainability rating with appropriate styling
    sustainabilityRating.textContent = data.sustainability;
    // Add color class based on sustainability level (optional enhancement)
    sustainabilityRating.className = `result-value sustainability-${data.sustainability.toLowerCase().replace(' ', '-')}`;
    
    // Display environmental impact description
    environmentalImpact.textContent = data.impact;
    
    // Display water usage information
    waterUsage.textContent = data.water_usage;
    
    // Display biodegradability status
    biodegradable.textContent = data.biodegradable;
    
    // Display sustainable alternatives as clickable tags
    displayAlternatives(data.alternatives);
    
    // Display AI-generated explanation if available
    if (data.ai_explanation) {
        aiExplanation.textContent = data.ai_explanation;
        aiExplanationCard.style.display = 'block';
    } else {
        aiExplanationCard.style.display = 'none';
    }
    
    // Show the results section
    resultsSection.style.display = 'block';
    
    // Scroll to results so user can see them (smooth scroll)
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Display alternative materials as styled tags
 * Creates clickable elements for each alternative
 * 
 * @param {array} alternatives - Array of alternative material names
 */
function displayAlternatives(alternatives) {
    // Clear any previous alternatives
    alternativesList.innerHTML = '';
    
    // Check if there are any alternatives to display
    if (!alternatives || alternatives.length === 0) {
        alternativesList.innerHTML = '<p>No alternatives available</p>';
        return;
    }
    
    // Loop through each alternative and create a tag for it
    alternatives.forEach(alternative => {
        // Create a new div element for the tag
        const tag = document.createElement('div');
        
        // Add the 'alternative-tag' class for styling
        tag.className = 'alternative-tag';
        
        // Set the text content to the alternative name
        tag.textContent = alternative;
        
        // Add click handler so user can analyze the alternative
        tag.addEventListener('click', function() {
            // Set the input to the alternative material
            materialInput.value = alternative;
            
            // Automatically analyze it
            analyzeMaterial();
        });
        
        // Add the tag to the alternatives list container
        alternativesList.appendChild(tag);
    });
}

/**
 * Display an error message to the user
 * Shows a visible error message in the error container
 * 
 * @param {string} message - The error message to display
 */
function showError(message) {
    // Set the error message content
    errorContainer.textContent = message;
    
    // Make the error container visible
    errorContainer.style.display = 'block';
    
    // Scroll to the error so user notices it
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ============================================================================
// PAGE INITIALIZATION
// ============================================================================

/**
 * Initialize the page when it loads
 * Sets up the UI to be ready for user interaction
 */
function initializePage() {
    // Focus on the input field so user can start typing immediately
    materialInput.focus();
    
    // Log a welcome message to browser console (for debugging)
    console.log('🌿 ReThread - Sustainable Fashion Analyzer loaded successfully!');
    console.log('Ready to analyze materials. Enter a fabric name to get started.');
}

/**
 * Run initialization when the DOM is ready
 * The 'DOMContentLoaded' event fires after the entire HTML is loaded
 */
document.addEventListener('DOMContentLoaded', initializePage);

// ============================================================================
// ADDITIONAL FEATURES (Optional Enhancements for Later)
// ============================================================================

/**
 * Optional: Add keyboard shortcuts
 * Allow users to press Enter to analyze (already works with form submission)
 * Allow users to press Escape to clear the form
 */
document.addEventListener('keydown', function(event) {
    // If user presses Escape, clear the form
    if (event.key === 'Escape' || event.key === 'Esc') {
        materialInput.value = '';
        materialInput.focus();
        errorContainer.style.display = 'none';
    }
});

/**
 * Optional: Auto-focus feature
 * If the page is not focused, remind user with a subtle change
 */
window.addEventListener('focus', function() {
    // Page regains focus - you could add a visual indicator here
    console.log('Welcome back to ReThread!');
});

// ============================================================================
// DEBUGGING HELPER FUNCTION
// ============================================================================

/**
 * Helper function for testing the API connection
 * Call this in the browser console: testAPIConnection()
 * 
 * Uncomment this section during development to test the API
 */
/*
function testAPIConnection() {
    console.log('Testing API connection...');
    
    const testMaterial = 'hemp';
    
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ material: testMaterial })
    })
    .then(response => response.json())
    .then(data => {
        console.log('API Response:', data);
        if (data.success) {
            console.log('✅ API connection successful!');
        }
    })
    .catch(error => {
        console.error('❌ API connection failed:', error);
    });
}
*/
