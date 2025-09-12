# 🎓 EduAI - Plataforma de Ensino Inteligente

Uma aplicação desktop moderna e intuitiva para aprendizado personalizado, desenvolvida em Python com PySide6 (PyQt6).

## ✨ Características

- 🔐 **Sistema de Login**: Autenticação segura com hash de senhas e interface elegante
- 🎨 **Interface Moderna**: Design elegante e responsivo com logos personalizadas
- 🔍 **Busca Inteligente**: Sistema de busca para encontrar aulas personalizadas
- 📚 **Aulas Simuladas**: Gera conteúdo educacional baseado nas perguntas do usuário
- 📋 **Histórico**: Mantém registro das buscas realizadas (últimas 3)
- 💡 **Dicas Interativas**: Sugestões para melhorar a experiência de aprendizado
- 👤 **Perfil do Usuário**: Informações do usuário logado no cabeçalho
- ❓ **Ajuda Contextual**: Botão de ajuda "sticky" no canto inferior direito
- 🖼️ **Logos Personalizadas**: Logo branca no login e logo preta no dashboard

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10+ recomendado
- PySide6 (PyQt6)
- qtawesome
- Arquivos de logo na pasta `Imagens/`

### Instalação e Execução

1. **Clone ou baixe o projeto**
   ```bash
   git clone https://github.com/RyanBezerra/TCC-secreto.git
   cd TCC-secreto
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação**
   ```bash
   python app.py
   ```

## 🎯 Como Usar

### 🔐 Login
1. **Execute a aplicação**: `python app.py`
2. **Faça login** com as credenciais:
   - **Email/Usuário**: `admin@eduai.com`
   - **Senha**: `123456`
3. **Acesse o dashboard** após o login bem-sucedido

### 📚 Dashboard Principal
1. **Faça uma pergunta**: Digite sua dúvida no campo de busca
   - Exemplo: "Como resolver equações do segundo grau?"
   - Seja específico para melhores resultados

2. **Busque a aula**: Clique em "Buscar"

3. **Explore o conteúdo**: A aplicação gerará uma aula personalizada com:
   - Objetivos de aprendizagem
   - Conteúdo estruturado
   - Exercícios práticos
   - Dicas de estudo

4. **Use as funcionalidades**:
   - **Histórico**: Veja suas buscas anteriores (máx. 3 entradas)
   - **Dicas**: Acesse sugestões para melhorar sua experiência
   - **Logout**: Use o botão de sair no canto superior direito
   - **Ajuda**: Consulte o botão de ajuda "sticky" no canto inferior direito

## 🛠️ Funcionalidades

### Área Principal

- **Campo de Busca**: Digite suas perguntas educacionais
- **Área de Aula**: Visualize o conteúdo gerado
- **Histórico**: Acesse buscas anteriores

### Botões de Ação

- **🔄 Buscar**: Encontra a melhor aula para sua pergunta
- **📖 Histórico**: Mostra suas últimas 3 buscas
- **💡 Dicas**: Sugestões para melhorar o aprendizado

### Interface Responsiva

- **Layout Adaptativo**: Alterna entre 1 e 2 colunas baseado na largura da janela
- **Escala Inteligente**: Ajusta margens e tamanhos baseado na resolução da tela
- **Botão de Ajuda Sticky**: Sempre visível no canto inferior direito

## 📁 Estrutura do Projeto

```
TCC-secreto/
├── app.py              # Aplicação principal (Dashboard)
├── login.py            # Tela de login e autenticação
├── requirements.txt    # Dependências do projeto
├── users.json          # Arquivo de usuários (criado automaticamente)
├── Imagens/            # Pasta com logos personalizadas
│   ├── LogoBrancaSemFundo - Editado.png  # Logo para tela de login
│   ├── LogoPretaSemFundo - Editado.png   # Logo para dashboard
│   ├── LogoBrancaSemFundo.png
│   └── LogoPretaSemFundo.png
└── README.md          # Documentação
```

## 🎨 Tecnologias Utilizadas

- **Python 3.x**: Linguagem principal
- **PySide6 (PyQt6)**: Interface gráfica moderna
- **QtAwesome**: Ícones Font Awesome
- **Grid Layout**: Sistema de layout responsivo
- **QPixmap**: Manipulação de imagens e logos
- **JSON**: Armazenamento de dados de usuários

## 🔧 Desenvolvimento

### Estrutura do Código

- `EduAIApp`: Classe principal da aplicação (Dashboard)
- `LoginWindow`: Classe da tela de login e autenticação
- `EduAIManager`: Gerenciador principal que controla o fluxo entre login e dashboard
- `_create_header()`: Cria o cabeçalho com logo e informações do usuário
- `_on_search()`: Processa as buscas e gera aulas
- `_generate_mock_lesson()`: Gera conteúdo educacional simulado
- `_update_responsive_layout()`: Gerencia layout responsivo
- `_apply_scale_metrics()`: Ajusta escala baseada na resolução da tela

### Personalização

A aplicação pode ser facilmente personalizada:

- **Logos**: Substitua os arquivos na pasta `Imagens/` para personalizar as logos
- **Cores e temas**: Modifique os estilos CSS no código
- **Tamanhos de logo**: Ajuste as dimensões em `login.py` (135x135) e `app.py` (48x48)
- **Funcionalidades adicionais**: Adicione novas seções e funcionalidades
- **Integração com APIs de IA real**: Substitua o sistema de aulas simuladas
- **Banco de dados**: Implemente persistência mais robusta
- **Responsividade**: O botão de ajuda é posicionado de forma "sticky" via `resizeEvent`

## 🚧 Melhorias Futuras

- [x] Sistema de login e perfis de usuário
- [x] Logos personalizadas para login e dashboard
- [x] Interface responsiva e escalável
- [x] Sistema de histórico de buscas
- [ ] Integração com APIs de IA real (OpenAI, etc.)
- [ ] Banco de dados para persistência
- [ ] Exportação de aulas em PDF
- [ ] Sistema de avaliação e feedback
- [ ] Múltiplos idiomas
- [ ] Modo offline com conteúdo pré-carregado
- [ ] Tema claro/escuro com alternância
- [ ] Sistema de recuperação de senha
- [ ] Cadastro de novos usuários
- [ ] Sistema de notificações
- [ ] Métricas de progresso do usuário

## 📝 Licença

Este projeto foi desenvolvido como parte do TCC (Trabalho de Conclusão de Curso).

## 👨‍💻 Autor

Desenvolvido para demonstrar conceitos de interface gráfica e aplicações educacionais.

---

**🎓 Aprenda de forma inteligente e personalizada com o EduAI!**

