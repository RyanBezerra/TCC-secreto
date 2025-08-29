# 🎓 EduAI - Plataforma de Ensino Inteligente

Aplicação desktop para aprendizado personalizado, construída em Python com PyQt6.

## ✨ Principais recursos

- 🔎 Busca com IA (simulada) para sugerir “aulas” baseadas na sua pergunta
- 🧭 Layout responsivo (1 ou 2 colunas), início maximizado e alinhamentos ajustados
- 🗂️ Histórico de buscas (limitado aos 3 itens mais recentes)
- 💡 Dicas rápidas na lateral
- 🖼️ Ícones Font Awesome via `qtawesome` (pretos por padrão)
- ❓ Botão de ajuda “sticky” no canto inferior direito

## 🚀 Executando localmente (Windows)

### Pré‑requisitos
- Python 3.10+ recomendado

### Passo a passo
1) Crie o ambiente virtual
```powershell
python -m venv .venv
```

2) (Opcional) Se houver erro de certificado ao instalar pacotes, aponte o `SSL_CERT_FILE` para o certifi do venv:
```powershell
$env:SSL_CERT_FILE="$PWD\.venv\Lib\site-packages\pip\_vendor\certifi\cacert.pem"
$env:REQUESTS_CA_BUNDLE=$env:SSL_CERT_FILE
```

3) Instale as dependências
```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

4) Rode o app
```powershell
.\.venv\Scripts\python .\app.py
```

## 🧩 Como usar

1) Digite uma pergunta no campo de busca (ex.: “Como resolver equações do 2º grau?”)
2) Clique em “Buscar”
3) Veja o conteúdo simulado na área “Selecionar aula”
4) Consulte o “Histórico de Buscas” (máx. 3 entradas) e as “Dicas”

## 📁 Estrutura

```
TCC-secreto/
├── app.py              # Aplicação principal (PyQt6)
├── requirements.txt    # Dependências (PyQt6, qtawesome)
└── README.md           # Documentação
```

## 🛠️ Tecnologias

- Python 3.x
- PyQt6 (widgets, layouts, estilos)
- QtAwesome (ícones Font Awesome)

## 🔧 Notas de implementação

- O app inicia maximizado e usa `QGridLayout` para organizar: barra de busca no topo; abaixo, “Selecionar aula” à esquerda e painel lateral (Histórico/Dica) à direita.
- O histórico é truncado para os últimos 3 itens.
- O botão de ajuda é posicionado de forma “sticky” via `resizeEvent`.

## 🚧 Ideias futuras

- Integração com IA real para gerar aulas
- Persistência de histórico
- Exportação de conteúdo
- Tema claro/escuro com alternância

## 📝 Licença

Projeto acadêmico (TCC) para demonstração de UI e UX com PyQt6.
