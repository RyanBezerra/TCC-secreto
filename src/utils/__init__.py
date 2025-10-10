"""
EduAI - Utilitários
Módulo de utilitários para a Plataforma de Ensino Inteligente
"""

from .logger import get_logger, log_function_call, LogOperation
from .validators import validator, search_validator, db_validator, ValidationResult
from .cache import cache_manager, cached, get_user_cache, get_aula_cache, get_historico_cache

__all__ = [
    'get_logger',
    'log_function_call', 
    'LogOperation',
    'validator',
    'search_validator',
    'db_validator',
    'ValidationResult',
    'cache_manager',
    'cached',
    'get_user_cache',
    'get_aula_cache',
    'get_historico_cache'
]
