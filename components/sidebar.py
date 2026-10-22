"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil (Hover para expandir/recolher)
Dois conjuntos de botões pré-prontos — sem scrambling visual na transição.
"""

import customtkinter as ctk
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """Barra lateral retrátil: alterna entre dois conjuntos fixos de botões."""

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

        # Dois dicionários: botões para estado recolhido e expandido
        self._btns_col: dict[str, ctk.CTkButton] = {}
        self._btns_exp: dict[str, ctk.CTkButton] = {}

        self.grid_propagate(False)
        self._build()
        # Inicia recolhido
        self._show_collapsed()

    # ------------------------------------------------------------------ #
    #  Construção                                                          #
    # ------------------------------------------------------------------ #

    def _build(self):
        self.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ── Logo compacto (recolhido) ──────────────────────────────────
        self.logo_col = ctk.CTkLabel(
            self, text="🖥️",
            font=get_font("sidebar_title"),
            text_color="#FFFFFF",
        )

        # ── Logo expandido ─────────────────────────────────────────────
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

        # ── Separador ─────────────────────────────────────────────────
        self.sep = ctk.CTkFrame(self, height=1, fg_color="#1D2E47", corner_radius=0)
        self.sep.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 14))

        # ── Botões recolhidos (ícone, centralizado) ───────────────────
        _icon_font = ctk.CTkFont(family="Segoe UI Emoji", size=18)
        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self,
                text=item["icon"],
                font=_icon_font,
                anchor="center",
                height=44,
                corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            # row=i+2 — mesmo grid row dos botões expandidos (só um aparece por vez)
            btn.grid(row=i + 2, column=0, sticky="ew", padx=8, pady=3)
            self._btns_col[item["id"]] = btn

        # ── Botões expandidos (ícone + nome, à esquerda) ─────────────
        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self,
                text=f"  {item['icon']}   {item['label']}",
                font=get_font("sidebar_item"),
                anchor="w",
                height=44,
                corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=12, pady=3)
            self._btns_exp[item["id"]] = btn

        # ── Rodapé ────────────────────────────────────────────────────
        self.footer_col = ctk.CTkLabel(
            self, text=f"v{APP_VERSION}",
            font=get_font("small"), text_color="#627594",
        )
        self.footer_exp = ctk.CTkLabel(
            self, text=f"PDV v{APP_VERSION}",
            font=get_font("small"), text_color="#627594",
        )

        # Aplica estado ativo inicial
        self._apply_active_style(self.active_page)

        # Hover apenas no frame raiz + filhos diretos (2 níveis)
        self._bind_hover(self)

    # ------------------------------------------------------------------ #
    #  Alternar estado: mostra UM conjunto, esconde o outro               #
    # ------------------------------------------------------------------ #

    def _show_collapsed(self):
        """Exibe o conjunto recolhido e esconde o expandido."""
        self._is_expanded = False
        self.configure(width=self.COLLAPSED_WIDTH)

        # Logo
        try: self.logo_exp_frame.grid_remove()
        except Exception: pass
        self.logo_col.grid(row=0, column=0, pady=(20, 10))

        # Separador
        self.sep.grid_configure(padx=12)

        # Botões: remove expandidos, mostra recolhidos
        for item in self.NAV_ITEMS:
            self._btns_exp[item["id"]].grid_remove()
            self._btns_col[item["id"]].grid(
                row=self.NAV_ITEMS.index(item) + 2,
                column=0, sticky="ew", padx=8, pady=3,
            )

        # Rodapé
        try: self.footer_exp.grid_remove()
        except Exception: pass
        self.footer_col.grid(row=100, column=0, sticky="s", pady=16)

    def _show_expanded(self):
        """Exibe o conjunto expandido e esconde o recolhido."""
        self._is_expanded = True
        self.configure(width=self.EXPANDED_WIDTH)

        # Logo
        try: self.logo_col.grid_remove()
        except Exception: pass
        self.logo_exp_frame.grid(row=0, column=0, sticky="ew", padx=18, pady=(20, 10))

        # Separador
        self.sep.grid_configure(padx=16)

        # Botões: remove recolhidos, mostra expandidos
        for item in self.NAV_ITEMS:
            self._btns_col[item["id"]].grid_remove()
            self._btns_exp[item["id"]].grid(
                row=self.NAV_ITEMS.index(item) + 2,
                column=0, sticky="ew", padx=12, pady=3,
            )

        # Rodapé
        try: self.footer_col.grid_remove()
        except Exception: pass
        self.footer_exp.grid(row=100, column=0, sticky="s", pady=16)

    # ------------------------------------------------------------------ #
    #  Hover                                                               #
    # ------------------------------------------------------------------ #

    def _bind_hover(self, root):
        for w in [root] + list(root.winfo_children()):
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

    def _on_enter(self, event=None):
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
            self._collapse_job = None
        if not self._is_expanded:
            self._show_expanded()

    def _on_leave(self, event=None):
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
        self._collapse_job = self.after(80, self._check_and_collapse)

    def _check_and_collapse(self):
        self._collapse_job = None
        try:
            x, y  = self.winfo_pointerxy()
            sx    = self.winfo_rootx()
            sy    = self.winfo_rooty()
            sw    = self.winfo_width()
            sh    = self.winfo_height()
            inside = sx <= x <= sx + sw and sy <= y <= sy + sh
        except Exception:
            inside = False
        if not inside:
            self._show_collapsed()

    # ------------------------------------------------------------------ #
    #  Navegação e estado ativo                                            #
    # ------------------------------------------------------------------ #

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        self._apply_active_style(page_id)

    def _apply_active_style(self, page_id):
        for pid in self._btns_col:
            active = pid == page_id
            color  = COLORS["primary"] if active else "transparent"
            tcolor = "#FFFFFF" if active else COLORS["sidebar_text"]
            self._btns_col[pid].configure(fg_color=color, text_color=tcolor)
            self._btns_exp[pid].configure(fg_color=color, text_color=tcolor)
