# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Coleta arquivos de dados do CustomTkinter (temas, imagens, fontes)
ctk_datas = collect_data_files("customtkinter")
app_datas = ctk_datas + [("icon.ico", ".")]

a = Analysis(
    ["main.py"],
    pathex=["."],
    binaries=[],
    datas=app_datas,
    hiddenimports=collect_submodules("customtkinter"),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="PDV",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # Sem janela de terminal
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icon.ico",        # Ícone do aplicativo
)
