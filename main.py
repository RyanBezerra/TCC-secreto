#!/usr/bin/env python3
"""
EduAI - Ponto de Entrada Principal
Sistema de inicialização da Plataforma de Ensino Inteligente
"""

import sys
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importar e executar o main da aplicação
from src.main import main

if __name__ == '__main__':
    sys.exit(main())
