import ast
import re
import configparser

# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

HIGHLIGHT_COLOR_MAP = ast.literal_eval(config['VARIABLES']['HIGHLIGHT_COLOR_MAP'])


# ----------------- FUNCIONES -----------------
def highlight_contenido_general(analysis_contenido_general, text):

    highlighted = text

    # Para evitar parches anidados, procesamos primero las frases más largas
    all_phrases = []
    for campo, frases in analysis_contenido_general.items():
        # solo campos que tengan mapeo de color
        if campo in HIGHLIGHT_COLOR_MAP:
            all_phrases += [(campo, f) for f in frases]

    # Ordenar por longitud de frase (descendente)
    all_phrases.sort(key=lambda cf: len(cf[1]), reverse=True)

    # Reemplazar cada frase en el texto
    for campo, frase in all_phrases:
        css = HIGHLIGHT_COLOR_MAP[campo]
        clases = f"{css}"
        # re.escape para no romper la regex; sin \b para capturar espacios/puntuación
        pattern = re.escape(frase)
        highlighted = re.sub(
            pattern,
            fr'<mark class="{clases}">{frase}</mark>',
            highlighted
        )
    
    return highlighted