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

CHALLENGE_TEXTS = [
    {
        'id': 1,
        'title': 'Mujer nombrada CEO de empresa tecnológica',
        'text': 'María González, de 35 años, ha sido nombrada nueva directora ejecutiva de TechCorp, una empresa líder en inteligencia artificial. Es la primera mujer en ocupar este cargo en la historia de la compañía. González, quien tiene un doctorado en Ciencias de la Computación del MIT, ha trabajado en la empresa durante ocho años, donde se destacó por su liderazgo en el desarrollo de algoritmos de machine learning. "Estoy emocionada de asumir este reto y continuar impulsando la innovación en nuestra empresa", declaró González en una conferencia de prensa. El presidente de la junta directiva, Carlos Ruiz, destacó que la elección de González se basó "exclusivamente en su mérito y experiencia profesional".',
        'difficulty': 'Fácil',
        'difficulty_reason': 'Sesgos evidentes: "primera mujer", "exclusivamente por mérito" (redundante), desequilibrio en fuentes (solo 2 personas)',
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


def simulate_ai_analysis(text_data, manual_annotations):
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
            'contenido_general': {
                'personas_mencionadas': 1,
                'genero_periodista': 1,
                'tema': 1
            },
            'lenguaje': {
                'lenguaje_sexista': 1,
                'androcentrismo': 1,
                'asimetria': 1,
                'infantilizacion': 1,
                'denominacion_sexualizada': 1,
                'denominacion_redundante': 1,
                'denominacion_dependiente': 1,
                'masculino_generico': 1,
                'dual_aparente': 1,
                'hombre_humanidad': 1,
                'cargos_mujeres': 1,
                'sexismo_social': 1,
                'comparacion_mujeres_hombres': 1,
                'criterios_excepcion_noticiabilidad': 1
            },
            'fuentes': {
                'nombre_fuente': 1,
                'genero_fuente': 1,
                'tipo_fuente': 1
            }
        }

    cg = analyze_task_challenge('avanzado', text, title, 'contenido_general') or {}
    personas = cg.get('personas_mencionadas') or []
    genero_periodista = cg.get('genero_periodista')
    tema = cg.get('tema')

    lg = analyze_task_challenge('avanzado', text, title, 'lenguaje') or {}

    def map_lenguaje(label_obj):
        if not isinstance(label_obj, dict):
            return 1
        etiqueta = label_obj.get('etiqueta')
        return safe_first_int(etiqueta, default=1)

    lenguaje_map = {
        'lenguaje_sexista': map_lenguaje(lg.get('lenguaje_sexista', {})),
        'masculino_generico': map_lenguaje(lg.get('masculino_generico', {})),
        'hombre_humanidad': map_lenguaje(lg.get('hombre_humanidad', {})),
        'dual_aparente': map_lenguaje(lg.get('dual_aparente', {})),
        'cargos_mujeres': map_lenguaje(lg.get('cargos_mujeres', {})),
        'sexismo_social': map_lenguaje(lg.get('sexismo_social', {})),
        'androcentrismo': map_lenguaje(lg.get('androcentrismo', {})),
        'asimetria': map_lenguaje(lg.get('asimetria', {})),
        'infantilizacion': map_lenguaje(lg.get('infantilizacion', {})),
        'denominacion_sexualizada': map_lenguaje(lg.get('denominacion_sexualizada', {})),
        'denominacion_redundante': map_lenguaje(lg.get('denominacion_redundante', {})),
        'denominacion_dependiente': map_lenguaje(lg.get('denominacion_dependiente', {})),
        'comparacion_mujeres_hombres': map_lenguaje(lg.get('comparacion_mujeres_hombres', {})),
        'criterios_excepcion_noticiabilidad': map_lenguaje(lg.get('excepcion_noticiabilidad', {})),
    }

    fs = analyze_task_challenge('avanzado', text, title, 'fuentes') or {}
    fuentes = fs.get('fuentes') or []

    def mode_or_first(items, key, default=1):
        try:
            values = [int(it.get(key)) for it in items if key in it]
            if not values:
                return default
            return max(set(values), key=values.count)
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


