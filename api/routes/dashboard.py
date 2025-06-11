# api/routes/dashboard.py

# ==================================
#  LIBRARIES 
# ==================================
from collections import Counter
from flask import Blueprint, abort, request, jsonify

from database.db import db
from api.utils.logger import logger

import api
import api.utils.dashboard

# ==================================
#  BLUEPRINT 
# ==================================
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


# ==================================
#  ENDPOINTS 
# ==================================
@bp.route("/data", methods=["POST"])
def dashboard_data():
    """
    Espera un JSON con:
    {
        "data": [...],
        "total_count": N
    }
    """
    payload = request.get_json(silent=True)
    if not payload or 'data' not in payload or 'total_count' not in payload:
        abort(400, "Se requieren 'data' y 'total_count' en el cuerpo JSON")

    data = payload['data']
    total_count = payload['total_count'] or 1

    # 1) Nombre propio titular
    cnt = Counter(item.get('nombre_propio_titular') for item in data)
    labels_npt, values_npt = api.utils.dashboard.prepare_chart(cnt, api.GENERO_NOMBRE_PROPIO_TITULAR)
    perc_npt = [round(v/total_count*100,1) for v in values_npt]

    # 2) Cita en el titular
    cnt = Counter(item.get('cita_titular') for item in data)
    labels_ct, values_ct = api.utils.dashboard.prepare_chart(cnt, api.CITA_TITULAR)
    perc_ct = [round(v/total_count*100,1) for v in values_ct]

    # 3) Temática de las Noticias
    cnt = Counter(item.get('tema') for item in data)
    labels_tema, values_tema = api.utils.dashboard.prepare_chart(cnt, api.TEMA)
    perc_tema = [round(v/total_count*100,1) for v in values_tema]

    # 4) Menciona IA
    cnt = Counter(item.get('menciona_ia') for item in data)
    labels_mia, values_mia = api.utils.dashboard.prepare_chart(cnt, api.MENCIONA_IA)
    perc_mia = [round(v/total_count*100,1) for v in values_mia]

    # 5) IA Tema principal
    cnt = Counter(item.get('ia_tema_central') for item in data)
    labels_itc, values_itc = api.utils.dashboard.prepare_chart(cnt, api.IA_TEMA_CENTRAL)
    perc_itc = [round(v/total_count*100,1) for v in values_itc]

    # 6) Explicación Significado IA
    cnt = Counter(item.get('significado_ia') for item in data)
    labels_sia, values_sia = api.utils.dashboard.prepare_chart(cnt, api.SIGNIFICADO_IA)
    perc_sia = [round(v/total_count*100,1) for v in values_sia]

    # 7) Género de las personas
    cnt = Counter(item.get('genero_personas') for item in data)
    labels_gp, values_gp = api.utils.dashboard.prepare_chart(cnt, api.GENERO_PERSONAS_MENCIONADAS)
    perc_gp = [round(v/total_count*100,1) for v in values_gp]

    # 8) Extensión de la noticia
    lengths = []
    for item in data:
        nc_raw = item.get('Caracteres')
        try:
            nc = int(nc_raw)
        except (TypeError, ValueError):
            texto = item.get('textonoticia') or ''
            nc = len(texto)
        lengths.append(nc)
    cnt_ext = Counter()
    thresholds = sorted(api.EXTENSION_NOTICIA.keys())
    for l in lengths:
        for thr in reversed(thresholds):
            if l >= thr:
                cnt_ext[thr] += 1
                break
    cnt_ext_str = Counter({ str(k): v for k,v in cnt_ext.items() })
    mapping_ext = { str(k): api.EXTENSION_NOTICIA[k] for k in thresholds }
    labels_en, values_en = api.utils.dashboard.prepare_chart(cnt_ext_str, mapping_ext)
    perc_en = [round(v/total_count*100,1) for v in values_en]

    # 9) Género periodista
    cnt = Counter(item.get('genero_periodista') for item in data)
    labels_per, values_per = api.utils.dashboard.prepare_chart(cnt, api.GENERO_PERIODISTA)
    perc_per = [round(v/total_count*100,1) for v in values_per]

    # Armamos y devolvemos JSON
    dashboard = {
        "total_count": total_count,
        "chart_data": {
            'nombreTitular':   {'type':'bar',      'labels':labels_npt, 'data':values_npt, 'percent':perc_npt, 'colors': api.utils.dashboard.generate_colors(len(labels_npt))},
            'citaTitular':     {'type':'bar',      'labels':labels_ct,  'data':values_ct,  'percent':perc_ct,  'colors': api.utils.dashboard.generate_colors(len(labels_ct))},
            'tematica':        {'type':'bar',      'labels':labels_tema,'data':values_tema,'percent':perc_tema,'colors': api.utils.dashboard.generate_colors(len(labels_tema))},
            'mencionaIA':      {'type':'doughnut', 'labels':labels_mia, 'data':values_mia, 'percent':perc_mia, 'colors': api.utils.dashboard.generate_colors(len(labels_mia))},
            'iaTemaPrincipal': {'type':'doughnut', 'labels':labels_itc, 'data':values_itc, 'percent':perc_itc, 'colors': api.utils.dashboard.generate_colors(len(labels_itc))},
            'significadoIA':   {'type':'doughnut', 'labels':labels_sia, 'data':values_sia, 'percent':perc_sia, 'colors': api.utils.dashboard.generate_colors(len(labels_sia))},
            'generoPersonas':  {'type':'doughnut', 'labels':labels_gp,  'data':values_gp,  'percent':perc_gp,  'colors': api.utils.dashboard.generate_colors(len(labels_gp))},
            'extensionNoticia':{'type':'doughnut', 'labels':labels_en,  'data':values_en,  'percent':perc_en,  'colors': api.utils.dashboard.generate_colors(len(labels_en))},
            'generoPeriodista':{'type':'bar',      'labels':labels_per, 'data':values_per,'percent':perc_per,  'colors': api.utils.dashboard.generate_colors(len(labels_per))}
        }
    }

    return jsonify(dashboard)