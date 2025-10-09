"""
Utilitários de fonte para melhor portabilidade entre sistemas operacionais
"""

import platform
import os

try:
    from PySide6.QtGui import QFont, QFontDatabase
    from PySide6.QtCore import QCoreApplication
except ImportError:
    # Fallback para versões mais antigas do PySide6
    from PySide6.QtGui import QFont
    QFontDatabase = None
    QCoreApplication = None

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
    # Detectar sistema operacional
    system = platform.system().lower()
    
    # Configurar fonte baseada no sistema
    if system == "windows":
        if family == "Segoe UI":
            font_families = ["Segoe UI", "Arial", "Helvetica", "sans-serif"]
        else:
            font_families = [family, "Segoe UI", "Arial", "Helvetica", "sans-serif"]
    elif system == "linux":
        if family == "Segoe UI":
            font_families = ["Ubuntu", "Liberation Sans", "DejaVu Sans", "Arial", "Helvetica", "sans-serif"]
        else:
            font_families = [family, "Ubuntu", "Liberation Sans", "DejaVu Sans", "Arial", "Helvetica", "sans-serif"]
    elif system == "darwin":  # macOS
        if family == "Segoe UI":
            font_families = ["SF Pro Display", "Helvetica Neue", "Helvetica", "Arial", "sans-serif"]
        else:
            font_families = [family, "SF Pro Display", "Helvetica Neue", "Helvetica", "Arial", "sans-serif"]
    else:
        # Sistema desconhecido - usar fallbacks genéricos
        font_families = [family, "Arial", "Helvetica", "Liberation Sans", "DejaVu Sans", "sans-serif"]
    
    # Criar fonte
    font = QFont(family, size, weight)
    font.setFamilies(font_families)
    
    # Configurações adicionais para melhor renderização
    font.setHintingPreference(QFont.HintingPreference.PreferDefaultHinting)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    
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

def get_best_available_font(preferred_fonts):
    """
    Retorna a melhor fonte disponível de uma lista de preferências
    
    Args:
        preferred_fonts (list): Lista de fontes em ordem de preferência
    
    Returns:
        str: Nome da melhor fonte disponível
    """
    available_fonts = get_system_fonts()
    
    for font in preferred_fonts:
        if font in available_fonts:
            return font
    
    # Se nenhuma fonte preferida estiver disponível, retornar a primeira disponível
    if available_fonts:
        return available_fonts[0]
    
    return "Arial"  # Fallback final

def setup_application_fonts():
    """
    Configura as fontes padrão da aplicação para melhor portabilidade
    """
    if QCoreApplication is None:
        return
    
    app = QCoreApplication.instance()
    if app is None:
        return
    
    # Configurar fonte padrão da aplicação
    system = platform.system().lower()
    
    if system == "windows":
        default_font = get_portable_font("Segoe UI", 9)
    elif system == "linux":
        default_font = get_portable_font("Ubuntu", 9)
    elif system == "darwin":
        default_font = get_portable_font("SF Pro Display", 9)
    else:
        default_font = get_portable_font("Arial", 9)
    
    app.setFont(default_font)

def get_ui_font(size=11, weight=QFont.Weight.Normal):
    """
    Retorna uma fonte otimizada para interface do usuário
    
    Args:
        size (int): Tamanho da fonte
        weight (QFont.Weight): Peso da fonte
    
    Returns:
        QFont: Fonte otimizada para UI
    """
    system = platform.system().lower()
    
    if system == "windows":
        return get_portable_font("Segoe UI", size, weight)
    elif system == "linux":
        return get_portable_font("Ubuntu", size, weight)
    elif system == "darwin":
        return get_portable_font("SF Pro Display", size, weight)
    else:
        return get_portable_font("Arial", size, weight)
