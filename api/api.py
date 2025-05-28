import json
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from flask_cors import CORS, cross_origin
import configparser
from newspaper import Article
import analyze
import highlight


# ----------------- CONFIG -----------------
config = configparser.ConfigParser()
config.read('config.ini')

WEB_HOST = config['WEB']['HOST']
WEB_PORT = config['WEB']['PORT']
DEBUG = config['WEB'].getboolean('DEBUG')
API_HOST = config['API']['HOST']
API_PORT = config['API']['PORT']


app = Flask(__name__)
# Habilitar CORS para todas las rutas
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

language_map = {
            "es": "español",
            "en": "inglés",
        }

# ----------------- ENDPOINTS -----------------
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"})

@app.route('/analysis/analyze', methods=['POST'])
def analysis_analyze():
    # Obtener datos de la web
    print("[/ANALYSIS/ANALYZE] Receiving data from web...")
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Payload inválido. Debe ser JSON.'}), 400

    # Acceder directamente, porque siempre están presentes (aunque puedan estar vacíos)
    model = data['model']
    text  = data['text']
    title = data['title']
    authors = data['authors']
    url = data['url']

    # Validar que model no esté vacío
    if not model.strip():
        return jsonify({
            'error': 'El campo "model" no puede estar vacío.',
            'received': {
                'model': bool(model.strip()),
                'text': bool(text.strip()),
                'url': bool(url.strip())
            }
        }), 400

    # Validar que al menos uno de text o url tenga contenido
    if not text.strip() and not url.strip():
        return jsonify({
            'error': 'Se requiere al menos un campo no vacío: "text" o "url".',
            'received': {
                'model': bool(model.strip()),
                'text': bool(text.strip()),
                'url': bool(url.strip())
            }
        }), 400
    
    # Si URL está presente, usamos newspaper3k para obtener texto, título y autores
    if url.strip():
        print(f"{url=}")
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            title = title or article.title  # Si el usuario no lo envió
            authors = authors or article.authors
            print(f"{text=}")
        except Exception as e:
            return jsonify({'error': f'Error al procesar la URL: {str(e)}'}), 500



    # Ejecutar el análisis y highlight
    try:
        # Analysis
        print("[/ANALYSIS/ANALYZE] Initializing analysis...")
        analysis_contenido_general = analyze.analyze_text(model, text, title, task="contenido_general")
        analysis_fuentes = analyze.analyze_text(model, text, title, task="fuentes")
        analysis_lenguaje = analyze.analyze_text(model, text, title, task="lenguaje")

        # Highlight
        print("[/ANALYSIS/ANALYZE] Initializing highlight...")
        highlight_contenido_general = highlight.highlight_text(analysis_contenido_general, text, task="contenido_general")
        highlight_fuentes = highlight.highlight_text(analysis_fuentes, text, task="fuentes")
        highlight_lenguaje = highlight.highlight_text(analysis_lenguaje, text, task="lenguaje")

    except ValueError as ve:
        # por si analyze_text lanza errores de validación de parámetros
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # error inesperado
        app.logger.exception("Error en el análisis")
        return jsonify({'error': 'Error interno en el servidor.'}), 500

    # Devolver resultado estructurado
    return jsonify({
        'status': 'ok',
        'model': model,
        'text': text,
        'title': title,
        'authors': authors,
        'url': url,
        'analysis': {
            'analysis_contenido_general': analysis_contenido_general,
            'analysis_fuentes': analysis_fuentes,
            'analysis_lenguaje': analysis_lenguaje
        },
        'highlight': {
            'highlight_contenido_general': highlight_contenido_general,
            'highlight_fuentes': highlight_fuentes,
            'highlight_lenguaje': highlight_lenguaje
        }
        
    }), 200   





if __name__ == '__main__':
    app.run(debug=True, host=API_HOST, port=API_PORT)

    app.config['SECRET_KEY'] = config['DEFAULT']['SECRET_KEY']