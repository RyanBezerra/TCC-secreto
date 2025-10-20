# EduAI - Dockerfile
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY . .

# Criar diretórios necessários
RUN mkdir -p logs cache

# Definir variáveis de ambiente
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Expor porta (se necessário para futuras funcionalidades web)
EXPOSE 8000

# Comando padrão
CMD ["python", "main.py"]
