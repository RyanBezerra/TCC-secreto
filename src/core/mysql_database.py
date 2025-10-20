"""
EduAI - Gerenciamento de Banco de Dados MySQL
Sistema de conexão e operações com MySQL
"""

import pymysql
import pymysql.cursors
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
logger = get_logger('mysql_database')

class MySQLDatabaseManager:
    """Classe para gerenciar conexões e operações com o banco de dados MySQL"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not MySQLDatabaseManager._initialized:
            # Configurações de conexão
            self.host = config.database.host
            self.port = config.database.port
            self.database = config.database.database
            self.user = config.database.user
            self.password = config.database.password
            
            # Pool de conexões
            self.connection_pool = None
            self._initialize_pool()
            
            # Garantir que as tabelas necessárias existam
            self._ensure_tables()
            
            MySQLDatabaseManager._initialized = True
    
    def _initialize_pool(self):
        """Inicializa o pool de conexões"""
        try:
            # Para MySQL, vamos usar uma conexão simples por enquanto
            # PyMySQL não tem pool nativo como psycopg2
            self.connection_pool = True
            logger.info("Conexão MySQL inicializada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar conexão MySQL: {e}")
            self.connection_pool = None
    
    def _ensure_tables(self):
        """Garante que todas as tabelas necessárias existam"""
        try:
            # Garantir tabela de usuários
            self.ensure_usuario_table()
            # Garantir tabela de aulas
            self.ensure_aulas_table()
            # Garantir tabela de sugestões
            self.ensure_suggestions_table()
            # Garantir tabela de feedback
            self.ensure_feedback_table()
            # Garantir tabela de instituições
            self.ensure_instituicoes_table()
            logger.info("Tabelas MySQL verificadas e criadas com sucesso")
        except Exception as e:
            logger.error(f"Erro ao verificar/criar tabelas MySQL: {e}")
    
    @contextmanager
    def get_connection(self):
        """Context manager para obter conexão"""
        connection = None
        try:
            if not self.connection_pool:
                raise Exception("Pool de conexões não inicializado")
            
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            
            yield connection
            
        except Exception as e:
            logger.error(f"Erro ao obter conexão MySQL: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()
    
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
    
    def test_connection(self) -> bool:
        """Testa a conexão com o banco de dados"""
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    return result is not None
        except Exception as e:
            logger.error(f"Erro ao testar conexão MySQL: {e}")
            return False
    
    def ensure_usuario_table(self) -> None:
        """Garante que a tabela usuario existe com a estrutura correta"""
        try:
            with self.get_cursor() as cursor:
                # Verificar se a tabela existe
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usuario (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nome VARCHAR(100) UNIQUE NOT NULL,
                        idade INT,
                        senha_hash VARCHAR(255) NOT NULL,
                        nota DECIMAL(5,2),
                        perfil ENUM('admin', 'educador', 'aluno') DEFAULT 'aluno',
                        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ultimo_acesso TIMESTAMP NULL,
                        ativo BOOLEAN DEFAULT TRUE,
                        
                        INDEX idx_usuario_nome (nome),
                        INDEX idx_usuario_perfil (perfil),
                        INDEX idx_usuario_ativo (ativo)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                logger.info("Tabela usuario verificada/criada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao verificar/criar tabela usuario: {e}")
            raise
    
    def ensure_aulas_table(self) -> None:
        """Garante que a tabela aulas existe"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS aulas (
                        id_aula INT AUTO_INCREMENT PRIMARY KEY,
                        titulo VARCHAR(200) NOT NULL,
                        descricao TEXT,
                        tags TEXT,
                        legendas TEXT,
                        embedding_json LONGTEXT,
                        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        
                        INDEX idx_aulas_titulo (titulo),
                        INDEX idx_aulas_data_criacao (data_criacao),
                        FULLTEXT idx_aulas_fulltext (titulo, descricao, tags)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                logger.info("Tabela aulas verificada/criada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao verificar/criar tabela aulas: {e}")
            raise
    
    def ensure_suggestions_table(self) -> None:
        """Garante a existência da tabela de sugestões"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sugestoes_aulas (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        titulo VARCHAR(255) NOT NULL,
                        categoria VARCHAR(100) NOT NULL,
                        nivel_dificuldade VARCHAR(50) NOT NULL,
                        duracao_estimada INT NOT NULL,
                        descricao TEXT NOT NULL,
                        objetivos TEXT,
                        sugerido_por VARCHAR(100) NOT NULL,
                        status ENUM('Pendente', 'Aprovado', 'Rejeitado', 'Em Análise') DEFAULT 'Pendente',
                        feedback TEXT,
                        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        data_avaliacao TIMESTAMP NULL,
                        
                        INDEX idx_sugestoes_sugerido_por (sugerido_por),
                        INDEX idx_sugestoes_status (status),
                        INDEX idx_sugestoes_categoria (categoria),
                        INDEX idx_sugestoes_data_criacao (data_criacao)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                logger.info("Tabela sugestoes_aulas verificada/criada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao verificar/criar tabela sugestoes_aulas: {e}")
            raise
    
    def ensure_feedback_table(self) -> None:
        """Garante a existência da tabela de feedback"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        id_usuario INT NOT NULL,
                        id_aula INT NOT NULL,
                        rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
                        comentario TEXT,
                        tipo_feedback ENUM('aula', 'conteudo', 'dificuldade', 'geral') DEFAULT 'aula',
                        anonimo BOOLEAN DEFAULT FALSE,
                        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        
                        FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
                        FOREIGN KEY (id_aula) REFERENCES aulas(id_aula) ON DELETE CASCADE,
                        
                        INDEX idx_feedback_usuario (id_usuario),
                        INDEX idx_feedback_aula (id_aula),
                        INDEX idx_feedback_rating (rating),
                        INDEX idx_feedback_data (data_criacao),
                        INDEX idx_feedback_tipo (tipo_feedback)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                logger.info("Tabela feedback verificada/criada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao verificar/criar tabela feedback: {e}")
            raise
    
    def ensure_instituicoes_table(self) -> None:
        """Garante a existência da tabela de instituições"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS instituicoes (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nome VARCHAR(255) NOT NULL,
                        cnpj VARCHAR(18) UNIQUE NOT NULL,
                        tipo_instituicao VARCHAR(100) NOT NULL,
                        area_atuacao VARCHAR(100) NOT NULL,
                        data_fundacao DATE NOT NULL,
                        cep VARCHAR(9) NOT NULL,
                        logradouro VARCHAR(255) NOT NULL,
                        numero VARCHAR(20) NOT NULL,
                        complemento VARCHAR(100),
                        bairro VARCHAR(100) NOT NULL,
                        cidade VARCHAR(100) NOT NULL,
                        estado VARCHAR(2) NOT NULL,
                        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        
                        INDEX idx_instituicoes_cnpj (cnpj),
                        INDEX idx_instituicoes_nome (nome),
                        INDEX idx_instituicoes_cidade (cidade),
                        INDEX idx_instituicoes_estado (estado),
                        INDEX idx_instituicoes_tipo (tipo_instituicao)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                logger.info("Tabela instituicoes verificada/criada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao verificar/criar tabela instituicoes: {e}")
            raise
    
    # Métodos básicos de operação
    def create_user(self, nome: str, idade: int, senha: str, nota: Optional[float] = None) -> bool:
        """Cria um novo usuário"""
        try:
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            with self.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuario (nome, idade, senha_hash, nota)
                    VALUES (%s, %s, %s, %s)
                """, (nome, idade, senha_hash, nota))
                
                logger.info(f"Usuário {nome} criado com sucesso")
                return True
        except Exception as e:
            logger.error(f"Erro ao criar usuário {nome}: {e}")
            return False
    
    def authenticate_user(self, nome: str, senha: str) -> Optional[Dict]:
        """Autentica um usuário"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    SELECT id, nome, idade, nota, perfil, ativo, senha_hash
                    FROM usuario WHERE nome = %s AND ativo = TRUE
                """, (nome,))
                
                user = cursor.fetchone()
                if user and bcrypt.checkpw(senha.encode('utf-8'), user['senha_hash'].encode('utf-8')):
                    # Atualizar último acesso
                    cursor.execute("""
                        UPDATE usuario SET ultimo_acesso = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """, (user['id'],))
                    
                    # Remover senha_hash do retorno
                    del user['senha_hash']
                    return user
                return None
        except Exception as e:
            logger.error(f"Erro ao autenticar usuário {nome}: {e}")
            return None
    
    def get_all_users(self) -> List[Dict]:
        """Retorna todos os usuários"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    SELECT id, nome, idade, nota, perfil, data_cadastro, ultimo_acesso, ativo
                    FROM usuario ORDER BY nome
                """)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao buscar usuários: {e}")
            return []
    
    def get_user_by_name(self, nome: str) -> Optional[Dict]:
        """Busca usuário por nome"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    SELECT id, nome, idade, nota, perfil, data_cadastro, ultimo_acesso, ativo
                    FROM usuario WHERE nome = %s
                """, (nome,))
                return cursor.fetchone()
        except Exception as e:
            logger.error(f"Erro ao buscar usuário {nome}: {e}")
            return None
    
    def get_all_aulas(self) -> List[Dict]:
        """Retorna todas as aulas"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    SELECT id_aula, titulo, descricao, tags, legendas, data_criacao
                    FROM aulas ORDER BY titulo
                """)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao buscar aulas: {e}")
            return []
    
    def create_aula(self, titulo: str, descricao: str, tags: str, legendas: str) -> bool:
        """Cria uma nova aula"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO aulas (titulo, descricao, tags, legendas)
                    VALUES (%s, %s, %s, %s)
                """, (titulo, descricao, tags, legendas))
                
                logger.info(f"Aula '{titulo}' criada com sucesso")
                return True
        except Exception as e:
            logger.error(f"Erro ao criar aula '{titulo}': {e}")
            return False
    
    def get_all_suggestions(self) -> List[Dict]:
        """Retorna todas as sugestões"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    SELECT id, titulo, categoria, nivel_dificuldade, duracao_estimada,
                           descricao, objetivos, sugerido_por, status, feedback,
                           data_criacao, data_avaliacao
                    FROM sugestoes_aulas ORDER BY data_criacao DESC
                """)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Erro ao buscar sugestões: {e}")
            return []
    
    def create_suggestion(self, suggestion_data: Dict) -> bool:
        """Cria uma nova sugestão"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO sugestoes_aulas (titulo, categoria, nivel_dificuldade, duracao_estimada,
                                               descricao, objetivos, sugerido_por, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    suggestion_data['titulo'],
                    suggestion_data['categoria'],
                    suggestion_data['nivel_dificuldade'],
                    suggestion_data['duracao_estimada'],
                    suggestion_data['descricao'],
                    suggestion_data.get('objetivos'),
                    suggestion_data['sugerido_por'],
                    suggestion_data.get('status', 'Pendente')
                ))
                
                logger.info(f"Sugestão '{suggestion_data['titulo']}' criada com sucesso")
                return True
        except Exception as e:
            logger.error(f"Erro ao criar sugestão: {e}")
            return False
    
    def get_dashboard_kpis(self) -> Dict:
        """Retorna KPIs para o dashboard"""
        try:
            with self.get_cursor() as cursor:
                # Total de usuários
                cursor.execute("SELECT COUNT(*) as total FROM usuario WHERE ativo = TRUE")
                total_users = cursor.fetchone()['total']
                
                # Total de aulas
                cursor.execute("SELECT COUNT(*) as total FROM aulas")
                total_aulas = cursor.fetchone()['total']
                
                # Total de sugestões
                cursor.execute("SELECT COUNT(*) as total FROM sugestoes_aulas")
                total_sugestoes = cursor.fetchone()['total']
                
                # Sugestões pendentes
                cursor.execute("SELECT COUNT(*) as total FROM sugestoes_aulas WHERE status = 'Pendente'")
                sugestoes_pendentes = cursor.fetchone()['total']
                
                return {
                    'total_users': total_users,
                    'total_aulas': total_aulas,
                    'total_sugestoes': total_sugestoes,
                    'sugestoes_pendentes': sugestoes_pendentes
                }
        except Exception as e:
            logger.error(f"Erro ao buscar KPIs: {e}")
            return {
                'total_users': 0,
                'total_aulas': 0,
                'total_sugestoes': 0,
                'sugestoes_pendentes': 0
            }
    
    def close_pool(self):
        """Fecha o pool de conexões"""
        self.connection_pool = None
        logger.info("Pool de conexões MySQL fechado")

# Instância global do gerenciador MySQL
mysql_db_manager = MySQLDatabaseManager()
