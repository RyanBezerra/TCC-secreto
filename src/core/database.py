"""
EduAI - Gerenciamento de Banco de Dados
Sistema de conexão e operações com PostgreSQL
"""

import psycopg2
import psycopg2.extras
import psycopg2.pool
import hashlib
import bcrypt
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from contextlib import contextmanager
from ..config import config
from ..utils.logger import get_logger, LogOperation
from ..utils.cache import cached, get_user_cache, get_aula_cache, get_historico_cache
from ..utils.validators import db_validator

# Configurar logging
logger = get_logger('database')

class DatabaseManager:
    """Classe para gerenciar conexões e operações com o banco de dados PostgreSQL"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not DatabaseManager._initialized:
            # Configurações de conexão
            self.host = config.database.host
            self.port = config.database.port
            self.database = config.database.database
            self.user = config.database.user
            self.password = config.database.password
            
            # Pool de conexões
            self.connection_pool = None
            self._initialize_pool()
            
            DatabaseManager._initialized = True
    
    def _initialize_pool(self):
        """Inicializa o pool de conexões"""
        try:
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=config.database.max_connections,
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=psycopg2.extras.RealDictCursor
            )
            logger.info("Pool de conexões inicializado com sucesso")
        except psycopg2.Error as e:
            logger.error(f"Erro ao inicializar pool de conexões: {e}")
            self.connection_pool = None
    
    @contextmanager
    def get_connection(self):
        """Context manager para obter conexão do pool"""
        connection = None
        try:
            if not self.connection_pool:
                raise psycopg2.Error("Pool de conexões não inicializado")
            
            connection = self.connection_pool.getconn()
            yield connection
        except psycopg2.Error as e:
            logger.error(f"Erro ao obter conexão: {e}")
            raise
        finally:
            if connection:
                self.connection_pool.putconn(connection)
    
    @contextmanager
    def get_cursor(self):
        """Context manager para obter cursor"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            try:
                yield cursor
                connection.commit()
            except Exception as e:
                connection.rollback()
                raise
            finally:
                cursor.close()
    
    def close_pool(self):
        """Fecha o pool de conexões"""
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("Pool de conexões fechado")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Executa uma consulta SELECT e retorna os resultados"""
        with LogOperation(f"Query: {query[:50]}..."):
            try:
                with self.get_cursor() as cursor:
                    cursor.execute(query, params)
                    results = cursor.fetchall()
                    logger.info(f"Database SELECT operation successful - returned {len(results)} rows")
                    return [dict(row) for row in results]
            except psycopg2.Error as e:
                logger.error(f"Database SELECT operation failed: {str(e)}")
                return []
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Executa uma consulta INSERT, UPDATE ou DELETE"""
        with LogOperation(f"Update: {query[:50]}..."):
            try:
                with self.get_cursor() as cursor:
                    cursor.execute(query, params)
                    logger.info("Database UPDATE operation successful")
                    return True
            except psycopg2.Error as e:
                logger.error(f"Database UPDATE operation failed: {str(e)}")
                return False
    
    def hash_password(self, password: str) -> str:
        """Cria hash da senha usando SHA-256 (para compatibilidade)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def hash_password_bcrypt(self, password: str) -> str:
        """Cria hash da senha usando bcrypt (mais seguro)"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica se a senha corresponde ao hash (suporta SHA-256 e bcrypt)"""
        try:
            # Verificar se é um hash bcrypt (começa com $2a$, $2b$, $2y$)
            if hashed_password.startswith('$2a$') or hashed_password.startswith('$2b$') or hashed_password.startswith('$2y$'):
                return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            else:
                # Verificar se é um hash SHA-256 (64 caracteres hexadecimais)
                if len(hashed_password) == 64:
                    return self.hash_password(password) == hashed_password
                else:
                    # Fallback para SHA-256
                    return self.hash_password(password) == hashed_password
        except Exception as e:
            logger.error(f"Erro ao verificar senha: {e}")
            return False
    
    # Métodos específicos para usuários
    
    def create_user(self, nome: str, idade: int, senha: str, nota: float = None) -> bool:
        """Cria um novo usuário no banco de dados"""
        senha_hash = self.hash_password(senha)
        query = """
            INSERT INTO usuario (nome, idade, senha_hash, nota, data_cadastro)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (nome, idade, senha_hash, nota, datetime.now())
        return self.execute_update(query, params)
    
    @cached('users', ttl=300)
    def get_user_by_name(self, nome: str) -> Optional[Dict]:
        """Busca usuário pelo nome"""
        query = "SELECT * FROM usuario WHERE nome = %s"
        results = self.execute_query(query, (nome,))
        return results[0] if results else None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Busca usuário pelo nome de usuário (alias para get_user_by_name)"""
        return self.get_user_by_name(username)
    
    @cached('users', ttl=300)
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Busca usuário pelo ID"""
        # Validar ID
        validation = db_validator.validate_user_id(user_id)
        if not validation.is_valid:
            logger.error(f"Invalid user ID: {validation.errors}")
            return None
            
        query = "SELECT * FROM usuario WHERE id = %s"
        results = self.execute_query(query, (user_id,))
        return results[0] if results else None
    
    def authenticate_user(self, nome: str, senha: str) -> Optional[Dict]:
        """Autentica usuário com nome e senha"""
        user = self.get_user_by_name(nome)
        if user and self.verify_password(senha, user['senha_hash']):
            # Atualizar último acesso
            self.update_last_access(user['id'])
            return user
        return None
    
    def update_last_access(self, user_id: int) -> bool:
        """Atualiza o timestamp do último acesso do usuário"""
        query = "UPDATE usuario SET ultimo_acesso = %s WHERE id = %s"
        params = (datetime.now(), user_id)
        return self.execute_update(query, params)
    
    def update_user_nota(self, user_id: int, nota: float) -> bool:
        """Atualiza a nota do usuário"""
        query = "UPDATE usuario SET nota = %s WHERE id = %s"
        params = (nota, user_id)
        return self.execute_update(query, params)
    
    def update_user_data(self, user_id: int, nome: str = None, idade: int = None, nota: float = None) -> bool:
        """Atualiza dados do usuário"""
        updates = []
        params = []
        
        if nome is not None:
            updates.append("nome = %s")
            params.append(nome)
        
        if idade is not None:
            updates.append("idade = %s")
            params.append(idade)
        
        if nota is not None:
            updates.append("nota = %s")
            params.append(nota)
        
        if not updates:
            return True  # Nada para atualizar
        
        params.append(user_id)
        query = f"UPDATE usuario SET {', '.join(updates)} WHERE id = %s"
        return self.execute_update(query, tuple(params))
    
    def get_all_users(self) -> List[Dict]:
        """Retorna todos os usuários"""
        query = "SELECT id, nome, idade, nota, data_cadastro, ultimo_acesso FROM usuario ORDER BY nome"
        return self.execute_query(query)
    
    def get_all_users_with_passwords(self) -> List[Dict]:
        """Retorna todos os usuários incluindo senhas (para debug)"""
        query = "SELECT * FROM usuario ORDER BY nome"
        return self.execute_query(query)
    
    # Métodos específicos para aulas
    
    def create_aula(self, titulo: str, descricao: str = None, tags: str = None, legendas: str = None) -> bool:
        """Cria uma nova aula"""
        query = """
            INSERT INTO aulas (titulo, descricao, tags, legendas)
            VALUES (%s, %s, %s, %s)
        """
        params = (titulo, descricao, tags, legendas)
        return self.execute_update(query, params)
    
    def get_aula_by_id(self, aula_id: int) -> Optional[Dict]:
        """Busca aula pelo ID"""
        query = "SELECT * FROM aulas WHERE id_aula = %s"
        results = self.execute_query(query, (aula_id,))
        return results[0] if results else None
    
    def get_all_aulas(self) -> List[Dict]:
        """Retorna todas as aulas"""
        query = "SELECT * FROM aulas ORDER BY titulo"
        return self.execute_query(query)
    
    def search_aulas_by_tag(self, tag: str) -> List[Dict]:
        """Busca aulas por tag"""
        query = "SELECT * FROM aulas WHERE tags ILIKE %s ORDER BY titulo"
        params = (f"%{tag}%",)
        return self.execute_query(query, params)
    
    # Métodos específicos para histórico
    
    def create_historico(self, id_usuario: int, id_aula: int, mensagem_usuario: str, resposta_llm: str) -> bool:
        """Cria uma nova entrada no histórico"""
        query = """
            INSERT INTO historico (id_usuario, id_aula, mensagem_usuario, resposta_llm, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (id_usuario, id_aula, mensagem_usuario, resposta_llm, datetime.now())
        return self.execute_update(query, params)
    
    def get_historico_by_user(self, user_id: int) -> List[Dict]:
        """Retorna histórico de um usuário"""
        query = """
            SELECT h.*, a.titulo as aula_titulo
            FROM historico h
            JOIN aulas a ON h.id_aula = a.id_aula
            WHERE h.id_usuario = %s
            ORDER BY h.timestamp DESC
        """
        return self.execute_query(query, (user_id,))
    
    def get_historico_by_aula(self, aula_id: int) -> List[Dict]:
        """Retorna histórico de uma aula"""
        query = """
            SELECT h.*, u.nome as usuario_nome
            FROM historico h
            JOIN usuario u ON h.id_usuario = u.id
            WHERE h.id_aula = %s
            ORDER BY h.timestamp DESC
        """
        return self.execute_query(query, (aula_id,))
    
    def test_connection(self) -> bool:
        """Testa a conexão com o banco de dados"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                logger.info("Teste de conexão com banco de dados: SUCESSO")
                return result is not None
        except psycopg2.Error as e:
            logger.error(f"Erro ao testar conexão: {e}")
            return False

# Instância global do gerenciador de banco de dados
db_manager = DatabaseManager()
