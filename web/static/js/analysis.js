// Analysis Page JavaScript

// Variable mappings from config.ini
const variableMappings = {
    // CONTENIDO_GENERAL
    'genero_nombre_propio_titular': {'1': 'No hay', '2': 'Sí, hombre', '3': 'Sí, mujer', '4': 'Sí, mujer y hombre'},
    'genero_personas_mencionadas': {'1': 'No hay', '2': 'Sí, hombre', '3': 'Sí, mujer', '4': 'Sí, mujer y hombre'},
    'genero_periodista': {'1': 'Masculino', '2': 'Femenino', '3': 'Mixto', '4': 'Ns/Nc', '5': 'Agencia/otros medios', '6': 'Redacción', '7': 'Corporativo'},
    'tema': {'1': 'Científica/Investigación', '2': 'Comunicación', '3': 'De farándula o espectáculo', '4': 'Deportiva', '5': 'Economía (incluido: consumo; compras; viajes…)', '6': 'Educación/cultura', '7': 'Empleo/Trabajo', '8': 'Empresa', '9': 'Judicial', '10': 'Medioambiente', '11': 'Policial', '12': 'Política', '13': 'Salud', '14': 'Social', '15': 'Tecnología', '16': 'Transporte', '17': 'Otros'},
    'cita_titular': {'0': 'No', '1': 'Sí'},
    
    // LENGUAJE
    'lenguaje_sexista': {'1': 'No', '2': 'Sí', '3': 'Sí, además se observa un salto semántico'},
    'androcentrismo': {'1': 'No', '2': 'Sí'},
    'asimetria': {'1': 'No', '2': 'Sí'},
    'cargos_mujeres': {'1': 'No', '2': 'Sí'},
    'comparacion_mujeres_hombres': {'1': 'No', '2': 'Sí'},
    'denominacion_dependiente': {'1': 'No', '2': 'Sí'},
    'denominacion_redundante': {'1': 'No', '2': 'Sí'},
    'denominacion_sexualizada': {'1': 'No', '2': 'Sí'},
    'dual_aparente': {'1': 'No', '2': 'Sí'},
    'excepcion_noticiabilidad': {'1': 'No', '2': 'Sí'},
    'hombre_humanidad': {'1': 'No', '2': 'Sí'},
    'infantilizacion': {'1': 'No', '2': 'Sí'},
    'masculino_generico': {'1': 'No', '2': 'Sí'},
    'sexismo_social': {'1': 'No', '2': 'Sí'},
    
    // FUENTES
    'nombre_fuente': {'1': 'No', '2': 'Sí'},
    'declaracion_fuente': {'1': 'No', '2': 'Sí'},
    'tipo_fuente': {'1': 'Abogado/a', '2': 'Activista', '3': 'Actor/Actriz', '4': 'Alto Cargo Directivo/a', '5': 'Alumno/a', '6': 'Analista', '7': 'Arquitecto/a', '8': 'Artista', '9': 'Ciudadano/a', '10': 'Corporativa', '11': 'Deportista', '12': 'Dir. Cine / guionista', '13': 'Director/a o presidente/a', '14': 'Economista', '15': 'El Papa', '16': 'Escritor/a', '17': 'Experto/a', '18': 'Famoso/a', '19': 'Institucional', '20': 'Investigador/a', '21': 'Médico', '22': 'Músico/a', '23': 'Periodista', '24': 'Personaje de Ficción', '25': 'Político/a', '26': 'Rey/Reina', '27': 'Trabajador/a'},
    'genero_fuente': {'1': 'Masculino', '2': 'Femenino', '3': 'Ns/Nc'}
};

// Function to convert numeric values to strings
function convertValueToLabel(variableName, value) {
    if (variableMappings[variableName] && variableMappings[variableName][value.toString()]) {
        return variableMappings[variableName][value.toString()];
    }
    return value; // Return original value if no mapping found
}

// Function to render variable card
function renderVariableCard(key, value, color) {
    const title = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    
    let valueHtml = '';
    if (Array.isArray(value)) {
        if (value.length > 0) {
            valueHtml = `<div class="value-list">${value.map(item => `<span class="value-item">${item}</span>`).join('')}</div>`;
        } else {
            valueHtml = '<span class="value-empty">No hay datos</span>';
        }
    } else {
        valueHtml = `<span class="value-single">${value}</span>`;
    }
    
    return `
        <div class="variable-card">
            <div class="variable-header">
                <div class="variable-icon" style="background-color: ${color};">
                    <i class="fas fa-circle"></i>
                </div>
                <div class="variable-title">${title}</div>
            </div>
            <div class="variable-value">
                ${valueHtml}
            </div>
        </div>
    `;
}

