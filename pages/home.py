"""
PDV - Ponto de Venda
Página: Início (Home)
"""

import customtkinter as ctk
from config import COLORS
from database import is_connected


class HomePage(ctk.CTkFrame):
    """Página inicial do PDV — limpa e minimalista."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg_primary"],
            corner_radius=0,
            **kwargs
        )
        self._build()

    def _build(self):
        # Centraliza o conteúdo verticalmente
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center = ctk.CTkFrame(self, fg_color="transparent")
        center.grid(row=1, column=0)

        # Ícone principal
        ctk.CTkLabel(
            center,
            text="💳",
            font=ctk.CTkFont(size=72),
        ).pack(pady=(0, 16))

        # Título
        ctk.CTkLabel(
            center,
            text="Bem-vindo ao PDV",
            font=ctk.CTkFont("Inter", 32, "bold"),
            text_color=COLORS["text_primary"],
        ).pack()

        # Subtítulo
        ctk.CTkLabel(
            center,
            text="Seu sistema de Ponto de Venda",
            font=ctk.CTkFont("Inter", 16),
            text_color=COLORS["text_secondary"],
        ).pack(pady=(6, 32))

        # Status de conexão
        status_color = COLORS["success"] if is_connected() else COLORS["warning"]
        status_text = "🟢 Conectado ao banco de dados" if is_connected() else "🟡 Modo offline — configure o Firebase para sincronizar"

        ctk.CTkLabel(
            center,
            text=status_text,
            font=ctk.CTkFont("Inter", 12),
            text_color=status_color,
        ).pack(pady=(0, 32))

        # Cards de atalho
        cards_frame = ctk.CTkFrame(center, fg_color="transparent")
        cards_frame.pack()

        shortcuts = [
            {"icon": "🛒", "label": "Abrir Caixa",   "page": "caixa"},
            {"icon": "📦", "label": "Produtos",       "page": "produtos"},
            {"icon": "📊", "label": "Ver Vendas",     "page": "vendas"},
            {"icon": "📋", "label": "Relatórios",     "page": "relatorio"},
        ]

        for i, s in enumerate(shortcuts):
            card = ctk.CTkButton(
                cards_frame,
                text=f"{s['icon']}\n{s['label']}",
                font=ctk.CTkFont("Inter", 13),
                width=130,
                height=100,
                corner_radius=14,
                fg_color=COLORS["bg_secondary"],
                hover_color=COLORS["border"],
                text_color=COLORS["text_primary"],
                command=lambda p=s["page"]: self._navigate(p),
            )
            card.grid(row=0, column=i, padx=10, pady=0)

    def _navigate(self, page_id):
        # Dispara navegação pelo app principal via evento
        self.event_generate("<<Navigate>>", data=page_id)
