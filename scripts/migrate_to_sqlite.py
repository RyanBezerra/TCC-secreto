#!/usr/bin/env python3
"""
Script para migrar a estrutura do banco PostgreSQL para SQLite
EduAI - Sistema de Ensino Inteligente
"""

import sqlite3
import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

def create_sqlite_schema():
    """Cria o schema SQLite baseado na estrutura PostgreSQL"""
    
    # Conectar ao banco SQLite
    db_path = Path(__file__).parent.parent / "database" / "eduai_local.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Habilitar foreign keys
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Criar tabela de usuários (adaptada para SQLite)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100) UNIQUE NOT NULL,
                idade INTEGER,
                senha_hash VARCHAR(255) NOT NULL,
                nota DECIMAL(5,2),
                perfil VARCHAR(20) DEFAULT 'aluno' CHECK (perfil IN ('admin', 'educador', 'aluno')),
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acesso TIMESTAMP,
                ativo BOOLEAN DEFAULT 1
            )
        """)
        
        # Criar tabela de aulas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aulas (
                id_aula INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo VARCHAR(200) NOT NULL,
                descricao TEXT,
                tags TEXT,
                legendas TEXT,
                embedding_json TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Criar tabela de histórico
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_aula INTEGER,
                mensagem_usuario TEXT NOT NULL,
                resposta_llm TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
                FOREIGN KEY (id_aula) REFERENCES aulas(id_aula) ON DELETE SET NULL
            )
        """)
        
        # Criar tabela de sugestões de aulas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sugestoes_aulas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        
        # Criar tabela de feedback
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_aula INTEGER NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                comentario TEXT,
                tipo_feedback VARCHAR(50) DEFAULT 'aula' CHECK (tipo_feedback IN ('aula', 'conteudo', 'dificuldade', 'geral')),
                anonimo BOOLEAN DEFAULT 0,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
                FOREIGN KEY (id_aula) REFERENCES aulas(id_aula) ON DELETE CASCADE
            )
        """)
        
        # Criar tabela de instituições
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS instituicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        
        # Criar índices para performance
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_usuario_nome ON usuario(nome)",
            "CREATE INDEX IF NOT EXISTS idx_usuario_perfil ON usuario(perfil)",
            "CREATE INDEX IF NOT EXISTS idx_aulas_titulo ON aulas(titulo)",
            "CREATE INDEX IF NOT EXISTS idx_historico_usuario ON historico(id_usuario)",
            "CREATE INDEX IF NOT EXISTS idx_historico_aula ON historico(id_aula)",
            "CREATE INDEX IF NOT EXISTS idx_historico_timestamp ON historico(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_sugestoes_sugerido_por ON sugestoes_aulas(sugerido_por)",
            "CREATE INDEX IF NOT EXISTS idx_sugestoes_status ON sugestoes_aulas(status)",
            "CREATE INDEX IF NOT EXISTS idx_feedback_usuario ON feedback(id_usuario)",
            "CREATE INDEX IF NOT EXISTS idx_feedback_aula ON feedback(id_aula)",
            "CREATE INDEX IF NOT EXISTS idx_feedback_rating ON feedback(rating)",
            "CREATE INDEX IF NOT EXISTS idx_feedback_data ON feedback(data_criacao)",
            "CREATE INDEX IF NOT EXISTS idx_instituicoes_cnpj ON instituicoes(cnpj)",
            "CREATE INDEX IF NOT EXISTS idx_instituicoes_nome ON instituicoes(nome)",
            "CREATE INDEX IF NOT EXISTS idx_instituicoes_cidade ON instituicoes(cidade)",
            "CREATE INDEX IF NOT EXISTS idx_instituicoes_estado ON instituicoes(estado)"
        ]
        
        for index_sql in indices:
            cursor.execute(index_sql)
        
        # Inserir usuário administrador padrão (senha: admin123)
        cursor.execute("""
            INSERT OR IGNORE INTO usuario (nome, idade, senha_hash, perfil, data_cadastro)
            VALUES ('admin', 30, 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'admin', CURRENT_TIMESTAMP)
        """)
        
        # Inserir alguns dados de exemplo
        cursor.execute("""
            INSERT OR IGNORE INTO aulas (titulo, descricao, tags, legendas)
            VALUES 
                ('Introdução à Programação', 'Aula básica sobre conceitos de programação', 'programação, básico, introdução', 'Conceitos fundamentais de programação'),
                ('Matemática Básica', 'Operações matemáticas fundamentais', 'matemática, básico, operações', 'Adição, subtração, multiplicação e divisão'),
                ('História do Brasil', 'Período colonial e independência', 'história, brasil, colonial', 'Fatos históricos importantes do Brasil')
        """)
        
        conn.commit()
        print("✅ Schema SQLite criado com sucesso!")
        print("✅ Tabelas criadas: usuario, aulas, historico, sugestoes_aulas, feedback, instituicoes")
        print("✅ Índices criados para otimização de performance")
        print("✅ Usuário administrador criado (admin/admin123)")
        print("✅ Dados de exemplo inseridos")
        
    except Exception as e:
        print(f"❌ Erro ao criar schema SQLite: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    print("🚀 Iniciando migração para SQLite...")
    print("=" * 50)
    
    # Criar schema
    create_sqlite_schema()
    
    print("\n" + "=" * 50)
    print("✅ Migração concluída com sucesso!")
    print("💡 Para testar a conexão, execute: python scripts/test_sqlite_connection.py")
    print("📝 Próximos passos:")
    print("   1. Atualizar configuração para usar SQLite")
    print("   2. Testar a aplicação com o banco local")
    print("   3. Verificar se todas as funcionalidades estão funcionando")
