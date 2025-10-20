"""
EduAI - Gerenciamento de Banco de Dados
Sistema de conexão e operações com MySQL e SQLite
"""

from ..config import config
from ..utils.logger import get_logger

# Importar o gerenciador MySQL
try:
    from .mysql_database import mysql_db_manager
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

# Importar o gerenciador SQLite se disponível
try:
    from .sqlite_database import sqlite_db_manager
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False

# Configurar logging
logger = get_logger('database')

def get_database_manager():
    """Retorna o gerenciador de banco de dados apropriado"""
    if config.database.use_sqlite and SQLITE_AVAILABLE:
        logger.info("Usando SQLite como banco de dados")
        return sqlite_db_manager
    elif MYSQL_AVAILABLE:
        logger.info("Usando MySQL como banco de dados")
        return mysql_db_manager
    else:
        logger.error("Nenhum gerenciador de banco de dados disponível")
        raise Exception("Nenhum gerenciador de banco de dados disponível")

# Instância global do gerenciador de banco
db_manager = get_database_manager()