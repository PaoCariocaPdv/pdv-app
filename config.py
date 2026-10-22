"""
PDV - Ponto de Venda
Configurações globais do aplicativo
"""

# Informações do App
APP_NAME = "PDV - Caixa"
APP_VERSION = "1.0.6"

# GitHub — usado pelo auto-updater
GITHUB_USER = "PaoCariocaPdv"
GITHUB_REPO = "pdv-app"
APP_WIDTH = 1280
APP_HEIGHT = 800
APP_MIN_WIDTH = 1024
APP_MIN_HEIGHT = 600

# Cores do tema
COLORS = {
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F5F5F5",
    "bg_sidebar": "#1E1E2E",
    "sidebar_text": "#FFFFFF",
    "sidebar_text_hover": "#A0A0B0",
    "sidebar_active": "#2D2D44",
    "accent": "#4F46E5",
    "accent_hover": "#4338CA",
    "text_primary": "#1A1A2E",
    "text_secondary": "#6B7280",
    "border": "#E5E7EB",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
}

# Fontes
FONTS = {
    "title": ("Inter", 24, "bold"),
    "subtitle": ("Inter", 16, "bold"),
    "body": ("Inter", 13),
    "small": ("Inter", 11),
    "button": ("Inter", 13, "bold"),
}

# Firebase - Configure suas credenciais aqui
FIREBASE_CONFIG = {
    "credential_path": "firebase_credentials.json",  # Arquivo de credenciais do Firebase
    "database_url": "",  # URL do seu Firestore (deixe vazio para Firestore padrão)
}
