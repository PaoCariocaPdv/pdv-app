"""
PDV - Ponto de Venda
Página: Início (Home)
"""

import customtkinter as ctk
from config import COLORS


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg_primary"],
            corner_radius=0,
            **kwargs
        )
