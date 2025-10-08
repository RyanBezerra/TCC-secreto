"""
EduAI - Sistema de Validação
Sistema centralizado de validação de dados
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from ..config import constants

@dataclass
class ValidationResult:
    """Resultado de uma validação"""
    is_valid: bool
    errors: List[str]
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
    
    def add_error(self, error: str):
        """Adiciona um erro"""
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, warning: str):
        """Adiciona um aviso"""
        self.warnings.append(warning)
    
    def has_errors(self) -> bool:
        """Verifica se há erros"""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """Verifica se há avisos"""
        return len(self.warnings) > 0

class Validator:
    """Classe base para validadores"""
    
    @staticmethod
    def validate_username(username: str) -> ValidationResult:
        """Valida nome de usuário"""
        result = ValidationResult(True, [])
        
        if not username:
            result.add_error("Nome de usuário é obrigatório")
            return result
        
        username = username.strip()
        
        if len(username) < constants.MIN_USERNAME_LENGTH:
            result.add_error(f"Nome de usuário deve ter pelo menos {constants.MIN_USERNAME_LENGTH} caracteres")
        
        if len(username) > constants.MAX_USERNAME_LENGTH:
            result.add_error(f"Nome de usuário deve ter no máximo {constants.MAX_USERNAME_LENGTH} caracteres")
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            result.add_error("Nome de usuário deve conter apenas letras, números e underscore")
        
        if username.startswith('_') or username.endswith('_'):
            result.add_warning("Nome de usuário não deve começar ou terminar com underscore")
        
        return result
    
    @staticmethod
    def validate_password(password: str, confirm_password: str = None) -> ValidationResult:
        """Valida senha"""
        result = ValidationResult(True, [])
        
        if not password:
            result.add_error("Senha é obrigatória")
            return result
        
        if len(password) < 6:
            result.add_error("Senha deve ter pelo menos 6 caracteres")
        
        if len(password) > 128:
            result.add_error("Senha deve ter no máximo 128 caracteres")
        
        # Verificar se contém pelo menos uma letra
        if not re.search(r'[a-zA-Z]', password):
            result.add_warning("Senha deve conter pelo menos uma letra")
        
        # Verificar se contém pelo menos um número
        if not re.search(r'\d', password):
            result.add_warning("Senha deve conter pelo menos um número")
        
        # Verificar confirmação de senha
        if confirm_password is not None and password != confirm_password:
            result.add_error("Senhas não coincidem")
        
        return result
    
    @staticmethod
    def validate_age(age: Any) -> ValidationResult:
        """Valida idade"""
        result = ValidationResult(True, [])
        
        if age is None or age == "":
            result.add_error("Idade é obrigatória")
            return result
        
        try:
            age_int = int(age)
        except (ValueError, TypeError):
            result.add_error("Idade deve ser um número válido")
            return result
        
        if age_int < constants.MIN_AGE:
            result.add_error(f"Idade deve ser pelo menos {constants.MIN_AGE} anos")
        
        if age_int > constants.MAX_AGE:
            result.add_error(f"Idade deve ser no máximo {constants.MAX_AGE} anos")
        
        return result
    
    @staticmethod
    def validate_grade(grade: Any) -> ValidationResult:
        """Valida nota"""
        result = ValidationResult(True, [])
        
        if grade is None or grade == "":
            return result  # Nota é opcional
        
        try:
            grade_float = float(grade)
        except (ValueError, TypeError):
            result.add_error("Nota deve ser um número válido")
            return result
        
        if grade_float < constants.MIN_GRADE:
            result.add_error(f"Nota deve ser pelo menos {constants.MIN_GRADE}")
        
        if grade_float > constants.MAX_GRADE:
            result.add_error(f"Nota deve ser no máximo {constants.MAX_GRADE}")
        
        return result
    
    @staticmethod
    def validate_email(email: str) -> ValidationResult:
        """Valida email (para uso futuro)"""
        result = ValidationResult(True, [])
        
        if not email:
            result.add_error("Email é obrigatório")
            return result
        
        email = email.strip().lower()
        
        # Regex básico para email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            result.add_error("Email deve ter um formato válido")
        
        return result
    
    @staticmethod
    def validate_user_data(data: Dict[str, Any]) -> ValidationResult:
        """Valida dados completos do usuário"""
        result = ValidationResult(True, [])
        
        # Validar nome de usuário
        username_result = Validator.validate_username(data.get('nome', ''))
        if not username_result.is_valid:
            result.errors.extend(username_result.errors)
            result.is_valid = False
        result.warnings.extend(username_result.warnings)
        
        # Validar idade
        age_result = Validator.validate_age(data.get('idade'))
        if not age_result.is_valid:
            result.errors.extend(age_result.errors)
            result.is_valid = False
        result.warnings.extend(age_result.warnings)
        
        # Validar senha (se fornecida)
        if 'senha' in data:
            password_result = Validator.validate_password(
                data.get('senha', ''),
                data.get('confirmar_senha')
            )
            if not password_result.is_valid:
                result.errors.extend(password_result.errors)
                result.is_valid = False
            result.warnings.extend(password_result.warnings)
        
        # Validar nota (se fornecida)
        if 'nota' in data:
            grade_result = Validator.validate_grade(data.get('nota'))
            if not grade_result.is_valid:
                result.errors.extend(grade_result.errors)
                result.is_valid = False
            result.warnings.extend(grade_result.warnings)
        
        return result

class SearchValidator:
    """Validador específico para buscas"""
    
    @staticmethod
    def validate_search_query(query: str) -> ValidationResult:
        """Valida query de busca"""
        result = ValidationResult(True, [])
        
        if not query:
            result.add_error("Query de busca é obrigatória")
            return result
        
        query = query.strip()
        
        if len(query) < 3:
            result.add_error("Query deve ter pelo menos 3 caracteres")
        
        if len(query) > 500:
            result.add_error("Query deve ter no máximo 500 caracteres")
        
        # Verificar caracteres especiais perigosos
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
        for char in dangerous_chars:
            if char in query:
                result.add_warning(f"Query contém caractere especial: {char}")
        
        return result

class DatabaseValidator:
    """Validador específico para dados do banco"""
    
    @staticmethod
    def validate_user_id(user_id: Any) -> ValidationResult:
        """Valida ID do usuário"""
        result = ValidationResult(True, [])
        
        if user_id is None:
            result.add_error("ID do usuário é obrigatório")
            return result
        
        try:
            user_id_int = int(user_id)
        except (ValueError, TypeError):
            result.add_error("ID do usuário deve ser um número válido")
            return result
        
        if user_id_int <= 0:
            result.add_error("ID do usuário deve ser um número positivo")
        
        return result
    
    @staticmethod
    def validate_aula_id(aula_id: Any) -> ValidationResult:
        """Valida ID da aula"""
        result = ValidationResult(True, [])
        
        if aula_id is None:
            result.add_error("ID da aula é obrigatório")
            return result
        
        try:
            aula_id_int = int(aula_id)
        except (ValueError, TypeError):
            result.add_error("ID da aula deve ser um número válido")
            return result
        
        if aula_id_int <= 0:
            result.add_error("ID da aula deve ser um número positivo")
        
        return result

# Instâncias globais dos validadores
validator = Validator()
search_validator = SearchValidator()
db_validator = DatabaseValidator()
