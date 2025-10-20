"""
EduAI - Ponto de Entrada Principal
Sistema de inicialização da Plataforma de Ensino Inteligente
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config, constants
from src.utils import get_logger, cache_manager
from src.core.database import db_manager
from src.core.app import EduAIManager

def setup_application():
    """Configura a aplicação Qt"""
    # Verificar se já existe uma instância do QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        app.setApplicationName(config.app.app_name)
        app.setApplicationVersion(config.app.app_version)
        app.setOrganizationName("EduAI")
        
        # Configurar estilo da aplicação
        app.setStyle('Fusion')
    
    return app

def setup_directories():
    """Cria diretórios necessários"""
    try:
        # Criar diretórios se não existirem
        constants.LOGS_DIR.mkdir(exist_ok=True)
        constants.CACHE_DIR.mkdir(exist_ok=True)
        constants.IMAGES_DIR.mkdir(exist_ok=True)
        
        return True
    except Exception as e:
        print(f"Erro ao criar diretórios: {e}")
        return False

def check_dependencies():
    """Verifica se todas as dependências estão disponíveis"""
    missing_deps = []
    
    try:
        import psycopg2
    except ImportError:
        missing_deps.append("psycopg2-binary")
    
    try:
        import qtawesome
    except ImportError:
        missing_deps.append("qtawesome")
    
    try:
        import bcrypt
    except ImportError:
        missing_deps.append("bcrypt")
    
    if missing_deps:
        print(f"Dependências faltando: {', '.join(missing_deps)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    return True

def initialize_database():
    """Inicializa conexão com o banco de dados"""
    logger = get_logger('main')
    
    try:
        if not db_manager.test_connection():
            logger.error("Falha ao conectar com o banco de dados")
            return False
        
        logger.info("Conexão com banco de dados estabelecida")
        return True
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        return False

def cleanup_resources():
    """Limpa recursos ao encerrar a aplicação"""
    logger = get_logger('main')
    
    try:
        # Fechar pool de conexões
        db_manager.close_pool()
        
        # Limpar cache
        cache_manager.clear_all()
        
        logger.info("Recursos limpos com sucesso")
    except Exception as e:
        logger.error(f"Erro ao limpar recursos: {e}")

def show_error_dialog(title: str, message: str):
    """Mostra diálogo de erro"""
    app = QApplication.instance()
    if app:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

def main():
    """Função principal"""
    logger = get_logger('main')
    
    try:
        logger.info(f"Iniciando {config.app.app_name} v{config.app.app_version}")
        
        # Verificar dependências
        if not check_dependencies():
            show_error_dialog(
                "Dependências Faltando",
                "Algumas dependências necessárias não foram encontradas.\n"
                "Execute: pip install -r requirements.txt"
            )
            return 1
        
        # Configurar diretórios
        if not setup_directories():
            show_error_dialog(
                "Erro de Configuração",
                "Não foi possível criar os diretórios necessários."
            )
            return 1
        
        # Configurar aplicação Qt
        app = setup_application()
        
        # Inicializar banco de dados
        if not initialize_database():
            show_error_dialog(
                "Erro de Conexão",
                "Não foi possível conectar com o banco de dados.\n"
                "Verifique sua conexão com a internet."
            )
            return 1
        
        # Configurar limpeza ao encerrar
        app.aboutToQuit.connect(cleanup_resources)
        
        # Iniciar gerenciador da aplicação
        manager = EduAIManager(app)
        manager.start()
        
        return 0
        
    except Exception as e:
        logger.error(f"Erro fatal na inicialização: {e}")
        show_error_dialog(
            "Erro Fatal",
            f"Ocorreu um erro inesperado:\n{str(e)}"
        )
        return 1

if __name__ == '__main__':
    sys.exit(main())
