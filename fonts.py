"""
PDV - Ponto de Venda
Gerenciamento de Fontes Personalizadas (Plus Jakarta Sans & Inter)
"""

import os
import sys
import ctypes
import customtkinter as ctk

_fonts_loaded = False
FAMILY_TITLE = "Segoe UI"
FAMILY_BODY = "Segoe UI"


def init_fonts():
    """Carrega as fontes TTF em tempo de execução no Windows."""
    global _fonts_loaded, FAMILY_TITLE, FAMILY_BODY
    if _fonts_loaded:
        return

    # Determina o diretório base (compatível com PyInstaller _MEIPASS)
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    fonts_dir = os.path.join(base_dir, "assets", "fonts")
    if sys.platform == "win32" and os.path.isdir(fonts_dir):
        for filename in os.listdir(fonts_dir):
            if filename.lower().endswith((".ttf", ".otf")):
                font_path = os.path.join(fonts_dir, filename)
                try:
                    # 0x10 = FR_PRIVATE (disponível apenas para este processo)
                    res = ctypes.windll.gdi32.AddFontResourceExW(font_path, 0x10, 0)
                    if res > 0:
                        pass
                except Exception as e:
                    print(f"[Fonts] Erro ao carregar {filename}: {e}")

    FAMILY_TITLE = "Plus Jakarta Sans"
    FAMILY_BODY = "Inter"
    _fonts_loaded = True


def get_font(style: str) -> ctk.CTkFont:
    """
    Retorna a fonte padronizada de acordo com a escala tipográfica do PDV:
    - screen_title: Plus Jakarta Sans, 800, 32px
    - total: Plus Jakarta Sans, 800, 40px (números tabulares)
    - card_price: Plus Jakarta Sans, 800, 22px
    - subtitle: Plus Jakarta Sans, 700, 20px
    - body: Inter, 500, 16px
    - body_bold: Inter, 600, 16px
    - button: Inter, 600, 16px
    - button_primary: Inter, 700, 17px
    - caption: Inter, 400, 13px
    - small: Inter, 400, 11px
    - sidebar_title: Plus Jakarta Sans, 800, 22px
    - sidebar_item: Inter, 600, 14px
    """
    init_fonts()

    styles = {
        "screen_title": (FAMILY_TITLE, 32, "bold"),
        "total": (FAMILY_TITLE, 40, "bold"),
        "card_price": (FAMILY_TITLE, 22, "bold"),
        "subtitle": (FAMILY_TITLE, 20, "bold"),
        "body": (FAMILY_BODY, 16),
        "body_bold": (FAMILY_BODY, 16, "bold"),
        "button": (FAMILY_BODY, 16, "bold"),
        "button_primary": (FAMILY_BODY, 17, "bold"),
        "caption": (FAMILY_BODY, 13),
        "small": (FAMILY_BODY, 11),
        "sidebar_title": (FAMILY_TITLE, 22, "bold"),
        "sidebar_item": (FAMILY_BODY, 14, "bold"),
    }

    family, size, *extra = styles.get(style, (FAMILY_BODY, 14))
    weight = extra[0] if extra else "normal"
    return ctk.CTkFont(family=family, size=size, weight=weight)
