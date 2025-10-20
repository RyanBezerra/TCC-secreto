# EduAI - Script de Build Otimizado para Docker (PowerShell)
# Este script otimiza o build do Docker para melhor portabilidade

param(
    [switch]$Clean,
    [switch]$Test,
    [switch]$Help
)

if ($Help) {
    Write-Host "Uso: .\docker-build-optimized.ps1 [-Clean] [-Test] [-Help]" -ForegroundColor Green
    Write-Host ""
    Write-Host "Opções:" -ForegroundColor Yellow
    Write-Host "  -Clean    Limpa imagens antigas antes do build" -ForegroundColor White
    Write-Host "  -Test     Executa testes de portabilidade após o build" -ForegroundColor White
    Write-Host "  -Help     Mostra esta ajuda" -ForegroundColor White
    exit 0
}

# Configurar para parar em caso de erro
$ErrorActionPreference = "Stop"

Write-Host "🚀 Iniciando build otimizado do EduAI Docker..." -ForegroundColor Blue

# Função para log colorido
function Write-Log {
    param([string]$Message, [string]$Color = "Blue")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor $Color
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERRO] $Message" -ForegroundColor Red
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCESSO] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[AVISO] $Message" -ForegroundColor Yellow
}

try {
    # Verificar se Docker está rodando
    Write-Log "Verificando se Docker está rodando..."
    docker info | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Docker não está rodando. Inicie o Docker Desktop e tente novamente."
        exit 1
    }
    Write-Success "Docker está rodando"

    # Verificar se docker-compose está disponível
    Write-Log "Verificando docker-compose..."
    $composeVersion = docker-compose --version
    if ($LASTEXITCODE -ne 0) {
        Write-Error "docker-compose não encontrado. Instale o docker-compose e tente novamente."
        exit 1
    }
    Write-Success "docker-compose encontrado: $composeVersion"

    # Navegar para o diretório do projeto
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $projectDir = Split-Path -Parent $scriptDir
    Set-Location $projectDir
    Write-Log "Diretório de trabalho: $(Get-Location)"

    # Parar containers existentes
    Write-Log "Parando containers existentes..."
    docker-compose -f docker/docker-compose.yml down --remove-orphans
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Alguns containers podem não ter sido parados corretamente"
    }

    # Limpar imagens antigas se solicitado
    if ($Clean) {
        Write-Log "Limpando imagens antigas..."
        docker system prune -f
        docker image prune -f
        Write-Success "Limpeza concluída"
    }

    # Build com cache otimizado
    Write-Log "Iniciando build com cache otimizado..."

    # Build da imagem principal
    Write-Log "Construindo imagem principal..."
    docker-compose -f docker/docker-compose.yml build --no-cache --parallel

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Build concluído com sucesso!"
    } else {
        Write-Error "Falha no build. Verifique os logs acima."
        exit 1
    }

    # Testar a imagem se solicitado
    if ($Test) {
        Write-Log "Testando a imagem construída..."

        # Executar teste de portabilidade
        Write-Log "Executando testes de portabilidade..."
        docker-compose -f docker/docker-compose.yml run --rm eduai python scripts/test-portability.py

        if ($LASTEXITCODE -eq 0) {
            Write-Success "Testes de portabilidade passaram!"
        } else {
            Write-Warning "Alguns testes de portabilidade falharam. Verifique os logs."
        }
    }

    # Mostrar informações da imagem
    Write-Log "Informações da imagem construída:"
    docker images | Select-String "eduai"

    # Mostrar tamanho da imagem
    $imageInfo = docker images --format "table {{.Size}}" | Select-String "eduai"
    if ($imageInfo) {
        Write-Log "Tamanho da imagem: $($imageInfo.Line.Trim())"
    }

    # Sugestões de otimização
    Write-Log "Sugestões para melhorar a portabilidade:"
    Write-Host "1. Certifique-se de que todas as máquinas tenham a mesma versão do Docker" -ForegroundColor White
    Write-Host "2. Use as mesmas variáveis de ambiente em todas as máquinas" -ForegroundColor White
    Write-Host "3. Verifique se as fontes estão disponíveis no sistema host" -ForegroundColor White
    Write-Host "4. Teste em diferentes sistemas operacionais" -ForegroundColor White

    Write-Success "Build otimizado concluído!"
    Write-Log "Para executar a aplicação: docker-compose -f docker/docker-compose.yml up"
    Write-Log "Para executar em modo desenvolvimento: docker-compose -f docker/docker-compose.yml up --build"

} catch {
    Write-Error "Erro inesperado: $($_.Exception.Message)"
    exit 1
}
