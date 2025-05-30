# web/analysis.py
import json
import re
from flask import Blueprint, render_template, request, jsonify, session
import requests
from flask_babel import get_locale
import configparser
import ast

# ----------------- BLUEPRINT -----------------
bp = Blueprint(
    'analysis',
    __name__,
    url_prefix='/analysis'
)

# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

WEB_HOST = config['WEB']['HOST']
WEB_PORT = config['WEB']['PORT']
DEBUG = config['WEB'].getboolean('DEBUG')
API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']
API_HEADERS_str = config['API']['HEADERS']
API_HEADERS = ast.literal_eval(API_HEADERS_str)
ENDPOINT_ANALYSIS = config['API']['ENDPOINT_ANALYSIS']
ENDPOINT_ANALYSIS_ANALYZE = config['API']['ENDPOINT_ANALYSIS_ANALYZE']
ENDPOINT_ANALYSIS_EDITS = config['API']['ENDPOINT_ANALYSIS_EDITS']

# ----------------- VARIABLES -----------------
HIGHLIGHT_COLOR_MAP = ast.literal_eval(config['VARIABLES']['HIGHLIGHT_COLOR_MAP'])
LENGUAJE_VARIABLES = ast.literal_eval(config['LENGUAJE']['VARIABLES'])

# ----------------- URLs -----------------
URL_API_ENDPOINT_ANALYSIS_ANALYZE = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_ANALYSIS}/{ENDPOINT_ANALYSIS_ANALYZE}"
URL_API_ENDPOINT_ANALYSIS_EDITS = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_ANALYSIS}/{ENDPOINT_ANALYSIS_EDITS}"

