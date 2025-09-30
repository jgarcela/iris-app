#!/usr/bin/env python3
"""
Precompute AI analyses for all challenge texts and store them in MongoDB
collection 'iris_semana_ciencia_2025_cache'.

Self-contained: includes texts, prompting, OpenAI call, Mongo connection,
and data mapping. No imports from the project app.
"""

import os
import json
from datetime import datetime, timezone

# ---------- Config (edit here if needed) ----------
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.environ.get('MONGO_DB', 'iris')
CACHE_COLLECTION = os.environ.get('CACHE_COLLECTION', 'iris_semana_ciencia_2025_cache')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')  # required
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')

# ---------- Data: Challenge texts (copied) ----------
CHALLENGE_TEXTS = [
    {
        'id': 1,
        'title': 'Mujer nombrada CEO de empresa tecnológica',
        'text': 'María González, de 35 años, ha sido nombrada nueva directora ejecutiva de TechCorp, una empresa líder en inteligencia artificial. Es la primera mujer en ocupar este cargo en la historia de la compañía. González, quien tiene un doctorado en Ciencias de la Computación del MIT, ha trabajado en la empresa durante ocho años, donde se destacó por su liderazgo en el desarrollo de algoritmos de machine learning. "Estoy emocionada de asumir este reto y continuar impulsando la innovación en nuestra empresa", declaró González en una conferencia de prensa. El presidente de la junta directiva, Carlos Ruiz, destacó que la elección de González se basó "exclusivamente en su mérito y experiencia profesional".',
        'difficulty': 'Fácil',
        'categories': ['Contenido General', 'Lenguaje', 'Fuentes']
    },
    {
        'id': 2,
        'title': 'Debate sobre paridad de género en el deporte',
        'text': 'El Comité Olímpico Internacional ha anunciado nuevas regulaciones para garantizar la igualdad de género en los Juegos Olímpicos de París 2024. La decisión incluye la eliminación de categorías "masculinas" y "femeninas" en favor de categorías por peso y habilidad. "Esta es una medida histórica que refleja los valores de igualdad y justicia que promueve el movimiento olímpico", afirmó la presidenta del comité, Sarah Johnson. Sin embargo, algunos atletas han expresado preocupación sobre el impacto en la competencia. "Creo que esto podría afectar negativamente a las deportistas que han entrenado toda su vida para competir en categorías específicas", comentó el ex-campeón olímpico Michael Torres. La implementación comenzará gradualmente en 2023.',
        'difficulty': 'Medio',
        'categories': ['Contenido General', 'Lenguaje', 'Fuentes']
    },
    {
        'id': 3,
        'title': 'Estudio sobre brecha salarial en el sector tecnológico',
        'text': 'Un estudio reciente de la Universidad de Stanford revela que las mujeres en el sector tecnológico ganan en promedio un 23% menos que sus colegas masculinos en posiciones similares. La investigación, que analizó datos de más de 10,000 empleados de 50 empresas tecnológicas, encontró que la brecha es más pronunciada en roles de liderazgo. "Los resultados son preocupantes pero no sorprendentes", señaló la Dra. Ana Martínez, autora principal del estudio. "Necesitamos políticas más agresivas para cerrar esta brecha". El estudio también reveló que las mujeres tienen menos probabilidades de ser promovidas a puestos directivos, con solo el 28% de los cargos de alta dirección ocupados por mujeres. Las empresas participantes se comprometieron a revisar sus políticas salariales.',
        'difficulty': 'Medio',
        'categories': ['Contenido General', 'Lenguaje', 'Fuentes']
    },
    {
        'id': 4,
        'title': 'Primera astronauta en comandar misión espacial',
        'text': 'La astronauta Elena Rodríguez se convertirá en la primera mujer en comandar una misión espacial de larga duración a Marte. La misión, programada para 2025, durará dos años y medio. Rodríguez, de 42 años, es ingeniera aeroespacial y tiene más de 15 años de experiencia en la NASA. "Es un honor y una responsabilidad enorme", declaró Rodríguez. "Espero inspirar a más mujeres a seguir carreras en ciencias espaciales". El director de la NASA, James Wilson, destacó que la selección de Rodríguez se basó "exclusivamente en sus calificaciones técnicas y experiencia". La misión incluirá experimentos sobre la viabilidad de la vida humana en Marte y el desarrollo de tecnologías para futuras colonias espaciales.',
        'difficulty': 'Fácil',
        'categories': ['Contenido General', 'Lenguaje', 'Fuentes']
    },
    {
        'id': 5,
        'title': 'Controversia sobre lenguaje inclusivo en medios',
        'text': 'La Real Academia Española ha emitido un comunicado criticando el uso del lenguaje inclusivo en los medios de comunicación, calificándolo de "innecesario y confuso". El pronunciamiento ha generado un intenso debate en redes sociales y medios. "El lenguaje debe evolucionar naturalmente, no por imposición", afirmó el director de la RAE, Santiago Muñoz. Por su parte, la lingüista feminista Carmen López argumentó que "el lenguaje inclusivo es una herramienta fundamental para visibilizar a las mujeres y combatir la discriminación". El debate se intensificó cuando varios medios decidieron adoptar el uso de "todos y todas" en sus publicaciones. Algunos lectores han expresado su apoyo, mientras otros consideran que "complica innecesariamente la lectura".',
        'difficulty': 'Difícil',
        'categories': ['Contenido General', 'Lenguaje', 'Fuentes']
    },
    {
        'id': 6,
        'title': 'Mujer gana Premio Nobel de Física',
        'text': 'La física teórica Lisa Chen ha sido galardonada con el Premio Nobel de Física 2024 por sus contribuciones revolucionarias en el campo de la mecánica cuántica. Chen, de 38 años, es la tercera mujer en recibir este prestigioso premio en la historia. Su investigación sobre el entrelazamiento cuántico ha abierto nuevas posibilidades para la computación cuántica. "Espero que este reconocimiento inspire a más mujeres jóvenes a seguir carreras en física", declaró Chen durante la ceremonia. El comité del Nobel destacó que el trabajo de Chen "ha transformado nuestra comprensión del mundo cuántico". La científica, nacida en Singapur, estudió en el MIT y actualmente trabaja en el Instituto de Tecnología de California.',
        'difficulty': 'Fácil',
        'categories': ['Contenido General', 'Lenguaje', 'Fuentes']
    },
    {
        'id': 7,
        'title': 'Análisis de representación femenina en el cine',
        'text': 'Un estudio del Instituto de Medios de Comunicación revela que solo el 32% de los personajes protagonistas en las películas más taquilleras de 2023 son mujeres. El análisis, que examinó 100 películas, encontró que las mujeres aparecen más frecuentemente en roles de apoyo o como "interés romántico" del protagonista masculino. "Los resultados muestran que aún hay mucho trabajo por hacer en la representación equitativa", señaló la directora del estudio, Patricia García. El informe también reveló que las películas dirigidas por mujeres tienden a tener una representación más equilibrada. "Necesitamos más mujeres detrás de la cámara para cambiar lo que vemos en pantalla", agregó García. Las productoras han comenzado a implementar políticas de diversidad en respuesta a estos hallazgos.',
        'difficulty': 'Medio',
        'categories': ['Contenido General', 'Lenguaje', 'Fuentes']
    },
    {
        'id': 8,
        'title': 'Debate sobre cuotas de género en política',
        'text': 'El Parlamento Europeo ha aprobado una nueva directiva que exige que al menos el 40% de los candidatos en las listas electorales sean mujeres. La medida, que entrará en vigor en 2025, ha generado controversia entre los partidos políticos. "Las cuotas son necesarias para garantizar la representación equitativa", argumentó la eurodiputada francesa Marie Dubois. Sin embargo, algunos críticos consideran que "las cuotas van en contra del mérito y la democracia". El partido conservador alemán ha anunciado que impugnará la directiva ante el Tribunal de Justicia de la Unión Europea. "Creemos en la igualdad de oportunidades, no en la igualdad de resultados", declaró el portavoz del partido, Hans Weber. Las organizaciones feministas han celebrado la medida como "un paso histórico hacia la paridad política".',
        'difficulty': 'Difícil',
        'categories': ['Contenido General', 'Lenguaje', 'Fuentes']
    },
    {
        'id': 9,
        'title': 'Mujer lidera investigación sobre cambio climático',
        'text': 'La climatóloga Dra. Sofia Andersson dirige el mayor proyecto de investigación sobre el impacto del cambio climático en las regiones polares. El estudio, financiado por la Unión Europea con 50 millones de euros, involucra a más de 200 científicos de 15 países. Andersson, de 45 años, ha pasado los últimos 20 años estudiando el deshielo de los glaciares. "El cambio climático es el desafío más urgente de nuestro tiempo", declaró Andersson. "Las mujeres científicas tienen un papel crucial en encontrar soluciones". El proyecto ha descubierto que el deshielo se está acelerando más rápido de lo previsto. "Necesitamos actuar ahora", advirtió Andersson. Los resultados del estudio serán presentados en la próxima cumbre climática de la ONU.',
        'difficulty': 'Medio',
        'categories': ['Contenido General', 'Lenguaje', 'Fuentes']
    },
    {
        'id': 10,
        'title': 'Controversia sobre estereotipos en publicidad',
        'text': 'La Autoridad de Estándares Publicitarios ha multado a varias empresas por usar estereotipos de género en sus campañas publicitarias. Las sanciones, que ascienden a más de 2 millones de euros, incluyen anuncios que muestran a mujeres solo en roles domésticos y a hombres como únicos proveedores del hogar. "Estos estereotipos perpetúan roles de género obsoletos y dañinos", explicó la directora de la agencia, Emma Thompson. Las empresas multadas han defendido sus campañas argumentando que "reflejan la realidad de muchos hogares". Sin embargo, los grupos feministas han celebrado las sanciones como "una victoria para la igualdad de género". La nueva normativa publicitaria entrará en vigor el próximo año y requerirá que todas las campañas pasen por una revisión de diversidad e inclusión.',
        'difficulty': 'Difícil',
        'categories': ['Contenido General', 'Lenguaje', 'Fuentes']
    }
]


