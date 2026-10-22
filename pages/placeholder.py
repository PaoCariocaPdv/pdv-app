"""
PDV - Ponto de Venda
Página placeholder (em construção)
"""

import customtkinter as ctk
from config import COLORS


class PlaceholderPage(ctk.CTkFrame):
    """Página genérica para seções ainda não implementadas."""

    def __init__(self, parent, title="", **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg_primary"],
            corner_radius=0,
            **kwargs
        )
        self.title = title
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center = ctk.CTkFrame(self, fg_color="transparent")
        center.grid(row=1, column=0)

        ctk.CTkLabel(
            center,
            text="🚧",
            font=ctk.CTkFont(size=56),
        ).pack(pady=(0, 12))

        ctk.CTkLabel(
            center,
            text=self.title,
            font=ctk.CTkFont("Inter", 26, "bold"),
            text_color=COLORS["text_primary"],
        ).pack()

        ctk.CTkLabel(
            center,
            text="Esta seção está em desenvolvimento.",
            font=ctk.CTkFont("Inter", 14),
            text_color=COLORS["text_secondary"],
        ).pack(pady=(8, 0))
