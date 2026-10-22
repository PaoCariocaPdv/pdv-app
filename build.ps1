# ============================================================
#  PDV — Script de Build e Publicação Automática
#  Uso: .\build.ps1 -Version "1.0.8"
# ============================================================
param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)

$PYTHON    = "python"
$ISCC      = "C:\Users\escri\AppData\Local\Programs\Inno Setup 6\ISCC.exe"
$REPO      = "PaoCariocaPdv/pdv-app"
$EXE_PATH  = "dist\PDV.exe"
$INSTALLER = "installer\PDV_Setup_v$Version.exe"
$SPEC_FILE = "pdv.spec"
$ISS_FILE  = "pdv_installer.iss"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PDV Build & Release — v$Version" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Atualiza versão no config.py e pdv_installer.iss ───────
Write-Host "[1/5] Atualizando versão para v$Version..." -ForegroundColor Yellow
$configPath = "config.py"
(Get-Content $configPath) -replace 'APP_VERSION = ".*?"', "APP_VERSION = `"$Version`"" |
    Set-Content $configPath
Write-Host "      config.py atualizado." -ForegroundColor Green

if (Test-Path $ISS_FILE) {
    (Get-Content $ISS_FILE) -replace '#define AppVersion ".*?"', "#define AppVersion `"$Version`"" |
        Set-Content $ISS_FILE
    Write-Host "      pdv_installer.iss atualizado." -ForegroundColor Green
}

# ── 2. Limpa builds anteriores e fecha processos ─────────────
Write-Host "[2/5] Fechando instâncias antigas e limpando builds..." -ForegroundColor Yellow
Stop-Process -Name "PDV" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
Write-Host "      Limpo." -ForegroundColor Green

# ── 3. Gera o .exe com PyInstaller ───────────────────────────
Write-Host "[3/5] Gerando PDV.exe com PyInstaller..." -ForegroundColor Yellow
& $PYTHON -m PyInstaller $SPEC_FILE --clean
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: PyInstaller falhou!" -ForegroundColor Red
    exit 1
}
Write-Host "      PDV.exe gerado em dist\" -ForegroundColor Green

# ── 4. Cria tag no Git e faz commit ──────────────────────────
Write-Host "[4/5] Publicando tag v$Version no GitHub..." -ForegroundColor Yellow
git add -A
git commit -m "Release v$Version"
git tag -f "v$Version"
git push origin main --tags -f
if ($LASTEXITCODE -ne 0) {
    Write-Host "AVISO: git push falhou. Verifique sua conexão ou credenciais." -ForegroundColor Red
}
Write-Host "      Tag v$Version publicada." -ForegroundColor Green

# ── 5. Cria Release no GitHub e envia PDV.exe ────────────────
Write-Host "[5/5] Criando Release no GitHub e enviando PDV.exe..." -ForegroundColor Yellow

# Gera o instalador se Inno Setup estiver presente
if (Test-Path $ISCC) {
    Write-Host "      Gerando instalador PDV_Setup_v$Version.exe..." -ForegroundColor Yellow
    & $ISCC $ISS_FILE
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      Instalador gerado em installer\" -ForegroundColor Green
    }
}

# Publica a release via script Python
& $PYTHON publish_release.py $Version $EXE_PATH
if ($LASTEXITCODE -eq 0) {
    Write-Host "      Release criada no GitHub com sucesso!" -ForegroundColor Green
} else {
    Write-Host "ERRO ao publicar release no GitHub." -ForegroundColor Red
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Build concluído! v$Version pronta." -ForegroundColor Green
Write-Host "  Arquivo: $EXE_PATH" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