// Function to render source card
function renderSourceCard(fuente, index) {
    let sourceDetails = '';
    Object.keys(fuente).forEach(key => {
        const color = window.highlight_color_map[key] || '#ffffff';
        const title = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        
        let valueHtml = '';
        if (Array.isArray(fuente[key])) {
            valueHtml = `<div class="source-value-list">${fuente[key].map(item => `<span class="source-value-item">${item}</span>`).join('')}</div>`;
        } else {
            valueHtml = `<span class="source-value-single">${fuente[key]}</span>`;
        }
        
        sourceDetails += `
            <div class="source-item">
                <div class="source-item-header">
                    <div class="source-item-icon" style="background-color: ${color};">
                        <i class="fas fa-circle"></i>
                    </div>
                    <span class="source-item-label">${title}</span>
                </div>
                <div class="source-item-value">
                    ${valueHtml}
                </div>
            </div>
        `;
    });
    
    return `
        <div class="source-card">
            <div class="source-header">
                <div class="source-icon">
                    <i class="fas fa-user"></i>
                </div>
                <div class="source-title">Fuente #${index + 1}</div>
            </div>
            <div class="source-details">
                ${sourceDetails}
            </div>
        </div>
    `;
}

// Function to render all content
function renderContent() {
    // Render contenido general
    const contenidoGeneral = window.data.analysis.original.contenido_general;
    const contenidoContainer = document.getElementById('contenido-variables');
    if (contenidoGeneral && contenidoContainer) {
        let html = '';
        Object.keys(contenidoGeneral).forEach(key => {
            const value = contenidoGeneral[key];
            const convertedValue = Array.isArray(value) 
                ? value.map(item => convertValueToLabel(key, item))
                : convertValueToLabel(key, value);
            const color = window.highlight_color_map[key] || '#ffffff';
            html += renderVariableCard(key, convertedValue, color);
        });
        contenidoContainer.innerHTML = html;
    }
    
    // Render lenguaje
    const lenguaje = window.data.analysis.original.lenguaje;
    const lenguajeContainer = document.getElementById('lenguaje-variables');
    if (lenguaje && lenguajeContainer) {
        let html = '';
        Object.keys(lenguaje).forEach(key => {
            const value = lenguaje[key];
            const color = window.highlight_color_map[key] || '#ffffff';
            
            if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                // Handle nested objects (like androcentrismo, asimetria, etc.)
                let subItems = '';
                Object.keys(value).forEach(subKey => {
                    const subValue = value[subKey];
                    
                    if (subKey === 'etiqueta' && Array.isArray(subValue)) {
                        // Convert etiqueta array values
                        const convertedEtiqueta = subValue.map(item => convertValueToLabel(key, item));
                        subItems += `
                            <div class="sub-item">
                                <span class="sub-label">${subKey.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
                                <div class="sub-value-list">${convertedEtiqueta.map(item => `<span class="sub-value-item">${item}</span>`).join('')}</div>
                            </div>
                        `;
                    } else if (subKey === 'ejemplos_articulo' && Array.isArray(subValue)) {
                        // Keep ejemplos_articulo as is (these are text examples)
                        subItems += `
                            <div class="sub-item">
                                <span class="sub-label">${subKey.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
                                <div class="sub-value-list">${subValue.map(item => `<span class="sub-value-item">${item}</span>`).join('')}</div>
                            </div>
                        `;
                    } else {
                        // Handle other sub-values
                        const convertedSubValue = Array.isArray(subValue) 
                            ? subValue.map(item => convertValueToLabel(subKey, item))
                            : convertValueToLabel(subKey, subValue);
                        
                        if (Array.isArray(convertedSubValue)) {
                            subItems += `
                                <div class="sub-item">
                                    <span class="sub-label">${subKey.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
                                    <div class="sub-value-list">${convertedSubValue.map(item => `<span class="sub-value-item">${item}</span>`).join('')}</div>
                                </div>
                            `;
                        } else {
                            subItems += `
                                <div class="sub-item">
                                    <span class="sub-label">${subKey.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
                                    <span class="sub-value-single">${convertedSubValue}</span>
                                </div>
                            `;
                        }
                    }
                });
                
                html += `
                    <div class="variable-card">
                        <div class="variable-header">
                            <div class="variable-icon" style="background-color: ${color};">
                                <i class="fas fa-circle"></i>
                            </div>
                            <div class="variable-title">${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</div>
                        </div>
                        <div class="variable-value">
                            <div class="value-structure">${subItems}</div>
                        </div>
                    </div>
                `;
            } else {
                const convertedValue = Array.isArray(value) 
                    ? value.map(item => convertValueToLabel(key, item))
                    : convertValueToLabel(key, value);
                html += renderVariableCard(key, convertedValue, color);
            }
        });
        lenguajeContainer.innerHTML = html;
    }
    
    // Render fuentes
    const fuentes = window.data.analysis.original.fuentes;
    const fuentesContainer = document.getElementById('fuentes-sources');
    if (fuentes && fuentes.fuentes && fuentesContainer) {
        let html = '';
        fuentes.fuentes.forEach((fuente, index) => {
            // Convert values in the fuente object
            const convertedFuente = {};
            Object.keys(fuente).forEach(key => {
                const value = fuente[key];
                convertedFuente[key] = Array.isArray(value) 
                    ? value.map(item => convertValueToLabel(key, item))
                    : convertValueToLabel(key, value);
            });
            html += renderSourceCard(convertedFuente, index);
        });
        fuentesContainer.innerHTML = html;
    }
}

