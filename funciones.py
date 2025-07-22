import re

def extraer_habilidades_responsabilidades(texto):
    """Extrae habilidades/responsabilidades de descripciones de trabajo"""
    match = re.search(
        r'(habilidades|requisitos|responsabilidades|competencia)[\s:;\-–]+(.+?)(?=(\.|$|\n[^\s]))', 
        texto, 
        re.IGNORECASE | re.DOTALL
    )
    if match:
        habilidades = re.split(r'[,;•\-–]', match.group(2))
        return [h.strip() for h in habilidades if len(h.strip()) > 3] 
    return []