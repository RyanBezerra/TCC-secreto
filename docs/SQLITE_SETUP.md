# Configuração do Banco SQLite Local

## Visão Geral

O sistema EduAI foi configurado para usar um banco de dados SQLite local para desenvolvimento, resolvendo os problemas de conexão com o banco PostgreSQL remoto.

## Estrutura do Banco

O banco SQLite local (`database/eduai_local.db`) contém as seguintes tabelas:

### Tabelas Principais
- **usuario**: Usuários do sistema (admin, educador, aluno)
- **aulas**: Aulas disponíveis no sistema
- **historico**: Histórico de conversas com a IA
- **sugestoes_aulas**: Sugestões de aulas enviadas pelos usuários
- **feedback**: Feedback dos alunos sobre as aulas
- **instituicoes**: Instituições de ensino cadastradas

### Tabelas Adicionais (do schema original)
- **users**: Tabela de usuários do schema PostgreSQL original
- **classes**: Tabela de aulas do schema PostgreSQL original
- **ai_suggestions**: Sugestões de IA do schema original
- **conversations**: Conversas do schema original

## Configuração

### Arquivo de Configuração
O sistema está configurado em `src/config/config.py`:

```python
@dataclass
class DatabaseConfig:
    # Configuração para SQLite (desenvolvimento local)
    use_sqlite: bool = True
    sqlite_path: str = "database/eduai_local.db"
    
    # Configuração para PostgreSQL (produção)
    host: str = "centerbeam.proxy.rlwy.net"
    port: int = 38802
    database: str = "railway"
    user: str = "postgres"
    password: str = "wQzRPlMlCdkfNjwMkZHyfabrZubqFKPC"
```

### Gerenciador de Banco
O sistema usa automaticamente o SQLite quando `use_sqlite = True`. O gerenciador é selecionado em `src/core/database.py`:

```python
def get_database_manager():
    if config.database.use_sqlite and SQLITE_AVAILABLE:
        return sqlite_db_manager
    else:
        return DatabaseManager()  # PostgreSQL
```

## Scripts Disponíveis

### 1. Verificar Estrutura do Banco
```bash
python scripts/check_sqlite_structure.py
```

### 2. Testar Conexão
```bash
python scripts/test_sqlite_connection.py
```

### 3. Popular com Dados de Exemplo
```bash
python scripts/seed_sqlite_data.py
```

### 4. Migrar Estrutura (se necessário)
```bash
python scripts/migrate_to_sqlite.py
```

## Dados de Exemplo

O banco foi populado com os seguintes dados:

### Usuários
- **Administrador**: admin / 123456
- **Professor**: professor / 123456
- **Usuários de exemplo**: João Silva, Maria Santos, Pedro Oliveira, Ana Costa, Carlos Lima

### Aulas
- Introdução à Programação
- Matemática Básica
- História do Brasil
- Física - Mecânica
- Química Orgânica
- Literatura Brasileira
- Geografia do Brasil
- Biologia Celular

### Sugestões
- Aula de Python para Iniciantes
- Matemática Financeira

## Vantagens do SQLite Local

1. **Sem dependências externas**: Não precisa de conexão com internet
2. **Desenvolvimento rápido**: Inicialização instantânea
3. **Portabilidade**: Arquivo único, fácil de compartilhar
4. **Compatibilidade**: Funciona em qualquer sistema operacional
5. **Backup simples**: Copiar o arquivo `.db`

## Alternando entre SQLite e PostgreSQL

### Para usar SQLite (desenvolvimento local):
```python
# Em src/config/config.py
use_sqlite: bool = True
```

### Para usar PostgreSQL (produção):
```python
# Em src/config/config.py
use_sqlite: bool = False
```

## Solução de Problemas

### Erro de Conexão
Se houver problemas de conexão, verifique:
1. Se o arquivo `database/eduai_local.db` existe
2. Se as permissões de escrita estão corretas
3. Se o SQLite está instalado no sistema

### Dados Corrompidos
Se o banco estiver corrompido:
1. Delete o arquivo `database/eduai_local.db`
2. Execute `python scripts/migrate_to_sqlite.py`
3. Execute `python scripts/seed_sqlite_data.py`

### Performance
Para melhorar a performance:
1. Execute `VACUUM` no banco periodicamente
2. Use índices apropriados (já criados automaticamente)
3. Considere usar WAL mode para operações concorrentes

## Logs

Os logs do sistema mostram qual banco está sendo usado:
```
2025-10-17 16:37:50,690 - EduAI.database - INFO - Usando SQLite como banco de dados local
```

## Backup e Restauração

### Backup
```bash
cp database/eduai_local.db database/eduai_local_backup_$(date +%Y%m%d).db
```

### Restauração
```bash
cp database/eduai_local_backup_YYYYMMDD.db database/eduai_local.db
```

## Conclusão

O sistema agora está configurado para usar SQLite local por padrão, resolvendo os problemas de conexão com o banco PostgreSQL remoto. Isso permite desenvolvimento local sem dependências externas e garante que o sistema funcione mesmo sem conexão com a internet.

## Credenciais de Acesso

### Usuários Principais
- **Administrador**: `admin` / `123456`
- **Professor**: `professor` / `123456`

### Usuários de Exemplo
- **João Silva** (aluno)
- **Maria Santos** (aluno)  
- **Pedro Oliveira** (aluno)
- **Ana Costa** (aluno)
- **Carlos Lima** (aluno)

### Perfis de Acesso
- **admin**: Acesso completo ao sistema
- **educador**: Acesso ao dashboard do professor
- **aluno**: Acesso ao dashboard do aluno
