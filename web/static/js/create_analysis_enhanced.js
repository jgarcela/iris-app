/**
 * Enhanced Create Analysis Page JavaScript
 * Handles mode selection, model selection, and form interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the enhanced create analysis page
    initializeCreateAnalysis();
});

function initializeCreateAnalysis() {
    // Set up mode selection
    setupModeSelection();
    
    // Set up model selection
    setupModelSelection();
    
    // Set up form interactions
    setupFormInteractions();
    
    // Set up quick actions
    setupQuickActions();
    
    // Initialize with automatic mode
    selectMode('automatic');
}

/**
 * Setup mode selection functionality
 */
function setupModeSelection() {
    const modeOptions = document.querySelectorAll('.mode-card-modern, .mode-option, .mode-card, .mode-card-compact');
    
    console.log('Found mode options:', modeOptions.length);
    
    modeOptions.forEach((option, index) => {
        console.log(`Option ${index}:`, option, 'data-mode:', option.dataset.mode);
        
        option.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const mode = this.dataset.mode;
            console.log('Mode option clicked:', mode);
            selectMode(mode);
        });
        
        // Add keyboard support
        option.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                e.stopPropagation();
                const mode = this.dataset.mode;
                console.log('Mode option key pressed:', mode);
                selectMode(mode);
            }
        });
        
        // Make options focusable
        option.setAttribute('tabindex', '0');
        option.setAttribute('role', 'button');
        option.setAttribute('aria-label', `Seleccionar análisis ${option.dataset.mode}`);
    });
}

/**
 * Select analysis mode and update UI
 */
function selectMode(mode) {
    console.log('selectMode called with:', mode);
    
    // Remove selected class from all options
    document.querySelectorAll('.mode-card-modern, .mode-option, .mode-card, .mode-card-compact').forEach(option => {
        option.classList.remove('selected');
        option.setAttribute('aria-pressed', 'false');
    });
    
    // Add selected class to clicked option
    const selectedOption = document.querySelector(`[data-mode="${mode}"]`);
    console.log('Selected option found:', selectedOption);
    
    if (selectedOption) {
        selectedOption.classList.add('selected');
        selectedOption.setAttribute('aria-pressed', 'true');
        console.log('Added selected class to:', selectedOption);
    } else {
        console.error('No option found with data-mode:', mode);
    }
    
    // Update hidden input
    const analysisModeInput = document.getElementById('analysis-mode');
    if (analysisModeInput) {
        analysisModeInput.value = mode;
    }
    
    // Update UI based on mode
    updateUIForMode(mode);
    
    // Update analysis info badge
    updateAnalysisInfo(mode);
    
    console.log(`Analysis mode changed to: ${mode}`);
}

/**
 * Update UI based on selected mode
 */
function updateUIForMode(mode) {
    const modelSelection = document.getElementById('model-selection');
    const analysisModeInfo = document.getElementById('analysis-mode-info');
    const modelInfo = document.getElementById('model-info');
    
    console.log('Updating UI for mode:', mode);
    
    if (mode === 'automatic') {
        // Show model selection for automatic mode
        if (modelSelection) {
            modelSelection.style.display = 'block';
            console.log('Showing model selection');
        }
        
        // Update analysis mode info
        if (analysisModeInfo) {
            analysisModeInfo.innerHTML = '<i class="fas fa-robot me-1"></i>Análisis Automático';
            analysisModeInfo.className = 'badge bg-primary me-2';
        }
        
        // Show model info
        if (modelInfo) {
            modelInfo.style.display = 'inline-flex';
        }
        
        // Update form action for automatic analysis
        const form = document.getElementById('analyzer-form');
        if (form) {
            form.action = '/analysis/analyze';
        }
        
    } else if (mode === 'manual') {
        // Hide model selection for manual mode
        if (modelSelection) {
            modelSelection.style.display = 'none';
            console.log('Hiding model selection');
        }
        
        // Update analysis mode info
        if (analysisModeInfo) {
            analysisModeInfo.innerHTML = '<i class="fas fa-user-edit me-1"></i>Análisis Manual';
            analysisModeInfo.className = 'badge bg-warning me-2';
        }
        
        // Hide model info
        if (modelInfo) {
            modelInfo.style.display = 'none';
        }
        
        // Update form action for manual analysis
        const form = document.getElementById('analyzer-form');
        if (form) {
            form.action = '/analysis/analyze_manual';
        }
    }
}

/**
 * Setup model selection functionality
 */
function setupModelSelection() {
    const modelSelect = document.getElementById('model');
    
    if (modelSelect) {
        modelSelect.addEventListener('change', function() {
            updateModelInfo(this.value);
        });
        
        // Initialize model info
        updateModelInfo(modelSelect.value);
    }
}

/**
 * Update model information display
 */
