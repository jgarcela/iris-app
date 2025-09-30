# web/routes/challenge.py
from flask import Blueprint, render_template, request, jsonify, session
from flask_babel import get_locale, _
from web.utils.challenge_decorators import challenge_required
import json
import os

bp = Blueprint('challenge', __name__, url_prefix='/challenge')

# Sample texts for the challenge
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

@bp.route('/')
@challenge_required
def challenge_home():
    """Página principal del desafío"""
    return render_template('challenge/challenge_home.html', 
                         texts=CHALLENGE_TEXTS,
                         language=get_locale())

@bp.route('/analyze/<int:text_id>')
@challenge_required
def analyze_text(text_id):
    """Página de análisis individual"""
    text_data = next((text for text in CHALLENGE_TEXTS if text['id'] == text_id), None)
    if not text_data:
        return "Texto no encontrado", 404
    
    return render_template('challenge/challenge_analysis.html', 
                         text_data=text_data,
                         language=get_locale())

@bp.route('/results')
@challenge_required
def results():
    """Página de resultados y ranking"""
    return render_template('challenge/challenge_results.html', 
                         language=get_locale())

@bp.route('/analyze-ai', methods=['POST'])
@challenge_required
def analyze_with_ai():
    """Endpoint para análisis con IA"""
    try:
        data = request.get_json()
        text_id = data.get('text_id')
        manual_annotations = data.get('manual_annotations', [])
        text_data = data.get('text_data', {})
        
        # Obtener el texto del desafío
        challenge_text = next((text for text in CHALLENGE_TEXTS if text['id'] == text_id), None)
        if not challenge_text:
            return jsonify({'success': False, 'error': 'Texto no encontrado'}), 404
        
        # Simular análisis con IA (aquí conectarías con tu API real de IA)
        ai_analysis = simulate_ai_analysis(challenge_text, manual_annotations)
        
        # Guardar análisis en sesión para la página de resultados
        session[f'ai_analysis_{text_id}'] = ai_analysis
        session[f'manual_annotations_{text_id}'] = manual_annotations
        session[f'text_data_{text_id}'] = text_data
        
        return jsonify({
            'success': True,
            'ai_analysis': ai_analysis,
            'redirect_url': f'/challenge/ai-results/{text_id}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/ai-results/<int:text_id>')
@challenge_required
def ai_results(text_id):
    """Página de resultados del análisis con IA"""
    # Obtener datos de la sesión
    ai_analysis = session.get(f'ai_analysis_{text_id}', {})
    manual_annotations = session.get(f'manual_annotations_{text_id}', [])
    text_data = session.get(f'text_data_{text_id}', {})
    
    if not ai_analysis:
        return "Análisis no encontrado", 404
    
    return render_template('challenge/challenge_ai_results.html',
                         text_data=text_data,
                         ai_analysis=ai_analysis,
                         manual_annotations=manual_annotations,
                         analysis_data={'text_id': text_id},
                         language=get_locale())

@bp.route('/api/compare', methods=['POST'])
@challenge_required
def compare_analysis():
    """API para comparar análisis manual vs IA"""
    try:
        data = request.get_json()
        manual_analysis = data.get('manual_analysis', {})
        ai_analysis = data.get('ai_analysis', {})
        text_id = data.get('text_id')
        
        # Calcular métricas de comparación
        comparison_metrics = calculate_comparison_metrics(manual_analysis, ai_analysis)
        
        return jsonify({
            'success': True,
            'metrics': comparison_metrics,
            'score': comparison_metrics['total_score']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def calculate_comparison_metrics(manual, ai):
    """Calcular métricas de comparación entre análisis manual e IA"""
    metrics = {
        'contenido_general': {'precision': 0, 'recall': 0, 'f1': 0},
        'lenguaje': {'precision': 0, 'recall': 0, 'f1': 0},
        'fuentes': {'precision': 0, 'recall': 0, 'f1': 0},
        'total_score': 0
    }
    
    # Calcular métricas por categoría
    for category in ['contenido_general', 'lenguaje', 'fuentes']:
        if category in manual and category in ai:
            manual_vars = set(manual[category].keys()) if isinstance(manual[category], dict) else set()
            ai_vars = set(ai[category].keys()) if isinstance(ai[category], dict) else set()
            
            if ai_vars:
                precision = len(manual_vars & ai_vars) / len(ai_vars)
                recall = len(manual_vars & ai_vars) / len(manual_vars) if manual_vars else 0
                f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
                
                metrics[category] = {
                    'precision': round(precision * 100, 2),
                    'recall': round(recall * 100, 2),
                    'f1': round(f1 * 100, 2)
                }
    
    # Calcular puntuación total (promedio ponderado)
    weights = {'contenido_general': 0.4, 'lenguaje': 0.4, 'fuentes': 0.2}
    total_score = sum(metrics[cat]['f1'] * weights[cat] for cat in weights.keys())
    metrics['total_score'] = round(total_score, 2)
    
    return metrics

def simulate_ai_analysis(text_data, manual_annotations):
    """Simular análisis con IA basado en el texto y anotaciones manuales"""
    # Esta es una simulación - en producción conectarías con tu API real de IA
    import random
    
    # Generar análisis simulado basado en el contenido del texto
    ai_analysis = {
        'contenido_general': {
            'personas_mencionadas': random.randint(1, 3),
            'genero_periodista': random.randint(1, 3),
            'tema': random.randint(1, 5)
        },
        'lenguaje': {
            'lenguaje_sexista': random.randint(1, 2),
            'androcentrismo': random.randint(1, 2),
            'asimetria': random.randint(1, 2),
            'infantilizacion': random.randint(1, 2),
            'denominacion_sexualizada': random.randint(1, 2),
            'denominacion_redundante': random.randint(1, 2),
            'denominacion_dependiente': random.randint(1, 2),
            'masculino_generico': random.randint(1, 2),
            'dual_aparente': random.randint(1, 2),
            'hombre_humanidad': random.randint(1, 2),
            'cargos_mujeres': random.randint(1, 2),
            'sexismo_social': random.randint(1, 2),
            'comparacion_mujeres_hombres': random.randint(1, 2),
            'criterios_excepcion_noticiabilidad': random.randint(1, 2)
        },
        'fuentes': {
            'nombre_fuente': random.randint(1, 3),
            'genero_fuente': random.randint(1, 3),
            'tipo_fuente': random.randint(1, 3)
        }
    }
    
    # Ajustar algunos valores basándose en las anotaciones manuales para hacer la comparación más realista
    if manual_annotations:
        for annotation in manual_annotations:
            category = annotation.get('category', '')
            variable = annotation.get('variable', '')
            value = annotation.get('value', '')
            
            if category in ai_analysis and variable in ai_analysis[category]:
                # A veces coincidir con el análisis manual, a veces no
                if random.random() > 0.3:  # 70% de probabilidad de coincidir
                    ai_analysis[category][variable] = int(value)
    
    return ai_analysis

