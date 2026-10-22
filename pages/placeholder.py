"""
PDV - Ponto de Venda
Página genérica em branco
"""

import customtkinter as ctk
from config import COLORS


class PlaceholderPage(ctk.CTkFrame):
    def __init__(self, parent, title="", **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg_primary"],
            corner_radius=0,
            **kwargs
        )
        self.title_text = title
