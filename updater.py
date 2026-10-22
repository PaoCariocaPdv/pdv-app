"""
PDV - Ponto de Venda
Módulo de atualização automática via GitHub Releases
"""

import os
import sys
import json
import threading
import subprocess
import tempfile
import urllib.request
import urllib.error
from config import APP_VERSION, GITHUB_USER, GITHUB_REPO


def _get_latest_release() -> dict | None:
    """Consulta a API do GitHub para obter a última release."""
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PDV-Updater"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def _version_tuple(v: str):
    """Converte '1.2.3' em (1, 2, 3) para comparação."""
    return tuple(int(x) for x in v.lstrip("v").split("."))


def check_for_update() -> dict | None:
    """
    Verifica se há uma versão mais nova disponível.
    Retorna dict com {'version', 'download_url'} ou None se não houver update.
    """
    release = _get_latest_release()
    if not release:
        return None

    latest_version = release.get("tag_name", "").lstrip("v")
    if not latest_version:
        return None

    try:
        if _version_tuple(latest_version) > _version_tuple(APP_VERSION):
            # Procura especificamente PDV.exe nos assets da release
            for asset in release.get("assets", []):
                if asset["name"].lower() == "pdv.exe":
                    return {
                        "version": latest_version,
                        "download_url": asset["browser_download_url"],
                        "notes": release.get("body", ""),
                    }
            for asset in release.get("assets", []):
                if asset["name"].lower().endswith(".exe") and not asset["name"].lower().startswith("pdv_setup"):
                    return {
                        "version": latest_version,
                        "download_url": asset["browser_download_url"],
                        "notes": release.get("body", ""),
                    }
    except Exception:
        pass

    return None


def download_and_install(download_url: str, on_progress=None):
    """
    Baixa o novo .exe e executa o instalador.
    Cria um script .bat temporário que substitui o executável atual após fechar.
    """
    try:
        tmp_dir = tempfile.mkdtemp()
        new_exe_path = os.path.join(tmp_dir, "PDV_new.exe")

        # Download com progresso
        def _reporthook(count, block_size, total_size):
            if on_progress and total_size > 0:
                percent = min(int(count * block_size * 100 / total_size), 100)
                on_progress(percent)

        urllib.request.urlretrieve(download_url, new_exe_path, _reporthook)

        # Script bat que substitui o exe atual depois que o app fechar
        current_exe = sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)
        bat_path = os.path.join(tmp_dir, "update.bat")

        bat_content = f"""@echo off
timeout /t 2 /nobreak >nul
taskkill /f /im PDV.exe >nul 2>&1
timeout /t 2 /nobreak >nul
set RETRIES=0
:wait_loop
copy /y "{new_exe_path}" "{current_exe}" >nul 2>&1
if errorlevel 1 (
    set /a RETRIES+=1
    timeout /t 1 /nobreak >nul
    if %RETRIES% lss 10 goto wait_loop
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process cmd -ArgumentList '/c timeout /t 2 /nobreak >nul & taskkill /f /im PDV.exe >nul 2>&1 & timeout /t 2 /nobreak >nul & copy /y \"\"{new_exe_path}\"\" \"\"{current_exe}\"\" & timeout /t 1 /nobreak >nul & start \"\" \"\"{current_exe}\"\"' -Verb RunAs"
    del "%~f0"
    exit /b
)
timeout /t 1 /nobreak >nul
start "" "{current_exe}"
del "%~f0"
"""
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(bat_content)

        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(
            ["cmd.exe", "/c", bat_path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
            creationflags=subprocess.CREATE_NO_WINDOW | DETACHED_PROCESS,
        )
        os._exit(0)

    except Exception as e:
        raise RuntimeError(f"Falha no download: {e}")


def check_update_async(callback):
    """
    Verifica atualização em background (não trava a UI).
    Chama callback(update_info) se houver update, ou callback(None) se não houver.
    """
    def _run():
        update = check_for_update()
        callback(update)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
