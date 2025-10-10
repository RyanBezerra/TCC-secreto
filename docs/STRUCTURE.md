# Estrutura do Projeto EduAI

## 📁 Organização de Diretórios

```
TCC-secreto/
├── 📁 src/                          # Código fonte principal
│   ├── 📁 core/                     # Lógica de negócio e gerenciamento
│   │   ├── __init__.py
│   │   ├── app.py                   # Aplicação principal e gerenciador
│   │   └── database.py              # Gerenciamento do banco de dados
│   ├── 📁 ui/                       # Interface do usuário
│   │   ├── __init__.py
│   │   ├── auth_window.py           # Janela de autenticação unificada
│   │   ├── login.py                 # Sistema de login (legado)
│   │   └── profile.py               # Perfil do usuário
│   ├── 📁 utils/                    # Utilitários e ferramentas
│   │   ├── __init__.py
│   │   ├── logger.py                # Sistema de logging
│   │   ├── validators.py            # Validação de dados
│   │   └── cache.py                 # Sistema de cache
│   ├── 📁 config/                   # Configurações
│   │   ├── __init__.py
│   │   └── config.py                # Configurações centralizadas
│   ├── __init__.py
│   └── main.py                      # Ponto de entrada da aplicação
├── 📁 assets/                       # Recursos estáticos
│   ├── 📁 images/                   # Imagens e logos
│   │   ├── LogoBrancaSemFundo - Editado.png
│   │   ├── LogoPretaSemFundo - Editado.png
│   │   └── Logo.jpg
│   └── 📁 icons/                    # Ícones (futuro)
├── 📁 docs/                         # Documentação
│   └── STRUCTURE.md                 # Este arquivo
├── 📁 tests/                        # Testes (futuro)
├── 📁 logs/                         # Arquivos de log (gerado automaticamente)
├── 📁 cache/                        # Cache da aplicação (gerado automaticamente)
├── main.py                          # Ponto de entrada principal
├── setup.py                         # Configuração do pacote Python
├── requirements.txt                 # Dependências Python
├── env.example                      # Exemplo de variáveis de ambiente
├── Dockerfile                       # Configuração Docker
├── docker-compose.yml               # Orquestração Docker
├── .gitignore                       # Arquivos ignorados pelo Git
└── README.md                        # Documentação principal
```

## 🏗️ Arquitetura

### **Core Module** (`src/core/`)
- **`app.py`**: Contém as classes principais da aplicação
  - `EduAIApp`: Janela principal do dashboard
  - `EduAIManager`: Gerenciador que controla o fluxo da aplicação
- **`database.py`**: Gerenciamento do banco de dados
  - `DatabaseManager`: Classe singleton para operações de banco
  - Connection pooling e cache integrado

### **UI Module** (`src/ui/`)
- **`auth_window.py`**: Interface unificada de login/cadastro
- **`login.py`**: Sistema de login (mantido para compatibilidade)
- **`profile.py`**: Interface do perfil do usuário

### **Utils Module** (`src/utils/`)
- **`logger.py`**: Sistema de logging estruturado
- **`validators.py`**: Validação centralizada de dados
- **`cache.py`**: Sistema de cache em memória

### **Config Module** (`src/config/`)
- **`config.py`**: Configurações centralizadas e constantes

## 🔄 Fluxo de Execução

1. **`main.py`** (raiz) → **`src/main.py`** → **`EduAIManager`**
2. **`EduAIManager`** → **`AuthWindow`** (login/cadastro)
3. **`AuthWindow`** → **`EduAIApp`** (dashboard principal)
4. **`EduAIApp`** → **`ProfileWindow`** (perfil do usuário)

## 📦 Dependências

### **Principais**
- `PySide6`: Interface gráfica
- `qtawesome`: Ícones Font Awesome
- `psycopg2-binary`: Driver PostgreSQL
- `bcrypt`: Hash de senhas

### **Desenvolvimento**
- `pytest`: Testes
- `black`: Formatação de código
- `flake8`: Linting
- `mypy`: Verificação de tipos

## 🚀 Como Executar

### **Desenvolvimento Local**
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python main.py
```

### **Docker**
```bash
# Construir e executar
docker-compose up --build

# Apenas executar
docker-compose up
```

### **Instalação como Pacote**
```bash
# Instalar em modo desenvolvimento
pip install -e .

# Executar
eduai
```

## 🔧 Configuração

### **Variáveis de Ambiente**
Copie `env.example` para `.env` e ajuste as configurações:

```bash
cp env.example .env
```

### **Configurações Principais**
- **Banco de Dados**: Host, porta, credenciais
- **Aplicação**: Debug, nível de log
- **Segurança**: Tamanho mínimo de senha
- **Cache**: TTL e configurações

## 📊 Logs

Os logs são salvos em:
- `logs/eduai_YYYYMMDD.log`: Logs gerais
- `logs/errors.log`: Erros críticos

## 🗄️ Cache

O cache é armazenado em:
- `cache/`: Arquivos de cache (se implementado)
- Memória: Cache em tempo de execução

## 🧪 Testes

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=src
```

## 📝 Desenvolvimento

### **Adicionando Novas Funcionalidades**

1. **UI**: Adicione em `src/ui/`
2. **Lógica**: Adicione em `src/core/`
3. **Utilitários**: Adicione em `src/utils/`
4. **Configurações**: Adicione em `src/config/`

### **Padrões Seguidos**
- **Singleton**: Para gerenciadores (Database, Cache, Logger)
- **Factory**: Para criação de componentes
- **Observer**: Para eventos da interface
- **Strategy**: Para validações

## 🔒 Segurança

- Hash de senhas com bcrypt
- Validação robusta de entrada
- Logging de eventos de segurança
- Sanitização de queries

## 📈 Performance

- Connection pooling para PostgreSQL
- Cache em memória thread-safe
- Lazy loading de componentes
- Validação otimizada

---

**EduAI** - Estrutura organizada e escalável para desenvolvimento contínuo! 🎓✨