#  ----------------- ENDPOINTS -----------------
@bp.route('/analyze', methods=['GET', 'POST'])
def analyze():
    # Leer datos enviados
    text = request.form.get('text', '')
    model = request.form.get('model', '')
    title = request.form.get('title', '')
    authors = request.form.get('authors', '')
    url = request.form.get('url', '')

    app = bp.get_app() if hasattr(bp, 'get_app') else None

    # Preparar JSON
    payload = {'text': text, 
               'model': model,
               'title': title,
               'authors': authors,
               'url': url}

    # Llamada a la API
    print(f"[/ANALYZE] Sending request to API ({URL_API_ENDPOINT_ANALYSIS_ANALYZE})...")
    resp = requests.post(URL_API_ENDPOINT_ANALYSIS_ANALYZE, json=payload, headers=API_HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        print(f"Respuesta de la API: {data}")

        return render_template(
            'analysis.html',
            language=get_locale(),
            data=data,
            highlight_map=HIGHLIGHT_COLOR_MAP,
            lenguaje_variables=LENGUAJE_VARIABLES,
            api_url_edit=URL_API_ENDPOINT_ANALYSIS_EDITS
        )
    else:
        return jsonify({"error": "Error en la solicitud al API"}), 500


@bp.route('/analyze/v0', methods=['GET', 'POST'])
def analyze_v0():
    # Leer datos enviados
    text = "La ingeniera Laura Gómez fue elegida como la responsable del ambicioso proyecto de inteligencia artificial en la empresa tecnológica Neuronix. Esta decisión marcó un hito importante, ya que es la primera vez que una mujer lidera un equipo técnico de esa magnitud dentro de la compañía, un puesto que tradicionalmente había sido ocupado exclusivamente por hombres. Laura, de 34 años, cuenta con una trayectoria profesional sólida: obtuvo su doctorado en aprendizaje automático en la Universidad de Stanford, trabajó durante cinco años en una reconocida startup de Silicon Valley y publicó múltiples artículos en conferencias internacionales. A pesar de estos logros, algunos medios destacaron su “juventud” y se refirieron a ella como “una joven promesa con carisma y ambición”. “Me siento honrada y lista para afrontar este reto con todo mi equipo”, declaró en la rueda de prensa. Sin embargo, el jefe del área técnica, Andrés Morales, comentó que “es un cambio arriesgado” y que “espera que el equipo esté preparado para ajustarse a su estilo de liderazgo”. En redes sociales, las reacciones fueron mixtas. Mientras muchas personas celebraron el nombramiento como un avance hacia la igualdad de género en el sector tecnológico, otros cuestionaron si su elección respondía a criterios de mérito o simplemente a una estrategia de imagen por parte de la empresa. “No es cuestión de género, es cuestión de experiencia real”, escribió un usuario. Paradójicamente, Laura tiene más experiencia que varios de los anteriores líderes del mismo equipo. Este caso ha abierto nuevamente el debate sobre el tratamiento que reciben las mujeres en puestos de alta responsabilidad, especialmente en sectores tradicionalmente masculinizados como la tecnología. Aunque Laura ha demostrado sobradamente su preparación, el foco mediático sigue centrado más en su condición de mujer que en su capacidad profesional."
    model = "avanzado"

    app = bp.get_app() if hasattr(bp, 'get_app') else None

    # Preparar JSON
    payload = {'text': text, 'model': model}

    # Llamada a la API
    print(f"[/ANALYZE/V0] Retrieving default example...")
    data = {'_id': '683977562b6934310b5f8d5c', 'analysis': {'edited': {'contenido_general': None, 'fuentes': None, 'lenguaje': None}, 'original': {'contenido_general': {'genero_periodista': 5, 'genero_personas_mencionadas': [2, 1], 'personas_mencionadas': ['Laura', 'Andrés Morales'], 'tema': 12}, 'fuentes': {'fuentes': [{'declaracion_fuente': 'Me siento honrada y lista para afrontar este reto con todo mi equipo', 'genero_fuente': 2, 'nombre_fuente': 'Laura', 'tipo_fuente': 1}, {'declaracion_fuente': 'es un cambio arriesgado', 'genero_fuente': 1, 'nombre_fuente': 'Andrés Morales', 'tipo_fuente': 1}, {'declaracion_fuente': 'espera que el equipo esté preparado para ajustarse a su estilo de liderazgo', 'genero_fuente': 1, 'nombre_fuente': 'Andrés Morales', 'tipo_fuente': 1}, {'declaracion_fuente': 'No es cuestión de género, es cuestión de experiencia real', 'genero_fuente': 3, 'nombre_fuente': 'usuario anónimo', 'tipo_fuente': 2}]}, 'lenguaje': {'androcentrismo': {'ejemplos_articulo': ['Este caso ha abierto nuevamente el debate sobre el tratamiento que reciben las mujeres en puestos de alta responsabilidad, especialmente en sectores tradicionalmente masculinizados como la tecnología.'], 'etiqueta': [1]}, 'asimetria': {'ejemplos_articulo': ['Algunos medios destacaron su “juventud” y se refirieron a ella como “una joven promesa con carisma y ambición”.', 'El foco mediático sigue centrado más en su condición de mujer que en su capacidad profesional.'], 'etiqueta': [1]}, 'cargos_mujeres': {'ejemplos_articulo': ['Es la primera vez que una mujer lidera un equipo técnico de esa magnitud.'], 'etiqueta': [1]}, 'comparacion_mujeres_hombres': {'ejemplos_articulo': ['Algunos medios destacaron su “juventud” y se refirieron a ella como “una joven promesa con carisma y ambición”.', 'A pesar de estos logros, algunos medios destacaron su “juventud”.'], 'etiqueta': [1]}, 'denominacion_dependiente': {'ejemplos_articulo': ['El foco mediático sigue centrado más en su condición de mujer que en su capacidad profesional.'], 'etiqueta': [1]}, 'denominacion_redundante': {'ejemplos_articulo': ['Un puesto que tradicionalmente había sido ocupado exclusivamente por hombres.'], 'etiqueta': [1]}, 'denominacion_sexualizada': {'ejemplos_articulo': ['El foco mediático sigue centrado más en su condición de mujer que en su capacidad profesional.'], 'etiqueta': [1]}, 'dual_aparente': {'ejemplos_articulo': ['La primera vez que una mujer lidera un equipo técnico de esa magnitud dentro de la compañía, un puesto que tradicionalmente había sido ocupado exclusivamente por hombres.'], 'etiqueta': [1]}, 'excepcion_noticiabilidad': {'ejemplos_articulo': ['Es la primera vez que una mujer lidera un equipo técnico de esa magnitud.'], 'etiqueta': [1]}, 'hombre_humanidad': {'ejemplos_articulo': ['Puesto que tradicionalmente había sido ocupado exclusivamente por hombres.'], 'etiqueta': [1]}, 'infantilizacion': {'ejemplos_articulo': ['Se refirieron a ella como “una joven promesa con carisma y ambición”.'], 'etiqueta': [1]}, 'lenguaje_sexista': {'ejemplos_articulo': ['Es la primera vez que una mujer lidera un equipo técnico de esa magnitud dentro de la compañía, un puesto que tradicionalmente había sido ocupado exclusivamente por hombres.', 'Algunos medios destacaron su “juventud” y se refirieron a ella como “una joven promesa con carisma y ambición”.', 'El foco mediático sigue centrado más en su condición de mujer que en su capacidad profesional.'], 'etiqueta': [1]}, 'masculino_generico': {'ejemplos_articulo': ['Puesto que tradicionalmente había sido ocupado exclusivamente por hombres.', 'Es un cambio arriesgado y que espera que el equipo esté preparado para ajustarse a su estilo de liderazgo.'], 'etiqueta': [1]}, 'sexismo_social': {'ejemplos_articulo': ['Mientras muchas personas celebraron el nombramiento como un avance hacia la igualdad de género en el sector tecnológico, otros cuestionaron si su elección respondía a criterios de mérito o simplemente a una estrategia de imagen por parte de la empresa.'], 'etiqueta': [1]}}}}, 'authors': '', 'highlight': {'edited': {'contenido_general': None, 'fuentes': None, 'lenguaje': None}, 'original': {'contenido_general': 'Esta decisión marcó un hito importante, ya que es la primera vez que una mujer lidera un equipo técnico de esa magnitud dentro de la compañía, un puesto que tradicionalmente había sido ocupado exclusivamente por hombres. <mark class="color-3">Laura</mark>, de 34 años, cuenta con una trayectoria profesional sólida: obtuvo su doctorado en aprendizaje automático en la Universidad de Stanford, trabajó durante cinco años en una reconocida startup de Silicon Valley y publicó múltiples artículos en conferencias internacionales. A pesar de estos logros, algunos medios destacaron su “juventud” y se refirieron a ella como “una joven promesa con carisma y ambición”. “Me siento honrada y lista para afrontar este reto con todo mi equipo”, declaró en la rueda de prensa. Sin embargo, el jefe del área técnica, <mark class="color-3">Andrés Morales</mark>, comentó que “es un cambio arriesgado” y que “espera que el equipo esté preparado para ajustarse a su estilo de liderazgo”. En redes sociales, las reacciones fueron mixtas. Mientras muchas personas celebraron el nombramiento como un avance hacia la igualdad de género en el sector tecnológico, otros cuestionaron si su elección respondía a criterios de mérito o simplemente a una estrategia de imagen por parte de la empresa. “No es cuestión de género, es cuestión de experiencia real”, escribió un usuario. Paradójicamente, <mark class="color-3">Laura</mark> tiene más experiencia que varios de los anteriores líderes del mismo equipo. Este caso ha abierto nuevamente el debate sobre el tratamiento que reciben las mujeres en puestos de alta responsabilidad, especialmente en sectores tradicionalmente masculinizados como la tecnología. Aunque <mark class="color-3">Laura</mark> ha demostrado sobradamente su preparación, el foco mediático sigue centrado más en su condición de mujer que en su capacidad profesional.\r\n', 'fuentes': 'Esta decisión marcó un hito importante, ya que es la primera vez que una mujer lidera un equipo técnico de esa magnitud dentro de la compañía, un puesto que tradicionalmente había sido ocupado exclusivamente por hombres. <mark class="color-3">Laura</mark>, de 34 años, cuenta con una trayectoria profesional sólida: obtuvo su doctorado en aprendizaje automático en la Universidad de Stanford, trabajó durante cinco años en una reconocida startup de Silicon Valley y publicó múltiples artículos en conferencias internacionales. A pesar de estos logros, algunos medios destacaron su “juventud” y se refirieron a ella como “una joven promesa con carisma y ambición”. “<mark class="color-4">Me siento honrada y lista para afrontar este reto con todo mi equipo</mark>”, declaró en la rueda de prensa. Sin embargo, el jefe del área técnica, <mark class="color-3"><mark class="color-3">Andrés Morales</mark></mark>, comentó que “<mark class="color-4">es un cambio arriesgado</mark>” y que “<mark class="color-4">espera que el equipo esté preparado para ajustarse a su estilo de liderazgo</mark>”. En redes sociales, las reacciones fueron mixtas. Mientras muchas personas celebraron el nombramiento como un avance hacia la igualdad de género en el sector tecnológico, otros cuestionaron si su elección respondía a criterios de mérito o simplemente a una estrategia de imagen por parte de la empresa. “<mark class="color-4">No es cuestión de género, es cuestión de experiencia real</mark>”, escribió un usuario. Paradójicamente, <mark class="color-3">Laura</mark> tiene más experiencia que varios de los anteriores líderes del mismo equipo. Este caso ha abierto nuevamente el debate sobre el tratamiento que reciben las mujeres en puestos de alta responsabilidad, especialmente en sectores tradicionalmente masculinizados como la tecnología. Aunque <mark class="color-3">Laura</mark> ha demostrado sobradamente su preparación, el foco mediático sigue centrado más en su condición de mujer que en su capacidad profesional.\r\n', 'lenguaje': 'Esta decisión marcó un hito importante, ya que es la primera vez que una mujer lidera un equipo técnico de esa magnitud dentro de la compañía, un puesto que tradicionalmente había sido ocupado exclusivamente por hombres. Laura, de 34 años, cuenta con una trayectoria profesional sólida: obtuvo su doctorado en aprendizaje automático en la Universidad de Stanford, trabajó durante cinco años en una reconocida startup de Silicon Valley y publicó múltiples artículos en conferencias internacionales. A pesar de estos logros, algunos medios destacaron su “juventud” y se refirieron a ella como “una joven promesa con carisma y ambición”. “Me siento honrada y lista para afrontar este reto con todo mi equipo”, declaró en la rueda de prensa. Sin embargo, el jefe del área técnica, Andrés Morales, comentó que “es un cambio arriesgado” y que “espera que el equipo esté preparado para ajustarse a su estilo de liderazgo”. En redes sociales, las reacciones fueron mixtas. <mark class="color-8">Mientras muchas personas celebraron el nombramiento como un avance hacia la igualdad de género en el sector tecnológico, otros cuestionaron si su elección respondía a criterios de mérito o simplemente a una estrategia de imagen por parte de la empresa.</mark> “No es cuestión de género, es cuestión de experiencia real”, escribió un usuario. Paradójicamente, Laura tiene más experiencia que varios de los anteriores líderes del mismo equipo. <mark class="color-9">Este caso ha abierto nuevamente el debate sobre el tratamiento que reciben las mujeres en puestos de alta responsabilidad, especialmente en sectores tradicionalmente masculinizados como la tecnología.</mark> Aunque Laura ha demostrado sobradamente su preparación, el foco mediático sigue centrado más en su condición de mujer que en su capacidad profesional.\r\n'}}, 'model': 'avanzado', 'status': 'ok', 'text': 'Esta decisión marcó un hito importante, ya que es la primera vez que una mujer lidera un equipo técnico de esa magnitud dentro de la compañía, un puesto que tradicionalmente había sido ocupado exclusivamente por hombres. Laura, de 34 años, cuenta con una trayectoria profesional sólida: obtuvo su doctorado en aprendizaje automático en la Universidad de Stanford, trabajó durante cinco años en una reconocida startup de Silicon Valley y publicó múltiples artículos en conferencias internacionales. A pesar de estos logros, algunos medios destacaron su “juventud” y se refirieron a ella como “una joven promesa con carisma y ambición”. “Me siento honrada y lista para afrontar este reto con todo mi equipo”, declaró en la rueda de prensa. Sin embargo, el jefe del área técnica, Andrés Morales, comentó que “es un cambio arriesgado” y que “espera que el equipo esté preparado para ajustarse a su estilo de liderazgo”. En redes sociales, las reacciones fueron mixtas. Mientras muchas personas celebraron el nombramiento como un avance hacia la igualdad de género en el sector tecnológico, otros cuestionaron si su elección respondía a criterios de mérito o simplemente a una estrategia de imagen por parte de la empresa. “No es cuestión de género, es cuestión de experiencia real”, escribió un usuario. Paradójicamente, Laura tiene más experiencia que varios de los anteriores líderes del mismo equipo. Este caso ha abierto nuevamente el debate sobre el tratamiento que reciben las mujeres en puestos de alta responsabilidad, especialmente en sectores tradicionalmente masculinizados como la tecnología. Aunque Laura ha demostrado sobradamente su preparación, el foco mediático sigue centrado más en su condición de mujer que en su capacidad profesional.\r\n', 'timestamp': '2025-05-30T09:16:06.513754+00:00', 'title': '', 'url': ''}
    print(f"Respuesta: {data}")
    return render_template(
        'analysis.html',
        language=get_locale(),
        data=data,
        highlight_map=HIGHLIGHT_COLOR_MAP,
        lenguaje_variables=LENGUAJE_VARIABLES,
        api_url_edit=URL_API_ENDPOINT_ANALYSIS_EDITS
    )
