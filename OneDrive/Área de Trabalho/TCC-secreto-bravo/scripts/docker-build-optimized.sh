#!/bin/bash

# EduAI - Script de Build Otimizado para Docker
# Este script otimiza o build do Docker para melhor portabilidade

set -e  # Parar em caso de erro

echo "🚀 Iniciando build otimizado do EduAI Docker..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCESSO]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    error "Docker não está rodando. Inicie o Docker e tente novamente."
    exit 1
fi

# Verificar se docker-compose está disponível
if ! command -v docker-compose &> /dev/null; then
    error "docker-compose não encontrado. Instale o docker-compose e tente novamente."
    exit 1
fi

# Navegar para o diretório do projeto
cd "$(dirname "$0")/.."

log "Diretório de trabalho: $(pwd)"

# Parar containers existentes
log "Parando containers existentes..."
docker-compose -f docker/docker-compose.yml down --remove-orphans || true

# Limpar imagens antigas (opcional)
read -p "Deseja limpar imagens antigas? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log "Limpando imagens antigas..."
    docker system prune -f
    docker image prune -f
fi

# Build com cache otimizado
log "Iniciando build com cache otimizado..."

# Build da imagem principal
log "Construindo imagem principal..."
docker-compose -f docker/docker-compose.yml build --no-cache --parallel

# Verificar se o build foi bem-sucedido
if [ $? -eq 0 ]; then
    success "Build concluído com sucesso!"
else
    error "Falha no build. Verifique os logs acima."
    exit 1
fi

# Testar a imagem
log "Testando a imagem construída..."

# Executar teste de portabilidade
log "Executando testes de portabilidade..."
docker-compose -f docker/docker-compose.yml run --rm eduai python scripts/test-portability.py

if [ $? -eq 0 ]; then
    success "Testes de portabilidade passaram!"
else
    warning "Alguns testes de portabilidade falharam. Verifique os logs."
fi

# Mostrar informações da imagem
log "Informações da imagem construída:"
docker images | grep eduai

# Mostrar tamanho da imagem
IMAGE_SIZE=$(docker images --format "table {{.Size}}" eduai-app | tail -n 1)
log "Tamanho da imagem: $IMAGE_SIZE"

# Sugestões de otimização
log "Sugestões para melhorar a portabilidade:"
echo "1. Certifique-se de que todas as máquinas tenham a mesma versão do Docker"
echo "2. Use as mesmas variáveis de ambiente em todas as máquinas"
echo "3. Verifique se as fontes estão disponíveis no sistema host"
echo "4. Teste em diferentes sistemas operacionais"

success "Build otimizado concluído!"
log "Para executar a aplicação: docker-compose -f docker/docker-compose.yml up"
log "Para executar em modo desenvolvimento: docker-compose -f docker/docker-compose.yml up --build"
