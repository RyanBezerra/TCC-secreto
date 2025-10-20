"""
EduAI - Core Module
Módulo principal com lógica de negócio e gerenciamento da aplicação
"""

from .app import EduAIApp, EduAIManager
from .database import db_manager

__all__ = ['EduAIApp', 'EduAIManager', 'db_manager']