function updateModelInfo(model) {
    const modelInfo = document.getElementById('model-info');
    
    if (modelInfo) {
        const modelNames = {
            'basico': 'Modelo Básico',
            'avanzado': 'Modelo Avanzado'
        };
        
        const modelDescriptions = {
            'basico': 'Análisis estándar',
            'avanzado': 'Análisis detallado con GPT-4'
        };
        
        modelInfo.innerHTML = `<i class="fas fa-brain me-1"></i>${modelNames[model]}`;
        modelInfo.title = modelDescriptions[model];
    }
}

/**
 * Update analysis information display
 */
function updateAnalysisInfo(mode) {
    const analysisModeInfo = document.getElementById('analysis-mode-info');
    
    if (analysisModeInfo) {
        const modeInfo = {
            'automatic': {
                text: 'Análisis Automático',
                icon: 'fas fa-robot',
                class: 'badge bg-primary me-2'
            },
            'manual': {
                text: 'Análisis Manual',
                icon: 'fas fa-user-edit',
                class: 'badge bg-warning me-2'
            }
        };
        
        const info = modeInfo[mode];
        if (info) {
            analysisModeInfo.innerHTML = `<i class="${info.icon} me-1"></i>${info.text}`;
            analysisModeInfo.className = info.class;
        }
    }
}

/**
 * Setup form interactions
 */
function setupFormInteractions() {
    const form = document.getElementById('analyzer-form');
    const analyzeButton = document.getElementById('analyze-button');
    
    if (form && analyzeButton) {
        form.addEventListener('submit', function(e) {
            // Add loading state to button
            analyzeButton.classList.add('loading');
            analyzeButton.disabled = true;
            
            // Show loading modal if available
            const loadingModal = document.getElementById('loadingModal');
            if (loadingModal) {
                loadingModal.style.display = 'block';
            }
        });
    }
    
    // Setup form validation
    setupFormValidation();
}

/**
 * Setup form validation
 */
function setupFormValidation() {
    const textInput = document.getElementById('input-text');
    const urlInput = document.getElementById('url');
    const form = document.getElementById('analyzer-form');
    
    if (textInput) {
        textInput.addEventListener('input', function() {
            validateForm();
        });
    }
    
    if (urlInput) {
        urlInput.addEventListener('input', function() {
            validateForm();
        });
    }
    
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                showValidationError('Por favor, completa todos los campos requeridos.');
            }
        });
    }
}

/**
 * Validate form inputs
 */
function validateForm() {
    const isUrlMode = document.getElementById('fields-url').style.display !== 'none';
    const textInput = document.getElementById('input-text');
    const urlInput = document.getElementById('url');
    const analyzeButton = document.getElementById('analyze-button');
    
    let isValid = true;
    
    if (isUrlMode) {
        // URL mode validation
        if (!urlInput.value.trim()) {
            isValid = false;
        }
    } else {
        // Text mode validation
        if (!textInput.value.trim()) {
            isValid = false;
        }
    }
    
    // Update button state
    if (analyzeButton) {
        analyzeButton.disabled = !isValid;
        if (isValid) {
            analyzeButton.classList.remove('btn-secondary');
            analyzeButton.classList.add('btn-primary');
        } else {
            analyzeButton.classList.remove('btn-primary');
            analyzeButton.classList.add('btn-secondary');
        }
    }
    
    return isValid;
}

/**
 * Show validation error message
 */
