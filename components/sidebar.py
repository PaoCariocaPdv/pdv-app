"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação
"""

import customtkinter as ctk
from config import COLORS, FONTS


class Sidebar(ctk.CTkFrame):
    """Barra lateral de navegação do app."""

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
            width=220,
            fg_color=COLORS["bg_sidebar"],
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
        logo_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(24, 10))

        ctk.CTkLabel(
            logo_frame,
            text="💳 PDV",
            font=ctk.CTkFont("Inter", 22, "bold"),
            text_color="#FFFFFF",
        ).pack(anchor="w")

        ctk.CTkLabel(
            logo_frame,
            text="Ponto de Venda",
            font=ctk.CTkFont("Inter", 11),
            text_color=COLORS["sidebar_text_hover"],
        ).pack(anchor="w")

        # Separador
        sep = ctk.CTkFrame(self, height=1, fg_color="#3D3D5C", corner_radius=0)
        sep.grid(row=1, column=0, sticky="ew", padx=16, pady=(8, 16))

        # Itens de navegação
        for i, item in enumerate(self.NAV_ITEMS):
            btn = self._make_nav_button(item)
            btn.grid(row=i + 2, column=0, sticky="ew", padx=10, pady=2)
            self._buttons[item["id"]] = btn

        # Versão no rodapé
        ctk.CTkLabel(
            self,
            text="v1.0.0",
            font=ctk.CTkFont("Inter", 10),
            text_color="#555570",
        ).grid(row=100, column=0, sticky="s", pady=16)

        self.set_active("home")

    def _make_nav_button(self, item):
        btn = ctk.CTkButton(
            self,
            text=f"  {item['icon']}  {item['label']}",
            font=ctk.CTkFont("Inter", 13),
            anchor="w",
            height=42,
            corner_radius=10,
            fg_color="transparent",
            hover_color=COLORS["sidebar_active"],
            text_color=COLORS["sidebar_text_hover"],
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
                    fg_color=COLORS["sidebar_active"],
                    text_color="#FFFFFF",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["sidebar_text_hover"],
                )
