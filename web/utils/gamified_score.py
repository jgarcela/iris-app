# web/utils/gamified_score.py

"""
Sistema de puntuación gamificada usando comparación exacta.
Compara anotaciones del usuario con anotaciones de IRIS.
"""


def convert_annotations_to_dict(annotations):
    """
    Convierte anotaciones de formato lista a formato diccionario agrupado.
    
    Input: [{category, variable, text}, ...]
    Output: {category: {variable: [text1, text2, ...]}}
    """
    result = {}
    for ann in annotations:
        cat = ann.get('category', '')
        var = ann.get('variable', '')
        text = ann.get('text', '').strip()
        
        if not cat or not var or not text:
            continue
        
        if cat not in result:
            result[cat] = {}
        
        if var not in result[cat]:
            result[cat][var] = []
        
        # Evitar duplicados
        if text not in result[cat][var]:
            result[cat][var].append(text)
    
    return result


def gamified_score_detailed(user_ann_list, iris_ann_list, threshold=0.8):
    """
    Calcula puntuación gamificada comparando anotaciones del usuario con IRIS.
    Usa comparación exacta (sin embeddings).
    
    Args:
        user_ann_list: Lista de anotaciones del usuario [{category, variable, text}, ...]
        iris_ann_list: Lista de anotaciones de IRIS [{category, variable, text}, ...]
        threshold: No se usa (mantenido para compatibilidad)
    
    Returns:
        dict: Reporte con categorías y resumen global
    """
    report = {
        "categorías": {},
        "resumen_global": {
            "exactos": 0,
            "parciales": 0,
            "extras": 0,
            "faltantes": 0,
            "puntos_totales": 0
        }
    }
    
    # Convertir a formato diccionario para procesar por categoría/variable
    user_ann = convert_annotations_to_dict(user_ann_list)
    iris_ann = convert_annotations_to_dict(iris_ann_list)
    
    # Procesar cada categoría
    for cat, vars_user in user_ann.items():
        vars_iris = iris_ann.get(cat, {})
        cat_report = {}

        # Procesar cada variable en la categoría
        for var, vals_user in vars_user.items():
            vals_iris_same_var = vars_iris.get(var, [])
            
            # Si no hay anotaciones en ninguna, continuar
            if not vals_iris_same_var and not vals_user:
                continue

            exactos = parciales = extras = faltantes = 0
            puntos = 0
            matched_iris_same_var = set()  # Índices de textos IRIS que ya fueron matcheados

            # Comparar usuario → IRIS
            for u_text in vals_user:
                found_match = False
                u_text_clean = u_text.strip().lower()
                
                # Buscar en la misma variable (exactos)
                for idx, iris_text in enumerate(vals_iris_same_var):
                    if idx in matched_iris_same_var:
                        continue  # Ya fue matcheado
                    
                    iris_text_clean = iris_text.strip().lower()
                    if u_text_clean == iris_text_clean:
                        # Match exacto en la misma variable
                        exactos += 1
                        puntos += 100
                        matched_iris_same_var.add(idx)
                        found_match = True
                        break
                
                # Si no hay match exacto, buscar en otras variables de la categoría (parciales)
                if not found_match:
                    for other_var, other_vals_iris in vars_iris.items():
                        if other_var == var:
                            continue  # Ya lo buscamos arriba
                        
                        for iris_text in other_vals_iris:
                            iris_text_clean = iris_text.strip().lower()
                            if u_text_clean == iris_text_clean:
                                # Match parcial en otra variable (mismo texto, diferente variable)
                                parciales += 1
                                puntos += 50
                                found_match = True
                                break
                        if found_match:
                            break
                
                if not found_match:
                    # No hay match (extras: sin puntos, sin penalización)
                    extras += 1
                    puntos += 0

            # Faltantes = IRIS que el usuario no marcó (en la misma variable)
            # Sin penalización: 0 puntos
            faltantes = len(vals_iris_same_var) - len(matched_iris_same_var)
            puntos += 0 * max(0, faltantes)

            cat_report[var] = {
                "exactos": exactos,
                "parciales": parciales,
                "extras": extras,
                "faltantes": faltantes,
                "puntos": puntos
            }

            # Sumar al global
            report["resumen_global"]["exactos"] += exactos
            report["resumen_global"]["parciales"] += parciales
            report["resumen_global"]["extras"] += extras
            report["resumen_global"]["faltantes"] += faltantes
            report["resumen_global"]["puntos_totales"] += puntos

        report["categorías"][cat] = cat_report
    
    # También considerar categorías/variables que están en IRIS pero no en usuario
    for cat, vars_iris in iris_ann.items():
        if cat not in report["categorías"]:
            report["categorías"][cat] = {}
        
        for var, vals_iris in vars_iris.items():
            if var not in report["categorías"][cat]:
                # Variable solo en IRIS (faltante: sin puntos, sin penalización)
                faltantes = len(vals_iris)
                puntos = 0 * faltantes
                report["categorías"][cat][var] = {
                    "exactos": 0,
                    "parciales": 0,
                    "extras": 0,
                    "faltantes": faltantes,
                    "puntos": puntos
                }
                report["resumen_global"]["faltantes"] += faltantes
                report["resumen_global"]["puntos_totales"] += puntos

    # Calcular score final normalizado sobre 100%
    # El máximo teórico es cuando todas las anotaciones IRIS son exactas
    total_items_iris = (report["resumen_global"]["exactos"] + 
                        report["resumen_global"]["parciales"] + 
                        report["resumen_global"]["faltantes"])
    
    if total_items_iris == 0:
        # Si no hay anotaciones IRIS, el score es 0
        report["resumen_global"]["score_final"] = 0
    else:
        # Máximo teórico: todas las anotaciones IRIS perfectas (exactas) = total_items_iris * 100
        puntos_maximos_posibles = total_items_iris * 100
        
        # Puntos actuales (puede ser negativo por extras/faltantes)
        puntos_actuales = report["resumen_global"]["puntos_totales"]
        
        # Normalizar sobre 100%
        # Score = (puntos_actuales / puntos_maximos_posibles) * 100
        score_raw = (puntos_actuales / puntos_maximos_posibles) * 100
        
        # Asegurar que esté entre 0 y 100
        score_raw = max(0, min(score_raw, 100))
        
        report["resumen_global"]["score_final"] = round(score_raw, 2)
    
    return report
