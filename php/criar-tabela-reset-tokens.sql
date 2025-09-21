-- Script SQL para criar tabela de tokens de redefinição de senha
-- Execute este script no seu banco de dados se quiser usar a funcionalidade completa

CREATE TABLE IF NOT EXISTS reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    token VARCHAR(64) NOT NULL UNIQUE,
    expira_em DATETIME NOT NULL,
    usado TINYINT(1) DEFAULT 0,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    usado_em DATETIME NULL,
    INDEX idx_token (token),
    INDEX idx_usuario (usuario_id),
    INDEX idx_expira (expira_em),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Comentário: Esta tabela armazena tokens temporários para redefinição de senha
-- Os tokens expiram em 1 hora e são únicos para cada usuário
