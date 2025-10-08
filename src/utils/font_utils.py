"""
Utilitários de fonte para melhor portabilidade entre sistemas operacionais
"""

try:
    from PySide6.QtGui import QFont, QFontDatabase
except ImportError:
    # Fallback para versões mais antigas do PySide6
    from PySide6.QtGui import QFont
    QFontDatabase = None

def get_portable_font(family="Segoe UI", size=11, weight=QFont.Weight.Normal):
    """
    Cria uma fonte com fallbacks para diferentes sistemas operacionais
    
    Args:
        family (str): Nome da família da fonte
        size (int): Tamanho da fonte
        weight (QFont.Weight): Peso da fonte
    
    Returns:
        QFont: Fonte configurada com fallbacks
    """
    font = QFont(family, size, weight)
    
    # Fallbacks para diferentes sistemas operacionais
    if family == "Segoe UI":
        # Windows: Segoe UI, Linux/Mac: Arial, Helvetica, sans-serif
        font.setFamilies(["Segoe UI", "Arial", "Helvetica", "sans-serif"])
    elif family == "Arial":
        font.setFamilies(["Arial", "Helvetica", "sans-serif"])
    elif family == "Helvetica":
        font.setFamilies(["Helvetica", "Arial", "sans-serif"])
    else:
        # Para outras fontes, adicionar fallbacks genéricos
        font.setFamilies([family, "Arial", "Helvetica", "sans-serif"])
    
    return font

def get_system_fonts():
    """
    Retorna uma lista de fontes disponíveis no sistema
    
    Returns:
        list: Lista de nomes de fontes disponíveis
    """
    if QFontDatabase is None:
        return []
    
    db = QFontDatabase()
    return db.families()

def is_font_available(font_name):
    """
    Verifica se uma fonte está disponível no sistema
    
    Args:
        font_name (str): Nome da fonte a verificar
    
    Returns:
        bool: True se a fonte estiver disponível
    """
    return font_name in get_system_fonts()
