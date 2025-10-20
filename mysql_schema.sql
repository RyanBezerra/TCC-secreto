-- EduAI - Script de Inicialização do Banco MySQL
-- Este script cria todas as tabelas necessárias para o sistema EduAI
-- Execute este script no phpMyAdmin ou via linha de comando MySQL

-- Configurar charset e collation
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = 'utf8mb4_unicode_ci';

-- Usar o banco correto
USE u359247811_biocalculadora;

-- =====================================================
-- TABELA DE USUÁRIOS
-- =====================================================
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
    
    -- Índices
    INDEX idx_usuario_nome (nome),
    INDEX idx_usuario_perfil (perfil),
    INDEX idx_usuario_ativo (ativo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA DE AULAS
-- =====================================================
CREATE TABLE IF NOT EXISTS aulas (
    id_aula INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    tags TEXT,
    legendas TEXT,
    embedding_json LONGTEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices
    INDEX idx_aulas_titulo (titulo),
    INDEX idx_aulas_data_criacao (data_criacao),
    FULLTEXT idx_aulas_fulltext (titulo, descricao, tags)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA DE HISTÓRICO
-- =====================================================
CREATE TABLE IF NOT EXISTS historico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_aula INT NULL,
    mensagem_usuario TEXT NOT NULL,
    resposta_llm TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Chaves estrangeiras
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_aula) REFERENCES aulas(id_aula) ON DELETE SET NULL,
    
    -- Índices
    INDEX idx_historico_usuario (id_usuario),
    INDEX idx_historico_aula (id_aula),
    INDEX idx_historico_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA DE SUGESTÕES DE AULAS
-- =====================================================
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
    
    -- Índices
    INDEX idx_sugestoes_sugerido_por (sugerido_por),
    INDEX idx_sugestoes_status (status),
    INDEX idx_sugestoes_categoria (categoria),
    INDEX idx_sugestoes_data_criacao (data_criacao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA DE FEEDBACK
-- =====================================================
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
    
    -- Chaves estrangeiras
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (id_aula) REFERENCES aulas(id_aula) ON DELETE CASCADE,
    
    -- Índices
    INDEX idx_feedback_usuario (id_usuario),
    INDEX idx_feedback_aula (id_aula),
    INDEX idx_feedback_rating (rating),
    INDEX idx_feedback_data (data_criacao),
    INDEX idx_feedback_tipo (tipo_feedback)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- TABELA DE INSTITUIÇÕES
-- =====================================================
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
    
    -- Índices
    INDEX idx_instituicoes_cnpj (cnpj),
    INDEX idx_instituicoes_nome (nome),
    INDEX idx_instituicoes_cidade (cidade),
    INDEX idx_instituicoes_estado (estado),
    INDEX idx_instituicoes_tipo (tipo_instituicao)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- DADOS INICIAIS
-- =====================================================

-- Inserir usuário administrador padrão (senha: admin123)
-- Hash da senha 'admin123' usando bcrypt
INSERT IGNORE INTO usuario (nome, idade, senha_hash, perfil, data_cadastro) 
VALUES ('admin', 30, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KzKz2K', 'admin', CURRENT_TIMESTAMP);

-- Inserir alguns dados de exemplo para aulas
INSERT IGNORE INTO aulas (titulo, descricao, tags, legendas) VALUES 
('Introdução à Programação', 'Aula básica sobre conceitos de programação e algoritmos', 'programação, básico, introdução', 'Conceitos fundamentais de programação e desenvolvimento de software'),
('Matemática Básica', 'Operações matemáticas fundamentais e resolução de problemas', 'matemática, básico, operações', 'Adição, subtração, multiplicação, divisão e problemas matemáticos'),
('História do Brasil', 'Período colonial, independência e república', 'história, brasil, colonial', 'Fatos históricos importantes do Brasil desde o descobrimento'),
('Física - Mecânica', 'Conceitos básicos de mecânica clássica', 'física, mecânica, movimento', 'Leis de Newton, movimento retilíneo e circular'),
('Química Orgânica', 'Compostos orgânicos e suas propriedades', 'química, orgânica, compostos', 'Hidrocarbonetos, álcoois, ácidos e bases orgânicas');

-- Inserir algumas sugestões de exemplo
INSERT IGNORE INTO sugestoes_aulas (titulo, categoria, nivel_dificuldade, duracao_estimada, descricao, objetivos, sugerido_por, status) VALUES 
('Aula de Python para Iniciantes', 'Programação', 'Iniciante', 60, 'Aula introdutória sobre Python com exemplos práticos', 'Ensinar sintaxe básica, variáveis, estruturas de controle', 'admin', 'Aprovado'),
('Matemática Financeira', 'Matemática', 'Intermediário', 90, 'Conceitos de juros, descontos e aplicações financeiras', 'Calcular juros simples e compostos, entender inflação', 'admin', 'Pendente');

-- =====================================================
-- VERIFICAÇÃO FINAL
-- =====================================================

-- Mostrar tabelas criadas
SHOW TABLES;

-- Mostrar estrutura das tabelas principais
DESCRIBE usuario;
DESCRIBE aulas;
DESCRIBE historico;
DESCRIBE sugestoes_aulas;
DESCRIBE feedback;
DESCRIBE instituicoes;

-- Mostrar dados iniciais
SELECT 'Usuários criados:' as info;
SELECT id, nome, perfil, data_cadastro FROM usuario;

SELECT 'Aulas criadas:' as info;
SELECT id_aula, titulo, data_criacao FROM aulas;

SELECT 'Sugestões criadas:' as info;
SELECT id, titulo, categoria, status FROM sugestoes_aulas;

-- =====================================================
-- COMENTÁRIOS FINAIS
-- =====================================================

/*
ESTRUTURA CRIADA COM SUCESSO!

Tabelas criadas:
✅ usuario - Usuários do sistema (admin, educador, aluno)
✅ aulas - Conteúdo das aulas com embeddings
✅ historico - Histórico de conversas com IA
✅ sugestoes_aulas - Sugestões de novas aulas
✅ feedback - Avaliações dos usuários
✅ instituicoes - Dados das instituições

Dados iniciais:
✅ Usuário admin (admin/admin123)
✅ 5 aulas de exemplo
✅ 2 sugestões de exemplo

Próximos passos:
1. Execute este script no phpMyAdmin
2. Verifique se todas as tabelas foram criadas
3. Teste a aplicação EduAI
4. Faça login com admin/admin123

Para executar via linha de comando:
mysql -h auth-db1524.hstgr.io -P 3306 -u u359247811_admin2 -p u359247811_biocalculadora < mysql_schema.sql
*/
