"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil
Dois conjuntos de botões pré-prontos + binding de hover pós-renderização.
"""

import customtkinter as ctk
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):

    COLLAPSED_WIDTH = 70
    EXPANDED_WIDTH  = 230

    NAV_ITEMS = [
        {"id": "home",      "icon": "🏠", "label": "Início"},
        {"id": "caixa",     "icon": "🛒", "label": "Caixa"},
        {"id": "produtos",  "icon": "📦", "label": "Produtos"},
        {"id": "vendas",    "icon": "📊", "label": "Vendas"},
        {"id": "clientes",  "icon": "👤", "label": "Clientes"},
        {"id": "relatorio", "icon": "📋", "label": "Relatórios"},
        {"id": "config",    "icon": "⚙️",  "label": "Configurações"},
    ]

    def __init__(self, parent, navigate_callback, **kwargs):
        super().__init__(
            parent,
            width=self.COLLAPSED_WIDTH,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
            **kwargs,
        )
        self.navigate_callback = navigate_callback
        self._is_expanded  = False
        self._collapse_job = None
        self.active_page   = "home"

        self._btns_col: dict[str, ctk.CTkButton] = {}
        self._btns_exp: dict[str, ctk.CTkButton] = {}

        # Lista de todos os widgets que precisam de binding (preenchida em _build)
        self._hover_widgets: list = []

        self.grid_propagate(False)
        self._build()
        self._show_collapsed()

        # Binding feito APÓS renderização para garantir que winfo_children() funcione
        self.after(50, self._bind_hover_all)

    # ------------------------------------------------------------------ #
    #  Construção                                                          #
    # ------------------------------------------------------------------ #

    def _build(self):
        self.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Logo compacto
        self.logo_col = ctk.CTkLabel(
            self, text="🖥️",
            font=get_font("sidebar_title"),
            text_color="#FFFFFF",
        )

        # Logo expandido
        self.logo_exp_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(
            self.logo_exp_frame,
            text="🖥️  PDV Caixa",
            font=get_font("sidebar_title"),
            text_color="#FFFFFF",
        ).pack(anchor="w")
        ctk.CTkLabel(
            self.logo_exp_frame,
            text="Sistema de Ponto de Venda",
            font=get_font("small"),
            text_color=COLORS["sidebar_text"],
        ).pack(anchor="w", pady=(2, 0))

        # Separador
        self.sep = ctk.CTkFrame(self, height=1, fg_color="#1D2E47", corner_radius=0)
        self.sep.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 14))

        # Botões recolhidos
        _icon_font = ctk.CTkFont(family="Segoe UI Emoji", size=18)
        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self, text=item["icon"],
                font=_icon_font, anchor="center",
                height=44, corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=8, pady=3)
            self._btns_col[item["id"]] = btn

        # Botões expandidos
        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self, text=f"  {item['icon']}   {item['label']}",
                font=get_font("sidebar_item"), anchor="w",
                height=44, corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=12, pady=3)
            self._btns_exp[item["id"]] = btn

        # Rodapés
        self.footer_col = ctk.CTkLabel(
            self, text=f"v{APP_VERSION}",
            font=get_font("small"), text_color="#627594",
        )
        self.footer_exp = ctk.CTkLabel(
            self, text=f"PDV v{APP_VERSION}",
            font=get_font("small"), text_color="#627594",
        )

        self._apply_active(self.active_page)

    # ------------------------------------------------------------------ #
    #  Binding de hover — chamado após renderização                        #
    # ------------------------------------------------------------------ #

    def _bind_hover_all(self):
        """Percorre toda a árvore de widgets da sidebar e registra hover."""
        self._bind_recursive(self)

    def _bind_recursive(self, widget, depth=0):
        if depth > 4:
            return
        try:
            widget.bind("<Enter>", self._on_enter, add="+")
            widget.bind("<Leave>", self._on_leave, add="+")
        except Exception:
            pass
        # Canvas interno dos CTk widgets
        for attr in ("_canvas", "_text_label", "_image_label"):
            sub = getattr(widget, attr, None)
            if sub:
                try:
                    sub.bind("<Enter>", self._on_enter, add="+")
                    sub.bind("<Leave>", self._on_leave, add="+")
                except Exception:
                    pass
        for child in widget.winfo_children():
            self._bind_recursive(child, depth + 1)

    # ------------------------------------------------------------------ #
    #  Expandido / Recolhido                                               #
    # ------------------------------------------------------------------ #

    def _show_collapsed(self):
        self._is_expanded = False
        self.configure(width=self.COLLAPSED_WIDTH)
        try: self.logo_exp_frame.grid_remove()
        except Exception: pass
        self.logo_col.grid(row=0, column=0, pady=(20, 10))
        self.sep.grid_configure(padx=12)
        for i, item in enumerate(self.NAV_ITEMS):
            self._btns_exp[item["id"]].grid_remove()
            self._btns_col[item["id"]].grid(row=i + 2, column=0, sticky="ew", padx=8, pady=3)
        try: self.footer_exp.grid_remove()
        except Exception: pass
        self.footer_col.grid(row=100, column=0, sticky="s", pady=16)

    def _show_expanded(self):
        self._is_expanded = True
        self.configure(width=self.EXPANDED_WIDTH)
        try: self.logo_col.grid_remove()
        except Exception: pass
        self.logo_exp_frame.grid(row=0, column=0, sticky="ew", padx=18, pady=(20, 10))
        self.sep.grid_configure(padx=16)
        for i, item in enumerate(self.NAV_ITEMS):
            self._btns_col[item["id"]].grid_remove()
            self._btns_exp[item["id"]].grid(row=i + 2, column=0, sticky="ew", padx=12, pady=3)
        try: self.footer_col.grid_remove()
        except Exception: pass
        self.footer_exp.grid(row=100, column=0, sticky="s", pady=16)
        # Rebind nos novos filhos visíveis
        self.after(10, self._bind_hover_all)

    # ------------------------------------------------------------------ #
    #  Hover events                                                        #
    # ------------------------------------------------------------------ #

    def _on_enter(self, event=None):
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
            self._collapse_job = None
        if not self._is_expanded:
            self._show_expanded()

    def _on_leave(self, event=None):
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
        self._collapse_job = self.after(100, self._check_and_collapse)

    def _check_and_collapse(self):
        self._collapse_job = None
        try:
            x, y   = self.winfo_pointerxy()
            sx, sy = self.winfo_rootx(), self.winfo_rooty()
            sw, sh = self.winfo_width(), self.winfo_height()
            inside = sx <= x <= sx + sw and sy <= y <= sy + sh
        except Exception:
            inside = False
        if not inside:
            self._show_collapsed()

    # ------------------------------------------------------------------ #
    #  Navegação                                                           #
    # ------------------------------------------------------------------ #

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        self._apply_active(page_id)

    def _apply_active(self, page_id):
        for pid in self._btns_col:
            active = pid == page_id
            c = COLORS["primary"] if active else "transparent"
            t = "#FFFFFF" if active else COLORS["sidebar_text"]
            self._btns_col[pid].configure(fg_color=c, text_color=t)
            self._btns_exp[pid].configure(fg_color=c, text_color=t)
