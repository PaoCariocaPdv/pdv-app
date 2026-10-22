# ============================================================
#  PDV — Script de Build e Publicação Automática
#  Uso: .\build.ps1 -Version "1.1.0"
# ============================================================
param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)

$PYTHON    = "C:\Users\escri\AppData\Local\Programs\Python\Python311\python.exe"
$REPO      = "PaoCariocaPdv/pdv-app"
$EXE_PATH  = "dist\PDV.exe"
$SPEC_FILE = "pdv.spec"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PDV Build & Release — v$Version" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Atualiza versão no config.py ──────────────────────────
Write-Host "[1/5] Atualizando versão para v$Version..." -ForegroundColor Yellow
$configPath = "config.py"
(Get-Content $configPath) -replace 'APP_VERSION = ".*?"', "APP_VERSION = `"$Version`"" |
    Set-Content $configPath
Write-Host "      config.py atualizado." -ForegroundColor Green

# ── 2. Limpa builds anteriores ───────────────────────────────
Write-Host "[2/5] Limpando builds anteriores..." -ForegroundColor Yellow
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
Write-Host "      Limpo." -ForegroundColor Green

# ── 3. Gera o .exe com PyInstaller ───────────────────────────
Write-Host "[3/5] Gerando PDV.exe com PyInstaller..." -ForegroundColor Yellow
& $PYTHON -m PyInstaller $SPEC_FILE
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: PyInstaller falhou!" -ForegroundColor Red
    exit 1
}
Write-Host "      PDV.exe gerado em dist\" -ForegroundColor Green

# ── 4. Cria tag no Git e faz commit ──────────────────────────
Write-Host "[4/5] Publicando tag v$Version no GitHub..." -ForegroundColor Yellow
git add -A
git commit -m "Release v$Version"
git tag "v$Version"
git push origin main --tags
if ($LASTEXITCODE -ne 0) {
    Write-Host "AVISO: git push falhou. Verifique sua conexão ou credenciais." -ForegroundColor Red
}
Write-Host "      Tag v$Version publicada." -ForegroundColor Green

# ── 5. Cria Release no GitHub com o .exe ─────────────────────
Write-Host "[5/5] Criando Release no GitHub e enviando PDV.exe..." -ForegroundColor Yellow

# Verifica se gh (GitHub CLI) está instalado
if (Get-Command gh -ErrorAction SilentlyContinue) {
    gh release create "v$Version" $EXE_PATH `
        --repo $REPO `
        --title "PDV v$Version" `
        --notes "Versão $Version do PDV - Ponto de Venda"
    Write-Host "      Release criada no GitHub!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "  AVISO: GitHub CLI (gh) não está instalado." -ForegroundColor Red
    Write-Host "  Instale em: https://cli.github.com" -ForegroundColor Yellow
    Write-Host "  Depois rode: gh release create v$Version dist\PDV.exe --title 'PDV v$Version'" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Build concluído! v$Version pronta." -ForegroundColor Green
Write-Host "  Arquivo: $EXE_PATH" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
