"""
PDV - Ponto de Venda
Página: Caixa / PDV
"""

import customtkinter as ctk
from config import COLORS


class CaixaPage(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg_screen"],
            corner_radius=0,
            **kwargs
        )
