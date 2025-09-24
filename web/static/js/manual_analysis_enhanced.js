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
    
    // Close annotation panel button
    const closeAnnotationBtn = document.getElementById('close-annotation');
    if (closeAnnotationBtn) {
        closeAnnotationBtn.addEventListener('click', hideAnnotationPanel);
    }
    
    // Cancel annotation button
    const cancelAnnotationBtn = document.getElementById('cancel-annotation');
    if (cancelAnnotationBtn) {
        cancelAnnotationBtn.addEventListener('click', hideAnnotationPanel);
    }
    
    // Setup collapsible panels
    setupCollapsiblePanels();
}

function setupCollapsiblePanels() {
    const collapsibleHeaders = document.querySelectorAll('.collapsible-header');
    
    collapsibleHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const content = document.getElementById(targetId);
            
            if (content) {
                toggleCollapsible(this, content);
            }
        });
    });
}

function toggleCollapsible(header, content) {
    const isCollapsed = header.classList.contains('collapsed');
    
    if (isCollapsed) {
        // Expand
        header.classList.remove('collapsed');
        content.classList.remove('collapsed');
    } else {
        // Collapse
        header.classList.add('collapsed');
        content.classList.add('collapsed');
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
        
        // Show annotation panel
        showAnnotationPanel(selectedText);
    }
}

function showAnnotationPanel(text) {
    const panel = document.getElementById('annotation-panel');
    const selectedTextPreview = document.getElementById('selected-text-preview');
    
    if (selectedTextPreview) {
        selectedTextPreview.textContent = text;
    }
    
    // Reset form
    resetAnnotationForm();
    
    // Show panel
    if (panel) {
        panel.style.display = 'block';
    }
}

