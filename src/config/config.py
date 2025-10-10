"""
EduAI - Configurações Centralizadas
Sistema de configuração para a Plataforma de Ensino Inteligente
"""

import os
from typing import Dict, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DatabaseConfig:
    """Configurações do banco de dados"""
    host: str = "centerbeam.proxy.rlwy.net"
    port: int = 38802
    database: str = "railway"
    user: str = "postgres"
    password: str = "wQzRPlMlCdkfNjwMkZHyfabrZubqFKPC"
    max_connections: int = 10
    connection_timeout: int = 30

@dataclass
class UIConfig:
    """Configurações da interface do usuário"""
    window_width: int = 1200
    window_height: int = 800
    min_window_width: int = 800
    min_window_height: int = 600
    theme: str = "light"
    font_family: str = "Segoe UI"
    primary_color: str = "#000000"
    secondary_color: str = "#3498db"
    success_color: str = "#27ae60"
    error_color: str = "#e74c3c"
    warning_color: str = "#f39c12"

@dataclass
class SecurityConfig:
    """Configurações de segurança"""
    password_min_length: int = 6
    password_require_special_chars: bool = False
    session_timeout: int = 3600  # 1 hora
    max_login_attempts: int = 5
    lockout_duration: int = 300  # 5 minutos

@dataclass
class AppConfig:
    """Configurações gerais da aplicação"""
    app_name: str = "EduAI"
    app_version: str = "1.0.0"
    app_description: str = "Plataforma de Ensino Inteligente"
    debug_mode: bool = False
    log_level: str = "INFO"
    cache_enabled: bool = True
    cache_ttl: int = 300  # 5 minutos

class Config:
    """Classe principal de configuração"""
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.ui = UIConfig()
        self.security = SecurityConfig()
        self.app = AppConfig()
        
        # Carregar configurações de variáveis de ambiente
        self._load_from_env()
    
    def _load_from_env(self):
        """Carrega configurações de variáveis de ambiente"""
        # Configurações do banco de dados
        self.database.host = os.getenv('DB_HOST', self.database.host)
        self.database.port = int(os.getenv('DB_PORT', self.database.port))
        self.database.database = os.getenv('DB_NAME', self.database.database)
        self.database.user = os.getenv('DB_USER', self.database.user)
        self.database.password = os.getenv('DB_PASSWORD', self.database.password)
        
        # Configurações da aplicação
        self.app.debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
        self.app.log_level = os.getenv('LOG_LEVEL', self.app.log_level)
        
        # Configurações de segurança
        self.security.password_min_length = int(os.getenv('PASSWORD_MIN_LENGTH', self.security.password_min_length))
    
    def get_database_url(self) -> str:
        """Retorna a URL de conexão do banco de dados"""
        return f"postgresql://{self.database.user}:{self.database.password}@{self.database.host}:{self.database.port}/{self.database.database}"
    
    def get_app_info(self) -> Dict[str, str]:
        """Retorna informações da aplicação"""
        return {
            'name': self.app.app_name,
            'version': self.app.app_version,
            'description': self.app.app_description
        }
    
    def is_development(self) -> bool:
        """Verifica se está em modo de desenvolvimento"""
        return self.app.debug_mode
    
    def get_log_config(self) -> Dict[str, Any]:
        """Retorna configurações de logging"""
        return {
            'level': self.app.log_level,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': 'eduai.log' if not self.app.debug_mode else None
        }

# Instância global de configuração
config = Config()

# Constantes da aplicação
class Constants:
    """Constantes da aplicação"""
    
    # Diretórios
    IMAGES_DIR = Path("assets/images")
    LOGS_DIR = Path("logs")
    CACHE_DIR = Path("cache")
    
    # Arquivos
    LOGO_WHITE = IMAGES_DIR / "LogoBrancaSemFundo - Editado.png"
    LOGO_BLACK = IMAGES_DIR / "LogoPretaSemFundo - Editado.png"
    LOGO_ORIGINAL = IMAGES_DIR / "Logo.jpg"
    
    # Mensagens
    WELCOME_MESSAGE = "Bem-vindo ao EduAI!"
    LOGIN_SUCCESS = "Login realizado com sucesso!"
    LOGOUT_SUCCESS = "Logout realizado com sucesso!"
    SAVE_SUCCESS = "Dados salvos com sucesso!"
    DELETE_SUCCESS = "Item removido com sucesso!"
    
    # Erros
    DATABASE_ERROR = "Erro de conexão com o banco de dados"
    VALIDATION_ERROR = "Erro de validação de dados"
    AUTHENTICATION_ERROR = "Erro de autenticação"
    PERMISSION_ERROR = "Erro de permissão"
    
    # Validações
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 50
    MIN_AGE = 1
    MAX_AGE = 120
    MIN_GRADE = 0.0
    MAX_GRADE = 10.0

# Instância global de constantes
constants = Constants()