# ---------- OpenAI helper ----------
def analyze_block(model: str, title: str, text: str, task: str) -> dict | None:
    """Minimal JSON-returning call per block (contenido_general, lenguaje, fuentes)."""
    if not OPENAI_API_KEY:
        return None
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        system = f"Devuelve SOLO JSON válido para la tarea {task}."
        user = f"Titulo: {title}\nArticulo: {text}"
        resp = openai.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0
        )
        content = resp.choices[0].message.content
        return json.loads(content)
    except Exception:
        return None


def simulate_ai_analysis(text: str, title: str) -> dict:
    """Call OpenAI per block; fallback to safe defaults; normalize integers/counts."""
    def safe_first_int(v, default=1):
        try:
            if isinstance(v, list) and v:
                return int(v[0])
            return int(v)
        except Exception:
            return default

    # contenido_general
    cg = analyze_block(OPENAI_MODEL, title, text, 'contenido_general') or {}
    personas = cg.get('personas_mencionadas') or []
    genero_periodista = cg.get('genero_periodista')
    tema = cg.get('tema')

    # lenguaje
    lg = analyze_block(OPENAI_MODEL, title, text, 'lenguaje') or {}
    def map_l(obj):
        if not isinstance(obj, dict):
            return 1
        return safe_first_int(obj.get('etiqueta'), 1)
    lenguaje = {
        'lenguaje_sexista': map_l(lg.get('lenguaje_sexista')),
        'masculino_generico': map_l(lg.get('masculino_generico')),
        'hombre_humanidad': map_l(lg.get('hombre_humanidad')),
        'dual_aparente': map_l(lg.get('dual_aparente')),
        'cargos_mujeres': map_l(lg.get('cargos_mujeres')),
        'sexismo_social': map_l(lg.get('sexismo_social')),
        'androcentrismo': map_l(lg.get('androcentrismo')),
        'asimetria': map_l(lg.get('asimetria')),
        'infantilizacion': map_l(lg.get('infantilizacion')),
        'denominacion_sexualizada': map_l(lg.get('denominacion_sexualizada')),
        'denominacion_redundante': map_l(lg.get('denominacion_redundante')),
        'denominacion_dependiente': map_l(lg.get('denominacion_dependiente')),
        'comparacion_mujeres_hombres': map_l(lg.get('comparacion_mujeres_hombres')),
        'criterios_excepcion_noticiabilidad': map_l(lg.get('excepcion_noticiabilidad')),
    }

    # fuentes
    fs = analyze_block(OPENAI_MODEL, title, text, 'fuentes') or {}
    fuentes = fs.get('fuentes') or []
    def mode_or_first(items, key, default=1):
        try:
            vals = [int(it.get(key)) for it in items if key in it]
            return max(set(vals), key=vals.count) if vals else default
        except Exception:
            return default

    return {
        'contenido_general': {
            'personas_mencionadas': len(personas),
            'genero_periodista': safe_first_int(genero_periodista, 1),
            'tema': safe_first_int(tema, 1)
        },
        'lenguaje': lenguaje,
        'fuentes': {
            'nombre_fuente': len(fuentes),
            'genero_fuente': mode_or_first(fuentes, 'genero_fuente', 1),
            'tipo_fuente': mode_or_first(fuentes, 'tipo_fuente', 1)
        }
    }


# ---------- Mongo helpers ----------
def upsert_cache(doc: dict):
    from pymongo import MongoClient
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    col = db[CACHE_COLLECTION]
    col.create_index('text_id', unique=True)
    col.update_one({'text_id': doc['text_id']}, {'$set': doc}, upsert=True)


def main():
    created, updated = 0, 0
    for text in CHALLENGE_TEXTS:
        text_id = text['id']
        title = text['title']
        body = text['text']
        ai = simulate_ai_analysis(body, title)
        doc = {
            'text_id': text_id,
            'text_title': title,
            'ai_analysis': ai,
            'source': 'precompute',
            'created_at': datetime.now(timezone.utc),
            'updated_at': datetime.now(timezone.utc)
        }
        upsert_cache(doc)
        updated += 1
        print(f"[CACHE] upsert text_id={text_id}")
    print(f"Done. Upserts: {updated}")


if __name__ == '__main__':
    main()