// Function to process highlights with tooltips
function processHighlights() {
    const tooltip = document.getElementById('highlight-tooltip');
    
    if (!tooltip) {
        console.error('Tooltip element not found!');
        return;
    }
    
    // Find actual highlight elements (mark elements with color-* classes)
    const highlightElements = document.querySelectorAll('mark[class*="color-"]');
    
    highlightElements.forEach(element => {
        // Add tooltip functionality
        element.addEventListener('mouseenter', function(e) {
            const classList = Array.from(this.classList);
            const colorClasses = classList.filter(cls => cls.startsWith('color-'));
            
            if (colorClasses.length > 0) {
                // Try to get real data from the analysis results
                if (window.data && window.data.analysis && window.data.analysis.original) {
                    const analysis = window.data.analysis.original;
                    
                    // Map color classes to specific variables based on HIGHLIGHT_COLOR_MAP from config.ini
                    const colorToVariableMap = {
                        'color-1': { category: 'contenido_general', variable: 'nombre_propio_titular' },
                        'color-2': { category: 'contenido_general', variable: 'cita_textual_titular' },
                        'color-3': { category: 'contenido_general', variable: 'personas_mencionadas' },
                        'color-4': { category: 'lenguaje', variable: 'lenguaje_sexista' },
                        'color-5': { category: 'lenguaje', variable: 'hombre_humanidad' },
                        'color-6': { category: 'lenguaje', variable: 'dual_aparente' },
                        'color-7': { category: 'lenguaje', variable: 'cargos_mujeres' },
                        'color-8': { category: 'lenguaje', variable: 'sexismo_social' },
                        'color-9': { category: 'lenguaje', variable: 'androcentrismo' },
                        'color-10': { category: 'lenguaje', variable: 'asimetria' },
                        'color-11': { category: 'lenguaje', variable: 'infantilizacion' },
                        'color-12': { category: 'lenguaje', variable: 'denominacion_sexualizada' },
                        'color-13': { category: 'lenguaje', variable: 'denominacion_redundante' },
                        'color-14': { category: 'lenguaje', variable: 'denominacion_dependiente' },
                        'color-15': { category: 'lenguaje', variable: 'masculino_generico' },
                        'color-16': { category: 'contenido_general', variable: 'criterios_excepcion_noticiabilidad' },
                        'color-17': { category: 'lenguaje', variable: 'comparacion_mujeres_hombres' },
                        'color-18': { category: 'fuentes', variable: 'nombre_fuente' },
                        'color-19': { category: 'fuentes', variable: 'declaracion_fuente' },
                        'color-20': { category: 'fuentes', variable: 'tipo_fuente' },
                        'color-21': { category: 'fuentes', variable: 'genero_fuente' }
                    };
                    
                    // Process all color classes and collect tooltip data
                    const tooltipData = [];
                    
                    // Determine which category we're currently viewing
                    const currentHighlightBlock = this.closest('.highlight-block');
                    let currentCategory = null;
                    if (currentHighlightBlock) {
                        if (currentHighlightBlock.id === 'highlight-contenido') currentCategory = 'contenido_general';
                        else if (currentHighlightBlock.id === 'highlight-lenguaje') currentCategory = 'lenguaje';
                        else if (currentHighlightBlock.id === 'highlight-fuentes') currentCategory = 'fuentes';
                    }
                    
                    for (const colorClass of colorClasses) {
                        const mapping = colorToVariableMap[colorClass];
                        
                        if (mapping && analysis[mapping.category]) {
                            // Only process variables that match the current category
                            if (currentCategory && mapping.category !== currentCategory) {
                                continue;
                            }
                            
                            const categoryData = analysis[mapping.category];
                            let varValue = null;
                            
                            // Get the value based on category
                            if (mapping.category === 'fuentes' && categoryData.fuentes) {
                                if (categoryData.fuentes.length > 0) {
                                    varValue = categoryData.fuentes[0][mapping.variable];
                                }
                            } else if (mapping.category === 'lenguaje' && categoryData[mapping.variable]) {
                                const langVar = categoryData[mapping.variable];
                                if (typeof langVar === 'object' && !Array.isArray(langVar) && langVar.etiqueta) {
                                    varValue = langVar.etiqueta;
                                } else {
                                    varValue = langVar;
                                }
                            } else {
                                varValue = categoryData[mapping.variable];
                            }
                            
                            // Convert value to label and add to tooltip data
                            if (varValue && (Array.isArray(varValue) ? varValue.length > 0 : true)) {
                                const variableName = mapping.variable.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                                const convertedValue = Array.isArray(varValue) 
                                    ? varValue.map(item => convertValueToLabel(mapping.variable, item)).join(', ')
                                    : convertValueToLabel(mapping.variable, varValue);
                                
                                tooltipData.push({
                                    variable: variableName,
                                    value: convertedValue
                                });
                            }
                        }
                    }
                    
                    // Display tooltip with all variables
                    if (tooltipData.length > 0) {
                        const title = tooltipData.length === 1 ? tooltipData[0].variable : 'Variables de análisis';
                        const description = tooltipData.map(item => `${item.variable}: ${item.value}`).join('\n');
                        
                        tooltip.querySelector('.tooltip-title').textContent = title;
                        tooltip.querySelector('.tooltip-description').textContent = description;
                        
                        const rect = this.getBoundingClientRect();
                        let left = rect.left + (rect.width / 2) - 100;
                        let top = rect.top - 50;
                        if (left < 10) left = 10;
                        if (left + 200 > window.innerWidth - 10) left = window.innerWidth - 210;
                        if (top < 10) top = rect.bottom + 10;
                        
                        tooltip.style.left = left + 'px';
                        tooltip.style.top = top + 'px';
                        tooltip.style.position = 'fixed';
                        tooltip.style.zIndex = '9999';
                        tooltip.classList.add('show');
                    }
                }
            }
        });
        
        element.addEventListener('mouseleave', function() {
            tooltip.classList.remove('show');
        });
    });
}