function hideAnnotationPanel() {
    const panel = document.getElementById('annotation-panel');
    if (panel) {
        panel.style.display = 'none';
    }
    
    // Clear current selection
    currentSelection = null;
    
    // Clear any text selection
    if (window.getSelection) {
        window.getSelection().removeAllRanges();
    }
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
    // Values from config.ini
    const valueOptions = {
        // CONTENIDO_GENERAL variables
        'genero_nombre_propio_titular': [
            { key: '1', label: 'No hay' },
            { key: '2', label: 'Sí, hombre' },
            { key: '3', label: 'Sí, mujer' },
            { key: '4', label: 'Sí, mujer y hombre' }
        ],
        'genero_personas_mencionadas': [
            { key: '1', label: 'No hay' },
            { key: '2', label: 'Sí, hombre' },
            { key: '3', label: 'Sí, mujer' },
            { key: '4', label: 'Sí, mujer y hombre' }
        ],
        'genero_periodista': [
            { key: '1', label: 'Masculino' },
            { key: '2', label: 'Femenino' },
            { key: '3', label: 'Mixto' },
            { key: '4', label: 'Ns/Nc' },
            { key: '5', label: 'Agencia/otros medios' },
            { key: '6', label: 'Redacción' },
            { key: '7', label: 'Corporativo' }
        ],
        'tema': [
            { key: '1', label: 'Científica/Investigación' },
            { key: '2', label: 'Comunicación' },
            { key: '3', label: 'De farándula o espectáculo' },
            { key: '4', label: 'Deportiva' },
            { key: '5', label: 'Economía (incluido: consumo; compras; viajes…)' },
            { key: '6', label: 'Educación/cultura' },
            { key: '7', label: 'Empleo/Trabajo' },
            { key: '8', label: 'Empresa' },
            { key: '9', label: 'Judicial' },
            { key: '10', label: 'Medioambiente' },
            { key: '11', label: 'Policial' },
            { key: '12', label: 'Política' },
            { key: '13', label: 'Salud' },
            { key: '14', label: 'Social' },
            { key: '15', label: 'Tecnología' },
            { key: '16', label: 'Transporte' },
            { key: '17', label: 'Otros' }
        ],
        'cita_textual_titular': [
            { key: '0', label: 'No' },
            { key: '1', label: 'Sí' }
        ],
        'nombre_propio_titular': [
            { key: '0', label: 'No' },
            { key: '1', label: 'Sí' }
        ],
        'personas_mencionadas': [
            { key: '0', label: 'No' },
            { key: '1', label: 'Sí' }
        ],
        
        // LENGUAJE variables
        'lenguaje_sexista': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' },
            { key: '3', label: 'Sí, además se observa un salto semántico' }
        ],
        'androcentrismo': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'asimetria': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'cargos_mujeres': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'comparacion_mujeres_hombres': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'denominacion_dependiente': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'denominacion_redundante': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'denominacion_sexualizada': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'dual_aparente': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'excepcion_noticiabilidad': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'hombre_humanidad': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'infantilizacion': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'masculino_generico': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'sexismo_social': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        
        // FUENTES variables
        'declaracion_fuente': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'genero_fuente': [
            { key: '1', label: 'Masculino' },
            { key: '2', label: 'Femenino' },
            { key: '3', label: 'Mixto' },
            { key: '4', label: 'Ns/Nc' }
        ],
        'nombre_fuente': [
            { key: '1', label: 'No' },
            { key: '2', label: 'Sí' }
        ],
        'tipo_fuente': [
            { key: '1', label: 'Abogado/a' },
            { key: '2', label: 'Activista' },
            { key: '3', label: 'Actor/Actriz' },
            { key: '4', label: 'Alto Cargo Directivo/a' },
            { key: '5', label: 'Alumno/a' },
            { key: '6', label: 'Analista' },
            { key: '7', label: 'Arquitecto/a' },
            { key: '8', label: 'Artista' },
            { key: '9', label: 'Ciudadano/a' },
            { key: '10', label: 'Corporativa' },
            { key: '11', label: 'Deportista' },
            { key: '12', label: 'Dir. Cine / guionista' },
            { key: '13', label: 'Director/a o presidente/a' },
            { key: '14', label: 'Economista' },
            { key: '15', label: 'El Papa' },
            { key: '16', label: 'Escritor/a' },
            { key: '17', label: 'Experto/a' },
            { key: '18', label: 'Famoso/a' },
            { key: '19', label: 'Institucional' },
            { key: '20', label: 'Investigador/a' },
            { key: '21', label: 'Médico' },
            { key: '22', label: 'Músico/a' },
            { key: '23', label: 'Periodista' },
            { key: '24', label: 'Personaje de Ficción' },
            { key: '25', label: 'Político/a' },
            { key: '26', label: 'Rey/Reina' },
            { key: '27', label: 'Trabajador/a' }
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
    
    // Update annotations summary
    updateAnnotationsSummary();
    
    // Hide annotation panel
    hideAnnotationPanel();
    
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
    
    // Update annotations summary
    updateAnnotationsSummary();
    
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

function updateAnnotationsSummary() {
    const summaryContainer = document.getElementById('annotations-summary');
    if (!summaryContainer) return;

    if (annotations.length === 0) {
        summaryContainer.innerHTML = `
            <div class="no-annotations text-muted text-center py-3">
                <i class="fas fa-info-circle me-2"></i>
                No hay anotaciones aún
            </div>
        `;
        return;
    }

    let html = '';
    annotations.forEach((annotation, index) => {
        const categoryLabel = getCategoryLabel(annotation.category);
        const variableLabel = getVariableLabel(annotation.variable);
        const valueLabel = getValueLabel(annotation.variable, annotation.value);
        
        html += `
            <div class="annotation-item">
                <div class="annotation-text">
                    "${annotation.text.length > 50 ? annotation.text.substring(0, 50) + '...' : annotation.text}"
                </div>
                <div class="annotation-details">
                    <div class="annotation-detail">
                        <span class="annotation-detail-label">Categoría:</span>
                        <span class="annotation-detail-value">${categoryLabel}</span>
                    </div>
                    <div class="annotation-detail">
                        <span class="annotation-detail-label">Variable:</span>
                        <span class="annotation-detail-value">${variableLabel}</span>
                    </div>
                    <div class="annotation-detail">
                        <span class="annotation-detail-label">Valor:</span>
                        <span class="annotation-detail-value">${valueLabel}</span>
                    </div>
                </div>
            </div>
        `;
    });

    summaryContainer.innerHTML = html;
}

function getCategoryLabel(category) {
    const labels = {
        'contenido_general': 'Contenido General',
        'lenguaje': 'Lenguaje',
        'fuentes': 'Fuentes'
    };
    return labels[category] || category;
}

function getVariableLabel(variable) {
    return variable.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function getValueLabel(variable, value) {
    const valueOptions = getValuesForVariable('', variable);
    const option = valueOptions.find(opt => opt.key === value);
    return option ? option.label : value;
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
