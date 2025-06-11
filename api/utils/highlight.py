import ast
import re
import configparser

# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

HIGHLIGHT_COLOR_MAP = ast.literal_eval(config['VARIABLES']['HIGHLIGHT_COLOR_MAP'])


# ----------------- FUNCIONES -----------------
def highlight_text(analysis, text, task):

    highlighted = text
    data = analysis.items()

    if task == "contenido_general":
        # Para evitar parches anidados, procesamos primero las frases más largas
        all_phrases = []
        for campo, frases in data:
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
    if task == "lenguaje":
        # Para evitar parches anidados, procesamos primero las frases más largas
        all_phrases = []
        for campo, details in data:
            for etiqueta, frases in details.items():
                # solo campos que tengan mapeo de color
                if campo in HIGHLIGHT_COLOR_MAP:
                    all_phrases += [(campo, f) for f in frases if isinstance(f, str)]

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
    if task == "fuentes":
        all_phrases = []

        # Convertimos dict_items a dict
        data_dict = dict(data)

        for campo, details in data_dict.items():
            # Nos interesa solo si el campo es 'fuentes'
            if campo == "fuentes":
                for fuente in details:
                    for subcampo, valor in fuente.items():
                        # Solo marcamos campos que estén en HIGHLIGHT_COLOR_MAP y cuyo valor sea str
                        if subcampo in HIGHLIGHT_COLOR_MAP and isinstance(valor, str):
                            all_phrases.append((subcampo, valor))

        # Ordenamos por longitud de frase descendente
        all_phrases.sort(key=lambda cf: len(cf[1]), reverse=True)

        # Aplicamos el marcado en el texto
        for campo, frase in all_phrases:
            css = HIGHLIGHT_COLOR_MAP[campo]
            clases = f"{css}"
            pattern = re.escape(frase)
            highlighted = re.sub(
                pattern,
                fr'<mark class="{clases}">{frase}</mark>',
                highlighted
            )

    
    return highlighted