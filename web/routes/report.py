# web/report.py
from flask import Blueprint, render_template, request, jsonify, session, send_file, abort
import requests
from flask_babel import get_locale
import configparser
import ast
from io import BytesIO
from datetime import datetime
from collections import Counter, OrderedDict
from web.utils.logger import logger
from web.utils.decorators import challenge_restricted


# ----------------- BLUEPRINT -----------------
bp = Blueprint(
    'report',
    __name__,
    url_prefix='/report'
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
ENDPOINT_DATA = config['API']['ENDPOINT_DATA']
ENDPOINT_DATA_GET_CONTEXTO = config['API']['ENDPOINT_DATA_GET_CONTEXTO']
COLLECTION_DATA = config['DATABASE']['COLLECTION_DATA']

# ----------------- URLs -----------------
URL_API_ENDPOINT_ANALYSIS_ANALYZE = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_ANALYSIS}/{ENDPOINT_ANALYSIS_ANALYZE}"
URL_API_ENDPOINT_DATA = f"http://{API_HOST}:{API_PORT}/{ENDPOINT_DATA}"
URL_API_ENDPOINT_DATA_COLLECTION = f"{URL_API_ENDPOINT_DATA}/{COLLECTION_DATA}"
URL_API_ENDPOINT_DATA_GET_CONTEXTO = f"{URL_API_ENDPOINT_DATA}/{ENDPOINT_DATA_GET_CONTEXTO}"


# ----------------- VARIABLE CATALOG -----------------
# Report-friendly categorical variables → (human label, config map key)
REPORT_VARIABLES = OrderedDict([
    ('menciona_ia',        ('Menciona IA',                    'MENCIONA_IA')),
    ('ia_tema_central',    ('IA como tema central',           'IA_TEMA_CENTRAL')),
    ('significado_ia',     ('Explicación del significado de IA', 'SIGNIFICADO_IA')),
    ('tema',               ('Temática de la noticia',         'TEMA')),
    ('genero_periodista',  ('Género del/la periodista',       'GENERO_PERIODISTA')),
    ('genero_personas',    ('Género de las personas mencionadas', 'GENERO_PERSONAS_MENCIONADAS')),
    ('cita_titular',       ('Cita en el titular',             'CITA_TITULAR')),
    ('lenguaje_sexista',   ('Lenguaje sexista',               'LENGUAJE_SEXISTA')),
])


def _load_map(cfg_key):
    """Parse a mapping dict from config.ini and normalise keys to str."""
    try:
        raw = ast.literal_eval(config['VARIABLES'][cfg_key]) if config.has_option('VARIABLES', cfg_key) \
            else ast.literal_eval(config['DEFAULT'][cfg_key])
    except Exception:
        # Fall back to a flat scan of every section
        raw = {}
        for section in config.sections():
            if config.has_option(section, cfg_key):
                try:
                    raw = ast.literal_eval(config[section][cfg_key])
                    break
                except Exception:
                    continue
    return {str(k): v for k, v in (raw or {}).items()}


def _fetch_contextos():
    try:
        r = requests.get(URL_API_ENDPOINT_DATA_GET_CONTEXTO, timeout=8)
        r.raise_for_status()
        return r.json().get('contextos', [])
    except Exception as e:
        logger.warning(f"[/REPORT] No se pudieron obtener contextos: {e}")
        return []


def _fetch_data():
    r = requests.get(URL_API_ENDPOINT_DATA_COLLECTION, timeout=15)
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, list) else data.get('data', [])


