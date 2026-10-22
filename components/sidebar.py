"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil
Abordagem overlay (place): sidebar colapsada fixa + painel expandido por cima.
Grid nunca muda → abertura instantânea sem recálculo de layout.
"""

import customtkinter as ctk
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """
    Barra lateral com overlay:
    - Frame base (70px) sempre no grid — nunca muda de tamanho.
    - Painel expandido (230px) usa place() sobre a janela — abre/fecha instantâneo.
    """

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
        # Frame base: sempre 70px, nunca muda
        super().__init__(
            parent,
            width=self.COLLAPSED_WIDTH,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
            **kwargs,
        )
        self._parent           = parent
        self.navigate_callback = navigate_callback
        self._is_expanded      = False
        self._collapse_job     = None
        self.active_page       = "home"

        self._btns_col: dict[str, ctk.CTkButton] = {}  # botões do frame base
        self._btns_exp: dict[str, ctk.CTkButton] = {}  # botões do overlay

        self.grid_propagate(False)
        self._build_base()
        self._overlay = self._build_overlay()

    # ------------------------------------------------------------------ #
    #  Frame base (recolhido, 70px, sempre visível no grid)               #
    # ------------------------------------------------------------------ #

    def _build_base(self):
        self.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Logo
        ctk.CTkLabel(
            self, text="🖥️",
            font=get_font("sidebar_title"),
            text_color="#FFFFFF",
        ).grid(row=0, column=0, pady=(20, 10))

        # Separador
        ctk.CTkFrame(self, height=1, fg_color="#1D2E47", corner_radius=0).grid(
            row=1, column=0, sticky="ew", padx=12, pady=(6, 14),
        )

        # Botões (ícone centralizado)
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

        # Rodapé
        ctk.CTkLabel(
            self, text=f"v{APP_VERSION}",
            font=get_font("small"), text_color="#627594",
        ).grid(row=100, column=0, sticky="s", pady=16)

        self._apply_active(self.active_page, self._btns_col)

        # Hover no frame base
        self._bind_hover_on(self)

    # ------------------------------------------------------------------ #
    #  Overlay expandido (230px, place() sobre o parent)                  #
    # ------------------------------------------------------------------ #

    def _build_overlay(self) -> ctk.CTkFrame:
        """Cria o painel expandido mas não o exibe ainda."""
        ov = ctk.CTkFrame(
            self._parent,
            width=self.EXPANDED_WIDTH,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
        )
        ov.grid_propagate(False)
        ov.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)
        ov.grid_columnconfigure(0, weight=1)

        # Logo expandido
        logo_frame = ctk.CTkFrame(ov, fg_color="transparent")
        logo_frame.grid(row=0, column=0, sticky="ew", padx=18, pady=(20, 10))
        ctk.CTkLabel(
            logo_frame, text="🖥️  PDV Caixa",
            font=get_font("sidebar_title"), text_color="#FFFFFF",
        ).pack(anchor="w")
        ctk.CTkLabel(
            logo_frame, text="Sistema de Ponto de Venda",
            font=get_font("small"), text_color=COLORS["sidebar_text"],
        ).pack(anchor="w", pady=(2, 0))

        # Separador
        ctk.CTkFrame(ov, height=1, fg_color="#1D2E47", corner_radius=0).grid(
            row=1, column=0, sticky="ew", padx=16, pady=(6, 14),
        )

        # Botões expandidos (ícone + nome)
        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                ov, text=f"  {item['icon']}   {item['label']}",
                font=get_font("sidebar_item"), anchor="w",
                height=44, corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=12, pady=3)
            self._btns_exp[item["id"]] = btn

        # Rodapé
        ctk.CTkLabel(
            ov, text=f"PDV v{APP_VERSION}",
            font=get_font("small"), text_color="#627594",
        ).grid(row=100, column=0, sticky="s", pady=16)

        self._apply_active(self.active_page, self._btns_exp)

        # Hover no overlay
        self._bind_hover_on(ov)

        return ov

    # ------------------------------------------------------------------ #
    #  Mostrar / Esconder overlay                                          #
    # ------------------------------------------------------------------ #

    def _show_overlay(self):
        """Posiciona e exibe o overlay sobre o frame base."""
        self._is_expanded = True
        # Usa place() relativo ao parent — sem afetar o grid
        self._overlay.place(x=0, y=0, width=self.EXPANDED_WIDTH, relheight=1.0)
        self._overlay.lift()

    def _hide_overlay(self):
        """Remove o overlay da tela."""
        self._is_expanded = False
        self._overlay.place_forget()

    # ------------------------------------------------------------------ #
    #  Hover                                                               #
    # ------------------------------------------------------------------ #

    def _bind_hover_on(self, widget):
        """Vincula hover em widget e seus filhos diretos (2 níveis)."""
        for w in [widget] + list(widget.winfo_children()):
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
            self._show_overlay()

    def _on_leave(self, event=None):
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
        self._collapse_job = self.after(80, self._check_and_collapse)

    def _check_and_collapse(self):
        self._collapse_job = None
        # Verifica se o mouse ainda está sobre o base OU sobre o overlay
        try:
            x, y = self.winfo_pointerxy()
            # Área do overlay
            ox, oy = self._overlay.winfo_rootx(), self._overlay.winfo_rooty()
            ow, oh = self._overlay.winfo_width(), self._overlay.winfo_height()
            # Área do frame base
            bx, by = self.winfo_rootx(), self.winfo_rooty()
            bw, bh = self.winfo_width(), self.winfo_height()

            in_overlay = ox <= x <= ox + ow and oy <= y <= oy + oh
            in_base    = bx <= x <= bx + bw and by <= y <= by + bh
            inside     = in_overlay or in_base
        except Exception:
            inside = False

        if not inside:
            self._hide_overlay()

    # ------------------------------------------------------------------ #
    #  Navegação e estado ativo                                            #
    # ------------------------------------------------------------------ #

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        self._apply_active(page_id, self._btns_col)
        self._apply_active(page_id, self._btns_exp)

    def _apply_active(self, page_id, btns: dict):
        for pid, btn in btns.items():
            active = pid == page_id
            btn.configure(
                fg_color=COLORS["primary"] if active else "transparent",
                text_color="#FFFFFF" if active else COLORS["sidebar_text"],
            )
