"""
EduAI - Sistema de Logging
Sistema centralizado de logging para a aplicação
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from ..config import config

class EduAILogger:
    """Classe para gerenciamento de logs da aplicação"""
    
    _instance: Optional['EduAILogger'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._setup_logging()
            EduAILogger._initialized = True
    
    def _setup_logging(self):
        """Configura o sistema de logging"""
        # Criar diretório de logs se não existir
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configuração do logger principal
        self.logger = logging.getLogger('EduAI')
        self.logger.setLevel(getattr(logging, config.app.log_level))
        
        # Limpar handlers existentes
        self.logger.handlers.clear()
        
        # Formato das mensagens
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        # Handler para console (sempre ativo)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Handler para arquivo (apenas em produção)
        if not config.app.debug_mode:
            log_file = log_dir / f"eduai_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, 
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        # Handler para erros críticos
        error_file = log_dir / "errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
    
    def get_logger(self, name: str = None) -> logging.Logger:
        """Retorna um logger específico"""
        if name:
            return logging.getLogger(f'EduAI.{name}')
        return self.logger
    
    def log_database_operation(self, operation: str, table: str, success: bool, details: str = ""):
        """Log específico para operações de banco de dados"""
        level = logging.INFO if success else logging.ERROR
        message = f"DB {operation} on {table} - {'SUCCESS' if success else 'FAILED'}"
        if details:
            message += f" - {details}"
        self.logger.log(level, message)
    
    def log_user_action(self, user: str, action: str, success: bool, details: str = ""):
        """Log específico para ações do usuário"""
        level = logging.INFO if success else logging.WARNING
        message = f"USER {user} - {action} - {'SUCCESS' if success else 'FAILED'}"
        if details:
            message += f" - {details}"
        self.logger.log(level, message)
    
    def log_security_event(self, event: str, user: str = None, ip: str = None, details: str = ""):
        """Log específico para eventos de segurança"""
        message = f"SECURITY - {event}"
        if user:
            message += f" - User: {user}"
        if ip:
            message += f" - IP: {ip}"
        if details:
            message += f" - {details}"
        self.logger.warning(message)
    
    def log_performance(self, operation: str, duration: float, details: str = ""):
        """Log específico para métricas de performance"""
        message = f"PERFORMANCE - {operation} took {duration:.3f}s"
        if details:
            message += f" - {details}"
        self.logger.info(message)

# Instância global do logger
logger_manager = EduAILogger()

# Função de conveniência para obter logger
def get_logger(name: str = None) -> logging.Logger:
    """Função de conveniência para obter um logger"""
    return logger_manager.get_logger(name)

# Decorator para logging automático de funções
def log_function_call(logger_name: str = None):
    """Decorator para logar automaticamente chamadas de função"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} failed with error: {str(e)}")
                raise
        return wrapper
    return decorator

# Context manager para logging de operações
class LogOperation:
    """Context manager para logar operações"""
    
    def __init__(self, operation: str, logger_name: str = None):
        self.operation = operation
        self.logger = get_logger(logger_name)
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        if exc_type is None:
            self.logger.info(f"Completed {self.operation} in {duration:.3f}s")
        else:
            self.logger.error(f"Failed {self.operation} after {duration:.3f}s: {exc_val}")
        return False  # Não suprimir exceções
