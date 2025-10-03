# GestiX - Sistema de Gestão Inteligente

Sistema de gestão empresarial com IA integrada para otimização de processos e aumento da produtividade.

## 🚀 Funcionalidades

- **Dashboard**: Visão geral das operações da empresa
- **Cronograma**: Gestão inteligente de turnos e escalas
- **Agendamentos**: Controle completo de consultas e serviços
- **Insights IA**: Análises inteligentes e recomendações automatizadas
- **Cadastro**: Gerenciamento de usuários e empresas

## 📁 Estrutura do Projeto

```
TCC/
├── index.html                 # Página inicial
├── configDB.php              # Configuração do banco de dados
├── css/
│   └── style.css             # Estilos principais
├── js/
│   └── app.js                # JavaScript principal
└── pages/
    ├── dashboard/
    │   ├── dashboard.html
    │   └── dasboard.css
    ├── agendamentos/
    │   ├── agendamentos.html
    │   └── agendamentos.css
    ├── cronograma/
    │   ├── cronograma.html
    │   └── cronograma.css
    ├── insights/
    │   ├── insights.html
    │   └── insights.css
    └── registro/
        ├── login/
        │   ├── login.html
        │   └── login.php
        ├── cadastro/
        │   ├── cadastro.html
        │   └── cadastro.php
        └── esqueceu-senha/
            ├── esqueceu-senha.html
            └── esqueceu-senha.php
```

## 🛠️ Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: PHP 7.4+
- **Banco de Dados**: MySQL
- **Ícones**: Feather Icons
- **Fontes**: Inter (Google Fonts)

## 📋 Pré-requisitos

- PHP 7.4 ou superior
- MySQL 5.7 ou superior
- Servidor web (Apache/Nginx) ou PHP built-in server

## 🚀 Como Executar

### 1. Configuração do Banco de Dados

Edite o arquivo `configDB.php` com as credenciais do seu banco de dados:

```php
$dbHost = 'seu_host';
$dbName = 'seu_banco';
$dbUser = 'seu_usuario';
$dbPass = 'sua_senha';
```

### 2. Executar o Servidor

#### Opção 1: Servidor PHP Built-in
```bash
cd /caminho/para/TCC
php -S localhost:8000
```

#### Opção 2: Servidor Web
Configure um servidor web (Apache/Nginx) apontando para a pasta do projeto.

### 3. Acessar o Sistema

Abra seu navegador e acesse:
- **Desenvolvimento**: `http://localhost:8000`
- **Produção**: `http://seu-dominio.com`

## 📱 Páginas do Sistema

### Página Inicial
- **URL**: `/index.html`
- **Descrição**: Página de boas-vindas com links para login e cadastro

### Autenticação
- **Login**: `/pages/registro/login/login.html`
- **Cadastro**: `/pages/registro/cadastro/cadastro.html`
- **Recuperar Senha**: `/pages/registro/esqueceu-senha/esqueceu-senha.html`

### Sistema Principal
- **Dashboard**: `/pages/dashboard/dashboard.html`
- **Cronograma**: `/pages/cronograma/cronograma.html`
- **Agendamentos**: `/pages/agendamentos/agendamentos.html`
- **Insights**: `/pages/insights/insights.html`

## 🎨 Personalização

### Cores e Tema
As variáveis CSS estão definidas no arquivo `css/style.css`:

```css
:root {
  --bg: #ffffff;
  --panel: #f8f9fa;
  --muted: #6c757d;
  --text: #212529;
  --brand: #000000;
  --ok: #28a745;
  --warn: #ffc107;
  --alert: #dc3545;
  --card: #ffffff;
  --border: #dee2e6;
}
```

### Adicionando Novas Páginas
1. Crie a pasta da nova página em `pages/`
2. Adicione os arquivos HTML e CSS
3. Atualize os links de navegação nos arquivos existentes
4. Referencie o CSS principal: `../../css/style.css`
5. Referencie o JS principal: `../../js/app.js`

## 🔧 Funcionalidades JavaScript

O arquivo `js/app.js` inclui:

- Inicialização automática de ícones Feather
- Sidebar responsiva para dispositivos móveis
- Sistema de notificações
- Utilitários para requisições AJAX
- Funções de formatação de data
- Validação de email
- Sistema de modais

## 📊 Banco de Dados

### Tabelas Principais

- **usuarios**: Dados dos usuários do sistema
- **empresas**: Informações das empresas
- **reset_tokens**: Tokens para recuperação de senha

### Estrutura de Usuários
```sql
CREATE TABLE usuarios (
    id VARCHAR(36) PRIMARY KEY,
    empresa_id INT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    cargo VARCHAR(100),
    status ENUM('ativo', 'inativo') DEFAULT 'ativo',
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚨 Solução de Problemas

### Erro de Conexão com Banco
- Verifique as credenciais em `configDB.php`
- Confirme se o servidor MySQL está rodando
- Teste a conexão manualmente

### Páginas não Carregam
- Verifique se o servidor web está rodando
- Confirme os caminhos dos arquivos CSS/JS
- Verifique o console do navegador para erros

### Problemas de Navegação
- Confirme se todos os links estão atualizados
- Verifique se os arquivos HTML existem nos caminhos corretos

## 📝 Logs e Debug

Para debug, verifique:
- Console do navegador (F12)
- Logs do servidor PHP
- Logs do servidor web

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Abra uma issue no repositório
- Entre em contato com a equipe de desenvolvimento

---

**GestiX** - Transformando a gestão empresarial com inteligência artificial.