"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil
Animação suave da largura + troca de conteúdo apenas no final.
"""

import customtkinter as ctk
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """Barra lateral retrátil com slide suave."""

    COLLAPSED_WIDTH = 70
    EXPANDED_WIDTH  = 230
    ANIM_STEP_MS    = 10   # ms por frame
    ANIM_PX_STEP    = 16   # px por frame → ~10 frames → ~100ms total

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
        self._anim_job      = None
        self._current_width = float(self.COLLAPSED_WIDTH)
        self._target_width  = float(self.COLLAPSED_WIDTH)
        self.active_page    = "home"

        # Dois conjuntos de botões (sem scrambling)
        self._btns_col: dict[str, ctk.CTkButton] = {}
        self._btns_exp: dict[str, ctk.CTkButton] = {}

        self.grid_propagate(False)
        self._build()
        self._show_collapsed_content()  # Inicia recolhido

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

        # Botões recolhidos (ícone centralizado)
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

        # Botões expandidos (ícone + nome)
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

        self._apply_active_style(self.active_page)
        self._bind_hover(self)

    # ------------------------------------------------------------------ #
    #  Conteúdo: troca apenas ícones ↔ ícones+nomes (sem animação)        #
    # ------------------------------------------------------------------ #

    def _show_collapsed_content(self):
        """Exibe ícones compactos — usado durante colapso e animação."""
        try: self.logo_exp_frame.grid_remove()
        except Exception: pass
        self.logo_col.grid(row=0, column=0, pady=(20, 10))
        self.sep.grid_configure(padx=12)

        for item in self.NAV_ITEMS:
            self._btns_exp[item["id"]].grid_remove()
            self._btns_col[item["id"]].grid(
                row=self.NAV_ITEMS.index(item) + 2,
                column=0, sticky="ew", padx=8, pady=3,
            )

        try: self.footer_exp.grid_remove()
        except Exception: pass
        self.footer_col.grid(row=100, column=0, sticky="s", pady=16)

    def _show_expanded_content(self):
        """Exibe ícones + nomes — chamado SOMENTE ao terminar a animação de expansão."""
        try: self.logo_col.grid_remove()
        except Exception: pass
        self.logo_exp_frame.grid(row=0, column=0, sticky="ew", padx=18, pady=(20, 10))
        self.sep.grid_configure(padx=16)

        for item in self.NAV_ITEMS:
            self._btns_col[item["id"]].grid_remove()
            self._btns_exp[item["id"]].grid(
                row=self.NAV_ITEMS.index(item) + 2,
                column=0, sticky="ew", padx=12, pady=3,
            )

        try: self.footer_col.grid_remove()
        except Exception: pass
        self.footer_exp.grid(row=100, column=0, sticky="s", pady=16)

    # ------------------------------------------------------------------ #
    #  Animação de largura                                                 #
    # ------------------------------------------------------------------ #

    def _animate_to(self, target: float):
        """Inicia animação de largura para 'target'. Não altera o conteúdo."""
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None
        self._target_width = target
        self._step()

    def _step(self):
        diff = self._target_width - self._current_width
        if abs(diff) <= self.ANIM_PX_STEP:
            # Chegou — aplica largura final
            self._current_width = self._target_width
            self.configure(width=int(self._current_width))
            self._anim_job = None
            # Só agora troca para conteúdo expandido (se foi expansão)
            if self._target_width == self.EXPANDED_WIDTH:
                self._is_expanded = True
                self._show_expanded_content()
            return

        self._current_width += self.ANIM_PX_STEP if diff > 0 else -self.ANIM_PX_STEP
        self.configure(width=int(self._current_width))
        self._anim_job = self.after(self.ANIM_STEP_MS, self._step)

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
        if not self._is_expanded and self._target_width != self.EXPANDED_WIDTH:
            # Mostra ícones compactos durante a animação de abertura
            self._show_collapsed_content()
            self._animate_to(self.EXPANDED_WIDTH)

    def _on_leave(self, event=None):
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
        self._collapse_job = self.after(80, self._check_and_collapse)

    def _check_and_collapse(self):
        self._collapse_job = None
        try:
            x, y   = self.winfo_pointerxy()
            sx, sy = self.winfo_rootx(), self.winfo_rooty()
            sw, sh = self.winfo_width(), self.winfo_height()
            inside = sx <= x <= sx + sw and sy <= y <= sy + sh
        except Exception:
            inside = False

        if not inside and self._target_width != self.COLLAPSED_WIDTH:
            # Troca conteúdo para ícones IMEDIATAMENTE, depois anima a largura
            self._is_expanded = False
            self._show_collapsed_content()
            self._animate_to(self.COLLAPSED_WIDTH)

    # ------------------------------------------------------------------ #
    #  Navegação                                                           #
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
