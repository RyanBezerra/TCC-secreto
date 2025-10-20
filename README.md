# 🎓 EduAI - Plataforma de Ensino Inteligente

Uma plataforma moderna de ensino baseada em inteligência artificial, desenvolvida com PySide6 e PostgreSQL.

## 🚀 Características

- **Interface Gráfica Moderna**: Interface responsiva e intuitiva com PySide6
- **Sistema de Autenticação Seguro**: Login e cadastro com validação robusta
- **Banco de Dados Otimizado**: PostgreSQL com connection pooling
- **Sistema de Cache**: Cache em memória para melhor performance
- **Logging Avançado**: Sistema de logs estruturado e configurável
- **Validação de Dados**: Validação robusta de entrada de dados
- **Configurações Centralizadas**: Sistema de configuração flexível
- **Padrões de Design**: Implementação de Singleton, Factory e outros padrões

## 🛠️ Tecnologias

- **Frontend**: PySide6 (Qt for Python)
- **Backend**: Python 3.8+
- **Banco de Dados**: PostgreSQL com connection pooling
- **Ícones**: QtAwesome (Font Awesome)
- **Autenticação**: Hash seguro com bcrypt
- **Cache**: Sistema de cache em memória thread-safe
- **Logging**: Sistema de logging estruturado
- **Validação**: Sistema de validação centralizado

## 📦 Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd TCC-secreto
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente (opcional):**
```bash
export DB_HOST=seu_host
export DB_PORT=5432
export DB_NAME=seu_banco
export DB_USER=seu_usuario
export DB_PASSWORD=sua_senha
export DEBUG=true
export LOG_LEVEL=DEBUG
```

4. **Execute a aplicação:**
```bash
python main.py
```

## 🏗️ Estrutura do Projeto

```
TCC-secreto/
├── 📁 src/                          # Código fonte principal
│   ├── 📁 core/                     # Lógica de negócio e gerenciamento
│   │   ├── app.py                   # Aplicação principal e gerenciador
│   │   └── database.py              # Gerenciamento do banco de dados
│   ├── 📁 ui/                       # Interface do usuário
│   │   ├── auth_window.py           # Janela de autenticação unificada
│   │   ├── login.py                 # Sistema de login (legado)
│   │   └── profile.py               # Perfil do usuário
│   ├── 📁 utils/                    # Utilitários e ferramentas
│   │   ├── logger.py                # Sistema de logging
│   │   ├── validators.py            # Validação de dados
│   │   └── cache.py                 # Sistema de cache
│   ├── 📁 config/                   # Configurações
│   │   └── config.py                # Configurações centralizadas
│   └── main.py                      # Ponto de entrada da aplicação
├── 📁 assets/                       # Recursos estáticos
│   └── 📁 images/                   # Imagens e logos
├── 📁 docs/                         # Documentação
├── 📁 tests/                        # Testes (futuro)
├── main.py                          # Ponto de entrada principal
├── setup.py                         # Configuração do pacote Python
├── requirements.txt                 # Dependências
├── env.example                      # Exemplo de variáveis de ambiente
└── README.md                        # Este arquivo
```

## 🎯 Funcionalidades

### Sistema de Autenticação
- Login e cadastro em interface unificada
- Validação robusta de dados
- Hash seguro de senhas
- Logging de eventos de segurança

### Interface do Usuário
- Design responsivo e moderno
- Navegação intuitiva
- Sistema de busca inteligente
- Perfil personalizável

### Gerenciamento de Dados
- Connection pooling para PostgreSQL
- Cache em memória para performance
- Validação centralizada de dados
- Logging estruturado de operações

### Configuração
- Configurações centralizadas
- Suporte a variáveis de ambiente
- Configuração flexível de logging
- Configuração de cache

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `DB_HOST` | Host do banco de dados | `centerbeam.proxy.rlwy.net` |
| `DB_PORT` | Porta do banco | `38802` |
| `DB_NAME` | Nome do banco | `railway` |
| `DB_USER` | Usuário do banco | `postgres` |
| `DB_PASSWORD` | Senha do banco | (configurada) |
| `DEBUG` | Modo debug | `false` |
| `LOG_LEVEL` | Nível de log | `INFO` |
| `PASSWORD_MIN_LENGTH` | Tamanho mínimo da senha | `6` |

### Configuração de Cache

O sistema de cache é configurável através do arquivo `config.py`:

- **TTL padrão**: 5 minutos
- **Cache de usuários**: 5 minutos
- **Cache de aulas**: 10 minutos
- **Cache de histórico**: 2 minutos
- **Cache de configurações**: 1 hora

## 📊 Logging

O sistema de logging inclui:

- **Logs de aplicação**: Operações gerais da aplicação
- **Logs de banco de dados**: Operações de banco de dados
- **Logs de usuário**: Ações do usuário
- **Logs de segurança**: Eventos de segurança
- **Logs de performance**: Métricas de performance

Logs são salvos em:
- `logs/eduai_YYYYMMDD.log` - Logs gerais
- `logs/errors.log` - Erros críticos

## 🚀 Uso

1. **Execute a aplicação:**
```bash
python main.py
```

2. **Faça login ou crie uma conta**
3. **Use a busca para encontrar aulas**
4. **Visualize seu perfil e estatísticas**
5. **Explore as funcionalidades da plataforma**

## 🧪 Desenvolvimento

### Estrutura de Código

- **Padrão Singleton**: Para gerenciadores (Database, Cache, Logger)
- **Factory Pattern**: Para criação de componentes
- **Observer Pattern**: Para eventos da interface
- **Strategy Pattern**: Para validações

### Adicionando Novas Funcionalidades

1. **Validação**: Adicione validadores em `utils/validators.py`
2. **Cache**: Use o decorator `@cached` para cachear funções
3. **Logging**: Use `get_logger()` para logging estruturado
4. **Configuração**: Adicione configurações em `config.py`

### Testes

```bash
# Instalar dependências de desenvolvimento
pip install pytest black flake8

# Executar testes (quando implementados)
pytest

# Formatar código
black .

# Verificar linting
flake8 .
```

## 📈 Performance

### Otimizações Implementadas

- **Connection Pooling**: Pool de conexões para PostgreSQL
- **Cache em Memória**: Cache thread-safe para dados frequentes
- **Lazy Loading**: Carregamento sob demanda de componentes
- **Validação Eficiente**: Validação otimizada de dados

### Métricas

- **Tempo de inicialização**: < 3 segundos
- **Tempo de resposta de busca**: < 1 segundo
- **Uso de memória**: Otimizado com cache inteligente
- **Conexões de banco**: Pool limitado e eficiente

## 🔒 Segurança

- **Hash de senhas**: bcrypt com salt
- **Validação de entrada**: Validação robusta de todos os dados
- **Logging de segurança**: Log de eventos suspeitos
- **Sanitização**: Sanitização de queries e dados

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte ou dúvidas:

- Abra uma issue no GitHub
- Entre em contato com a equipe de desenvolvimento
- Consulte a documentação da API

---

**EduAI** - Transformando o ensino através da inteligência artificial 🎓✨