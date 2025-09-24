/**
 * Enhanced Manual Analysis JavaScript
 * Handles text selection, annotation, and analysis functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeManualAnalysis();
});

let selectedText = '';
let currentSelection = null;
let annotations = [];
let wordCount = 0;
let enabledVariablesByCategory = { contenido_general: [], lenguaje: [], fuentes: [] };

function initializeManualAnalysis() {
    // Initialize text analysis
    setupTextAnalysis();
    
    // Setup event listeners
    setupEventListeners();
    
    // Initialize word count
    updateWordCount();
    
    // Setup category change handlers
    setupCategoryHandlers();
}

function setupTextAnalysis() {
    const analysisText = document.getElementById('analysis-text');
    
    if (analysisText) {
        // Enable text selection
        analysisText.addEventListener('mouseup', handleTextSelection);
        analysisText.addEventListener('keyup', handleTextSelection);
        
        // Prevent default text selection behavior
        analysisText.addEventListener('selectstart', function(e) {
            // Allow text selection
        });
    }
}

function setupEventListeners() {
    // Clear selections button
    const clearSelectionsBtn = document.getElementById('clear-selections');
    if (clearSelectionsBtn) {
        clearSelectionsBtn.addEventListener('click', clearSelections);
    }
    
    // Save analysis button
    const saveAnalysisBtn = document.getElementById('save-analysis');
    if (saveAnalysisBtn) {
        saveAnalysisBtn.addEventListener('click', saveAnalysis);
    }
    
    // Save annotation button
    const saveAnnotationBtn = document.getElementById('save-annotation');
    if (saveAnnotationBtn) {
        saveAnnotationBtn.addEventListener('click', saveAnnotation);
    }
    
    // Category change handler
    const categorySelect = document.getElementById('annotation-category');
    if (categorySelect) {
        categorySelect.addEventListener('change', handleCategoryChange);
    }
    
    // Variable change handler
    const variableSelect = document.getElementById('annotation-variable');
    if (variableSelect) {
        variableSelect.addEventListener('change', handleVariableChange);
    }
}

function setupCategoryHandlers() {
    // No user selection: load all variables from server-provided lists
    updateEnabledVariables(true);
    renderLoadedInfo();
}

function handleTextSelection() {
    const selection = window.getSelection();
    const selectedText = selection.toString().trim();
    
    if (selectedText.length > 0) {
        currentSelection = {
            text: selectedText,
            range: selection.getRangeAt(0)
        };
        
        // Show annotation modal
        showAnnotationModal(selectedText);
    }
}

function showAnnotationModal(text) {
    const modal = new bootstrap.Modal(document.getElementById('analysisModal'));
    const selectedTextContent = document.getElementById('selected-text-content');
    
    if (selectedTextContent) {
        selectedTextContent.textContent = text;
    }
    
    // Reset form
    resetAnnotationForm();
    
    // Show modal
    modal.show();
}

function resetAnnotationForm() {
    document.getElementById('annotation-category').value = '';
    document.getElementById('annotation-variable').value = '';
    document.getElementById('annotation-value').value = '';
    
    // Clear variable options
    const variableSelect = document.getElementById('annotation-variable');
    variableSelect.innerHTML = '<option value="">Selecciona una variable</option>';
    
    // Clear value options
    const valueSelect = document.getElementById('annotation-value');
    valueSelect.innerHTML = '<option value="">Selecciona un valor</option>';
}

function handleCategoryChange() {
    const category = document.getElementById('annotation-category').value;
    const variableSelect = document.getElementById('annotation-variable');
    
    // Clear existing options
    variableSelect.innerHTML = '<option value="">Selecciona una variable</option>';
    
    if (category) {
        // Get variables for selected category
        const variables = getVariablesForCategory(category);
        
        variables.forEach(variable => {
            const option = document.createElement('option');
            option.value = variable;
            option.textContent = variable.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            variableSelect.appendChild(option);
        });
    }
}

function handleVariableChange() {
    const category = document.getElementById('annotation-category').value;
    const variable = document.getElementById('annotation-variable').value;
    const valueSelect = document.getElementById('annotation-value');
    
    // Clear existing options
    valueSelect.innerHTML = '<option value="">Selecciona un valor</option>';
    
    if (category && variable) {
        // Get values for selected variable
        const values = getValuesForVariable(category, variable);
        
        values.forEach(value => {
            const option = document.createElement('option');
            option.value = value.key;
            option.textContent = value.label;
            valueSelect.appendChild(option);
        });
    }
}

function getVariablesForCategory(category) {
    const variables = {
        'contenido_general': ['cita_textual_titular', 'genero_nombre_propio_titular', 'genero_periodista', 'genero_personas_mencionadas', 'nombre_propio_titular', 'personas_mencionadas', 'tema'],
        'lenguaje': ['androcentrismo', 'asimetria', 'cargos_mujeres', 'comparacion_mujeres_hombres', 'denominacion_dependiente', 'denominacion_redundante', 'denominacion_sexualizada', 'dual_aparente', 'excepcion_noticiabilidad', 'hombre_humanidad', 'infantilizacion', 'lenguaje_sexista', 'masculino_generico', 'sexismo_social'],
        'fuentes': ['declaracion_fuente', 'genero_fuente', 'nombre_fuente', 'tipo_fuente']
    };
    
    return variables[category] || [];
}

function getValuesForVariable(category, variable) {
    // This would typically come from the server configuration
    // For now, we'll provide some basic options
    const valueOptions = {
        'genero_periodista': [
            { key: '1', label: 'Masculino' },
            { key: '2', label: 'Femenino' },
            { key: '3', label: 'Mixto' },
            { key: '4', label: 'Ns/Nc' },
            { key: '5', label: 'Agencia/otros medios' }
        ],
        'tema': [
            { key: '1', label: 'Científica/Investigación' },
            { key: '2', label: 'Comunicación' },
            { key: '3', label: 'De farándula o espectáculo' },
            { key: '4', label: 'Deportiva' },
            { key: '5', label: 'Economía' },
            { key: '12', label: 'Política' },
            { key: '15', label: 'Tecnología' }
        ],
        'lenguaje_sexista': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' },
            { key: '3', label: 'Sí, además se observa un salto semántico' }
        ]
    };
    
    return valueOptions[variable] || [
        { key: '1', label: 'No' },
        { key: '2', label: 'Sí' }
    ];
}

function saveAnnotation() {
    const category = document.getElementById('annotation-category').value;
    const variable = document.getElementById('annotation-variable').value;
    const value = document.getElementById('annotation-value').value;
    
    if (!category || !variable || !value) {
        showError('Por favor, completa todos los campos de la anotación.');
        return;
    }
    
    if (!currentSelection) {
        showError('No hay texto seleccionado.');
        return;
    }
    
    // Create annotation
    const annotation = {
        id: Date.now(),
        text: currentSelection.text,
        category: category,
        variable: variable,
        value: value,
        timestamp: new Date().toISOString()
    };
    
    // Add to annotations array
    annotations.push(annotation);
    
    // Highlight text in the document
    highlightText(currentSelection.range, annotation);
    
    // Update selection count
    updateSelectionCount();
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('analysisModal'));
    modal.hide();
    
    // Clear current selection
    currentSelection = null;
    
    // Show success message
    showSuccess('Anotación guardada correctamente.');
}

function highlightText(range, annotation) {
    const span = document.createElement('span');
    span.className = 'highlight';
    span.setAttribute('data-annotation-id', annotation.id);
    span.setAttribute('data-category', annotation.category);
    span.setAttribute('data-variable', annotation.variable);
    span.setAttribute('data-value', annotation.value);
    span.title = `${annotation.category}: ${annotation.variable} = ${annotation.value}`;
    
    try {
        range.surroundContents(span);
    } catch (e) {
        // If surroundContents fails, try a different approach
        const contents = range.extractContents();
        span.appendChild(contents);
        range.insertNode(span);
    }
}

function updateEnabledVariables(loadAll = false) {
    enabledVariablesByCategory = { contenido_general: [], lenguaje: [], fuentes: [] };
    if (loadAll && window.MANUAL_VARIABLES) {
        enabledVariablesByCategory.contenido_general = [...(window.MANUAL_VARIABLES.contenido_general || [])];
        enabledVariablesByCategory.lenguaje = [...(window.MANUAL_VARIABLES.lenguaje || [])];
        enabledVariablesByCategory.fuentes = [...(window.MANUAL_VARIABLES.fuentes || [])];
        return;
    }
    const checked = document.querySelectorAll('input[type="checkbox"][name]:checked');
    checked.forEach(cb => {
        const category = cb.name;
        const variable = cb.value;
        if (enabledVariablesByCategory[category] && !enabledVariablesByCategory[category].includes(variable)) {
            enabledVariablesByCategory[category].push(variable);
        }
    });
}

function renderLoadedInfo() {
    const container = document.getElementById('loaded-info');
    if (!container) return;

    const sections = Object.entries(enabledVariablesByCategory)
        .filter(([, vars]) => vars.length > 0)
        .map(([category, vars]) => {
            const title = category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            const chips = vars.map(v => `<span class="badge bg-light text-dark border me-1 mb-1">${v.replace(/_/g,' ')}</span>`).join(' ');
            return `
                <div class="mb-2">
                    <div class="small text-muted mb-1">${title}</div>
                    <div class="d-flex flex-wrap">${chips}</div>
                </div>
            `;
        }).join('');

    container.innerHTML = sections || `<div class="small text-muted">No hay variables seleccionadas.</div>`;
}

// Removed showAnalysisResults: no longer needed without a start action

function clearSelections() {
    // Remove all highlights
    const highlights = document.querySelectorAll('.highlight');
    highlights.forEach(highlight => {
        const parent = highlight.parentNode;
        parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
        parent.normalize();
    });
    
    // Clear annotations array
    annotations = [];
    
    // Update selection count
    updateSelectionCount();
    
    // Hide results
    const resultsDiv = document.getElementById('analysis-results');
    if (resultsDiv) {
        resultsDiv.style.display = 'none';
    }
    
    showSuccess('Selecciones limpiadas correctamente.');
}

function saveAnalysis() {
    if (annotations.length === 0) {
        showError('No hay anotaciones para guardar.');
        return;
    }
    
    // Prepare analysis data
    const analysisData = {
        annotations: annotations,
        timestamp: new Date().toISOString(),
        wordCount: wordCount,
        totalAnnotations: annotations.length
    };
    
    // Here you would typically send the data to the server
    console.log('Saving analysis:', analysisData);
    
    // For now, just show success message
    showSuccess(`Análisis guardado con ${annotations.length} anotaciones.`);
}

function updateWordCount() {
    const analysisText = document.getElementById('analysis-text');
    if (analysisText) {
        const text = analysisText.textContent || analysisText.innerText || '';
        wordCount = text.trim().split(/\s+/).filter(word => word.length > 0).length;
        
        const wordCountBadge = document.getElementById('word-count');
        if (wordCountBadge) {
            wordCountBadge.textContent = `${wordCount} palabras`;
        }
    }
}

function updateSelectionCount() {
    const selectionCountBadge = document.getElementById('selection-count');
    if (selectionCountBadge) {
        selectionCountBadge.textContent = `${annotations.length} seleccionado`;
    }
}

function showError(message) {
    // Create or show error message
    showMessage(message, 'danger');
}

function showSuccess(message) {
    // Create or show success message
    showMessage(message, 'success');
}

function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.alert-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type} alert-message position-fixed`;
    messageDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    messageDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(messageDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 5000);
}

// Export functions for potential external use
window.ManualAnalysisEnhanced = {
    clearSelections,
    saveAnalysis,
    saveAnnotation,
    updateWordCount,
    updateSelectionCount
};