// Function to add manual annotation highlights to existing highlights
function addManualHighlights() {
    // Only add manual highlights if we're in annotation mode
    if (!annotationMode) return;
    
    const highlightTextElement = document.querySelector('.highlight-text .markup-area');
    if (!highlightTextElement) return;
    
    let highlightedText = highlightTextElement.innerHTML;
    
    // Process only new manual annotations (not already processed)
    annotations.forEach(annotation => {
        const { text, variable, timestamp } = annotation;
        
        // Check if this annotation was already processed by looking for the data-variable attribute
        const escapedText = text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const existingPattern = new RegExp(`<mark[^>]*data-variable="${variable}"[^>]*>.*?${escapedText}.*?</mark>`, 'gi');
        
        if (!existingPattern.test(highlightedText)) {
            // This annotation hasn't been processed yet, add it
            const colorClass = window.highlight_color_map && window.highlight_color_map[variable] 
                ? window.highlight_color_map[variable] 
                : 'color-1';
            
            const pattern = new RegExp(`(${escapedText})`, 'gi');
            highlightedText = highlightedText.replace(pattern, `<mark class="${colorClass}" data-variable="${variable}">$1</mark>`);
        }
    });
    
    // Update the highlight text
    highlightTextElement.innerHTML = highlightedText;
    
    // Process highlights for tooltips
    processHighlights();
}

// Function to show specific highlight block
function showHighlightBlock(category) {
    const plainText = document.querySelector('.plain-text');
    const highlightText = document.querySelector('.highlight-text');
    const highlightBlocks = {
        'contenido': document.getElementById('highlight-contenido'),
        'lenguaje': document.getElementById('highlight-lenguaje'),
        'fuentes': document.getElementById('highlight-fuentes')
    };
    
    if (!highlightText || !plainText) return;
    
    // Hide plain text and show highlight container
    plainText.style.display = 'none';
    highlightText.style.display = 'block';
    
    // Hide all highlight blocks
    Object.values(highlightBlocks).forEach(block => {
        if (block) block.style.display = 'none';
    });
    
    // Show the specific category block
    if (highlightBlocks[category]) {
        highlightBlocks[category].style.display = 'block';
        
        // Add manual highlights to existing highlights
        addManualHighlights();
        
        // Process highlights after a short delay to ensure DOM is ready
        setTimeout(() => {
            processHighlights();
        }, 100);
    }
}

// Function to hide highlights and show plain text
function hideHighlights() {
    const plainText = document.querySelector('.plain-text');
    const highlightText = document.querySelector('.highlight-text');
    const highlightBlocks = {
        'contenido': document.getElementById('highlight-contenido'),
        'lenguaje': document.getElementById('highlight-lenguaje'),
        'fuentes': document.getElementById('highlight-fuentes')
    };
    
    if (!highlightText || !plainText) return;
    
    plainText.style.display = 'block';
    highlightText.style.display = 'none';
    
    // Hide all highlight blocks
    Object.values(highlightBlocks).forEach(block => {
        if (block) block.style.display = 'none';
    });
}

// Setup collapsible panels
function setupCollapsiblePanels() {
    const collapsibleHeaders = document.querySelectorAll('.collapsible-header');
    
    collapsibleHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const content = document.getElementById(targetId);
            const icon = this.querySelector('.toggle-icon');

            if (content && icon) {
                if (content.style.display === 'none' || content.style.display === '') {
                    // Opening panel
                    content.style.display = 'block';
                    icon.classList.remove('fa-chevron-down');
                    icon.classList.add('fa-chevron-up');
                    
                    // Re-render content to include any new manual annotations
                    renderContent();
                    
                    // Show corresponding highlight block only if highlights exist
                    if (targetId === 'contenido-content' && window.data.highlight && window.data.highlight.original && window.data.highlight.original.contenido_general) {
                        showHighlightBlock('contenido');
                    } else if (targetId === 'lenguaje-content' && window.data.highlight && window.data.highlight.original && window.data.highlight.original.lenguaje) {
                        showHighlightBlock('lenguaje');
                    } else if (targetId === 'fuentes-content' && window.data.highlight && window.data.highlight.original && window.data.highlight.original.fuentes) {
                        showHighlightBlock('fuentes');
                    }
                } else {
                    // Closing panel
                    content.style.display = 'none';
                    icon.classList.remove('fa-chevron-up');
                    icon.classList.add('fa-chevron-down');
                    
                    // Hide highlights and show plain text
                    hideHighlights();
                }
            }
        });

        // Initialize all panels as collapsed
        const targetId = header.getAttribute('data-target');
        const content = document.getElementById(targetId);
        if (content) {
            content.style.display = 'none';
        }
    });
}

// ===========================================
// MANUAL ANNOTATION FUNCTIONALITY
// ===========================================

