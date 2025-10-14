# web/routes/glossary.py

# ==================================
#  LIBRARIES 
# ==================================
from flask import Blueprint, render_template
import configparser
import ast


# ==================================
#  BLUEPRINT 
# ==================================
bp = Blueprint('glossary', __name__, url_prefix='/glossary')


# ==================================
#  CONFIG 
# ==================================
config = configparser.ConfigParser()
config.read('config.ini')


def _safe_literal_eval(value):
    try:
        return ast.literal_eval(value)
    except Exception:
        return None


def _title_from_key(key: str) -> str:
    return key.replace('_', ' ').capitalize()


@bp.route('/', methods=['GET'])
def glossary_home():
    """Render a glossary of variables grouped by category using config.ini."""
    # Categories and variable lists
    contenido_vars = _safe_literal_eval(config['CONTENIDO_GENERAL'].get('VARIABLES', '[]')) or []
    lenguaje_vars = _safe_literal_eval(config['LENGUAJE'].get('VARIABLES', '[]')) or []
    fuentes_vars = _safe_literal_eval(config['FUENTES'].get('VARIABLES', '[]')) or []

    # Possible option maps present in config
    contenido_option_maps = {
        'genero_nombre_propio_titular': _safe_literal_eval(config['CONTENIDO_GENERAL'].get('GENERO_NOMBRE_PROPIO_TITULAR', '{}')),
        'genero_personas_mencionadas': _safe_literal_eval(config['CONTENIDO_GENERAL'].get('GENERO_PERSONAS_MENCIONADAS', '{}')),
        'genero_periodista': _safe_literal_eval(config['CONTENIDO_GENERAL'].get('GENERO_PERIODISTA', '{}')),
        'tema': _safe_literal_eval(config['CONTENIDO_GENERAL'].get('TEMA', '{}')),
        'cita_textual_titular': _safe_literal_eval(config['CONTENIDO_GENERAL'].get('CITA_TITULAR', '{}')),
    }

    lenguaje_option_maps = {
        # Many lenguaje variables are boolean-like (1/2). LENGUAJE_VARS applies to most
        'lenguaje_sexista': _safe_literal_eval(config['LENGUAJE'].get('LENGUAJE_SEXISTA', '{}')),
    }
    # A generic map that can be reused
    lenguaje_default_map = _safe_literal_eval(config['LENGUAJE'].get('LENGUAJE_VARS', '{}')) or {}

    fuentes_option_maps = {
        'tipo_fuente': _safe_literal_eval(config['FUENTES'].get('TIPO_FUENTE', '{}')),
    }

    # Descriptions for variables (Spanish)
    descriptions = {
        # Contenido general
        'cita_textual_titular': 'Indica si el titular contiene una cita textual explícita entrecomillada.',
        'genero_nombre_propio_titular': 'Género de los nombres propios que aparecen en el titular.',
        'genero_personas_mencionadas': 'Género de las personas mencionadas en el cuerpo del texto.',
        'genero_periodista': 'Género atribuido a la autoría periodística indicada en la pieza.',
        'nombre_propio_titular': 'Listado de nombres propios que aparecen en el titular.',
        'personas_mencionadas': 'Listado de personas identificadas dentro del texto (con o sin cargo).',
        'tema': 'Temática principal de la noticia o texto analizado.',

        # Lenguaje y análisis del discurso
        'lenguaje_sexista': 'Uso de lenguaje que discrimina o invisibiliza a un género, incluyendo posibles saltos semánticos.',
        'androcentrismo': 'Enfoque del discurso que sitúa lo masculino como medida o referencia universal.',
        'asimetria': 'Tratamiento desigual de mujeres y hombres en denominaciones, roles o relevancia.',
        'cargos_mujeres': 'Mención explícita de cargos o profesiones desempeñados por mujeres.',
        'comparacion_mujeres_hombres': 'Comparaciones explícitas o implícitas entre mujeres y hombres.',
        'denominacion_dependiente': 'Uso de denominaciones que definen a las mujeres por relación (esposa de, madre de).',
        'denominacion_redundante': 'Uso de marcadores de género innecesarios o redundantes.',
        'denominacion_sexualizada': 'Referencias que enfatizan rasgos físicos o sexuales por encima de lo profesional.',
        'dual_aparente': 'Uso de dobles formas que no garantizan igualdad real (p. ej., masculino genérico encubierto).',
        'excepcion_noticiabilidad': 'Criterio que hace relevante la noticia por excepcionar expectativas basadas en género.',
        'hombre_humanidad': 'Empleo de “hombre” como sinónimo de humanidad o personas.',
        'infantilizacion': 'Tratamiento de mujeres como niñas o condescendencia en el tono o los términos.',
        'masculino_generico': 'Uso del masculino como genérico para referirse a grupos mixtos o personas en general.',
        'sexismo_social': 'Expresiones o marcos que perpetúan estereotipos y roles de género desiguales.',

        # Fuentes de información
        'nombre_fuente': 'Nombre de la persona o entidad citada como fuente.',
        'declaracion_fuente': 'Fragmento textual o idea atribuida a la fuente.',
        'tipo_fuente': 'Clasificación del rol o perfil de la fuente citada.',
        'genero_fuente': 'Género de la persona citada como fuente (cuando procede).',
    }

    def build_items(var_keys, specific_maps, fallback_map=None, category_title=''):
        items = []
        for key in var_keys:
            options = specific_maps.get(key)
            if options is None and fallback_map is not None:
                # Apply fallback to boolean-like lenguaje variables
                options = fallback_map if key != 'lenguaje_sexista' else specific_maps.get('lenguaje_sexista')
            items.append({
                'key': key,
                'title': _title_from_key(key),
                'description': descriptions.get(key, 'Descripción no disponible por ahora.'),
                'category_title': category_title,
                'options': options  # dict or None
            })
        return items

    glossary = [
        {
            'category_key': 'contenido_general',
            'category_title': 'Contenido general',
            'variables': build_items(contenido_vars, contenido_option_maps, None, 'Contenido general')
        },
        {
            'category_key': 'lenguaje',
            'category_title': 'Lenguaje y análisis del discurso',
            'variables': build_items(lenguaje_vars, lenguaje_option_maps, lenguaje_default_map, 'Lenguaje y análisis del discurso')
        },
        {
            'category_key': 'fuentes',
            'category_title': 'Fuentes de información',
            'variables': build_items(fuentes_vars, fuentes_option_maps, None, 'Fuentes de información')
        },
    ]

    return render_template('glossary/glossary.html', glossary=glossary)


