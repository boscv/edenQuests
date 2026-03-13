# atualizar-edenQuests.ps1
# Atualiza a pasta onde este arquivo está com o conteúdo do repositório:
# https://github.com/billabong93/edenQuests

$ErrorActionPreference = 'Stop'

$repoOwner = 'billabong93'
$repoName  = 'edenQuests'
$branch    = 'main'

# Pasta onde o script está (pasta do plugin)
$targetDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Diretorio de destino:" $targetDir
Write-Host ""

# URL do zip do GitHub
$url     = "https://github.com/$repoOwner/$repoName/archive/refs/heads/$branch.zip"
$zipPath = Join-Path $env:TEMP "$repoName-$branch.zip"
$tmpPath = Join-Path $env:TEMP "$repoName-$branch"

# Limpa temp antigo, se existir
if (Test-Path $zipPath) { Remove-Item $zipPath -Force -ErrorAction SilentlyContinue }
if (Test-Path $tmpPath) { Remove-Item $tmpPath -Recurse -Force -ErrorAction SilentlyContinue }

try {
    Write-Host "Baixando ultima versao de $repoOwner/$repoName@$branch..."
    Invoke-WebRequest -Uri $url -OutFile $zipPath

    Write-Host "Extraindo arquivos temporariamente..."
    Expand-Archive -Path $zipPath -DestinationPath $tmpPath -Force

    $root = Join-Path $tmpPath "$repoName-$branch"
    if (-not (Test-Path $root)) {
        Write-Host "ERRO: pasta raiz '$repoName-$branch' nao encontrada dentro do zip." -ForegroundColor Red
        exit 1
    }

    Write-Host "Copiando arquivos para a pasta do plugin..."
    Copy-Item -Path (Join-Path $root '*') -Destination $targetDir -Recurse -Force

    Write-Host ""
    Write-Host "Limpando arquivos temporarios..."
    Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
    Remove-Item $tmpPath -Recurse -Force -ErrorAction SilentlyContinue

    Write-Host ""
    Write-Host "Concluido! edenQuests atualizado com sucesso." -ForegroundColor Green
    Write-Host ""
    Read-Host "Pressione ENTER para fechar"

    exit 0
}
catch {
    Write-Host ""
    Write-Host "Ocorreu um erro durante a atualizacao:" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Write-Host ""
    Read-Host "Pressione ENTER para fechar"
    exit 1
}
