"""
PDV - Ponto de Venda
Configurações globais do aplicativo — Sistema de Cores e Tipografia Padronizados
"""

# Informações do App
APP_NAME = "PDV - Caixa"
APP_VERSION = "1.0.17"

# GitHub — usado pelo auto-updater
GITHUB_USER = "PaoCariocaPdv"
GITHUB_REPO = "pdv-app"

# Dimensões da Janela
APP_WIDTH = 1280
APP_HEIGHT = 800
APP_MIN_WIDTH = 1024
APP_MIN_HEIGHT = 600

# ==============================================================================
# PALETA DE CORES OFICIAL
# ==============================================================================
COLORS = {
    # ── Marca ─────────────────────────────────────────────────────────────
    "primary": "#1D4ED8",               # Primária (botões, preços, seleção)
    "primary_hover": "#1E40AF",         # Primária no hover/pressionado
    "selected_bg": "#EAF0FF",           # Fundo de item selecionado
    "sidebar_bg": "#FFFFFF",            # Menu lateral estilo Caixa Bolo (fundo branco)
    "sidebar_border": "#E2E8F0",        # Borda sutil do menu lateral
    "sidebar_text": "#64748B",          # Texto/ícones do menu lateral
    "sidebar_hover": "#EFF6FF",         # Hover suave em azul claro
    "sidebar_active": "#1D4ED8",        # Item ativo em azul primário
    "total_bg": "#0B1B33",              # Fundo escuro do card de total
    "highlight": "#D97706",             # Destaque (detalhes e promoções)

    # ── Base ──────────────────────────────────────────────────────────────
    "bg_screen": "#F3F5F9",             # Fundo da tela
    "card_bg": "#FFFFFF",               # Cards e painéis
    "border": "#DDE3EC",                # Bordas
    "text_primary": "#0F1A2E",          # Texto principal
    "text_secondary": "#566178",        # Texto secundário

    # ── Status ────────────────────────────────────────────────────────────
    # Sucesso / Pago
    "status_success": "#0E7A4F",
    "status_success_bg": "#E3F6EC",
    "status_success_text": "#0B6140",

    # Erro / Cancelado
    "status_danger": "#C62828",
    "status_danger_bg": "#FDE8E8",
    "status_danger_text": "#9B1C1C",

    # Atenção / Pendente / Estoque baixo
    "status_warning_bg": "#FFF4DC",
    "status_warning_border": "#F3D391",
    "status_warning_text": "#8A4B08",

    # Informação
    "status_info": "#0E7490",
    "status_info_bg": "#E0F2FE",
    "status_info_text": "#0E7490",

    # ── Compatibilidade Retroativa ─────────────────────────────────────────
    "bg_primary": "#F3F5F9",            # Mapeia para o novo fundo da tela
    "bg_secondary": "#FFFFFF",          # Mapeia para fundo de cards
    "bg_sidebar": "#0B1B33",            # Menu lateral
    "sidebar_text_hover": "#FFFFFF",
    "accent": "#1D4ED8",
    "accent_hover": "#1E40AF",
    "success": "#0E7A4F",
    "danger": "#C62828",
    "warning": "#8A4B08",
}

# Medidas Padronizadas
MEASUREMENTS = {
    "card_radius": 12,
    "card_border_width": 1,
    "selected_border_width": 2,
    "button_radius": 12,
    "button_height": 48,
    "button_finish_height": 60,
    "pill_radius": 16,
}

# Firebase - Configurações
FIREBASE_CONFIG = {
    "credential_path": "firebase_credentials.json",
    "database_url": "",
}
