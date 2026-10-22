"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil (Hover para expandir/recolher)
Transição instantânea — sem animação para máxima fluidez.
"""

import customtkinter as ctk
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """Barra lateral de navegação retrátil: ícones compactos → expande ao hover."""

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
        self._is_expanded   = False
        self._collapse_job  = None
        self._buttons: dict[str, ctk.CTkButton] = {}

        self.grid_propagate(False)
        self._build()
        self._apply_collapsed()

    # ------------------------------------------------------------------ #
    #  Layout                                                              #
    # ------------------------------------------------------------------ #

    def _build(self):
        self.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Logo
        self.logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(20, 10))

        self.logo_title = ctk.CTkLabel(
            self.logo_frame,
            text="🖥️",
            font=get_font("sidebar_title"),
            text_color="#FFFFFF",
        )
        self.logo_title.pack(anchor="center")

        self.logo_subtitle = ctk.CTkLabel(
            self.logo_frame,
            text="Sistema de Ponto de Venda",
            font=get_font("small"),
            text_color=COLORS["sidebar_text"],
        )

        # Separador
        self.sep = ctk.CTkFrame(self, height=1, fg_color="#1D2E47", corner_radius=0)
        self.sep.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 14))

        # Botões
        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self,
                text=item["icon"],
                font=get_font("sidebar_title"),
                anchor="center",
                height=44,
                corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=10, pady=3)
            self._buttons[item["id"]] = btn

        # Rodapé
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=100, column=0, sticky="s", pady=16)

        self.footer_label = ctk.CTkLabel(
            self.footer_frame,
            text=f"v{APP_VERSION}",
            font=get_font("small"),
            text_color="#627594",
        )
        self.footer_label.pack(anchor="center")

        self.set_active("home")
        self._bind_hover(self)

    # ------------------------------------------------------------------ #
    #  Hover bindings — apenas filhos diretos (sem recursão profunda)     #
    # ------------------------------------------------------------------ #

    def _bind_hover(self, root):
        """Vincula <Enter>/<Leave> no frame raiz e em filhos diretos (2 níveis)."""
        for w in [root] + root.winfo_children():
            try:
                w.bind("<Enter>", self._on_enter, add="+")
                w.bind("<Leave>", self._on_leave, add="+")
            except Exception:
                pass
            for sub in w.winfo_children():
                try:
                    sub.bind("<Enter>", self._on_enter, add="+")
                    sub.bind("<Leave>", self._on_leave, add="+")
                except Exception:
                    pass

    # ------------------------------------------------------------------ #
    #  Expand / Collapse instantâneos                                      #
    # ------------------------------------------------------------------ #

    def _apply_expanded(self):
        self._is_expanded = True
        self.configure(width=self.EXPANDED_WIDTH)

        self.logo_title.configure(text="🖥️  PDV Caixa")
        self.logo_title.pack_configure(anchor="w")
        self.logo_subtitle.pack(anchor="w", pady=(2, 0))
        self.logo_frame.grid_configure(padx=18)
        self.sep.grid_configure(padx=16)

        for item in self.NAV_ITEMS:
            self._buttons[item["id"]].configure(
                text=f"  {item['icon']}   {item['label']}",
                font=get_font("sidebar_item"),
                anchor="w",
            )
            self._buttons[item["id"]].grid_configure(padx=12)

        self.footer_label.configure(text=f"PDV v{APP_VERSION}")

    def _apply_collapsed(self):
        self._is_expanded = False
        self.configure(width=self.COLLAPSED_WIDTH)

        self.logo_title.configure(text="🖥️")
        self.logo_title.pack_configure(anchor="center")
        try:
            self.logo_subtitle.pack_forget()
        except Exception:
            pass
        self.logo_frame.grid_configure(padx=6, pady=(16, 10))
        self.sep.grid_configure(padx=10)

        _icon_font = ctk.CTkFont(family="Segoe UI Emoji", size=18)
        for item in self.NAV_ITEMS:
            self._buttons[item["id"]].configure(
                text=item["icon"],
                font=_icon_font,
                anchor="center",
            )
            self._buttons[item["id"]].grid_configure(padx=8)

        self.footer_label.configure(text=f"v{APP_VERSION}")

    # ------------------------------------------------------------------ #
    #  Eventos                                                             #
    # ------------------------------------------------------------------ #

    def _on_enter(self, event=None):
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
            self._collapse_job = None
        if not self._is_expanded:
            self._apply_expanded()

    def _on_leave(self, event=None):
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
        self._collapse_job = self.after(80, self._check_and_collapse)

    def _check_and_collapse(self):
        self._collapse_job = None
        try:
            x, y   = self.winfo_pointerxy()
            sx, sy  = self.winfo_rootx(), self.winfo_rooty()
            sw, sh  = self.winfo_width(), self.winfo_height()
            inside  = sx <= x <= sx + sw and sy <= y <= sy + sh
        except Exception:
            inside = False
        if not inside:
            self._apply_collapsed()

    # ------------------------------------------------------------------ #
    #  Navegação                                                           #
    # ------------------------------------------------------------------ #

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        for pid, btn in self._buttons.items():
            if pid == page_id:
                btn.configure(fg_color=COLORS["primary"], text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color=COLORS["sidebar_text"])
