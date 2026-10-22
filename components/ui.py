"""
PDV - Ponto de Venda
Componentes de UI Padronizados (Design System)
"""

import customtkinter as ctk
from config import COLORS, MEASUREMENTS
from fonts import get_font


class StandardCard(ctk.CTkFrame):
    """Card padrão: fundo branco, borda #DDE3EC, raio 12px."""

    def __init__(self, parent, **kwargs):
        kwargs.setdefault("fg_color", COLORS["card_bg"])
        kwargs.setdefault("border_color", COLORS["border"])
        kwargs.setdefault("border_width", MEASUREMENTS["card_border_width"])
        kwargs.setdefault("corner_radius", MEASUREMENTS["card_radius"])
        super().__init__(parent, **kwargs)


class SelectedCard(ctk.CTkFrame):
    """Card selecionado: fundo #EAF0FF, borda de 2px em #1D4ED8, raio 12px."""

    def __init__(self, parent, **kwargs):
        kwargs.setdefault("fg_color", COLORS["selected_bg"])
        kwargs.setdefault("border_color", COLORS["primary"])
        kwargs.setdefault("border_width", MEASUREMENTS["selected_border_width"])
        kwargs.setdefault("corner_radius", MEASUREMENTS["card_radius"])
        super().__init__(parent, **kwargs)


class AttentionCard(ctk.CTkFrame):
    """Card de atenção: fundo #FFF4DC, borda #F3D391, raio 12px."""

    def __init__(self, parent, **kwargs):
        kwargs.setdefault("fg_color", COLORS["status_warning_bg"])
        kwargs.setdefault("border_color", COLORS["status_warning_border"])
        kwargs.setdefault("border_width", MEASUREMENTS["card_border_width"])
        kwargs.setdefault("corner_radius", MEASUREMENTS["card_radius"])
        super().__init__(parent, **kwargs)


class TotalCard(ctk.CTkFrame):
    """Card de total: fundo #0B1B33, texto branco, raio 12px."""

    def __init__(self, parent, **kwargs):
        kwargs.setdefault("fg_color", COLORS["sidebar_bg"])
        kwargs.setdefault("corner_radius", MEASUREMENTS["card_radius"])
        super().__init__(parent, **kwargs)


class PrimaryButton(ctk.CTkButton):
    """
    Botão primário:
    Fundo #1D4ED8, hover #1E40AF, texto branco.
    Altura 48px padrão (ou 60px para finalizar venda), raio 12px.
    """

    def __init__(self, parent, is_finish: bool = False, **kwargs):
        height = MEASUREMENTS["button_finish_height"] if is_finish else MEASUREMENTS["button_height"]
        font_key = "button_primary" if is_finish else "button"

        kwargs.setdefault("fg_color", COLORS["primary"])
        kwargs.setdefault("hover_color", COLORS["primary_hover"])
        kwargs.setdefault("text_color", "#FFFFFF")
        kwargs.setdefault("height", height)
        kwargs.setdefault("corner_radius", MEASUREMENTS["button_radius"])
        kwargs.setdefault("font", get_font(font_key))
        super().__init__(parent, **kwargs)


class SecondaryButton(ctk.CTkButton):
    """
    Botão secundário:
    Fundo branco com borda #1D4ED8 (2px), hover #EAF0FF, texto #1D4ED8.
    Altura 48px, raio 12px.
    """

    def __init__(self, parent, **kwargs):
        kwargs.setdefault("fg_color", COLORS["card_bg"])
        kwargs.setdefault("hover_color", COLORS["selected_bg"])
        kwargs.setdefault("border_color", COLORS["primary"])
        kwargs.setdefault("border_width", MEASUREMENTS["selected_border_width"])
        kwargs.setdefault("text_color", COLORS["primary"])
        kwargs.setdefault("height", MEASUREMENTS["button_height"])
        kwargs.setdefault("corner_radius", MEASUREMENTS["button_radius"])
        kwargs.setdefault("font", get_font("button"))
        super().__init__(parent, **kwargs)


class CancelButton(ctk.CTkButton):
    """
    Botão de cancelar:
    Fundo #C62828, hover #9B1C1C, texto branco.
    Altura 48px, raio 12px.
    """

    def __init__(self, parent, **kwargs):
        kwargs.setdefault("fg_color", COLORS["status_danger"])
        kwargs.setdefault("hover_color", COLORS["status_danger_text"])
        kwargs.setdefault("text_color", "#FFFFFF")
        kwargs.setdefault("height", MEASUREMENTS["button_height"])
        kwargs.setdefault("corner_radius", MEASUREMENTS["button_radius"])
        kwargs.setdefault("font", get_font("button"))
        super().__init__(parent, **kwargs)


class StatusPill(ctk.CTkFrame):
    """
    Etiqueta de status: formato de pílula, com fundo e texto dos tons de status.
    Tipos suportados: 'success' (Pago), 'danger' (Cancelado), 'warning' (Pendente/Estoque baixo), 'info'
    """

    CONFIGS = {
        "success": {
            "bg": COLORS["status_success_bg"],
            "fg": COLORS["status_success_text"],
            "border": None,
        },
        "danger": {
            "bg": COLORS["status_danger_bg"],
            "fg": COLORS["status_danger_text"],
            "border": None,
        },
        "warning": {
            "bg": COLORS["status_warning_bg"],
            "fg": COLORS["status_warning_text"],
            "border": COLORS["status_warning_border"],
        },
        "info": {
            "bg": COLORS["status_info_bg"],
            "fg": COLORS["status_info_text"],
            "border": None,
        },
    }

    def __init__(self, parent, text: str, status: str = "success", icon: str = "", **kwargs):
        cfg = self.CONFIGS.get(status, self.CONFIGS["info"])

        kwargs.setdefault("fg_color", cfg["bg"])
        kwargs.setdefault("corner_radius", MEASUREMENTS["pill_radius"])
        if cfg.get("border"):
            kwargs.setdefault("border_width", 1)
            kwargs.setdefault("border_color", cfg["border"])
        else:
            kwargs.setdefault("border_width", 0)

        super().__init__(parent, **kwargs)

        full_text = f"{icon}  {text}".strip() if icon else text
        self.label = ctk.CTkLabel(
            self,
            text=full_text,
            font=get_font("caption"),
            text_color=cfg["fg"],
        )
        self.label.pack(padx=12, pady=4)
