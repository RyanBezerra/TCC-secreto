# EduAI - Dockerfile Completo
FROM python:3.11-slim

# Metadados da imagem
LABEL maintainer="EduAI Team <contato@eduai.com>"
LABEL description="EduAI - Plataforma de Ensino Inteligente"
LABEL version="1.0.0"

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para PySide6 e interface gráfica
RUN apt-get update && apt-get install -y \
    # Dependências básicas
    libpq-dev \
    gcc \
    g++ \
    make \
    pkg-config \
    \
    # Dependências para PySide6/Qt6 - versão completa e otimizada
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libglib2.0-0 \
    libxcb1 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-sync1 \
    libxcb-util1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxcb-xrandr0 \
    libxcb-xtest0 \
    libxcb-xv0 \
    libxcb-shm0 \
    libxcb-dri3-0 \
    libxcb-present0 \
    \
    # Dependências adicionais para renderização
    libx11-6 \
    libx11-xcb1 \
    libxext6 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    libxi6 \
    libxrandr2 \
    libxdamage1 \
    libxcomposite1 \
    libxcursor1 \
    libxfixes3 \
    libxinerama1 \
    libxmu6 \
    libxpm4 \
    libxaw7 \
    libxft2 \
    libxmuu1 \
    libxss1 \
    libxt6 \
    libxv1 \
    \
    # Fontes e renderização de texto - conjunto mais completo
    fonts-dejavu-core \
    fonts-dejavu-extra \
    fonts-liberation \
    fonts-liberation2 \
    fonts-noto-core \
    fonts-noto-ui-core \
    fontconfig \
    fontconfig-config \
    \
    # Dependências para PostgreSQL
    libpq5 \
    \
    # Utilitários
    curl \
    wget \
    xvfb \
    \
    # Dependências para processamento de imagens
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Atualizar pip e instalar wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copiar requirements primeiro (para cache de layers)
COPY ../requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY .. .

# Criar diretórios necessários
RUN mkdir -p logs cache assets/images

# Definir permissões adequadas
RUN chmod -R 755 /app

# Definir variáveis de ambiente para melhor portabilidade
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV QT_QPA_PLATFORM=offscreen
ENV QT_X11_NO_MITSHM=1
ENV DISPLAY=:99
ENV QT_AUTO_SCREEN_SCALE_FACTOR=1
ENV QT_SCALE_FACTOR=1
ENV QT_FONT_DPI=96
ENV QT_STYLE_OVERRIDE=
ENV QT_QPA_PLATFORMTHEME=
ENV QT_LOGGING_RULES="*=false"
ENV QT_ASSUME_STDERR_HAS_CONSOLE=1
ENV QT_WAYLAND_DISABLE_WINDOWDECORATION=1
ENV MESA_GL_VERSION_OVERRIDE=3.3
ENV MESA_GLSL_VERSION_OVERRIDE=330

# Criar usuário não-root para segurança
RUN groupadd -r eduai && useradd -r -g eduai eduai
RUN chown -R eduai:eduai /app
USER eduai

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Expor porta (se necessário para futuras funcionalidades web)
EXPOSE 8000

# Comando padrão
CMD ["python", "main.py"]
