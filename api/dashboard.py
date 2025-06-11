from collections import Counter


def prepare_chart(counter, mapping, none_label='Sin datos', sort_desc=True):
    # 0) Normalize counter: strings of digits → ints
    norm = Counter()
    for k, v in counter.items():
        if isinstance(k, str) and k.isdigit():
            norm[int(k)] += v
        else:
            norm[k] += v
    counter = norm

    # 1) claves válidas (int)
    valid_keys = [int(k) for k in mapping.keys()]
    other_count = sum(v for k,v in counter.items() if (not isinstance(k,int)) or k not in valid_keys)
    m = mapping.copy()

    if other_count:
        m['None'] = none_label

    # 2) construye etiquetas/valores
    labels, values = [], []
    for key in m:
        if key == 'None':
            labels.append(m['None'])
            values.append(other_count)
        else:
            ik = int(key)
            labels.append(m[key])
            values.append(counter.get(ik, 0))

    # 3) orden descendente si hace falta
    if sort_desc:
        paired = sorted(zip(values, labels), reverse=True)
        values, labels = zip(*paired)
        return list(labels), list(values)
    return labels, values

def generate_colors(n):
    """
    Genera una lista de 'n' colores a partir de una paleta base.
    Si n es mayor que la paleta, los colores se repiten.
    """
    # Paleta de colores base
    palette = [
        '#6c5ce7', '#a29bfe', '#8e44ad', '#9b59b6', '#2980b9',
        '#3498db', '#1abc9c', '#16a085', '#27ae60', '#2ecc71',
        '#f1c40f', '#f39c12', '#e67e22', '#d35400', '#e74c3c',
        '#c0392b', '#b388eb'
    ]
    
    if n <= 0:
        return []

    # Genera la lista de colores repitiendo la paleta si es necesario
    num_repeats = (n + len(palette) - 1) // len(palette)
    extended_palette = palette * num_repeats
    
    return extended_palette[:n]