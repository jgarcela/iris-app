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
            valueHtml = `<div class="value-list">${value.map((item, idx) => `<span class=\"value-item\">${item} <button class=\"btn btn-sm btn-link text-danger p-0 ms-1\" data-action=\"delete-item\" data-key=\"${key}\" data-index=\"${idx}\" title=\"Eliminar\"><i class=\"fas fa-times\"></i></button></span>`).join('')}</div>`;
        } else {
            valueHtml = '<span class="value-empty">No hay datos</span>';
        }
    } else {
        valueHtml = `<span class=\"value-single\">${value}</span>`;
    }
    
    return `
        <div class="variable-card">
            <div class="variable-header">
                <div class="variable-icon" style="background-color: ${color};">
                    <i class="fas fa-circle"></i>
                </div>
                <div class="variable-title">${title}</div>
                <div class=\"ms-auto d-flex gap-1\">
                    <button class=\"btn btn-sm btn-outline-primary\" data-action=\"add-item\" data-key=\"${key}\" title=\"Añadir\"><i class=\"fas fa-plus\"></i></button>
                    <button class=\"btn btn-sm btn-outline-secondary\" data-action=\"edit-variable\" data-key=\"${key}\" title=\"Editar\"><i class=\"fas fa-pen\"></i></button>
                </div>
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
            <div class=\"d-flex gap-1 mt-2\">
                <button class=\"btn btn-sm btn-outline-primary\" data-action=\"add-fuente-item\" data-index=\"${index}\" title=\"Añadir campo\"><i class=\"fas fa-plus\"></i></button>
                <button class=\"btn btn-sm btn-outline-secondary\" data-action=\"edit-fuente\" data-index=\"${index}\" title=\"Editar fuente\"><i class=\"fas fa-pen\"></i></button>
                <button class=\"btn btn-sm btn-outline-danger\" data-action=\"delete-fuente\" data-index=\"${index}\" title=\"Eliminar fuente\"><i class=\"fas fa-trash\"></i></button>
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
        bindContenidoGeneralHandlers();
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
                    <div class=\"variable-card\">
                        <div class=\"variable-header\">
                            <div class=\"variable-icon\" style=\"background-color: ${color};\">\n                                <i class=\"fas fa-circle\"></i>\n                            </div>
                            <div class=\"variable-title\">${key.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase())}</div>
                            <div class=\"ms-auto d-flex gap-1\">
                                <button class=\"btn btn-sm btn-outline-primary\" data-action=\"add-etiqueta\" data-key=\"${key}\" title=\"Añadir etiqueta\"><i class=\"fas fa-plus\"></i></button>
                                <button class=\"btn btn-sm btn-outline-primary\" data-action=\"add-ejemplo\" data-key=\"${key}\" title=\"Añadir ejemplo\"><i class=\"fas fa-quote-right\"></i></button>
                            </div>
                        </div>
                        <div class=\"variable-value\">
                            <div class=\"value-structure\">${subItems}</div>
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
        bindLenguajeHandlers();
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
        bindFuentesHandlers();
    }
}

function bindFuentesHandlers() {
    const container = document.getElementById('fuentes-sources');
    if (!container) return;
    // Eliminar fuente
    container.querySelectorAll('[data-action="delete-fuente"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const idx = parseInt(btn.getAttribute('data-index'), 10);
            const list = window.data.analysis.original.fuentes.fuentes || [];
            if (idx >= 0 && idx < list.length) {
                list.splice(idx, 1);
                renderContent();
            }
        });
    });
    // Editar fuente completa (prompt por campos)
    container.querySelectorAll('[data-action="edit-fuente"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const idx = parseInt(btn.getAttribute('data-index'), 10);
            const list = window.data.analysis.original.fuentes.fuentes || [];
            const fuente = list[idx];
            if (!fuente) return;
            openFuenteFormModal(fuente, (val) => {
                list[idx] = {
                    nombre_fuente: val.nombre_fuente,
                    declaracion_fuente: val.declaracion_fuente,
                    tipo_fuente: val.tipo_fuente,
                    genero_fuente: val.genero_fuente
                };
                renderContent();
            });
        });
    });
    // Añadir campo a fuente
    container.querySelectorAll('[data-action="add-fuente-item"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const idx = parseInt(btn.getAttribute('data-index'), 10);
            const list = window.data.analysis.original.fuentes.fuentes || [];
            const fuente = list[idx];
            if (!fuente) return;
            const campo = prompt('Campo a añadir (nombre_fuente, declaracion_fuente, tipo_fuente, genero_fuente):');
            if (campo === null) return;
            const valor = prompt('Valor del campo:');
            if (valor === null) return;
            const key = String(campo).trim();
            if (!key) return;
            fuente[key] = valor.trim();
            list[idx] = fuente;
            renderContent();
        });
    });
    // Añadir nueva fuente (botón general si no existe)
    let addButton = document.getElementById('add-new-fuente');
    if (!addButton) {
        addButton = document.createElement('button');
        addButton.id = 'add-new-fuente';
        addButton.className = 'btn btn-sm btn-primary my-2';
        addButton.textContent = 'Añadir nueva fuente';
        container.parentElement.insertBefore(addButton, container);
    }
    addButton.onclick = () => {
        openFuenteFormModal({}, (val) => {
            const list = window.data.analysis.original.fuentes.fuentes || [];
            list.push({
                nombre_fuente: val.nombre_fuente,
                declaracion_fuente: val.declaracion_fuente,
                tipo_fuente: val.tipo_fuente,
                genero_fuente: val.genero_fuente
            });
            window.data.analysis.original.fuentes.fuentes = list;
            renderContent();
        });
    };
}

function bindLenguajeHandlers() {
    const container = document.getElementById('lenguaje-variables');
    if (!container) return;
    // Añadir etiqueta: pide clave de etiqueta (número) o texto mapeado
    container.querySelectorAll('[data-action="add-etiqueta"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.getAttribute('data-key');
            const options = getValuesForVariable(key).map(v => ({ value: v.key, label: v.label }));
            openSelectModal({
                title: 'Añadir etiqueta',
                label: 'Selecciona etiqueta',
                options: options,
                multiple: false,
                initial: [],
                onSave: (val) => {
                    if (!val) return;
                    const store = window.data.analysis.original.lenguaje[key] || { etiqueta: [], ejemplos_articulo: [] };
                    store.etiqueta = store.etiqueta || [];
                    store.etiqueta.push(val);
                    window.data.analysis.original.lenguaje[key] = store;
                    renderContent();
                }
            });
        });
    });
    // Añadir ejemplo de artículo
    container.querySelectorAll('[data-action="add-ejemplo"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.getAttribute('data-key');
            openSingleInputModal('Añadir ejemplo', 'Texto del ejemplo', '', (val) => {
                if (!val) return;
                const store = window.data.analysis.original.lenguaje[key] || { etiqueta: [], ejemplos_articulo: [] };
                store.ejemplos_articulo = store.ejemplos_articulo || [];
                store.ejemplos_articulo.push(val);
                window.data.analysis.original.lenguaje[key] = store;
                renderContent();
            });
        });
    });
    // Eliminar chips dentro de value-structure (etiquetas y ejemplos)
    container.querySelectorAll('.sub-item .sub-value-list .sub-value-item').forEach((chip, idx) => {
        // Agregar botón de eliminar si no existe
        if (!chip.querySelector('button[data-action="delete-subitem"]')) {
            const delBtn = document.createElement('button');
            delBtn.className = 'btn btn-sm btn-link text-danger p-0 ms-1';
            delBtn.setAttribute('data-action', 'delete-subitem');
            delBtn.innerHTML = '<i class="fas fa-times"></i>';
            chip.appendChild(delBtn);
        }
    });
    container.querySelectorAll('button[data-action="delete-subitem"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const chip = e.currentTarget.closest('.sub-value-item');
            const subItem = e.currentTarget.closest('.sub-item');
            const label = subItem.querySelector('.sub-label');
            if (!chip || !subItem || !label) return;
            const subKey = label.textContent.replace(':','').trim().toLowerCase().replace(/\s+/g,'_');
            // Encontrar variable padre por proximidad (buscamos título en tarjeta)
            const card = e.currentTarget.closest('.variable-card');
            const title = card?.querySelector('.variable-title')?.textContent || '';
            const variableKey = title.toLowerCase().replace(/\s+/g,'_');
            const store = window.data.analysis.original.lenguaje[variableKey];
            if (!store) return;
            const list = Array.isArray(store[subKey]) ? store[subKey] : [];
            const text = chip.childNodes[0]?.nodeValue?.trim() || chip.textContent.trim();
            const idx = list.findIndex(v => String(v).trim() === text);
            if (idx >= 0) {
                list.splice(idx, 1);
                store[subKey] = list;
                window.data.analysis.original.lenguaje[variableKey] = store;
                renderContent();
            }
        });
    });
}

function bindContenidoGeneralHandlers() {
    const container = document.getElementById('contenido-variables');
    if (!container) return;
    container.querySelectorAll('[data-action="delete-item"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.getAttribute('data-key');
            const index = parseInt(btn.getAttribute('data-index'), 10);
            const arr = window.data.analysis.original.contenido_general[key];
            if (Array.isArray(arr)) {
                arr.splice(index, 1);
            } else {
                window.data.analysis.original.contenido_general[key] = '';
            }
            renderContent();
        });
    });
    container.querySelectorAll('[data-action="add-item"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.getAttribute('data-key');
            const values = getValuesForVariable(key).map(v => ({ value: v.key, label: v.label }));
            openSelectModal({
                title: 'Añadir valor',
                label: 'Selecciona un valor',
                options: values,
                multiple: false,
                initial: [],
                onSave: (val) => {
                    if (!val) return;
                    const current = window.data.analysis.original.contenido_general[key];
                    if (Array.isArray(current)) {
                        current.push(val);
                    } else if (current) {
                        window.data.analysis.original.contenido_general[key] = [current, val];
                    } else {
                        window.data.analysis.original.contenido_general[key] = [val];
                    }
                    renderContent();
                }
            });
        });
    });
    container.querySelectorAll('[data-action="edit-variable"]').forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.getAttribute('data-key');
            const current = window.data.analysis.original.contenido_general[key];
            const currentStr = Array.isArray(current) ? current.join(', ') : (current ?? '');
            const values = getValuesForVariable(key).map(v => ({ value: v.key, label: v.label }));
            const currentList = Array.isArray(current) ? current : (current ? [current] : []);
            openSelectModal({
                title: 'Editar valor',
                label: 'Selecciona valores',
                options: values,
                multiple: true,
                initial: currentList,
                onSave: (selected) => {
                    window.data.analysis.original.contenido_general[key] = Array.isArray(selected) ? selected : (selected ? [selected] : []);
                    renderContent();
                }
            });
        });
    });
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
    
    // Ensure actions popover exists
    ensureMarkActionsPopover();

    highlightElements.forEach(element => {
        // provenance defaults to ai for loaded highlights
        if (!element.dataset.provenance) {
            element.dataset.provenance = 'ai';
        }
        // Remove empty marks defensively
        if (!element.textContent || element.textContent.trim() === '') {
            const span = document.createElement('span');
            span.textContent = '';
            element.replaceWith(span);
            return;
        }
        // Add tooltip functionality
        element.addEventListener('mouseenter', function(e) {
            const classList = Array.from(this.classList);
            const colorClasses = classList.filter(cls => cls.startsWith('color-'));
            
            if (colorClasses.length > 0) {
                if (window.data && window.data.analysis && window.data.analysis.original) {
                    const analysis = window.data.analysis.original;
                    const highlightColorMap = window.highlight_color_map || {};
                    
                    // Reverse map color -> [variables]
                    const colorToVariables = {};
                    Object.keys(highlightColorMap).forEach(variableName => {
                        const color = highlightColorMap[variableName];
                        if (!colorToVariables[color]) colorToVariables[color] = [];
                        colorToVariables[color].push(variableName);
                    });
                    
                    const tooltipData = [];
                    
                    // Determine which category we're currently viewing
                    const currentHighlightBlock = this.closest('.highlight-block');
                    let currentCategory = null;
                    if (currentHighlightBlock) {
                        if (currentHighlightBlock.id === 'highlight-contenido') currentCategory = 'contenido_general';
                        else if (currentHighlightBlock.id === 'highlight-lenguaje') currentCategory = 'lenguaje';
                        else if (currentHighlightBlock.id === 'highlight-fuentes') currentCategory = 'fuentes';
                    }
                    
                    const isFuenteVariable = (v) => ['nombre_fuente','declaracion_fuente','tipo_fuente','genero_fuente'].includes(v);
                    
                    const fuentesFallback = {
                      'color-3': ['nombre_fuente'],
                      'color-4': ['declaracion_fuente']
                    };
                    for (const colorClass of colorClasses) {
                        let variablesForColor = colorToVariables[colorClass] || [];
                        // En Fuentes, priorizar también las variables de fallback aunque el color mapee a otras categorías
                        if (currentCategory === 'fuentes') {
                          const extra = fuentesFallback[colorClass] || [];
                          if (extra.length) {
                            const set = new Set([...(variablesForColor || []), ...extra]);
                            variablesForColor = Array.from(set);
                          }
                        }
                        for (const variableNameRaw of variablesForColor) {
                            let category = null;
                            if (analysis.contenido_general && Object.prototype.hasOwnProperty.call(analysis.contenido_general, variableNameRaw)) {
                                category = 'contenido_general';
                            } else if (analysis.lenguaje && Object.prototype.hasOwnProperty.call(analysis.lenguaje, variableNameRaw)) {
                                category = 'lenguaje';
                            } else if (analysis.fuentes && isFuenteVariable(variableNameRaw)) {
                                category = 'fuentes';
                            }
                            
                            if (!category) continue;
                            if (currentCategory && category !== currentCategory) continue;
                            
                            let varValue = null;
                            if (category === 'fuentes' && analysis.fuentes && Array.isArray(analysis.fuentes.fuentes)) {
                                const values = analysis.fuentes.fuentes
                                  .map(src => src ? src[variableNameRaw] : undefined)
                                  .filter(v => v !== undefined && v !== null && (Array.isArray(v) ? v.length > 0 : String(v).trim() !== ''));
                                if (values.length > 0) {
                                  // Aplanar y unificar valores
                                  const flat = values.flat ? values.flat() : ([]).concat(...values);
                                  // Convertir etiquetas si procede
                                  const converted = flat.map(item => convertValueToLabel(variableNameRaw, item));
                                  // Quitar duplicados manteniendo orden
                                  const unique = Array.from(new Set(converted.map(v => typeof v === 'string' ? v.trim() : v)));
                                  varValue = unique;
                                }
                            } else if (category === 'lenguaje') {
                                const langVar = analysis.lenguaje[variableNameRaw];
                                if (langVar && typeof langVar === 'object' && !Array.isArray(langVar) && langVar.etiqueta) {
                                    varValue = langVar.etiqueta;
                                } else {
                                    varValue = langVar;
                                }
                            } else if (category === 'contenido_general') {
                                varValue = analysis.contenido_general[variableNameRaw];
                            }
                            
                            if (varValue !== undefined && varValue !== null && (Array.isArray(varValue) ? varValue.length > 0 : true)) {
                                const prettyVar = variableNameRaw.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                                const convertedValue = Array.isArray(varValue) 
                                  ? varValue.map(item => convertValueToLabel(variableNameRaw, item)).join(', ')
                                  : convertValueToLabel(variableNameRaw, varValue);
                                tooltipData.push({ variable: prettyVar, value: convertedValue });
                            }
                        }
                    }
                    
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

        // Contextual actions on click
        element.addEventListener('click', (ev) => {
            ev.stopPropagation();
            const actions = document.getElementById('mark-actions-popover');
            if (!actions) return;
            const rect = element.getBoundingClientRect();
            actions.style.position = 'fixed';
            actions.style.left = (rect.left + Math.min(rect.width, 150)) + 'px';
            actions.style.top = (rect.top - 8) + 'px';
            actions.style.display = 'block';
            actions.dataset.markUid = assignMarkUid(element);

            // Resolve category and candidate variables
            const currentHighlightBlock = element.closest('.highlight-block');
            let currentCategory = null;
            if (currentHighlightBlock) {
                if (currentHighlightBlock.id === 'highlight-contenido') currentCategory = 'contenido_general';
                else if (currentHighlightBlock.id === 'highlight-lenguaje') currentCategory = 'lenguaje';
                else if (currentHighlightBlock.id === 'highlight-fuentes') currentCategory = 'fuentes';
            }
            actions.dataset.category = currentCategory || '';
            actions.dataset.variable = resolveVariablesForMark(element, currentCategory)[0] || '';
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
            const pattern = new RegExp(`(${escapedText})`, 'gi');
            highlightedText = highlightedText.replace(pattern, `<mark data-variable="${variable}">$1</mark>`);
        }
    });
    
    // Update the highlight text
    highlightTextElement.innerHTML = highlightedText;
    
    // Process highlights for tooltips
    processHighlights();
}

// ------- Mark actions popover -------
function ensureMarkActionsPopover() {
    if (document.getElementById('mark-actions-popover')) return;
    const div = document.createElement('div');
    div.id = 'mark-actions-popover';
    div.style.cssText = 'display:none; background:#fff; border:1px solid #dee2e6; border-radius:6px; box-shadow:0 4px 12px rgba(0,0,0,0.1); padding:6px; z-index:10000;';
    div.innerHTML = `
      <div class="btn-group">
        <button class="btn btn-sm btn-outline-primary" data-action="mark-edit" title="Editar"><i class="fas fa-pen"></i></button>
        <button class="btn btn-sm btn-outline-success" data-action="mark-accept" title="Aceptar"><i class="fas fa-check"></i></button>
        <button class="btn btn-sm btn-outline-danger" data-action="mark-delete" title="Eliminar"><i class="fas fa-trash"></i></button>
      </div>
    `;
    document.body.appendChild(div);
    document.addEventListener('click', (e) => {
        const pop = document.getElementById('mark-actions-popover');
        if (!pop) return;
        if (pop.style.display === 'block' && !pop.contains(e.target)) {
            pop.style.display = 'none';
        }
    });
    div.addEventListener('click', (e) => {
        const btn = e.target.closest('button[data-action]');
        if (!btn) return;
        const action = btn.getAttribute('data-action');
        const pop = document.getElementById('mark-actions-popover');
        const mark = findMarkByUid(pop.dataset.markUid);
        if (!mark) return;
        if (action === 'mark-edit') {
            handleEditMark(mark, pop.dataset.category);
        } else if (action === 'mark-accept') {
            mark.classList.add('accepted');
            mark.dataset.status = 'accepted';
            // add visual tick if not present
            if (!mark.nextElementSibling || !mark.nextElementSibling.classList || !mark.nextElementSibling.classList.contains('tick-icon')) {
                const tick = document.createElement('i');
                tick.className = 'fa fa-check tick-icon ms-1';
                tick.title = 'Este fragmento ha sido aceptado';
                mark.insertAdjacentElement('afterend', tick);
            }
            pop.style.display = 'none';
        } else if (action === 'mark-delete') {
            // Delete only DOM, keep data untouched
            unwrapMark(mark);
            pop.style.display = 'none';
        }
    });
}

function assignMarkUid(mark) {
    if (!mark.dataset.uid) {
        mark.dataset.uid = 'm_' + Math.random().toString(36).slice(2);
    }
    return mark.dataset.uid;
}

function findMarkByUid(uid) {
    if (!uid) return null;
    return document.querySelector(`mark[data-uid="${uid}"]`);
}

function unwrapMark(mark) {
    const span = document.createElement('span');
    span.textContent = mark.textContent;
    mark.replaceWith(span);
}

function resolveVariablesForMark(mark, currentCategory) {
    const classList = Array.from(mark.classList);
    const colorClasses = classList.filter(cls => cls.startsWith('color-'));
    const highlightColorMap = window.highlight_color_map || {};
    const colorToVariables = {};
    Object.keys(highlightColorMap).forEach(variableName => {
        const color = highlightColorMap[variableName];
        if (!colorToVariables[color]) colorToVariables[color] = [];
        colorToVariables[color].push(variableName);
    });
    const candidates = [];
    for (const color of colorClasses) {
        const vars = colorToVariables[color] || [];
        for (const v of vars) {
            if (!currentCategory) { candidates.push(v); continue; }
            if (currentCategory === 'fuentes' && ['nombre_fuente','declaracion_fuente','tipo_fuente','genero_fuente'].includes(v)) candidates.push(v);
            if (currentCategory === 'lenguaje' && window.data.analysis.original.lenguaje && Object.prototype.hasOwnProperty.call(window.data.analysis.original.lenguaje, v)) candidates.push(v);
            if (currentCategory === 'contenido_general' && window.data.analysis.original.contenido_general && Object.prototype.hasOwnProperty.call(window.data.analysis.original.contenido_general, v)) candidates.push(v);
        }
    }
    return Array.from(new Set(candidates));
}

function handleEditMark(mark, category) {
    const candidates = resolveVariablesForMark(mark, category);
    const variable = candidates[0] || '';
    if (!variable) return;
    const options = getValuesForVariable(variable).map(v => ({ value: v.key, label: v.label }));
    openSelectModal({
        title: 'Editar anotación',
        label: 'Selecciona valor',
        options,
        multiple: false,
        initial: [],
        onSave: (val) => {
            if (!val) return;
            // Integrate into data similar to integrateAnnotationIntoAnalysis
            const text = mark.textContent.trim();
            if (category === 'contenido_general') {
                const obj = window.data.analysis.original.contenido_general;
                if (!obj[variable]) obj[variable] = [];
                if (Array.isArray(obj[variable])) obj[variable].push(text); else obj[variable] = [obj[variable], text];
            } else if (category === 'lenguaje') {
                const obj = window.data.analysis.original.lenguaje;
                if (!obj[variable]) obj[variable] = { etiqueta: [], ejemplos_articulo: [] };
                obj[variable].etiqueta = obj[variable].etiqueta || [];
                obj[variable].ejemplos_articulo = obj[variable].ejemplos_articulo || [];
                obj[variable].etiqueta.push(val);
                if (text) obj[variable].ejemplos_articulo.push(text);
            } else if (category === 'fuentes') {
                const obj = window.data.analysis.original.fuentes;
                obj.fuentes = obj.fuentes || [];
                // Create or update first fuente matching text
                let f = obj.fuentes.find(s => (s.nombre_fuente === text || s.declaracion_fuente === text));
                if (!f) { f = {}; obj.fuentes.push(f); }
                f[variable] = val;
                if (variable === 'nombre_fuente') f.nombre_fuente = text;
                if (variable === 'declaracion_fuente') f.declaracion_fuente = text;
            }
            mark.dataset.status = 'accepted';
            mark.classList.add('accepted');
            renderContent();
        }
    });
}

function removeMarkFromData(mark, category) {
    const text = (mark.textContent || '').trim();
    if (!text || !category) return;
    const data = window.data.analysis.original;
    if (category === 'contenido_general') {
        const obj = data.contenido_general || {};
        Object.keys(obj).forEach(k => {
            if (Array.isArray(obj[k])) {
                const idx = obj[k].findIndex(v => String(v).trim() === text);
                if (idx >= 0) obj[k].splice(idx, 1);
            }
        });
    } else if (category === 'lenguaje') {
        const obj = data.lenguaje || {};
        Object.keys(obj).forEach(k => {
            if (obj[k] && Array.isArray(obj[k].ejemplos_articulo)) {
                const idx = obj[k].ejemplos_articulo.findIndex(v => String(v).trim() === text);
                if (idx >= 0) obj[k].ejemplos_articulo.splice(idx, 1);
            }
        });
    } else if (category === 'fuentes') {
        const obj = data.fuentes || {};
        if (Array.isArray(obj.fuentes)) {
            obj.fuentes = obj.fuentes.filter(f => (f.nombre_fuente !== text && f.declaracion_fuente !== text));
        }
    }
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
            attachHighlightSelectionHandler();
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

    detachHighlightSelectionHandler();
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
                    
                    // Show text analysis panel only for analysis categories
                    if (targetId === 'contenido-content' || targetId === 'lenguaje-content' || targetId === 'fuentes-content') {
                        showTextAnalysisPanel();
                        
                        // Enable edit button when a category is opened
                        enableEditButton();
                        
                        // Re-render content to include any new manual annotations
                        renderContent();
                        
                        // Show corresponding highlight block for the category
                        if (targetId === 'contenido-content') {
                            showHighlightBlock('contenido');
                        } else if (targetId === 'lenguaje-content') {
                            showHighlightBlock('lenguaje');
                        } else if (targetId === 'fuentes-content') {
                            showHighlightBlock('fuentes');
                        }
                    } else {
                        // For non-analysis categories, just re-render content
                        renderContent();
                    }
                } else {
                    // Closing panel
                    content.style.display = 'none';
                    icon.classList.remove('fa-chevron-up');
                    icon.classList.add('fa-chevron-down');
                    
                    // Hide highlights and show plain text
                    hideHighlights();
                    
                    // Check if any other panels are still open, if not, show instructions
                    checkAndShowInstructions();
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

// Function to show text analysis panel
function showTextAnalysisPanel() {
    const instructionsPanel = document.querySelector('.plain-text');
    const textAnalysisPanel = document.querySelector('.text-analysis-panel');
    
    if (instructionsPanel && textAnalysisPanel) {
        instructionsPanel.style.display = 'none';
        textAnalysisPanel.style.display = 'block';
    }
}

// Function to check if any analysis category panels are open and show instructions if none are
function checkAndShowInstructions() {
    const analysisCategoryIds = ['contenido-content', 'lenguaje-content', 'fuentes-content'];
    const instructionsPanel = document.querySelector('.plain-text');
    const textAnalysisPanel = document.querySelector('.text-analysis-panel');
    
    let anyAnalysisPanelOpen = false;
    analysisCategoryIds.forEach(id => {
        const content = document.getElementById(id);
        if (content && content.style.display === 'block') {
            anyAnalysisPanelOpen = true;
        }
    });
    
    if (!anyAnalysisPanelOpen && instructionsPanel && textAnalysisPanel) {
        instructionsPanel.style.display = 'block';
        textAnalysisPanel.style.display = 'none';
        // Disable edit button when no categories are open
        disableEditButton();
    }
}

// Function to enable edit button
function enableEditButton() {
    const editButton = document.getElementById('edit-analysis-btn');
    if (editButton) {
        editButton.disabled = false;
    }
}

// Function to disable edit button
function disableEditButton() {
    const editButton = document.getElementById('edit-analysis-btn');
    if (editButton) {
        editButton.disabled = true;
    }
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
            <div id="composite-controls" style="display:none" class="mb-3"></div>
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
    
    const leftPanel = document.querySelector('.col-md-4');
    leftPanel.insertBefore(annotationPanel, leftPanel.children[2]);
    
    // Setup annotation form handlers
    setupAnnotationHandlers();
}

// Function to hide annotation controls
function hideAnnotationControls() {
    const annotationPanel = document.getElementById('annotation-panel');
    
    if (annotationPanel) annotationPanel.remove();
}

// Function to enable text selection
function enableTextSelection() {
    // Prefer the automatic analysis highlight container
    const analysisText = document.querySelector('.highlight-text') || document.querySelector('.analysis-text');
    if (analysisText) {
        analysisText.addEventListener('mouseup', handleTextSelection);
        analysisText.addEventListener('keyup', handleTextSelection);
        analysisText.style.cursor = 'text';
        
        // Add annotation mode class to body
        document.body.classList.add('annotation-mode');
        
        // Detach highlight selection handler to prevent modal
        detachHighlightSelectionHandler();
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
        
        // Reattach highlight selection handler
        attachHighlightSelectionHandler();
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
    // Try to update any preview placeholders that might exist in template or JS panel
    if (currentSelection && currentSelection.text) {
        const el1 = document.getElementById('selected-text-content');
        if (el1) el1.textContent = currentSelection.text;
        const el2 = document.getElementById('selected-text-preview');
        if (el2) el2.textContent = currentSelection.text;
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
    const composite = document.getElementById('composite-controls');
    
    // Clear variable and value selects
    variableSelect.innerHTML = '<option value="">Selecciona variable</option>';
    valueSelect.innerHTML = '<option value="">Selecciona valor</option>';
    if (composite) { composite.style.display = 'none'; composite.innerHTML = ''; }
    
    if (category) {
        // Get variables for the selected category from config.ini
        let variables = getVariablesForCategory(category);
        // Restrict Fuentes to declaracion_fuente (the others appear as composite controls)
        if (category === 'fuentes') {
            variables = ['declaracion_fuente'];
        }
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
    const composite = document.getElementById('composite-controls');
    
    // Clear value select
    valueSelect.innerHTML = '<option value="">Selecciona valor</option>';
    if (composite) { composite.style.display = 'none'; composite.innerHTML = ''; }
    
    if (variable) {
        // Get values for the selected variable from config.ini
        const values = getValuesForVariable(variable);
        
        values.forEach(value => {
            const option = document.createElement('option');
            option.value = value.key;
            option.textContent = value.label;
            valueSelect.appendChild(option);
        });

        // Default "Sí" for declaracion_fuente
        if (variable === 'declaracion_fuente') {
            // Try to find an option labeled "Sí" and select it
            const siOption = Array.from(valueSelect.options).find(opt => /sí/i.test(opt.textContent || ''));
            if (siOption) {
                valueSelect.value = siOption.value;
            }
        }

        // Show composite controls for declaracion_fuente
        if (variable === 'declaracion_fuente' && composite) {
            const nombreVals = getValuesForVariable('nombre_fuente');
            const generoVals = getValuesForVariable('genero_fuente');
            const tipoVals = getValuesForVariable('tipo_fuente');
            composite.innerHTML = `
                <div class="row g-2">
                    <div class="col-12">
                        <label class="form-label small">Nombre de la fuente</label>
                        <select class="form-select form-select-sm" id="composite-nombre-fuente">
                            ${nombreVals.map(v => `<option value="${v.key}">${v.label}</option>`).join('')}
                        </select>
                    </div>
                    <div class="col-12">
                        <label class="form-label small">Género de la fuente</label>
                        <select class="form-select form-select-sm" id="composite-genero-fuente">
                            ${generoVals.map(v => `<option value="${v.key}">${v.label}</option>`).join('')}
                        </select>
                    </div>
                    <div class="col-12">
                        <label class="form-label small">Tipo de fuente</label>
                        <select class="form-select form-select-sm" id="composite-tipo-fuente">
                            <option value="">Seleccionar tipo...</option>
                            ${tipoVals.map(v => `<option value="${v.key}">${v.label}</option>`).join('')}
                        </select>
                    </div>
                </div>`;
            composite.style.display = 'block';
        }
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
        // Match manual analysis options
        'genero_fuente': [
            { key: '1', label: 'No hay' },
            { key: '2', label: 'Sí, hombre' },
            { key: '3', label: 'Sí, mujer' },
            { key: '4', label: 'Sí, mujer y hombre' }
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
    
    // Declaración de fuente: guardar compuestos (declaración + nombre + género + tipo)
    if (category === 'fuentes' && variable === 'declaracion_fuente') {
        const nombreFuenteValue = document.getElementById('composite-nombre-fuente')?.value;
        const generoFuenteValue = document.getElementById('composite-genero-fuente')?.value;
        const tipoFuenteValue = document.getElementById('composite-tipo-fuente')?.value;
        const baseId = Date.now();
        const anns = [];
        anns.push({ id: baseId, text: currentSelection.text, category, variable, value, timestamp: new Date().toISOString() });
        if (nombreFuenteValue) anns.push({ id: baseId+1, text: currentSelection.text, category, variable: 'nombre_fuente', value: nombreFuenteValue, timestamp: new Date().toISOString() });
        if (generoFuenteValue) anns.push({ id: baseId+2, text: currentSelection.text, category, variable: 'genero_fuente', value: generoFuenteValue, timestamp: new Date().toISOString() });
        if (tipoFuenteValue) anns.push({ id: baseId+3, text: currentSelection.text, category, variable: 'tipo_fuente', value: tipoFuenteValue, timestamp: new Date().toISOString() });
        anns.forEach(a => { annotations.push(a); integrateAnnotationIntoAnalysis(a); });
        applyHighlight(currentSelection.range, variable);
    } else {
        // Create single annotation
        const annotation = {
            text: currentSelection.text,
            category: category,
            variable: variable,
            value: value,
            timestamp: new Date().toISOString()
        };
        annotations.push(annotation);
        integrateAnnotationIntoAnalysis(annotation);
        applyHighlight(currentSelection.range, variable);
    }
    
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
    if (!range || !variable) return;
    const mark = document.createElement('mark');
    mark.setAttribute('data-variable', variable);
    try {
        // Prefer surroundContents to preserve selection boundaries when possible
        const selectedText = range.toString();
        if (!selectedText) return;
        mark.textContent = selectedText;
        range.deleteContents();
        range.insertNode(mark);
    } catch (e) {
        // Fallback: extract and insert
        try {
            const contents = range.extractContents();
            mark.appendChild(contents);
            range.insertNode(mark);
        } catch (_) { /* noop */ }
    }
    // Clear selection and re-process highlights so tooltips and actions bind
    if (window.getSelection) {
        window.getSelection().removeAllRanges();
    }
    setTimeout(() => {
        processHighlights();
    }, 0);
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
        const headers = {
            'Content-Type': 'application/json',
        };
        
        // Add user headers if available
        if (window.current_user && window.current_user._id) {
            headers['X-User-ID'] = window.current_user._id;
            headers['X-User-Email'] = window.current_user.email || 'anonymous@example.com';
        }
        
        const response = await fetch(window.api_url_save_annotations, {
            method: 'POST',
            headers: headers,
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
    setupEditModalHelpers();
});

// Modal helpers
let editModalInstance = null;
function setupEditModalHelpers() {
    const modalEl = document.getElementById('editModal');
    if (!modalEl) return;
    editModalInstance = window.bootstrap ? new window.bootstrap.Modal(modalEl) : null;
}

function openSingleInputModal(title, label, initialValue, onSave) {
    // Don't open modal if we're in annotation mode
    if (document.body.classList.contains('annotation-mode')) {
        console.log('Modal blocked - in annotation mode');
        return;
    }
    
    const titleEl = document.getElementById('editModalTitle');
    const singleGroup = document.getElementById('singleInputGroup');
    const selectGroup = document.getElementById('selectInputGroup');
    const singleLabel = document.getElementById('singleInputLabel');
    const singleInput = document.getElementById('singleInput');
    const fuenteForm = document.getElementById('fuenteForm');
    const saveBtn = document.getElementById('editModalSave');
    if (!titleEl || !singleGroup || !singleLabel || !singleInput || !saveBtn) return;
    titleEl.textContent = title;
    singleGroup.style.display = 'block';
    selectGroup && (selectGroup.style.display = 'none');
    fuenteForm && (fuenteForm.style.display = 'none');
    singleLabel.textContent = label;
    singleInput.value = initialValue ?? '';
    saveBtn.onclick = () => {
        const val = singleInput.value.trim();
        if (onSave) onSave(val);
        const modalEl = document.getElementById('editModal');
        if (window.bootstrap && modalEl) window.bootstrap.Modal.getInstance(modalEl)?.hide();
    };
    const modalEl = document.getElementById('editModal');
    if (window.bootstrap && modalEl) window.bootstrap.Modal.getOrCreateInstance(modalEl).show();
}

function openFuenteFormModal(initial, onSave) {
    // Don't open modal if we're in annotation mode
    if (document.body.classList.contains('annotation-mode')) {
        console.log('Modal blocked - in annotation mode');
        return;
    }
    
    const titleEl = document.getElementById('editModalTitle');
    const singleGroup = document.getElementById('singleInputGroup');
    const selectGroup = document.getElementById('selectInputGroup');
    const fuenteForm = document.getElementById('fuenteForm');
    const saveBtn = document.getElementById('editModalSave');
    const nombre = document.getElementById('fuenteNombre');
    const declaracion = document.getElementById('fuenteDeclaracion');
    const tipo = document.getElementById('fuenteTipo');
    const genero = document.getElementById('fuenteGenero');
    if (!titleEl || !fuenteForm || !saveBtn || !nombre || !declaracion || !tipo || !genero) return;
    titleEl.textContent = 'Editar fuente';
    singleGroup && (singleGroup.style.display = 'none');
    selectGroup && (selectGroup.style.display = 'none');
    fuenteForm.style.display = 'block';
    nombre.value = initial?.nombre_fuente ?? '';
    declaracion.value = initial?.declaracion_fuente ?? '';
    tipo.value = initial?.tipo_fuente ?? '';
    genero.value = initial?.genero_fuente ?? '';
    saveBtn.onclick = () => {
        const val = {
            nombre_fuente: nombre.value.trim(),
            declaracion_fuente: declaracion.value.trim(),
            tipo_fuente: tipo.value.trim(),
            genero_fuente: genero.value.trim()
        };
        if (onSave) onSave(val);
        const modalEl = document.getElementById('editModal');
        if (window.bootstrap && modalEl) window.bootstrap.Modal.getInstance(modalEl)?.hide();
    };
    const modalEl = document.getElementById('editModal');
    if (window.bootstrap && modalEl) window.bootstrap.Modal.getOrCreateInstance(modalEl).show();
}

function openSelectModal({ title, label, options, multiple = false, initial = [], onSave }) {
    // Don't open modal if we're in annotation mode
    if (document.body.classList.contains('annotation-mode')) {
        console.log('Modal blocked - in annotation mode');
        return;
    }
    
    const titleEl = document.getElementById('editModalTitle');
    const singleGroup = document.getElementById('singleInputGroup');
    const selectGroup = document.getElementById('selectInputGroup');
    const fuenteForm = document.getElementById('fuenteForm');
    const selectInput = document.getElementById('selectInput');
    const selectLabel = document.getElementById('selectInputLabel');
    const selectHelp = document.getElementById('selectHelp');
    const saveBtn = document.getElementById('editModalSave');
    if (!titleEl || !selectGroup || !selectInput || !saveBtn || !selectLabel) return;
    titleEl.textContent = title;
    singleGroup && (singleGroup.style.display = 'none');
    fuenteForm && (fuenteForm.style.display = 'none');
    selectGroup.style.display = 'block';
    selectLabel.textContent = label;
    selectInput.innerHTML = '';
    selectInput.multiple = !!multiple;
    if (selectHelp) selectHelp.style.display = multiple ? 'block' : 'none';
    // options: array of { value, label }
    (options || []).forEach(opt => {
        const o = document.createElement('option');
        o.value = String(opt.value);
        o.textContent = opt.label;
        if (Array.isArray(initial) && initial.map(String).includes(String(opt.value))) {
            o.selected = true;
        }
        selectInput.appendChild(o);
    });
    saveBtn.onclick = () => {
        let val;
        if (multiple) {
            val = Array.from(selectInput.selectedOptions).map(o => o.value);
        } else {
            val = selectInput.value;
        }
        if (onSave) onSave(val);
        const modalEl = document.getElementById('editModal');
        if (window.bootstrap && modalEl) window.bootstrap.Modal.getInstance(modalEl)?.hide();
    };
    const modalEl = document.getElementById('editModal');
    if (window.bootstrap && modalEl) window.bootstrap.Modal.getOrCreateInstance(modalEl).show();
}

// ================================
// Selection → Add Annotation in highlight view
// ================================
let highlightSelectionHandlerBound = false;
function attachHighlightSelectionHandler() {
    if (highlightSelectionHandlerBound) return;
    const area = document.querySelector('.highlight-text .highlight-block[style*="display: block"] .markup-area') || document.querySelector('.highlight-text .markup-area');
    if (!area) return;
    
    // Don't attach if we're in annotation mode
    if (document.body.classList.contains('annotation-mode')) return;
    const handler = function(e) {
        const sel = window.getSelection();
        if (!sel || sel.isCollapsed) return;
        if (!area.contains(sel.anchorNode)) return;
        const text = sel.toString().trim();
        if (!text) return;
        
        // Use the new manual annotation panel system only if in edit mode
        if (typeof showAnnotationPanel === 'function' && document.body.classList.contains('edit-mode')) {
            showAnnotationPanel(text, sel.getRangeAt(0));
        } else {
            // Fallback to old system if new system not available
            // Determine current category from visible block
            const visibleBlock = document.querySelector('.highlight-text .highlight-block[style*="display: block"]');
            let currentCategory = null;
            if (visibleBlock) {
                if (visibleBlock.id === 'highlight-contenido') currentCategory = 'contenido_general';
                else if (visibleBlock.id === 'highlight-lenguaje') currentCategory = 'lenguaje';
                else if (visibleBlock.id === 'highlight-fuentes') currentCategory = 'fuentes';
            }
            // Step 1: pick variable for category
            const variableOptions = getVariablesForCategory(currentCategory).map(v => ({ value: v, label: v.replace(/_/g,' ').replace(/\b\w/g, l => l.toUpperCase()) }));
            openSelectModal({
                title: 'Nueva anotación',
                label: 'Variable',
                options: variableOptions,
                multiple: false,
                initial: [],
                onSave: (variable) => {
                    if (!variable) return;
                    // Step 2: pick value for variable
                    const valueOptions = getValuesForVariable(variable).map(v => ({ value: v.key, label: v.label }));
                    openSelectModal({
                        title: 'Selecciona valor',
                        label: 'Valor',
                        options: valueOptions,
                        multiple: false,
                        initial: [],
                        onSave: (value) => {
                            if (!value) return;
                            // Integrate into data
                            const annotation = { text, category: currentCategory, variable, value };
                            integrateAnnotationIntoAnalysis(annotation);
                            // Wrap selection in mark with default styling
                            const range = sel.getRangeAt(0);
                            const mark = document.createElement('mark');
                            mark.setAttribute('data-variable', variable);
                            mark.textContent = text;
                            try {
                                range.deleteContents();
                                range.insertNode(mark);
                            } catch (_) {}
                            window.getSelection().removeAllRanges();
                            // Re-run highlight processing
                            processHighlights();
                        }
                    });
                }
            });
        }
    };
    area.addEventListener('mouseup', handler);
    area.dataset.highlightSelectionHandler = 'true';
    highlightSelectionHandlerBound = true;
}

function detachHighlightSelectionHandler() {
    const area = document.querySelector('.highlight-text .markup-area');
    if (!area) return;
    if (area.dataset.highlightSelectionHandler) {
        area.replaceWith(area.cloneNode(true));
        delete area.dataset.highlightSelectionHandler;
    }
    highlightSelectionHandlerBound = false;
}
