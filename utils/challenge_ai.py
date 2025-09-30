CHALLENGE_TEXTS = CHALLENGE_TEXTS  # ensure symbol exported
import ast
import configparser
import json
try:
    import openai
except Exception:
    openai = None

config = configparser.ConfigParser()
config.read('config.ini')
MODELS = ast.literal_eval(config['API']['MODELS'])
OPENAI_MODEL = config['API']['OPENAI_MODEL']
OPENAI_API_KEY = config['API']['OPENAI_API_KEY']
if openai is not None:
    try:
        openai.api_key = OPENAI_API_KEY
    except Exception:
        pass



def analyze_task_challenge(model_key: str, text: str, title: str, task: str):
    if openai is None:
        return None
    try:
        with open(f'api/prompts/{task}.txt', 'r', encoding='utf-8') as f:
            prompt = f.read()
    except Exception:
        return None

    user_prompt = f"""
Titulo: {title}
Articulo: {text}
"""
    try:
        completion = openai.chat.completions.create(
            model=MODELS.get(model_key, OPENAI_MODEL),
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        response_message = completion.choices[0].message.content
        return json.loads(response_message)
    except Exception:
        return None

def simulate_ai_analysis(text_data, manual_annotations=None):
    manual_annotations = manual_annotations or []
    title = text_data.get('title', '')
    text = text_data.get('text', '')

    def safe_first_int(value, default=1):
        try:
            if isinstance(value, list) and value:
                return int(value[0])
            return int(value)
        except Exception:
            return default

    if openai is None:
        return {
            'contenido_general': {'personas_mencionadas': 1, 'genero_periodista': 1, 'tema': 1},
            'lenguaje': {k: 1 for k in ['lenguaje_sexista','androcentrismo','asimetria','infantilizacion','denominacion_sexualizada','denominacion_redundante','denominacion_dependiente','masculino_generico','dual_aparente','hombre_humanidad','cargos_mujeres','sexismo_social','comparacion_mujeres_hombres','criterios_excepcion_noticiabilidad']},
            'fuentes': {'nombre_fuente': 1, 'genero_fuente': 1, 'tipo_fuente': 1}
        }

    cg = analyze_task_challenge('avanzado', text, title, 'contenido_general') or {}
    personas = cg.get('personas_mencionadas') or []
    genero_periodista = cg.get('genero_periodista')
    tema = cg.get('tema')

    lg = analyze_task_challenge('avanzado', text, title, 'lenguaje') or {}
    def map_l(label_obj):
        if not isinstance(label_obj, dict):
            return 1
        etiqueta = label_obj.get('etiqueta')
        return safe_first_int(etiqueta, 1)
    lenguaje_map = {
        'lenguaje_sexista': map_l(lg.get('lenguaje_sexista', {})),
        'masculino_generico': map_l(lg.get('masculino_generico', {})),
        'hombre_humanidad': map_l(lg.get('hombre_humanidad', {})),
        'dual_aparente': map_l(lg.get('dual_aparente', {})),
        'cargos_mujeres': map_l(lg.get('cargos_mujeres', {})),
        'sexismo_social': map_l(lg.get('sexismo_social', {})),
        'androcentrismo': map_l(lg.get('androcentrismo', {})),
        'asimetria': map_l(lg.get('asimetria', {})),
        'infantilizacion': map_l(lg.get('infantilizacion', {})),
        'denominacion_sexualizada': map_l(lg.get('denominacion_sexualizada', {})),
        'denominacion_redundante': map_l(lg.get('denominacion_redundante', {})),
        'denominacion_dependiente': map_l(lg.get('denominacion_dependiente', {})),
        'comparacion_mujeres_hombres': map_l(lg.get('comparacion_mujeres_hombres', {})),
        'criterios_excepcion_noticiabilidad': map_l(lg.get('excepcion_noticiabilidad', {})),
    }

    fs = analyze_task_challenge('avanzado', text, title, 'fuentes') or {}
    fuentes = fs.get('fuentes') or []
    def mode_or_first(items, key, default=1):
        try:
            values = [int(it.get(key)) for it in items if key in it]
            return max(set(values), key=values.count) if values else default
        except Exception:
            return default

    return {
        'contenido_general': {
            'personas_mencionadas': len(personas),
            'genero_periodista': safe_first_int(genero_periodista, 1),
            'tema': safe_first_int(tema, 1)
        },
        'lenguaje': lenguaje_map,
        'fuentes': {
            'nombre_fuente': len(fuentes),
            'genero_fuente': mode_or_first(fuentes, 'genero_fuente', 1),
            'tipo_fuente': mode_or_first(fuentes, 'tipo_fuente', 1)
        }
    }


