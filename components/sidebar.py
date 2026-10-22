"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação (Menu Lateral Escuro #0B1B33)
"""

import customtkinter as ctk
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """Barra lateral de navegação estilizada conforme o Design System."""

    NAV_ITEMS = [
        {"id": "home",     "icon": "🏠", "label": "Início"},
        {"id": "caixa",    "icon": "🛒", "label": "Caixa"},
        {"id": "produtos", "icon": "📦", "label": "Produtos"},
        {"id": "vendas",   "icon": "📊", "label": "Vendas"},
        {"id": "clientes", "icon": "👤", "label": "Clientes"},
        {"id": "relatorio","icon": "📋", "label": "Relatórios"},
        {"id": "config",   "icon": "⚙️", "label": "Configurações"},
    ]

    def __init__(self, parent, navigate_callback, **kwargs):
        super().__init__(
            parent,
            width=230,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
            **kwargs
        )
        self.navigate_callback = navigate_callback
        self.active_page = "home"
        self._buttons = {}
        self._build()

    def _build(self):
        self.grid_propagate(False)
        self.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)

        # Logo / Título
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(24, 12))

        ctk.CTkLabel(
            logo_frame,
            text="🖥️  PDV Caixa",
            font=get_font("sidebar_title"),
            text_color="#FFFFFF",
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_frame,
            text="Sistema de Ponto de Venda",
            font=get_font("small"),
            text_color=COLORS["sidebar_text"],
        ).pack(anchor="w", pady=(2, 0))

        # Separador elegante
        sep = ctk.CTkFrame(self, height=1, fg_color="#1D2E47", corner_radius=0)
        sep.grid(row=1, column=0, sticky="ew", padx=16, pady=(10, 16))

        # Itens de navegação
        for i, item in enumerate(self.NAV_ITEMS):
            btn = self._make_nav_button(item)
            btn.grid(row=i + 2, column=0, sticky="ew", padx=12, pady=3)
            self._buttons[item["id"]] = btn

        # Versão no rodapé
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=100, column=0, sticky="s", pady=16)

        ctk.CTkLabel(
            footer_frame,
            text=f"PDV v{APP_VERSION}",
            font=get_font("small"),
            text_color="#627594",
        ).pack()

        self.set_active("home")

    def _make_nav_button(self, item):
        btn = ctk.CTkButton(
            self,
            text=f"  {item['icon']}  {item['label']}",
            font=get_font("sidebar_item"),
            anchor="w",
            height=44,
            corner_radius=10,
            fg_color="transparent",
            hover_color=COLORS["sidebar_active"],
            text_color=COLORS["sidebar_text"],
            command=lambda p=item["id"]: self._on_click(p),
        )
        return btn

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        for pid, btn in self._buttons.items():
            if pid == page_id:
                btn.configure(
                    fg_color=COLORS["primary"],
                    text_color="#FFFFFF",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["sidebar_text"],
                )
