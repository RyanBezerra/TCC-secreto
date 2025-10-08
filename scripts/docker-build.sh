#!/bin/bash

# EduAI - Script de Build e Execução Docker
# Este script facilita a construção e execução do container EduAI

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_message() {
    echo -e "${BLUE}[EduAI]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Função para verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker não está instalado. Por favor, instale o Docker primeiro."
        exit 1
    fi
    
    if ! command -v docker-compose -f ../docker/docker-compose.yml &> /dev/null; then
        print_error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
        exit 1
    fi
    
    print_success "Docker e Docker Compose estão instalados"
}

# Função para construir a imagem
build_image() {
    print_message "Construindo imagem Docker..."
    
    # Remover imagens antigas se existirem
    if docker images | grep -q "tcc-secreto_eduai"; then
        print_warning "Removendo imagem antiga..."
        docker rmi tcc-secreto_eduai 2>/dev/null || true
    fi
    
    # Construir nova imagem
    docker-compose -f ../docker/docker-compose.yml build --no-cache
    
    print_success "Imagem construída com sucesso!"
}

# Função para executar o container
run_container() {
    print_message "Iniciando containers..."
    
    # Parar containers existentes
    docker-compose -f ../docker/docker-compose.yml down 2>/dev/null || true
    
    # Iniciar containers
    docker-compose -f ../docker/docker-compose.yml up -d
    
    print_success "Containers iniciados com sucesso!"
    
    # Mostrar status
    print_message "Status dos containers:"
    docker-compose -f ../docker/docker-compose.yml ps
    
    # Mostrar logs
    print_message "Logs da aplicação (últimas 20 linhas):"
    docker-compose -f ../docker/docker-compose.yml logs --tail=20 eduai
}

# Função para parar containers
stop_containers() {
    print_message "Parando containers..."
    docker-compose -f ../docker/docker-compose.yml down
    print_success "Containers parados!"
}

# Função para mostrar logs
show_logs() {
    print_message "Mostrando logs da aplicação..."
    docker-compose -f ../docker/docker-compose.yml logs -f eduai
}

# Função para acessar o container
access_container() {
    print_message "Acessando container da aplicação..."
    docker-compose -f ../docker/docker-compose.yml exec eduai /bin/bash
}

# Função para limpar tudo
clean_all() {
    print_warning "Isso irá remover todos os containers, volumes e imagens do EduAI."
    read -p "Tem certeza? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_message "Limpando tudo..."
        docker-compose -f ../docker/docker-compose.yml down -v --rmi all
        docker system prune -f
        print_success "Limpeza concluída!"
    else
        print_message "Operação cancelada."
    fi
}

# Função para mostrar ajuda
show_help() {
    echo "EduAI - Script de Build e Execução Docker"
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  build     - Construir a imagem Docker"
    echo "  run       - Executar os containers"
    echo "  stop      - Parar os containers"
    echo "  restart   - Reiniciar os containers"
    echo "  logs      - Mostrar logs da aplicação"
    echo "  shell     - Acessar o container da aplicação"
    echo "  clean     - Limpar todos os containers e imagens"
    echo "  status    - Mostrar status dos containers"
    echo "  help      - Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 build && $0 run    # Construir e executar"
    echo "  $0 logs               # Ver logs em tempo real"
    echo "  $0 shell              # Acessar o container"
}

# Função para mostrar status
show_status() {
    print_message "Status dos containers:"
    docker-compose -f ../docker/docker-compose.yml ps
    
    print_message "Uso de recursos:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
}

# Função para reiniciar
restart_containers() {
    print_message "Reiniciando containers..."
    docker-compose -f ../docker/docker-compose.yml restart
    print_success "Containers reiniciados!"
}

# Main
main() {
    case "${1:-help}" in
        "build")
            check_docker
            build_image
            ;;
        "run")
            check_docker
            run_container
            ;;
        "stop")
            stop_containers
            ;;
        "restart")
            restart_containers
            ;;
        "logs")
            show_logs
            ;;
        "shell")
            access_container
            ;;
        "clean")
            clean_all
            ;;
        "status")
            show_status
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Executar função principal
main "$@"