def _parse_fecha(s):
    for fmt in ('%d/%m/%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(str(s), fmt).date()
        except Exception:
            continue
    return None


def _filter_rows(rows, context, fd, fh):
    d_from = _parse_fecha(fd) if fd else None
    d_to = _parse_fecha(fh) if fh else None
    out = []
    for it in rows:
        if context and it.get('contexto') != context:
            continue
        if d_from or d_to:
            f = _parse_fecha(it.get('Fecha'))
            if f is None:
                continue
            if d_from and f < d_from:
                continue
            if d_to and f > d_to:
                continue
        out.append(it)
    return out


def _build_tables(rows, variables):
    """For each variable, a distribution table: label → (count, pct)."""
    tables = []
    for field in variables:
        if field not in REPORT_VARIABLES:
            continue
        label, cfg_key = REPORT_VARIABLES[field]
        value_map = _load_map(cfg_key)
        counter = Counter()
        for it in rows:
            v = it.get(field)
            if v is None or str(v).strip() in ('', 'None', 'nan', '-1'):
                continue
            counter[str(v)] += 1
        total = sum(counter.values())
        entries = []
        for key, cnt in counter.most_common():
            name = value_map.get(key, f"Código {key}")
            pct = (cnt / total * 100) if total else 0
            entries.append({'label': name, 'count': cnt, 'pct': round(pct, 1)})
        tables.append({
            'field': field,
            'title': label,
            'total': total,
            'entries': entries,
        })
    return tables


def _prepare_report(args):
    context = (args.get('context') or '').strip()
    fd = args.get('fecha_desde') or ''
    fh = args.get('fecha_hasta') or ''
    variables = args.getlist('vars') if hasattr(args, 'getlist') else args.get('vars', [])
    variables = [v for v in variables if v in REPORT_VARIABLES]

    rows = _fetch_data()
    filtered = _filter_rows(rows, context, fd, fh)
    tables = _build_tables(filtered, variables)
    meta = {
        'context': context or 'Todas las bases de datos',
        'fecha_desde': fd,
        'fecha_hasta': fh,
        'total': len(filtered),
        'variables': variables,
    }
    return meta, tables


#  ----------------- ENDPOINTS -----------------
@bp.route('/create', methods=['GET', 'POST'])
@challenge_restricted
def create():
    logger.info(f"[/REPORT/CREATE] Request to report/create from {request.remote_addr} with method {request.method}")
    return render_template('report/create_report.html')


@bp.route('/generate', methods=['GET'])
@challenge_restricted
def generate():
    logger.info(f"[/REPORT/GENERATE] Request from {request.remote_addr}")
    contextos = _fetch_contextos()

    meta, tables = None, None
    submitted = bool(request.args.get('vars'))
    if submitted:
        try:
            meta, tables = _prepare_report(request.args)
        except Exception as e:
            logger.error(f"[/REPORT/GENERATE] Error building preview: {e}")
            abort(502, description=f"No se pudo generar la vista previa: {e}")

    return render_template(
        'report/generate_report.html',
        contextos=contextos,
        variables=REPORT_VARIABLES,
        meta=meta,
        tables=tables,
        selected_context=(request.args.get('context') or '').strip(),
        selected_vars=request.args.getlist('vars'),
        fecha_desde=request.args.get('fecha_desde', ''),
        fecha_hasta=request.args.get('fecha_hasta', ''),
    )


@bp.route('/download', methods=['GET'])
@challenge_restricted
def download():
    logger.info(f"[/REPORT/DOWNLOAD] Request from {request.remote_addr}")
    if not request.args.get('vars'):
        abort(400, description="Selecciona al menos una variable.")

    try:
        from docx import Document
        from docx.shared import Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
    except Exception as e:
        abort(500, description=f"python-docx no disponible: {e}")

    meta, tables = _prepare_report(request.args)

    doc = Document()
    doc.add_heading('Informe IRIS', 0)

    sub = doc.add_paragraph()
    sub.add_run('Base de datos: ').bold = True
    sub.add_run(meta['context'])
    periodo = doc.add_paragraph()
    periodo.add_run('Periodo: ').bold = True
    periodo.add_run(f"{meta['fecha_desde'] or 'inicio'} — {meta['fecha_hasta'] or 'hoy'}")
    ntot = doc.add_paragraph()
    ntot.add_run('Total de noticias analizadas: ').bold = True
    ntot.add_run(str(meta['total']))
    doc.add_paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    for tbl in tables:
        doc.add_heading(tbl['title'], level=1)
        t = doc.add_table(rows=1, cols=3)
        t.style = 'Table Grid'
        hdr = t.rows[0].cells
        hdr[0].text = tbl['title']
        hdr[1].text = 'Frecuencia'
        hdr[2].text = 'Porcentaje'
        for e in tbl['entries']:
            cells = t.add_row().cells
            cells[0].text = str(e['label'])
            cells[1].text = str(e['count'])
            cells[2].text = f"{e['pct']}%"
        tot = t.add_row().cells
        tot[0].text = 'Total'
        tot[1].text = str(tbl['total'])
        tot[2].text = '100%'
        doc.add_paragraph()

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    fname = f"informe_iris_{datetime.now().strftime('%Y%m%d_%H%M')}.docx"
    return send_file(
        buf,
        as_attachment=True,
        download_name=fname,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
