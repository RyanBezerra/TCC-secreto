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
            
            # Garantir que as tabelas necessárias existam
            self._ensure_tables()
            
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
    
    def _ensure_tables(self):
        """Garante que todas as tabelas necessárias existam"""
        try:
            # Garantir tabela de usuários
            self.ensure_usuario_table()
            # Garantir tabela de sugestões
            self.ensure_suggestions_table()
            # Garantir coluna de embeddings nas aulas
            self.ensure_aulas_embedding_column()
            # Garantir tabela de feedback
            self.ensure_feedback_table()
            # Garantir tabela de instituições
            self.ensure_instituicoes_table()
            logger.info("Tabelas verificadas e criadas com sucesso")
        except Exception as e:
            logger.error(f"Erro ao verificar/criar tabelas: {e}")
    
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
        query = "SELECT id, nome, idade, nota, data_cadastro, ultimo_acesso, perfil FROM usuario ORDER BY nome"
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

    def ensure_aulas_embedding_column(self) -> None:
        """Garante a existência da coluna embedding_json em aulas."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    ALTER TABLE aulas
                    ADD COLUMN IF NOT EXISTS embedding_json TEXT
                """)
        except Exception:
            pass

    def update_aula_embedding_json(self, aula_id: int, vec: List[float]) -> bool:
        """Atualiza o embedding (JSON) de uma aula."""
        import json as _json
        query = "UPDATE aulas SET embedding_json = %s WHERE id_aula = %s"
        return self.execute_update(query, (_json.dumps(vec), aula_id))

    def get_all_aulas_with_embeddings(self) -> List[Dict]:
        query = "SELECT * FROM aulas WHERE embedding_json IS NOT NULL"
        return self.execute_query(query)
    
    def search_aulas_by_tag(self, tag: str) -> List[Dict]:
        """Busca aulas por tag"""
        query = "SELECT * FROM aulas WHERE tags ILIKE %s ORDER BY titulo"
        params = (f"%{tag}%",)
        return self.execute_query(query, params)

    def search_aulas_keyword(self, query_text: str, limit: int = 5) -> List[Dict]:
        """Busca simples por palavras-chave quando embeddings não estão disponíveis."""
        # Dividir a query em palavras e remover palavras muito pequenas
        words = [word.strip() for word in query_text.split() if len(word.strip()) > 2]
        
        # Filtrar palavras muito comuns que não ajudam na busca
        common_words = {'como', 'para', 'queria', 'saber', 'meu', 'uma', 'fazer', 'usar', 'aprender'}
        words = [word for word in words if word.lower() not in common_words]
        
        if not words:
            # Se não há palavras válidas, buscar a string completa
            words = [query_text]
        
        # Construir condições OR para cada palavra
        conditions = []
        params = []
        
        for word in words:
            like_pattern = f"%{word}%"
            conditions.append("(titulo ILIKE %s OR descricao ILIKE %s OR tags ILIKE %s OR legendas ILIKE %s)")
            params.extend([like_pattern, like_pattern, like_pattern, like_pattern])
        
        # Query simplificada
        query = f"""
            SELECT *, 
                   (
                       CASE WHEN titulo ILIKE %s THEN 10 ELSE 0 END +
                       CASE WHEN descricao ILIKE %s THEN 5 ELSE 0 END +
                       CASE WHEN tags ILIKE %s THEN 8 ELSE 0 END +
                       CASE WHEN legendas ILIKE %s THEN 3 ELSE 0 END
                   ) as relevance_score
            FROM aulas 
            WHERE {' OR '.join(conditions)}
            ORDER BY relevance_score DESC, titulo
            LIMIT %s
        """
        
        # Parâmetros para o cálculo de relevância (busca principal)
        main_search_pattern = f"%{query_text}%"
        relevance_params = [main_search_pattern, main_search_pattern, main_search_pattern, main_search_pattern]
        
        # Combinar todos os parâmetros
        all_params = relevance_params + params + [limit]
        
        return self.execute_query(query, all_params)
    
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

    # ==========================
    # Relatórios para Educador
    # ==========================
    def get_all_students(self) -> List[Dict]:
        """Lista todos os usuários com perfil aluno."""
        query = """
            SELECT id, nome, idade, nota, ultimo_acesso, data_cadastro, perfil
            FROM usuario
            WHERE perfil = 'aluno'
            ORDER BY nome
        """
        return self.execute_query(query)

    def get_all_students_with_search_count(self) -> List[Dict]:
        """Lista alunos e total de pesquisas (entradas no histórico)."""
        query = """
            SELECT u.id,
                   u.nome,
                   u.idade,
                   u.nota,
                   u.ultimo_acesso,
                   u.data_cadastro,
                   u.perfil,
                   COUNT(*) FILTER (WHERE h.id_usuario IS NOT NULL) AS total_pesquisas
            FROM usuario u
            LEFT JOIN historico h ON h.id_usuario = u.id
            WHERE u.perfil = 'aluno'
            GROUP BY u.id, u.nome, u.idade, u.nota, u.ultimo_acesso, u.data_cadastro, u.perfil
            ORDER BY u.nome
        """
        return self.execute_query(query)

    def get_student_searches(self, student_id: int) -> List[Dict]:
        """Retorna todas as pesquisas do aluno (histórico com detalhes da aula)."""
        query = """
            SELECT h.timestamp,
                   h.mensagem_usuario AS pergunta,
                   h.resposta_llm,
                   a.id_aula,
                   a.titulo AS aula_titulo
            FROM historico h
            LEFT JOIN aulas a ON a.id_aula = h.id_aula
            WHERE h.id_usuario = %s
            ORDER BY h.timestamp DESC
        """
        return self.execute_query(query, (student_id,))

    def get_dashboard_kpis(self) -> Dict:
        """KPIs principais do painel (totais)."""
        # Total de alunos
        total_alunos = self.execute_query("SELECT COUNT(*) AS c FROM usuario WHERE perfil = 'aluno'")
        # Total de pesquisas (historico)
        total_pesquisas = self.execute_query("SELECT COUNT(*) AS c FROM historico")
        # "Interações com IA" pode ser igual a pesquisas para este contexto
        total_interacoes = total_pesquisas
        return {
            'total_alunos': (total_alunos[0]['c'] if total_alunos else 0),
            'total_pesquisas': (total_pesquisas[0]['c'] if total_pesquisas else 0),
            'total_interacoes': (total_interacoes[0]['c'] if total_interacoes else 0),
        }

    def get_monthly_search_counts(self, months: int = 6) -> List[Dict]:
        """Retorna contagem de pesquisas por mês (últimos N meses)."""
        query = """
            SELECT TO_CHAR(date_trunc('month', h.timestamp), 'Mon') AS mes,
                   date_trunc('month', h.timestamp) AS mes_data,
                   COUNT(*) AS total
            FROM historico h
            GROUP BY mes, mes_data
            ORDER BY mes_data DESC
            LIMIT %s
        """
        rows = self.execute_query(query, (months,))
        return list(reversed(rows)) if rows else []

    def get_nota_distribution(self) -> List[Dict]:
        """Distribuição de notas dos alunos por faixas (baixo/médio/alto)."""
        query = """
            SELECT
                SUM(CASE WHEN nota < 4 THEN 1 ELSE 0 END) AS baixo,
                SUM(CASE WHEN nota >= 4 AND nota < 7 THEN 1 ELSE 0 END) AS medio,
                SUM(CASE WHEN nota >= 7 THEN 1 ELSE 0 END) AS alto
            FROM usuario
            WHERE perfil = 'aluno'
        """
        rows = self.execute_query(query)
        if not rows:
            return []
        row = rows[0]
        return [
            {'categoria': 'Baixo', 'valor': row.get('baixo', 0)},
            {'categoria': 'Médio', 'valor': row.get('medio', 0)},
            {'categoria': 'Alto', 'valor': row.get('alto', 0)},
        ]
    
    # Métodos específicos para sugestões de aulas
    
    def create_suggestion(self, suggestion_data: Dict) -> bool:
        """Cria uma nova sugestão de aula"""
        query = """
            INSERT INTO sugestoes_aulas (
                titulo, categoria, nivel_dificuldade, duracao_estimada, 
                descricao, objetivos, sugerido_por, status, data_criacao
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            suggestion_data.get('titulo'),
            suggestion_data.get('categoria'),
            suggestion_data.get('nivel_dificuldade'),
            suggestion_data.get('duracao_estimada'),
            suggestion_data.get('descricao'),
            suggestion_data.get('objetivos'),
            suggestion_data.get('sugerido_por'),
            suggestion_data.get('status', 'Pendente'),
            datetime.now()
        )
        return self.execute_update(query, params)
    
    def get_user_suggestions(self, user_name: str) -> List[Dict]:
        """Retorna todas as sugestões de um usuário"""
        query = """
            SELECT * FROM sugestoes_aulas 
            WHERE sugerido_por = %s 
            ORDER BY data_criacao DESC
        """
        return self.execute_query(query, (user_name,))
    
    def get_all_suggestions(self) -> List[Dict]:
        """Retorna todas as sugestões (para administradores)"""
        query = """
            SELECT * FROM sugestoes_aulas 
            ORDER BY data_criacao DESC
        """
        return self.execute_query(query)
    
    def update_suggestion_status(self, suggestion_id: int, status: str, feedback: str = None) -> bool:
        """Atualiza o status de uma sugestão"""
        query = """
            UPDATE sugestoes_aulas 
            SET status = %s, feedback = %s, data_avaliacao = %s
            WHERE id = %s
        """
        params = (status, feedback, datetime.now(), suggestion_id)
        return self.execute_update(query, params)
    
    def ensure_suggestions_table(self) -> None:
        """Garante a existência da tabela de sugestões"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sugestoes_aulas (
                        id SERIAL PRIMARY KEY,
                        titulo VARCHAR(255) NOT NULL,
                        categoria VARCHAR(100) NOT NULL,
                        nivel_dificuldade VARCHAR(50) NOT NULL,
                        duracao_estimada INTEGER NOT NULL,
                        descricao TEXT NOT NULL,
                        objetivos TEXT,
                        sugerido_por VARCHAR(100) NOT NULL,
                        status VARCHAR(50) DEFAULT 'Pendente',
                        feedback TEXT,
                        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        data_avaliacao TIMESTAMP
                    )
                """)
        except Exception as e:
            logger.error(f"Erro ao criar tabela de sugestões: {e}")

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
    
    # ==========================
    # Métodos específicos para feedback
    # ==========================
    
    def ensure_feedback_table(self) -> None:
        """Garante a existência da tabela de feedback"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        id SERIAL PRIMARY KEY,
                        id_usuario INTEGER REFERENCES usuario(id) ON DELETE CASCADE,
                        id_aula INTEGER REFERENCES aulas(id_aula) ON DELETE CASCADE,
                        rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                        comentario TEXT,
                        tipo_feedback VARCHAR(50) DEFAULT 'aula' CHECK (tipo_feedback IN ('aula', 'conteudo', 'dificuldade', 'geral')),
                        anonimo BOOLEAN DEFAULT false,
                        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Criar índices se não existirem
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_feedback_usuario ON feedback(id_usuario)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_feedback_aula ON feedback(id_aula)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_feedback_rating ON feedback(rating)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_feedback_data ON feedback(data_criacao)
                """)
        except Exception as e:
            logger.error(f"Erro ao criar tabela de feedback: {e}")
    
    def create_feedback(self, user_id: int, aula_id: int, rating: int, comment: str = None, 
                       feedback_type: str = 'aula', is_anonymous: bool = False) -> bool:
        """Cria um novo feedback"""
        query = """
            INSERT INTO feedback (id_usuario, id_aula, rating, comentario, tipo_feedback, anonimo, data_criacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (user_id, aula_id, rating, comment, feedback_type, is_anonymous, datetime.now())
        return self.execute_update(query, params)
    
    def get_feedback_by_user(self, user_id: int) -> List[Dict]:
        """Retorna todos os feedbacks de um usuário"""
        query = """
            SELECT f.*, a.titulo as aula_titulo, a.descricao as aula_descricao
            FROM feedback f
            JOIN aulas a ON f.id_aula = a.id_aula
            WHERE f.id_usuario = %s
            ORDER BY f.data_criacao DESC
        """
        return self.execute_query(query, (user_id,))
    
    def get_feedback_by_aula(self, aula_id: int) -> List[Dict]:
        """Retorna todos os feedbacks de uma aula"""
        query = """
            SELECT f.*, u.nome as usuario_nome
            FROM feedback f
            JOIN usuario u ON f.id_usuario = u.id
            WHERE f.id_aula = %s
            ORDER BY f.data_criacao DESC
        """
        return self.execute_query(query, (aula_id,))
    
    def get_feedback_stats_by_aula(self, aula_id: int) -> Dict:
        """Retorna estatísticas de feedback de uma aula"""
        query = """
            SELECT 
                COUNT(*) as total_feedbacks,
                AVG(rating) as media_rating,
                COUNT(*) FILTER (WHERE rating = 5) as cinco_estrelas,
                COUNT(*) FILTER (WHERE rating = 4) as quatro_estrelas,
                COUNT(*) FILTER (WHERE rating = 3) as tres_estrelas,
                COUNT(*) FILTER (WHERE rating = 2) as duas_estrelas,
                COUNT(*) FILTER (WHERE rating = 1) as uma_estrela
            FROM feedback 
            WHERE id_aula = %s
        """
        results = self.execute_query(query, (aula_id,))
        return results[0] if results else {
            'total_feedbacks': 0,
            'media_rating': 0,
            'cinco_estrelas': 0,
            'quatro_estrelas': 0,
            'tres_estrelas': 0,
            'duas_estrelas': 0,
            'uma_estrela': 0
        }
    
    def update_feedback(self, feedback_id: int, rating: int = None, comment: str = None) -> bool:
        """Atualiza um feedback existente"""
        updates = []
        params = []
        
        if rating is not None:
            updates.append("rating = %s")
            params.append(rating)
        
        if comment is not None:
            updates.append("comentario = %s")
            params.append(comment)
        
        if not updates:
            return True  # Nada para atualizar
        
        updates.append("data_atualizacao = %s")
        params.append(datetime.now())
        params.append(feedback_id)
        
        query = f"UPDATE feedback SET {', '.join(updates)} WHERE id = %s"
        return self.execute_update(query, tuple(params))
    
    def delete_feedback(self, feedback_id: int) -> bool:
        """Remove um feedback"""
        query = "DELETE FROM feedback WHERE id = %s"
        return self.execute_update(query, (feedback_id,))
    
    def get_user_feedback_count(self, user_id: int) -> int:
        """Retorna o número total de feedbacks de um usuário"""
        query = "SELECT COUNT(*) as total FROM feedback WHERE id_usuario = %s"
        results = self.execute_query(query, (user_id,))
        return results[0]['total'] if results else 0
    
    # ==========================
    # Métodos específicos para instituições
    # ==========================
    
    def ensure_instituicoes_table(self) -> None:
        """Garante a existência da tabela de instituições"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS instituicoes (
                        id SERIAL PRIMARY KEY,
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
                        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Criar índices se não existirem
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_instituicoes_cnpj ON instituicoes(cnpj)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_instituicoes_nome ON instituicoes(nome)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_instituicoes_cidade ON instituicoes(cidade)
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_instituicoes_estado ON instituicoes(estado)
                """)
        except Exception as e:
            logger.error(f"Erro ao criar tabela de instituições: {e}")
    
    def create_instituicao(self, instituicao_data: Dict) -> Optional[int]:
        """Cria uma nova instituição e retorna o ID"""
        query = """
            INSERT INTO instituicoes (
                nome, cnpj, tipo_instituicao, area_atuacao, data_fundacao,
                cep, logradouro, numero, complemento, bairro, cidade, estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        params = (
            instituicao_data.get('nome'),
            instituicao_data.get('cnpj'),
            instituicao_data.get('tipo_instituicao'),
            instituicao_data.get('area_atuacao'),
            instituicao_data.get('data_fundacao'),
            instituicao_data.get('cep'),
            instituicao_data.get('logradouro'),
            instituicao_data.get('numero'),
            instituicao_data.get('complemento'),
            instituicao_data.get('bairro'),
            instituicao_data.get('cidade'),
            instituicao_data.get('estado')
        )
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                if result:
                    instituicao_id = result['id']
                    return instituicao_id
                return None
        except Exception as e:
            logger.error(f"Erro ao criar instituição: {e}")
            return None
    
    def get_instituicao_by_id(self, instituicao_id: int) -> Optional[Dict]:
        """Busca instituição pelo ID"""
        query = "SELECT * FROM instituicoes WHERE id = %s"
        results = self.execute_query(query, (instituicao_id,))
        return results[0] if results else None
    
    def get_instituicao_by_cnpj(self, cnpj: str) -> Optional[Dict]:
        """Busca instituição pelo CNPJ"""
        query = "SELECT * FROM instituicoes WHERE cnpj = %s"
        results = self.execute_query(query, (cnpj,))
        return results[0] if results else None
    
    def get_all_instituicoes(self) -> List[Dict]:
        """Retorna todas as instituições"""
        query = "SELECT * FROM instituicoes ORDER BY nome"
        return self.execute_query(query)
    
    def update_instituicao(self, instituicao_id: int, instituicao_data: Dict) -> bool:
        """Atualiza uma instituição existente"""
        updates = []
        params = []
        
        fields = ['nome', 'cnpj', 'tipo_instituicao', 'area_atuacao', 'data_fundacao',
                 'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
        
        for field in fields:
            if field in instituicao_data and instituicao_data[field] is not None:
                updates.append(f"{field} = %s")
                params.append(instituicao_data[field])
        
        if not updates:
            return True  # Nada para atualizar
        
        updates.append("data_atualizacao = %s")
        params.append(datetime.now())
        params.append(instituicao_id)
        
        query = f"UPDATE instituicoes SET {', '.join(updates)} WHERE id = %s"
        return self.execute_update(query, tuple(params))
    
    def delete_instituicao(self, instituicao_id: int) -> bool:
        """Remove uma instituição"""
        query = "DELETE FROM instituicoes WHERE id = %s"
        return self.execute_update(query, (instituicao_id,))
    
    def search_instituicoes(self, search_term: str) -> List[Dict]:
        """Busca instituições por nome, CNPJ ou cidade"""
        query = """
            SELECT * FROM instituicoes 
            WHERE nome ILIKE %s OR cnpj ILIKE %s OR cidade ILIKE %s
            ORDER BY nome
        """
        search_pattern = f"%{search_term}%"
        params = (search_pattern, search_pattern, search_pattern)
        return self.execute_query(query, params)
    
    def ensure_usuario_table(self) -> None:
        """Garante que a tabela usuario existe com a estrutura correta"""
        try:
            with self.get_cursor() as cursor:
                # Verificar se a tabela existe
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'usuario'
                    );
                """)
                
                result = cursor.fetchone()
                table_exists = result['exists'] if result else False
                
                if not table_exists:
                    # Criar tabela usuario
                    cursor.execute("""
                        CREATE TABLE usuario (
                            id SERIAL PRIMARY KEY,
                            nome VARCHAR(100) UNIQUE NOT NULL,
                            idade INTEGER,
                            senha_hash VARCHAR(255) NOT NULL,
                            nota DECIMAL(5,2),
                            perfil VARCHAR(20) DEFAULT 'aluno' CHECK (perfil IN ('admin', 'educador', 'aluno')),
                            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            ultimo_acesso TIMESTAMP,
                            ativo BOOLEAN DEFAULT true
                        );
                    """)
                    
                    # Criar índices
                    cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuario_nome ON usuario(nome);")
                    cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuario_perfil ON usuario(perfil);")
                    
                    logger.info("Tabela usuario criada com sucesso")
                else:
                    # Verificar se a coluna perfil existe
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns 
                            WHERE table_schema = 'public' 
                            AND table_name = 'usuario' 
                            AND column_name = 'perfil'
                        );
                    """)
                    
                    result = cursor.fetchone()
                    perfil_column_exists = result['exists'] if result else False
                    
                    if not perfil_column_exists:
                        # Adicionar coluna perfil
                        cursor.execute("""
                            ALTER TABLE usuario 
                            ADD COLUMN perfil VARCHAR(20) DEFAULT 'aluno' CHECK (perfil IN ('admin', 'educador', 'aluno'));
                        """)
                        logger.info("Coluna perfil adicionada à tabela usuario")
                    
                    # Verificar se a coluna ativo existe
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns 
                            WHERE table_schema = 'public' 
                            AND table_name = 'usuario' 
                            AND column_name = 'ativo'
                        );
                    """)
                    
                    result = cursor.fetchone()
                    ativo_column_exists = result['exists'] if result else False
                    
                    if not ativo_column_exists:
                        # Adicionar coluna ativo
                        cursor.execute("""
                            ALTER TABLE usuario 
                            ADD COLUMN ativo BOOLEAN DEFAULT true;
                        """)
                        logger.info("Coluna ativo adicionada à tabela usuario")
                
        except Exception as e:
            logger.error(f"Erro ao verificar/criar tabela usuario: {e}")
            raise

# Instância global do gerenciador de banco de dados
db_manager = DatabaseManager()
