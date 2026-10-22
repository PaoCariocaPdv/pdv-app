"""
PDV - Ponto de Venda
Página: Placeholder (Padronizada)
"""

import customtkinter as ctk
from config import COLORS
from fonts import get_font
from components.ui import StandardCard, SecondaryButton, StatusPill


class PlaceholderPage(ctk.CTkFrame):
    """Página genérica para seções em desenvolvimento seguindo o Design System."""

    def __init__(self, parent, title="", **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg_screen"],
            corner_radius=0,
            **kwargs
        )
        self.title = title
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        card = StandardCard(self, width=540, height=360)
        card.grid(row=1, column=0)
        card.pack_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(expand=True, fill="both", padx=32, pady=32)

        StatusPill(inner, text="Módulo em Desenvolvimento", status="info", icon="🚧").pack(anchor="center", pady=(0, 16))

        ctk.CTkLabel(
            inner,
            text=self.title,
            font=get_font("screen_title"),
            text_color=COLORS["text_primary"],
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            inner,
            text="Esta funcionalidade está sendo implementada.",
            font=get_font("body"),
            text_color=COLORS["text_secondary"],
        ).pack(pady=(0, 24))

        SecondaryButton(
            inner,
            text="← Voltar ao Início",
            command=self._go_home,
        ).pack(anchor="center")

    def _go_home(self):
        root = self.winfo_toplevel()
        if hasattr(root, "navigate"):
            root.navigate("home")
