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
// DARK MODE TOGGLE - Handle dark mode preferences
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    // Check if dark mode preference is saved in localStorage
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        updateDarkModeIcon();
    }
    
    // Toggle dark mode when button is clicked
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const isNowDarkMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', isNowDarkMode);
            updateDarkModeIcon();
        });
    }
    
    // Update icon based on current mode
    function updateDarkModeIcon() {
        const icon = darkModeToggle.querySelector('i');
        if (document.body.classList.contains('dark-mode')) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }
});

// ============================================================================
// DOM ELEMENTS - Cache frequently used DOM elements for performance
// ============================================================================

// Single Material Analysis Elements
const materialForm = document.getElementById('materialForm');
const materialInput = document.getElementById('materialInput');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorContainer = document.getElementById('errorContainer');
const resultsSection = document.getElementById('resultsSection');
const analyzeAnotherBtn = document.getElementById('analyzeAnotherBtn');

// Result display elements for single material
const materialName = document.getElementById('materialName');
const sustainabilityRating = document.getElementById('sustainabilityRating');
const environmentalImpact = document.getElementById('environmentalImpact');
const waterUsage = document.getElementById('waterUsage');
const biodegradable = document.getElementById('biodegradable');
const alternativesList = document.getElementById('alternativesList');
const aiExplanationCard = document.getElementById('aiExplanationCard');
const aiExplanation = document.getElementById('aiExplanation');

// Fabric Composition Analysis Elements
const compositionForm = document.getElementById('compositionForm');
const compositionInput = document.getElementById('compositionInput');
const compositionLoadingSpinner = document.getElementById('compositionLoadingSpinner');
const compositionErrorContainer = document.getElementById('compositionErrorContainer');
const compositionResultsSection = document.getElementById('compositionResultsSection');
const analyzeAnotherCompositionBtn = document.getElementById('analyzeAnotherCompositionBtn');

// Composition result display elements
const compositionTitle = document.getElementById('compositionTitle');
const compositionRating = document.getElementById('compositionRating');
const compositionAnalysis = document.getElementById('compositionAnalysis');
const compositionAICard = document.getElementById('compositionAICard');
const compositionAIAnalysis = document.getElementById('compositionAIAnalysis');

// ============================================================================
// EVENT LISTENERS - Set up event handlers for user interactions
// ============================================================================

/**
 * Handle single material form submission
 * Prevents default form behavior and calls analyzeMaterial()
 */
if (materialForm) {
    materialForm.addEventListener('submit', function(event) {
        // Prevent the form from actually submitting
        event.preventDefault();
        
        // Call the analyze function to process the material
        analyzeMaterial();
    });
} else {
    console.error('❌ materialForm not found in DOM');
}

/**
 * Handle "Analyze Another Material" button click
 * Resets the form and results to allow new analysis
 */
if (analyzeAnotherBtn) {
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
} else {
    console.warn('⚠️ analyzeAnotherBtn not found - "Analyze Another" button will not work');
}

/**
 * Handle fabric composition form submission
 * When user clicks "Analyze Composition", this function:
 * 1. Prevents default form behavior
 * 2. Gets the composition input
 * 3. Validates the input
 * 4. Sends it to the backend
 * 5. Displays results
 */
if (compositionForm) {
    compositionForm.addEventListener('submit', function(event) {
        // Prevent the form from actually submitting
        event.preventDefault();
        
        // Call the analyze function to process the composition
        analyzeComposition();
    });
} else {
    console.error('❌ compositionForm not found in DOM');
}

/**
 * Handle "Analyze Another Composition" button click
 * Resets the form and results to allow new analysis
 */
if (analyzeAnotherCompositionBtn) {
    analyzeAnotherCompositionBtn.addEventListener('click', function() {
        // Clear the input field
        compositionInput.value = '';
        
        // Hide the results section
        compositionResultsSection.style.display = 'none';
        
        // Hide any error messages
        compositionErrorContainer.textContent = '';
        
        // Focus on the input field so user can type immediately
        compositionInput.focus();
    });
}

// ============================================================================
// MAIN FUNCTIONS
// ============================================================================

/**
 * Main function to analyze a material
 * Gets the material name, validates it, and sends it to the backend
 */
