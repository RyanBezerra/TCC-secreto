# EduAI - Script de Build e Execução Docker (PowerShell)
# Este script facilita a construção e execução do container EduAI

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

# Função para imprimir mensagens coloridas
function Write-Message {
    param([string]$Message)
    Write-Host "[EduAI] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Função para verificar se Docker está instalado
function Test-Docker {
    try {
        $null = Get-Command docker -ErrorAction Stop
        $null = Get-Command docker-compose -f ../docker/docker-compose.yml -ErrorAction Stop
        Write-Success "Docker e Docker Compose estão instalados"
        return $true
    }
    catch {
        Write-Error "Docker ou Docker Compose não estão instalados. Por favor, instale-os primeiro."
        return $false
    }
}

# Função para construir a imagem
function Build-Image {
    Write-Message "Construindo imagem Docker..."
    
    # Remover imagens antigas se existirem
    $existingImages = docker images --format "{{.Repository}}:{{.Tag}}" | Where-Object { $_ -like "*tcc-secreto*" }
    if ($existingImages) {
        Write-Warning "Removendo imagens antigas..."
        $existingImages | ForEach-Object { docker rmi $_ 2>$null }
    }
    
    # Construir nova imagem
    docker-compose -f ../docker/docker-compose.yml -f ../docker/docker-compose -f ../docker/docker-compose.yml.yml build --no-cache
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Imagem construída com sucesso!"
    } else {
        Write-Error "Falha ao construir a imagem"
        exit 1
    }
}

# Função para executar o container
function Start-Containers {
    Write-Message "Iniciando containers..."
    
    # Parar containers existentes
    docker-compose -f ../docker/docker-compose.yml -f ../docker/docker-compose -f ../docker/docker-compose.yml.yml down 2>$null
    
    # Iniciar containers
    docker-compose -f ../docker/docker-compose.yml -f ../docker/docker-compose -f ../docker/docker-compose.yml.yml up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Containers iniciados com sucesso!"
        
        # Mostrar status
        Write-Message "Status dos containers:"
        docker-compose -f ../docker/docker-compose.yml -f ../docker/docker-compose -f ../docker/docker-compose.yml.yml ps
        
        # Mostrar logs
        Write-Message "Logs da aplicação (últimas 20 linhas):"
        docker-compose -f ../docker/docker-compose.yml -f ../docker/docker-compose -f ../docker/docker-compose.yml.yml logs --tail=20 eduai
    } else {
        Write-Error "Falha ao iniciar os containers"
        exit 1
    }
}

# Função para parar containers
function Stop-Containers {
    Write-Message "Parando containers..."
    docker-compose -f ../docker/docker-compose.yml down
    Write-Success "Containers parados!"
}

# Função para mostrar logs
function Show-Logs {
    Write-Message "Mostrando logs da aplicação..."
    docker-compose -f ../docker/docker-compose.yml logs -f eduai
}

# Função para acessar o container
function Enter-Container {
    Write-Message "Acessando container da aplicação..."
    docker-compose -f ../docker/docker-compose.yml exec eduai /bin/bash
}

# Função para limpar tudo
function Clear-All {
    Write-Warning "Isso irá remover todos os containers, volumes e imagens do EduAI."
    $confirmation = Read-Host "Tem certeza? (y/N)"
    if ($confirmation -eq "y" -or $confirmation -eq "Y") {
        Write-Message "Limpando tudo..."
        docker-compose -f ../docker/docker-compose.yml down -v --rmi all
        docker system prune -f
        Write-Success "Limpeza concluída!"
    } else {
        Write-Message "Operação cancelada."
    }
}

# Função para mostrar ajuda
function Show-Help {
    Write-Host "EduAI - Script de Build e Execução Docker" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Uso: .\docker-build.ps1 [COMANDO]"
    Write-Host ""
    Write-Host "Comandos disponíveis:"
    Write-Host "  build     - Construir a imagem Docker"
    Write-Host "  run       - Executar os containers"
    Write-Host "  stop      - Parar os containers"
    Write-Host "  restart   - Reiniciar os containers"
    Write-Host "  logs      - Mostrar logs da aplicação"
    Write-Host "  shell     - Acessar o container da aplicação"
    Write-Host "  clean     - Limpar todos os containers e imagens"
    Write-Host "  status    - Mostrar status dos containers"
    Write-Host "  help      - Mostrar esta ajuda"
    Write-Host ""
    Write-Host "Exemplos:"
    Write-Host "  .\docker-build.ps1 build; .\docker-build.ps1 run    # Construir e executar"
    Write-Host "  .\docker-build.ps1 logs                             # Ver logs em tempo real"
    Write-Host "  .\docker-build.ps1 shell                            # Acessar o container"
}

# Função para mostrar status
function Show-Status {
    Write-Message "Status dos containers:"
    docker-compose -f ../docker/docker-compose.yml ps
    
    Write-Message "Uso de recursos:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
}

# Função para reiniciar
function Restart-Containers {
    Write-Message "Reiniciando containers..."
    docker-compose -f ../docker/docker-compose.yml restart
    Write-Success "Containers reiniciados!"
}

# Main
switch ($Command.ToLower()) {
    "build" {
        if (Test-Docker) {
            Build-Image
        }
    }
    "run" {
        if (Test-Docker) {
            Start-Containers
        }
    }
    "stop" {
        Stop-Containers
    }
    "restart" {
        Restart-Containers
    }
    "logs" {
        Show-Logs
    }
    "shell" {
        Enter-Container
    }
    "clean" {
        Clear-All
    }
    "status" {
        Show-Status
    }
    "help" {
        Show-Help
    }
    default {
        Show-Help
    }
}