function showValidationError(message) {
    // Create or update error message
    let errorDiv = document.getElementById('validation-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'validation-error';
        errorDiv.className = 'alert alert-danger mt-3';
        errorDiv.style.display = 'none';
        
        const form = document.getElementById('analyzer-form');
        if (form) {
            form.appendChild(errorDiv);
        }
    }
    
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>${message}`;
    errorDiv.style.display = 'block';
    
    // Hide error after 5 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

/**
 * Setup quick actions
 */
function setupQuickActions() {
    const loadExampleBtn = document.getElementById('load-example');
    const useUrlBtn = document.getElementById('use-url');
    const backToTextBtn = document.getElementById('back-to-text');
    
    if (loadExampleBtn) {
        loadExampleBtn.addEventListener('click', loadExample);
    }
    
    if (useUrlBtn) {
        useUrlBtn.addEventListener('click', switchToUrlMode);
    }
    
    if (backToTextBtn) {
        backToTextBtn.addEventListener('click', switchToTextMode);
    }
}

/**
 * Load example text
 */
function loadExample() {
    const exampleTitle = "María Elena Rodríguez, la joven madre que revoluciona el liderazgo empresarial";
    const exampleAuthor = "Redacción de Economía Digital";
    const exampleText = `La nueva directora de la empresa tecnológica InnovateCorp, María Elena Rodríguez, de 28 años, fue nombrada para el cargo tras una intensa búsqueda que duró varios meses. La joven ejecutiva, conocida por su "belleza y carisma", asumirá las riendas de la compañía que factura más de 50 millones de euros anuales.

María Elena, madre de dos hijos pequeños, logró equilibrar su vida familiar con una exitosa carrera profesional. "Es un ejemplo perfecto de cómo las mujeres pueden tenerlo todo", comentó el presidente de la junta directiva, Carlos Mendoza, durante la presentación. "Su elegancia y determinación la convierten en la candidata ideal para liderar nuestro equipo".

La nueva directora, que se graduó con honores en Administración de Empresas, ha trabajado en la empresa durante solo tres años, un período relativamente corto para asumir una responsabilidad de tal magnitud. Sin embargo, su "intuición femenina" y su "capacidad natural para la comunicación" la han llevado a destacar entre sus colegas masculinos.

"Estoy emocionada de asumir este desafío", declaró María Elena, visiblemente emocionada. "Sé que mi experiencia como madre me ha dado las herramientas necesarias para manejar equipos y resolver conflictos de manera efectiva".

Algunos analistas han cuestionado si su nombramiento responde a una estrategia de diversidad de género más que a criterios puramente profesionales. "Es importante que las empresas promuevan la igualdad, pero no a costa de la experiencia", señaló un ejecutivo anónimo del sector.

La nueva directora planea implementar políticas de conciliación familiar y promover un ambiente de trabajo más "humano y empático", características que considera propias del liderazgo femenino.`;

    // Fill all form fields
    const titleInput = document.getElementById('title');
    const authorInput = document.getElementById('authors');
    const textInput = document.getElementById('input-text');
    
    if (titleInput) {
        titleInput.value = exampleTitle;
    }
    
    if (authorInput) {
        authorInput.value = exampleAuthor;
    }
    
    if (textInput) {
        textInput.value = exampleText;
        textInput.focus();
    }
    
    // Trigger validation
    validateForm();
    
    // Show success message
    showSuccessMessage('Ejemplo cargado correctamente. Puedes modificar el texto si lo deseas.');
}

/**
 * Switch to URL input mode
 */
function switchToUrlMode() {
    const textFields = document.getElementById('fields-text');
    const urlFields = document.getElementById('fields-url');
    const textInput = document.getElementById('input-text');
    const urlInput = document.getElementById('url');
    
    if (textFields && urlFields) {
        textFields.style.display = 'none';
        urlFields.style.display = 'block';
        
        // Focus on URL input
        if (urlInput) {
            urlInput.focus();
        }
        
        // Clear text input requirement
        if (textInput) {
            textInput.required = false;
        }
        
        // Set URL input as required
        if (urlInput) {
            urlInput.required = true;
        }
        
        // Trigger validation
        validateForm();
    }
}

/**
 * Switch to text input mode
 */
function switchToTextMode() {
    const textFields = document.getElementById('fields-text');
    const urlFields = document.getElementById('fields-url');
    const textInput = document.getElementById('input-text');
    const urlInput = document.getElementById('url');
    
    if (textFields && urlFields) {
        textFields.style.display = 'block';
        urlFields.style.display = 'none';
        
        // Focus on text input
        if (textInput) {
            textInput.focus();
        }
        
        // Set text input as required
        if (textInput) {
            textInput.required = true;
        }
        
        // Clear URL input requirement
        if (urlInput) {
            urlInput.required = false;
        }
        
        // Trigger validation
        validateForm();
    }
}

/**
 * Show success message
 */
function showSuccessMessage(message) {
    // Create or update success message
    let successDiv = document.getElementById('success-message');
    if (!successDiv) {
        successDiv = document.createElement('div');
        successDiv.id = 'success-message';
        successDiv.className = 'alert alert-success mt-3';
        successDiv.style.display = 'none';
        
        const form = document.getElementById('analyzer-form');
        if (form) {
            form.appendChild(successDiv);
        }
    }
    
    successDiv.innerHTML = `<i class="fas fa-check-circle me-2"></i>${message}`;
    successDiv.style.display = 'block';
    
    // Hide success message after 3 seconds
    setTimeout(() => {
        successDiv.style.display = 'none';
    }, 3000);
}

/**
 * Setup clear text button
 */
function setupClearTextButton() {
    const clearButton = document.getElementById('clear-text');
    if (clearButton) {
        clearButton.addEventListener('click', function() {
            const textInput = document.getElementById('input-text');
            if (textInput) {
                textInput.value = '';
                textInput.focus();
                validateForm();
                showSuccessMessage('Texto limpiado correctamente');
            }
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    setupModeSelection();
    setupModelSelection();
    setupUrlToggle();
    setupExampleLoader();
    updateAnalysisInfo();
    setupFormInteractions();
    setupQuickActions();
    
    // Initialize with automatic mode selected
    selectMode('automatic');
    console.log('Initialized with automatic mode selected');
    
    // Setup clear text button
    setupClearTextButton();
});

// Export functions for potential external use
window.CreateAnalysisEnhanced = {
    selectMode,
    updateModelInfo,
    loadExample,
    switchToUrlMode,
    switchToTextMode,
    validateForm
};