let annotationMode = false;
let selectedText = '';
let currentSelection = null;
let annotations = [];

// Function to enter annotation mode
function editAnalysis() {
    annotationMode = !annotationMode;
    const editButton = document.querySelector('button[onclick="editAnalysis()"]');
    const saveButton = document.getElementById('save-analysis-btn');
    
    if (annotationMode) {
        // Enter annotation mode
        editButton.innerHTML = '<i class="fas fa-times me-1"></i> Salir de Anotación';
        editButton.classList.remove('btn-edit-mode');
        editButton.classList.add('btn-danger');
        
        // Show save button
        if (saveButton) {
            saveButton.style.display = 'flex';
        }
        
        // Show annotation controls
        showAnnotationControls();
        
        // Enable text selection
        enableTextSelection();
        
    } else {
        // Exit annotation mode
        editButton.innerHTML = '<i class="fas fa-edit me-1"></i> Editar Análisis';
        editButton.classList.remove('btn-danger');
        editButton.classList.add('btn-edit-mode');
        
        // Hide save button
        if (saveButton) {
            saveButton.style.display = 'none';
        }
        
        // Hide annotation controls
        hideAnnotationControls();
        
        // Disable text selection
        disableTextSelection();
    }
}

// Function to show annotation controls
function showAnnotationControls() {
    // Add annotation mode indicator
    const annotationIndicator = document.createElement('div');
    annotationIndicator.id = 'annotation-indicator';
    annotationIndicator.className = 'alert alert-info mb-3';
    annotationIndicator.innerHTML = '<i class="fas fa-highlighter me-2"></i>Modo de anotación activo - Selecciona texto para anotar';
    
    const leftPanel = document.querySelector('.col-md-4');
    leftPanel.insertBefore(annotationIndicator, leftPanel.firstChild);
    
    // Add annotation panel
    const annotationPanel = document.createElement('div');
    annotationPanel.id = 'annotation-panel';
    annotationPanel.className = 'analysis-tools-panel mb-3';
    annotationPanel.style.display = 'none';
    annotationPanel.innerHTML = `
        <div class="annotation-header">
            <h6 class="panel-title mb-2">
                <i class="fas fa-tag me-2"></i>Anotar Texto
            </h6>
            <button type="button" class="btn-close btn-close-sm" onclick="hideAnnotationPanel()"></button>
        </div>
        
        <div class="selected-text-preview mb-3">
            <small class="text-muted">Texto seleccionado:</small>
            <div class="selected-text-content" id="selected-text-content" style="background: #f8f9fa; padding: 8px; border-radius: 4px; font-style: italic;"></div>
        </div>
        
        <div class="annotation-form">
            <div class="mb-2">
                <label class="form-label small">Categoría</label>
                <select class="form-select form-select-sm" id="annotation-category">
                    <option value="">Selecciona categoría</option>
                    <option value="contenido_general">Contenido General</option>
                    <option value="lenguaje">Lenguaje</option>
                    <option value="fuentes">Fuentes</option>
                </select>
            </div>
            <div class="mb-2">
                <label class="form-label small">Variable</label>
                <select class="form-select form-select-sm" id="annotation-variable">
                    <option value="">Selecciona variable</option>
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label small">Valor</label>
                <select class="form-select form-select-sm" id="annotation-value">
                    <option value="">Selecciona valor</option>
                </select>
            </div>
            <div class="d-grid gap-2">
                <button type="button" class="btn btn-primary btn-sm" onclick="saveAnnotation()">
                    <i class="fas fa-save me-1"></i>Guardar Anotación
                </button>
                <button type="button" class="btn btn-outline-secondary btn-sm" onclick="hideAnnotationPanel()">
                    <i class="fas fa-times me-1"></i>Cancelar
                </button>
            </div>
        </div>
    `;
    
    leftPanel.insertBefore(annotationPanel, leftPanel.children[2]);
    
    // Setup annotation form handlers
    setupAnnotationHandlers();
}

// Function to hide annotation controls
function hideAnnotationControls() {
    const annotationIndicator = document.getElementById('annotation-indicator');
    const annotationPanel = document.getElementById('annotation-panel');
    
    if (annotationIndicator) annotationIndicator.remove();
    if (annotationPanel) annotationPanel.remove();
}

// Function to enable text selection
function enableTextSelection() {
    const analysisText = document.querySelector('.analysis-text');
    if (analysisText) {
        analysisText.addEventListener('mouseup', handleTextSelection);
        analysisText.addEventListener('keyup', handleTextSelection);
        analysisText.style.cursor = 'text';
        
        // Add annotation mode class to body
        document.body.classList.add('annotation-mode');
    }
}

// Function to disable text selection
function disableTextSelection() {
    const analysisText = document.querySelector('.analysis-text');
    if (analysisText) {
        analysisText.removeEventListener('mouseup', handleTextSelection);
        analysisText.removeEventListener('keyup', handleTextSelection);
        analysisText.style.cursor = 'default';
        
        // Remove annotation mode class from body
        document.body.classList.remove('annotation-mode');
    }
}

