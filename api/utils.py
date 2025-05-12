

def analyze_text(model: str, text: str) -> dict:
    """
    Función de ejemplo que lleva a cabo el análisis.
    Aquí pondrías tu lógica real: conteo de términos,
    detección de patrones de lenguaje, modelo ML, etc.
    """
    # Ejemplo muy básico:
    words = text.split()
    female_forms = sum(1 for w in words if w.lower().endswith('a'))
    male_forms   = sum(1 for w in words if w.lower().endswith('o'))
    return {
        'word_count': len(words),
        'female_endings': female_forms,
        'male_endings': male_forms,
        'bias_indicator': round(female_forms / (male_forms + 1), 2)
    }