function analyzeMaterial() {
    console.log('📊 analyzeMaterial() called');
    
    // Get the material name and remove extra whitespace
    const material = materialInput.value.trim();
    console.log('  Material input:', material);
    
    // Validate that the input is not empty
    if (!material) {
        console.warn('⚠️ Material input is empty');
        showError('Please enter a material name to analyze');
        return;
    }
    
    console.log('✓ Validation passed, proceeding with analysis...');
    
    // Hide any previous error messages
    errorContainer.style.display = 'none';
    
    // Hide results section (will show again after API response)
    resultsSection.style.display = 'none';
    
    // Show loading spinner
    loadingSpinner.style.display = 'block';
    console.log('✓ Loading spinner shown');
    
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
        console.log('🔄 Fetching material analysis for:', material);
        
        // Create the request payload (JSON object with material name)
        const payload = {
            material: material
        };
        
        console.log('📤 Sending POST request to /analyze');
        
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
        
        console.log('📥 Received response, status:', response.status);
        
        // Parse the response as JSON
        const data = await response.json();
        
        // Hide loading spinner
        loadingSpinner.style.display = 'none';
        
        // Check if the request was successful
        if (response.ok && data.success) {
            console.log('✅ Analysis successful:', data);
            // Display the results on the page
            displayResults(data);
        } else {
            // Show error message from API or generic error
            const errorMsg = data.error || 'An error occurred while analyzing the material';
            console.error('❌ API error:', errorMsg);
            showError(errorMsg);
        }
        
    } catch (error) {
        // Hide loading spinner
        loadingSpinner.style.display = 'none';
        
        // Log the error to browser console for debugging
        console.error('❌ Network error:', error);
        
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
// FABRIC COMPOSITION ANALYSIS FUNCTIONS
// ============================================================================

/**
 * Main function to analyze a fabric composition
 * Gets the composition text, validates it, and sends it to the backend
 */
function analyzeComposition() {
    console.log('📊 analyzeComposition() called');
    
    // Get the composition text and remove extra whitespace
    const composition = compositionInput.value.trim();
    console.log('  Composition input:', composition);
    
    // Validate that the input is not empty
    if (!composition) {
        console.warn('⚠️ Composition input is empty');
        showCompositionError('Please enter a fabric composition to analyze');
        return;
    }
    
    console.log('✓ Validation passed, proceeding with analysis...');
    
    // Hide any previous error messages
    compositionErrorContainer.textContent = '';
    
    // Hide results section (will show again after API response)
    compositionResultsSection.style.display = 'none';
    
    // Show loading spinner
    compositionLoadingSpinner.style.display = 'block';
    console.log('✓ Loading spinner shown');
    
    // Call the API and process the response
    fetchCompositionAnalysis(composition);
}

/**
 * Fetch composition analysis from the backend API
 * Sends a POST request to "/analyze-composition" endpoint
 * 
 * @param {string} composition - The fabric composition to analyze (e.g., "50% cotton 50% polyester")
 */
async function fetchCompositionAnalysis(composition) {
    try {
        console.log('🔄 Fetching composition analysis for:', composition);
        
        // Create the request payload
        const payload = {
            composition: composition
        };
        
        console.log('📤 Sending POST request to /analyze-composition');
        
        // Send POST request to the backend
        const response = await fetch('/analyze-composition', {
            // Use POST method for sending data
            method: 'POST',
            // Specify that we're sending JSON
            headers: {
                'Content-Type': 'application/json'
            },
            // Convert the payload to JSON string
            body: JSON.stringify(payload)
        });
        
        console.log('📥 Received response, status:', response.status);
        
        // Parse the response as JSON
        const data = await response.json();
        
        // Hide loading spinner
        compositionLoadingSpinner.style.display = 'none';
        
        // Check if the request was successful
        if (response.ok && data.success) {
            console.log('✅ Analysis successful:', data);
            // Display the results on the page
            displayCompositionResults(data);
        } else {
            // Show error message from API or generic error
            const errorMsg = data.error || 'An error occurred while analyzing the composition';
            console.error('❌ API error:', errorMsg);
            showCompositionError(errorMsg);
        }
        
    } catch (error) {
        // Hide loading spinner
        compositionLoadingSpinner.style.display = 'none';
        
        // Log the error to browser console for debugging
        console.error('❌ Network error:', error);
        
        // Show user-friendly error message
        showCompositionError('Failed to connect to the server. Please try again.');
    }
}

/**
 * Display the composition analysis results on the page
 * Takes the API response and renders all the composition analysis information
 * 
 * @param {object} data - The API response object containing composition analysis
 */
function displayCompositionResults(data) {
    // Set the composition input in the results
    compositionTitle.textContent = `Analysis: ${data.composition}`;
    
    // Display sustainability rating
    compositionRating.textContent = data.sustainability_rating;
    // Add color class based on sustainability level
    compositionRating.className = `result-value sustainability-${data.sustainability_rating.toLowerCase().replace(' ', '-')}`;
    
    // Display the composition analysis explanation
    compositionAnalysis.textContent = data.explanation;
    
    // Display AI-generated analysis if available
    if (data.ai_analysis) {
        compositionAIAnalysis.textContent = data.ai_analysis;
        compositionAICard.style.display = 'block';
    } else {
        compositionAICard.style.display = 'none';
    }
    
    // Show the results section
    compositionResultsSection.style.display = 'block';
    
    // Scroll to results so user can see them
    compositionResultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Display a composition error message to the user
 * Shows a visible error message in the composition error container
 * 
 * @param {string} message - The error message to display
 */
function showCompositionError(message) {
    // Set the error message content
    compositionErrorContainer.textContent = message;
    
    // Make the error container visible
    compositionErrorContainer.style.display = 'block';
    
    // Scroll to the error so user notices it
    compositionErrorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ============================================================================
// PAGE INITIALIZATION
// ============================================================================

/**
 * Initialize the page when it loads
 * Sets up the UI to be ready for user interaction
 */
function initializePage() {
    console.log('🌿 ReThread - Sustainable Fashion Analyzer initializing...');
    
    // Debug: Log which elements were found
    console.log('✓ DOM Elements Status:');
    console.log('  Material Form:', materialForm ? '✅ Found' : '❌ NOT FOUND');
    console.log('  Material Input:', materialInput ? '✅ Found' : '❌ NOT FOUND');
    console.log('  Composition Form:', compositionForm ? '✅ Found' : '❌ NOT FOUND');
    console.log('  Composition Input:', compositionInput ? '✅ Found' : '❌ NOT FOUND');
    console.log('  Loading Spinner:', loadingSpinner ? '✅ Found' : '❌ NOT FOUND');
    console.log('  Composition Loading Spinner:', compositionLoadingSpinner ? '✅ Found' : '❌ NOT FOUND');
    
    // Only focus if materialInput exists
    if (materialInput) {
        materialInput.focus();
        console.log('✅ Focus set to material input field');
    } else {
        console.error('❌ Cannot set focus - materialInput not found');
    }
    
    console.log('🌿 ReThread loaded successfully!');
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
