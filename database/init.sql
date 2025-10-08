-- EduAI - Script de Inicialização do Banco de Dados
-- Este arquivo é executado automaticamente quando o container PostgreSQL é criado

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Configurar encoding e locale
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

-- Criar schema principal
CREATE SCHEMA IF NOT EXISTS eduai;

-- Definir search_path
ALTER DATABASE eduai SET search_path TO eduai, public;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS eduai.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'educator' CHECK (role IN ('admin', 'educator', 'student')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de aulas
CREATE TABLE IF NOT EXISTS eduai.classes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    subject VARCHAR(100),
    grade_level VARCHAR(50),
    duration_minutes INTEGER DEFAULT 60,
    objectives TEXT[],
    materials TEXT[],
    created_by UUID REFERENCES eduai.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de sugestões de IA
CREATE TABLE IF NOT EXISTS eduai.ai_suggestions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    class_id UUID REFERENCES eduai.classes(id) ON DELETE CASCADE,
    suggestion_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    confidence_score DECIMAL(3,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de histórico de conversas
CREATE TABLE IF NOT EXISTS eduai.conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES eduai.users(id),
    session_id VARCHAR(100),
    message_type VARCHAR(20) CHECK (message_type IN ('user', 'ai')),
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de embeddings para busca semântica
CREATE TABLE IF NOT EXISTS eduai.embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_type VARCHAR(50) NOT NULL,
    content_id UUID NOT NULL,
    embedding VECTOR(1536), -- OpenAI embeddings são 1536 dimensões
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de feedback dos alunos sobre as aulas
CREATE TABLE IF NOT EXISTS eduai.feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES eduai.users(id) ON DELETE CASCADE,
    class_id UUID REFERENCES eduai.classes(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    feedback_type VARCHAR(50) DEFAULT 'lesson' CHECK (feedback_type IN ('lesson', 'content', 'difficulty', 'general')),
    is_anonymous BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_users_username ON eduai.users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON eduai.users(email);
CREATE INDEX IF NOT EXISTS idx_classes_created_by ON eduai.classes(created_by);
CREATE INDEX IF NOT EXISTS idx_classes_subject ON eduai.classes(subject);
CREATE INDEX IF NOT EXISTS idx_ai_suggestions_class_id ON eduai.ai_suggestions(class_id);
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON eduai.conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON eduai.conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_content_type ON eduai.embeddings(content_type);
CREATE INDEX IF NOT EXISTS idx_embeddings_content_id ON eduai.embeddings(content_id);
CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON eduai.feedback(user_id);
CREATE INDEX IF NOT EXISTS idx_feedback_class_id ON eduai.feedback(class_id);
CREATE INDEX IF NOT EXISTS idx_feedback_rating ON eduai.feedback(rating);
CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON eduai.feedback(created_at);

-- Índice para busca semântica (requer extensão vector)
-- CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON eduai.embeddings USING ivfflat (embedding vector_cosine_ops);

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION eduai.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON eduai.users
    FOR EACH ROW EXECUTE FUNCTION eduai.update_updated_at_column();

CREATE TRIGGER update_classes_updated_at BEFORE UPDATE ON eduai.classes
    FOR EACH ROW EXECUTE FUNCTION eduai.update_updated_at_column();

CREATE TRIGGER update_feedback_updated_at BEFORE UPDATE ON eduai.feedback
    FOR EACH ROW EXECUTE FUNCTION eduai.update_updated_at_column();

-- Inserir usuário administrador padrão (senha: admin123)
INSERT INTO eduai.users (username, email, password_hash, full_name, role) 
VALUES (
    'admin', 
    'admin@eduai.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8Kz2', -- bcrypt hash de 'admin123'
    'Administrador do Sistema',
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- Comentários nas tabelas
COMMENT ON TABLE eduai.users IS 'Usuários do sistema EduAI';
COMMENT ON TABLE eduai.classes IS 'Aulas criadas pelos educadores';
COMMENT ON TABLE eduai.ai_suggestions IS 'Sugestões geradas pela IA';
COMMENT ON TABLE eduai.conversations IS 'Histórico de conversas com a IA';
COMMENT ON TABLE eduai.embeddings IS 'Embeddings para busca semântica';
COMMENT ON TABLE eduai.feedback IS 'Feedback dos alunos sobre as aulas';

-- Configurações de performance
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Recarregar configurações
SELECT pg_reload_conf();
