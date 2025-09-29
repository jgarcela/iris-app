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

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Render all content with converted values
    renderContent();
    
    // Setup collapsible panels
    setupCollapsiblePanels();
});
