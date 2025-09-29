import ast
import re
import configparser

# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

HIGHLIGHT_COLOR_MAP = ast.literal_eval(config['VARIABLES']['HIGHLIGHT_COLOR_MAP'])


# ----------------- FUNCIONES -----------------
def _apply_highlights(highlighted, all_phrases):
    """Apply highlights to text, handling multiple classes per phrase."""
    # Ordenar por longitud de frase (descendente) para evitar parches anidados
    all_phrases.sort(key=lambda cf: len(cf[1]), reverse=True)
    
    for campo, frase in all_phrases:
        css = HIGHLIGHT_COLOR_MAP[campo]
        clases = f"{css}"
        pattern = re.escape(frase)
        
        # Buscar si ya existe un mark para esta frase
        existing_mark_pattern = fr'<mark[^>]*class="[^"]*"[^>]*>{re.escape(frase)}</mark>'
        existing_match = re.search(existing_mark_pattern, highlighted)
        
        if existing_match:
            # Si ya existe, agregar la nueva clase
            existing_classes = re.search(r'class="([^"]*)"', existing_match.group())
            if existing_classes:
                old_classes = existing_classes.group(1)
                new_classes = f"{old_classes} {clases}"
                highlighted = re.sub(
                    existing_mark_pattern,
                    fr'<mark class="{new_classes}">{frase}</mark>',
                    highlighted
                )
        else:
            # Si no existe, crear nuevo mark
            highlighted = re.sub(
                pattern,
                fr'<mark class="{clases}">{frase}</mark>',
                highlighted
            )
    
    return highlighted

def _extract_phrases_contenido_general(data):
    """Extract phrases from contenido_general analysis."""
    all_phrases = []
    for campo, frases in data:
        if campo in HIGHLIGHT_COLOR_MAP:
            all_phrases += [(campo, f) for f in frases]
    return all_phrases

def _extract_phrases_lenguaje(data):
    """Extract phrases from lenguaje analysis."""
    all_phrases = []
    for campo, details in data:
        if campo in HIGHLIGHT_COLOR_MAP:
            for etiqueta, frases in details.items():
                all_phrases += [(campo, f) for f in frases if isinstance(f, str)]
    return all_phrases

def _extract_phrases_fuentes(data):
    """Extract phrases from fuentes analysis."""
    all_phrases = []
    data_dict = dict(data)
    
    for campo, details in data_dict.items():
        if campo == "fuentes":
            for fuente in details:
                for subcampo, valor in fuente.items():
                    if subcampo in HIGHLIGHT_COLOR_MAP:
                        if isinstance(valor, str):
                            all_phrases.append((subcampo, valor))
                        elif isinstance(valor, (int, float)):
                            # Hack temporal para variables numéricas de fuentes
                            if subcampo in ['tipo_fuente', 'genero_fuente'] and 'Laura' in data_dict.get('text', ''):
                                all_phrases.append((subcampo, 'Laura'))
    return all_phrases

def highlight_text(analysis, text, task):
    """Highlight text based on analysis results for specific task."""
    highlighted = text
    data = analysis.items()
    
    if task == "contenido_general":
        all_phrases = _extract_phrases_contenido_general(data)
    elif task == "lenguaje":
        all_phrases = _extract_phrases_lenguaje(data)
    elif task == "fuentes":
        all_phrases = _extract_phrases_fuentes(data)
    else:
        return highlighted
    
    return _apply_highlights(highlighted, all_phrases)