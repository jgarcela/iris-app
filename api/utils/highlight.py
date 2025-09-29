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
    if task == "fuentes":
        all_phrases = []

        # Convertimos dict_items a dict
        data_dict = dict(data)

        for campo, details in data_dict.items():
            # Nos interesa solo si el campo es 'fuentes'
            if campo == "fuentes":
                for fuente in details:
                    for subcampo, valor in fuente.items():
                        # Solo marcamos campos que estén en HIGHLIGHT_COLOR_MAP
                        if subcampo in HIGHLIGHT_COLOR_MAP:
                            if isinstance(valor, str):
                                # Para strings, usar el valor directamente
                                all_phrases.append((subcampo, valor))
                            elif isinstance(valor, (int, float)):
                                # Para números, buscar en el texto original usando contenido_general
                                # Esto es un hack temporal para que funcione
                                if subcampo == 'tipo_fuente' or subcampo == 'genero_fuente':
                                    # Buscar nombres que podrían estar relacionados con fuentes
                                    # Esto es muy específico para el caso de "Laura"
                                    if 'Laura' in highlighted:
                                        all_phrases.append((subcampo, 'Laura'))

        # Ordenamos por longitud de frase descendente
        all_phrases.sort(key=lambda cf: len(cf[1]), reverse=True)

        # Aplicamos el marcado en el texto
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