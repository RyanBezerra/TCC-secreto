CREATE DATABASE guia_estudos;


CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT CHECK (idade >= 0),
    senha_hash TEXT NOT NULL,
    nota NUMERIC(3,1),            
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acesso TIMESTAMP
);


CREATE TABLE aulas (
    id_aula SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descricao TEXT,
    tags TEXT,        
    legendas TEXT     
);

CREATE TABLE historico (
    id_historico SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    id_aula INT NOT NULL REFERENCES aulas(id_aula) ON DELETE CASCADE,
    mensagem_usuario TEXT,
    resposta_llm TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
