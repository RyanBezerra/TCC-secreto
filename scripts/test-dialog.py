#!/usr/bin/env python3
"""
Teste simples do dialog de instituição
"""

import sys
import os
from PySide6.QtWidgets import QApplication

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ui.instituicao_dialog import InstituicaoDialog

def test_dialog():
    app = QApplication(sys.argv)
    
    # Criar o dialog
    dialog = InstituicaoDialog()
    
    # Mostrar o dialog
    dialog.show()
    
    # Executar a aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    test_dialog()
