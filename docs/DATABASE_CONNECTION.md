# Conexão com Banco de Dados - EduAI

Este documento descreve como configurar e testar a conexão com o banco de dados PostgreSQL do EduAI, incluindo instruções para configurar o DBeaver.

## 📋 Informações de Conexão

### Banco Principal (Railway)
- **Host**: `centerbeam.proxy.rlwy.net`
- **Porta**: `38802`
- **Banco**: `railway`
- **Usuário**: `postgres`
- **Senha**: `wQzRPlMlCdkfNjwMkZHyfabrZubqFKPC`
- **SSL**: Desabilitado
- **Timeout**: 30 segundos

### URL de Conexão
```
postgresql://postgres:wQzRPlMlCdkfNjwMkZHyfabrZubqFKPC@centerbeam.proxy.rlwy.net:38802/railway
```

## 🗄️ Estrutura do Banco

O banco de dados contém as seguintes tabelas:

1. **usuario** - Dados dos usuários do sistema
2. **aulas** - Conteúdo das aulas
3. **historico** - Histórico de conversas com IA
4. **feedback** - Avaliações dos usuários
5. **sugestoes_aulas** - Sugestões de novas aulas

## 🔧 Configuração do DBeaver

### Passo a Passo

1. **Abra o DBeaver**
2. **Crie uma nova conexão**:
   - Clique no ícone "Nova Conexão" (plug)
   - Selecione "PostgreSQL"
3. **Configure a conexão**:
   - **Host**: `centerbeam.proxy.rlwy.net`
   - **Port**: `38802`
   - **Database**: `railway`
   - **Username**: `postgres`
   - **Password**: `wQzRPlMlCdkfNjwMkZHyfabrZubqFKPC`
4. **Teste a conexão**:
   - Clique em "Testar Conexão"
   - Aguarde a confirmação de sucesso
5. **Salve a conexão**:
   - Clique em "OK" para salvar

### Configurações Avançadas

- **SSL Mode**: Disable
- **Connection Timeout**: 30 segundos
- **Socket Timeout**: 30 segundos
- **Login Timeout**: 30 segundos
- **TCP Keep Alive**: Habilitado

## 🧪 Testando a Conexão

### Script de Teste Automático

Execute o script de teste para verificar a conexão:

```bash
python scripts/simple-db-test.py
```

Este script irá:
- ✅ Testar a conexão com o banco
- 📊 Exibir informações do banco
- 📋 Mostrar dados de conexão para DBeaver
- 📝 Fornecer instruções de configuração

### Teste Manual

Você também pode testar a conexão manualmente usando Python:

```python
import psycopg2

try:
    conn = psycopg2.connect(
        host='centerbeam.proxy.rlwy.net',
        port=38802,
        database='railway',
        user='postgres',
        password='wQzRPlMlCdkfNjwMkZHyfabrZubqFKPC'
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro na conexão: {e}")
```

## 📁 Arquivos de Configuração

### dbeaver-connection.json
Arquivo JSON com configurações pré-definidas para importação no DBeaver. Contém:
- Configurações para banco Railway (produção)
- Configurações para banco local (Docker)
- Instruções de importação

### env.example
Arquivo de exemplo com variáveis de ambiente para configuração do banco.

## 🐳 Banco Local (Docker)

Para desenvolvimento local, você pode usar o banco PostgreSQL via Docker:

### Configuração Local
- **Host**: `localhost`
- **Porta**: `5432`
- **Banco**: `eduai`
- **Usuário**: `eduai_user`
- **Senha**: `eduai_password`

### Iniciando o Banco Local

```bash
# Navegar para o diretório docker
cd docker

# Iniciar os serviços
docker-compose up -d postgres

# Verificar se está rodando
docker-compose ps
```

## 🔍 Solução de Problemas

### Erro de Conexão
- Verifique se a internet está funcionando
- Confirme se as credenciais estão corretas
- Teste a conectividade com o host

### Timeout de Conexão
- Aumente o timeout nas configurações
- Verifique se não há firewall bloqueando
- Teste com uma conexão mais simples

### Problemas de SSL
- Certifique-se de que SSL está desabilitado
- Verifique as configurações de certificado

## 📊 Monitoramento

### Informações do Banco
- **Versão PostgreSQL**: 17.6
- **Tamanho atual**: ~8MB
- **Conexões ativas**: Monitoradas automaticamente

### Logs
Os logs de conexão são salvos em:
- `logs/eduai_YYYYMMDD.log` - Logs gerais
- `logs/errors.log` - Erros críticos

## 🔐 Segurança

### Credenciais
- As credenciais estão configuradas no arquivo `config.py`
- Para produção, use variáveis de ambiente
- Nunca commite credenciais no código

### Acesso
- A conexão é criptografada via PostgreSQL
- Use conexões seguras em produção
- Monitore tentativas de acesso

## 📞 Suporte

Se encontrar problemas:

1. Execute o script de teste: `python scripts/simple-db-test.py`
2. Verifique os logs em `logs/`
3. Consulte a documentação do PostgreSQL
4. Verifique a documentação do DBeaver

---

**Última atualização**: 08/10/2025
**Versão**: 1.0.0
