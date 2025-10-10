"""
EduAI - Core Module
Módulo principal com lógica de negócio e gerenciamento da aplicação
"""

from .app import EduAIApp, EduAIManager
from .database import DatabaseManager, db_manager

__all__ = ['EduAIApp', 'EduAIManager', 'DatabaseManager', 'db_manager']