// Function to handle text selection
function handleTextSelection() {
    const selection = window.getSelection();
    const selectedText = selection.toString().trim();
    
    if (selectedText && selectedText.length > 0) {
        currentSelection = {
            text: selectedText,
            range: selection.getRangeAt(0)
        };
        
        // Show annotation panel
        showAnnotationPanel();
        
        // Update selected text preview
        document.getElementById('selected-text-content').textContent = selectedText;
    }
}

// Function to show annotation panel
function showAnnotationPanel() {
    const annotationPanel = document.getElementById('annotation-panel');
    if (annotationPanel) {
        annotationPanel.style.display = 'block';
    }
}

// Function to hide annotation panel
function hideAnnotationPanel() {
    const annotationPanel = document.getElementById('annotation-panel');
    if (annotationPanel) {
        annotationPanel.style.display = 'none';
    }
    
    // Clear selection
    if (window.getSelection) {
        window.getSelection().removeAllRanges();
    }
}

// Function to setup annotation handlers
function setupAnnotationHandlers() {
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

// Function to handle category change
function handleCategoryChange() {
    const category = document.getElementById('annotation-category').value;
    const variableSelect = document.getElementById('annotation-variable');
    const valueSelect = document.getElementById('annotation-value');
    
    // Clear variable and value selects
    variableSelect.innerHTML = '<option value="">Selecciona variable</option>';
    valueSelect.innerHTML = '<option value="">Selecciona valor</option>';
    
    if (category) {
        // Get variables for the selected category from config.ini
        const variables = getVariablesForCategory(category);
        
        variables.forEach(variable => {
            const option = document.createElement('option');
            option.value = variable;
            option.textContent = variable.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            variableSelect.appendChild(option);
        });
    }
}

// Function to handle variable change
function handleVariableChange() {
    const variable = document.getElementById('annotation-variable').value;
    const valueSelect = document.getElementById('annotation-value');
    
    // Clear value select
    valueSelect.innerHTML = '<option value="">Selecciona valor</option>';
    
    if (variable) {
        // Get values for the selected variable from config.ini
        const values = getValuesForVariable(variable);
        
        values.forEach(value => {
            const option = document.createElement('option');
            option.value = value.key;
            option.textContent = value.label;
            valueSelect.appendChild(option);
        });
    }
}

// Function to get variables for category
function getVariablesForCategory(category) {
    const categoryVariables = {
        'contenido_general': [
            'genero_nombre_propio_titular', 'genero_personas_mencionadas', 'genero_periodista',
            'tema', 'cita_titular', 'criterios_excepcion_noticiabilidad'
        ],
        'lenguaje': [
            'lenguaje_sexista', 'androcentrismo', 'asimetria', 'cargos_mujeres',
            'comparacion_mujeres_hombres', 'denominacion_dependiente', 'denominacion_redundante',
            'denominacion_sexualizada', 'dual_aparente', 'excepcion_noticiabilidad',
            'hombre_humanidad', 'infantilizacion', 'masculino_generico', 'sexismo_social'
        ],
        'fuentes': [
            'nombre_fuente', 'declaracion_fuente', 'tipo_fuente', 'genero_fuente'
        ]
    };
    
    return categoryVariables[category] || [];
}

// Function to get values for variable
function getValuesForVariable(variable) {
    const variableMappings = {
        // CONTENIDO_GENERAL
        'genero_nombre_propio_titular': [
            {key: '1', label: 'No hay'}, {key: '2', label: 'Sí, hombre'}, 
            {key: '3', label: 'Sí, mujer'}, {key: '4', label: 'Sí, mujer y hombre'}
        ],
        'genero_personas_mencionadas': [
            {key: '1', label: 'No hay'}, {key: '2', label: 'Sí, hombre'}, 
            {key: '3', label: 'Sí, mujer'}, {key: '4', label: 'Sí, mujer y hombre'}
        ],
        'genero_periodista': [
            {key: '1', label: 'Masculino'}, {key: '2', label: 'Femenino'}, 
            {key: '3', label: 'Mixto'}, {key: '4', label: 'Ns/Nc'}, 
            {key: '5', label: 'Agencia/otros medios'}, {key: '6', label: 'Redacción'}, 
            {key: '7', label: 'Corporativo'}
        ],
        'tema': [
            {key: '1', label: 'Científica/Investigación'}, {key: '2', label: 'Comunicación'}, 
            {key: '3', label: 'De farándula o espectáculo'}, {key: '4', label: 'Deportiva'}, 
            {key: '5', label: 'Economía (incluido: consumo; compras; viajes…)'}, 
            {key: '6', label: 'Educación/cultura'}, {key: '7', label: 'Empleo/Trabajo'}, 
            {key: '8', label: 'Empresa'}, {key: '9', label: 'Judicial'}, 
            {key: '10', label: 'Medioambiente'}, {key: '11', label: 'Policial'}, 
            {key: '12', label: 'Política'}, {key: '13', label: 'Salud'}, 
            {key: '14', label: 'Social'}, {key: '15', label: 'Tecnología'}, 
            {key: '16', label: 'Transporte'}, {key: '17', label: 'Otros'}
        ],
        'cita_titular': [
            {key: '0', label: 'No'}, {key: '1', label: 'Sí'}
        ],
        'criterios_excepcion_noticiabilidad': [
            {key: '1', label: 'No'}, {key: '2', label: 'Sí'}
        ],
        
        // LENGUAJE
        'lenguaje_sexista': [
            {key: '1', label: 'No'}, {key: '2', label: 'Sí'}, 
            {key: '3', label: 'Sí, además se observa un salto semántico'}
        ],
        'androcentrismo': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'asimetria': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'cargos_mujeres': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'comparacion_mujeres_hombres': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'denominacion_dependiente': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'denominacion_redundante': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'denominacion_sexualizada': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'dual_aparente': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'excepcion_noticiabilidad': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'hombre_humanidad': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'infantilizacion': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'masculino_generico': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'sexismo_social': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        
        // FUENTES
        'nombre_fuente': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'declaracion_fuente': [{key: '1', label: 'No'}, {key: '2', label: 'Sí'}],
        'tipo_fuente': [
            {key: '1', label: 'Abogado/a'}, {key: '2', label: 'Activista'}, 
            {key: '3', label: 'Actor/Actriz'}, {key: '4', label: 'Alto Cargo Directivo/a'}, 
            {key: '5', label: 'Alumno/a'}, {key: '6', label: 'Analista'}, 
            {key: '7', label: 'Arquitecto/a'}, {key: '8', label: 'Artista'}, 
            {key: '9', label: 'Ciudadano/a'}, {key: '10', label: 'Corporativa'}, 
            {key: '11', label: 'Deportista'}, {key: '12', label: 'Dir. Cine / guionista'}, 
            {key: '13', label: 'Director/a o presidente/a'}, {key: '14', label: 'Economista'}, 
            {key: '15', label: 'El Papa'}, {key: '16', label: 'Escritor/a'}, 
            {key: '17', label: 'Experto/a'}, {key: '18', label: 'Famoso/a'}, 
            {key: '19', label: 'Institucional'}, {key: '20', label: 'Investigador/a'}, 
            {key: '21', label: 'Médico'}, {key: '22', label: 'Músico/a'}, 
            {key: '23', label: 'Periodista'}, {key: '24', label: 'Personaje de Ficción'}, 
            {key: '25', label: 'Político/a'}, {key: '26', label: 'Rey/Reina'}, 
            {key: '27', label: 'Trabajador/a'}
        ],
        'genero_fuente': [
            {key: '1', label: 'Masculino'}, {key: '2', label: 'Femenino'}, 
            {key: '3', label: 'Ns/Nc'}
        ]
    };
    
    return variableMappings[variable] || [];
}

// Function to save annotation
function saveAnnotation() {
    const category = document.getElementById('annotation-category').value;
    const variable = document.getElementById('annotation-variable').value;
    const value = document.getElementById('annotation-value').value;
    
    if (!category || !variable || !value) {
        showNotification('Por favor completa todos los campos', 'error');
        return;
    }
    
    if (!currentSelection) {
        showNotification('No hay texto seleccionado', 'error');
        return;
    }
    
    // Create annotation object
    const annotation = {
        text: currentSelection.text,
        category: category,
        variable: variable,
        value: value,
        timestamp: new Date().toISOString()
    };
    
    // Add to annotations array
    annotations.push(annotation);
    
    // Integrate annotation into analysis data structure
    integrateAnnotationIntoAnalysis(annotation);
    
    // Apply highlight to the text
    applyHighlight(currentSelection.range, variable);
    
    // Show success message
    showNotification('Anotación guardada correctamente', 'success');
    
    // Hide annotation panel
    hideAnnotationPanel();
    
    // Clear form
    document.getElementById('annotation-category').value = '';
    document.getElementById('annotation-variable').innerHTML = '<option value="">Selecciona variable</option>';
    document.getElementById('annotation-value').innerHTML = '<option value="">Selecciona valor</option>';
}

// Function to integrate annotation into analysis data structure
function integrateAnnotationIntoAnalysis(annotation) {
    const { category, variable, value, text } = annotation;
    
    // Ensure analysis data structure exists
    if (!window.data.analysis) {
        window.data.analysis = {};
    }
    if (!window.data.analysis.original) {
        window.data.analysis.original = {};
    }
    
    // Initialize category if it doesn't exist
    if (!window.data.analysis.original[category]) {
        window.data.analysis.original[category] = {};
    }
    
    // Handle different category structures
    if (category === 'contenido_general') {
        // For contenido_general, add to the variable array
        if (!window.data.analysis.original[category][variable]) {
            window.data.analysis.original[category][variable] = [];
        }
        window.data.analysis.original[category][variable].push(text);
        
    } else if (category === 'lenguaje') {
        // For lenguaje, add to the variable's etiqueta array
        if (!window.data.analysis.original[category][variable]) {
            window.data.analysis.original[category][variable] = {
                etiqueta: [],
                ejemplos_articulo: []
            };
        }
        if (!window.data.analysis.original[category][variable].etiqueta) {
            window.data.analysis.original[category][variable].etiqueta = [];
        }
        window.data.analysis.original[category][variable].etiqueta.push(value);
        window.data.analysis.original[category][variable].ejemplos_articulo.push(text);
        
    } else if (category === 'fuentes') {
        // For fuentes, add to the fuentes array
        if (!window.data.analysis.original[category].fuentes) {
            window.data.analysis.original[category].fuentes = [];
        }
        
        // Check if there's already a source with this text
        let existingSource = window.data.analysis.original[category].fuentes.find(source => 
            source.nombre_fuente === text || source.declaracion_fuente === text
        );
        
        if (existingSource) {
            // Update existing source
            existingSource[variable] = value;
        } else {
            // Create new source
            const newSource = {
                nombre_fuente: variable === 'nombre_fuente' ? text : '',
                declaracion_fuente: variable === 'declaracion_fuente' ? text : '',
                tipo_fuente: variable === 'tipo_fuente' ? value : '',
                genero_fuente: variable === 'genero_fuente' ? value : ''
            };
            newSource[variable] = value;
            window.data.analysis.original[category].fuentes.push(newSource);
        }
    }
    
    // Re-render the content to show the new annotation
    renderContent();
    
    // Add manual highlights to existing highlights
    addManualHighlights();
    
    // Update annotation indicators
    updateAnnotationIndicators();
}

// Function to apply highlight (this is now handled by addManualHighlights)
function applyHighlight(range, variable) {
    // This function is kept for compatibility but the actual highlighting
    // is now handled by addManualHighlights() which preserves existing highlights
    console.log('Highlight applied for variable:', variable);
}

// Function to update annotation indicators
function updateAnnotationIndicators() {
    // Add visual indicators to show which categories have manual annotations
    const categories = ['contenido', 'lenguaje', 'fuentes'];
    
    categories.forEach(category => {
        const header = document.querySelector(`[data-target="${category}-content"]`);
        if (header) {
            // Remove existing indicator
            const existingIndicator = header.querySelector('.annotation-indicator');
            if (existingIndicator) {
                existingIndicator.remove();
            }
            
            // Check if this category has manual annotations
            const hasAnnotations = annotations.some(annotation => annotation.category === category);
            
            if (hasAnnotations) {
                // Add indicator
                const indicator = document.createElement('span');
                indicator.className = 'annotation-indicator badge bg-warning ms-2';
                indicator.innerHTML = '<i class="fas fa-edit me-1"></i>Manual';
                indicator.title = 'Contiene anotaciones manuales';
                header.appendChild(indicator);
            }
        }
    });
}

// Function to save analysis and annotations to database
async function saveAnalysisToDatabase() {
    const saveButton = document.getElementById('save-analysis-btn');
    
    if (!saveButton) return;
    
    // Show saving state
    saveButton.classList.add('saving');
    saveButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Guardando...';
    saveButton.disabled = true;
    
    try {
        // Prepare data to save
        const saveData = {
            doc_id: window.data._id,
            analysis: window.data.analysis.original,
            annotations: annotations,
            highlight_html: {
                contenido_general: document.querySelector('#highlight-contenido .markup-area')?.innerHTML || '',
                lenguaje: document.querySelector('#highlight-lenguaje .markup-area')?.innerHTML || '',
                fuentes: document.querySelector('#highlight-fuentes .markup-area')?.innerHTML || ''
            },
            timestamp: new Date().toISOString()
        };
        
        // Send to backend
        const response = await fetch(window.api_url_save_annotations, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(saveData)
        });
        
        if (response.ok) {
            const result = await response.json();
            
            // Show success state
            saveButton.classList.remove('saving');
            saveButton.classList.add('saved');
            saveButton.innerHTML = '<i class="fas fa-check me-2"></i> Guardado';
            
            showNotification('Análisis y anotaciones guardados correctamente', 'success');
            
            // Update the document ID if it's a new document
            if (result.doc_id) {
                window.data._id = result.doc_id;
            }
            
            // Reset button after 3 seconds
            setTimeout(() => {
                saveButton.classList.remove('saved');
                saveButton.innerHTML = '<i class="fas fa-save me-2"></i> Guardar';
                saveButton.disabled = false;
            }, 3000);
            
        } else {
            throw new Error('Error al guardar en la base de datos');
        }
        
    } catch (error) {
        console.error('Error saving analysis:', error);
        
        // Show error state
        saveButton.classList.remove('saving');
        saveButton.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i> Error';
        saveButton.disabled = false;
        
        showNotification('Error al guardar el análisis: ' + error.message, 'error');
        
        // Reset button after 3 seconds
        setTimeout(() => {
            saveButton.innerHTML = '<i class="fas fa-save me-2"></i> Guardar';
        }, 3000);
    }
}

// Function to show notification
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show position-fixed`;
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

// ===========================================
// EXPORT FUNCTIONS
// ===========================================

// Make functions globally available
window.editAnalysis = editAnalysis;
window.generatePDF = generatePDF;
window.generateWord = generateWord;
window.finishAnalysis = finishAnalysis;

// Function to generate PDF
function generatePDF() {
    showNotification('Funcionalidad de PDF en desarrollo', 'info');
    // TODO: Implement PDF generation
}

// Function to generate Word document
function generateWord() {
    showNotification('Funcionalidad de Word en desarrollo', 'info');
    // TODO: Implement Word generation
}

// Function to finish analysis
function finishAnalysis() {
    if (confirm('¿Estás seguro de que quieres finalizar el análisis?')) {
        showNotification('Análisis finalizado', 'success');
        // TODO: Implement finish analysis logic
        // Could redirect to a summary page or close the analysis
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Render all content with converted values
    renderContent();
    
    // Setup collapsible panels
    setupCollapsiblePanels();
});
